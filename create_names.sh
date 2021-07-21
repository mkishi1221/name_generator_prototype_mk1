#!/bin/bash
# load database credentials
if [[ -f db_creds.env ]]; then
  export $(cat db_creds.env | xargs)
fi

# Calculate time elapsed
date
start_time=`gdate +%s%3N`

# Create required folders
mkdir -p tmp
mkdir -p ref/logs
mkdir -p ref/mongo_entries
mkdir -p results

# Create log files if not exist
touch ref/logs/prev_source_data_log.tsv
touch ref/logs/prev_script_log.tsv

# Reset current log files to be blank
> ref/logs/source_data_log.tsv
> ref/logs/script_log.tsv

# Pour script file modification dates into one file
for f in *.py *.sh *.xlsx
do
ls -lh ${f} \
>> ref/logs/script_log.tsv
done

FILES=modules/*.*
for f in $FILES
do
ls -lh ${f} \
>> ref/logs/script_log.tsv
done

FILES=classes/*.*
for f in $FILES
do
ls -lh ${f} \
>> ref/logs/script_log.tsv
done

# Check if data with sentences exists
if [ -n "$(ls -A data/*.txt 2>/dev/null)" ]; then
    # Pour source texts modification dates into one file
    sentences="exists"
    FILES=data/*.*
    for f in $FILES
    do
    ls -lh ${f} \
    >> ref/logs/source_data_log.tsv
    done
else
    sentences="none"
    echo "No sentences found! Checking if keywords are supplied..."
fi

# Check if data with keywords exists
if [ -n "$(ls -A data/keywords/*.txt 2>/dev/null)" ]; then
    # Pour source texts modification dates into one file
    keywords="exists"
    FILES=data/keywords/*.*
    for f in $FILES
    do
    ls -lh ${f} \
    >> ref/logs/source_data_log.tsv
    done
else
    keywords="none"
    if [ ${sentences} == "exists" ]; then
        echo "No keywords found. Running script with only sentences..."
    fi
fi

# Exit script if no sentences or keywords detected.
if [ ${keywords} == "none" ] && [ ${sentences} == "none" ]; then
    echo "No sentences and keywords detetcted! Please add source data in txt format to the \"data\" folder."
    exit
fi

# Run blacklist / whitelist generator if files exist in results folder
if [ -n "$(ls -A results/*.xlsx 2>/dev/null)" ]; then
    echo "Files found in results folder: running black/grey/white-list generator"
    python3 preference_generator.py \
        results/
else
    echo "Results folder is empty: skipping black/grey/white-list generator"
fi

# Compare contents of current and previous log files
# If source data has changed, recompile source data, dictionary and generated name lists.
if [[ "$(cat ref/logs/prev_source_data_log.tsv)" == "$(cat ref/logs/source_data_log.tsv)" && "$(cat ref/logs/prev_script_log.tsv)" == "$(cat ref/logs/script_log.tsv)" ]];then
    echo "Source data or script unchanged. Moving on to domain availability check..."

else
    echo "Source data or script changed. Recompiling source data..."
    # Clear tmp files
    rm -r tmp/*

    # Check if data with sentences exists
    if [ -n "$(ls -A data/*.txt 2>/dev/null)" ]; then
        # Pour source texts into one file
        FILES=data/*.txt
        for f in $FILES
        do
        cat ${f} \
        >> tmp/user_sentences.tsv
        echo "" >> tmp/user_sentences.tsv
        done
    else
        > tmp/user_sentences.tsv
    fi

    # Check if data with keywords exists
    if [ -n "$(ls -A data/keywords/*.txt 2>/dev/null)" ]; then
        # Pour user provided keywords into one file
        FILES=data/keywords/*.txt
        for f in $FILES
        do
        cat ${f} \
        >> tmp/user_keywords.tsv
        echo "" >> tmp/user_keywords.tsv
        done
    else
        > tmp/user_keywords.tsv
    fi

    # Generate word list from source text
    # Words to be sorted by POS, length and other factors in the future to accomodate more complex name-generating algorithms.
    echo "Creating word list..."
    python3 keyword_generator.py \
        tmp/user_sentences.tsv \
        tmp/user_keywords.tsv \
        tmp/keywords.json

    # Generate names
    echo "Initiating name generator script..."
    python3 name_generator.py \
        tmp/keywords.json \
        tmp/potential_names.json
    
    cat ref/logs/source_data_log.tsv > ref/logs/prev_source_data_log.tsv
    cat ref/logs/script_log.tsv > ref/logs/prev_script_log.tsv
fi

# Check domains 
# To make sure we don't overuse the API, the loop breaks after finding 10 available domains. You can change this limit by changing the "limit" variable defined below.
echo "Choosing names and initiating domain availability check..."
echo ""
dt=$(gdate '+%Y%m%d_%H%M%S')
limit=10
python3 domain_checker.py \
    tmp/potential_names.json \
    results/names_${dt}.xlsx \
    ${limit}

# Calculate time elapsed
end_time=`gdate +%s%3N`
min_elapsed=$(echo "scale=0; (${end_time}-${start_time})/1000/60" | bc )
sec_elapsed=$(echo "scale=3; ((${end_time}-${start_time})/1000)-(${min_elapsed}*60)" | bc )
echo "All files processed. Total: ${min_elapsed}min, ${sec_elapsed}sec." 
date
