#!/bin/bash
# Calculate time elapsed
date
start_time=`gdate +%s%3N`

# Create required folders
mkdir -p tmp_keyw
mkdir -p ref/logs
mkdir -p results

# Create log files if not exist
touch ref/logs/keyw_prev_source_file_log.tsv
touch ref/logs/keyw_prev_script_log.tsv

# Reset current log files to be blank
> ref/logs/keyw_source_file_log.tsv
> ref/logs/keyw_script_log.tsv

# Pour source texts modification dates into one file
FILES=data/keywords/*.*
for f in $FILES
do
ls -lh ${f} \
>> ref/logs/keyw_source_file_log.tsv
done

# Pour script file modification dates into one file
FILES=scripts/*.*
for f in $FILES
do
ls -lh ${f} \
>> ref/logs/keyw_script_log.tsv
done

FILES=scripts/modules/*.*
for f in $FILES
do
ls -lh ${f} \
>> ref/logs/keyw_script_log.tsv
done

ls -lh create_names_from_keywords.sh \
>> ref/logs/keyw_script_log.tsv

# Compare contents of current and previous log files
# If source data has changed, recompile source data, dictionary and generated name lists.
if [[ "$(cat ref/logs/keyw_prev_source_file_log.tsv)" == "$(cat ref/logs/keyw_source_file_log.tsv)" && "$(cat ref/logs/keyw_prev_script_log.tsv)" == "$(cat ref/logs/keyw_script_log.tsv)" ]];then
        echo "Source data and scripts unchanged. Moving on to domain availability check..."

else
    echo "Source data or scripts changed. Recompiling source data..."
    # Clear tmp files
    rm -r tmp_keyw/*

    # Pour source texts into one file
    FILES=data/keywords/*.*
    for f in $FILES
    do
    cat ${f} \
    >> tmp_keyw/alltext_keyw.tsv
    echo "" >> tmp_keyw/alltext_keyw.tsv
    done

    #Generate names from keywords
    echo "Initiating name generator script..."
    python3 scripts/basic_name_generator.py \
        tmp_keyw/alltext_keyw.tsv \
        tmp_keyw/potential_names_keyw.tsv
    
    cat ref/logs/keyw_source_file_log.tsv > ref/logs/keyw_prev_source_file_log.tsv
    cat ref/logs/keyw_script_log.tsv > ref/logs/keyw_prev_script_log.tsv
fi

# Check domains 
# To make sure we don't overuse the API, the loop breaks after finding 10 available domains. You can change this limit by changing the "limit" variable defined below.
echo "Choosing names and initiating domain availability check..."
echo ""
dt=$(gdate '+%Y%m%d_%H%M%S')
limit=10
python3 scripts/domain_checker.py \
    tmp_keyw/potential_names_keyw.tsv \
    results/names_keyw_${dt}.tsv \
    ${limit}

# Calculate time elapsed
end_time=`gdate +%s%3N`
min_elapsed=$(echo "scale=0; (${end_time}-${start_time})/1000/60" | bc )
sec_elapsed=$(echo "scale=3; ((${end_time}-${start_time})/1000)-(${min_elapsed}*60)" | bc )
echo "All files processed. Total: ${min_elapsed}min, ${sec_elapsed}sec." 
date