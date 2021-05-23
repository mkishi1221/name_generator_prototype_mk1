#!/bin/bash
# Calculate time elapsed
date
start_time=`gdate +%s%3N`

# Create required folders
mkdir -p tmp_sents
mkdir -p ref/logs
mkdir -p results

# Make log files
touch ref/logs/prev_source_file_sent_log.tsv
> ref/logs/source_file_sent_log.tsv
touch ref/logs/prev_script_log.tsv
> ref/logs/script_log.tsv

# Pour source texts modification dates into one file
FILES=data/*.*
for f in $FILES
do
ls -lh ${f} \
>> ref/logs/source_file_sent_log.tsv
done

# Pour script file modification dates into one file
FILES=scripts/*.*
for f in $FILES
do
ls -lh ${f} \
>> ref/logs/script_log.tsv
done

FILES=scripts/modules/*.*
for f in $FILES
do
ls -lh ${f} \
>> ref/logs/script_log.tsv
done

ls -lh create_names_from_sentences.sh \
>> ref/logs/script_log.tsv

# If source data has changed, recompile source data, dictionary and name lists.
if [[ "$(cat ref/logs/prev_source_file_sent_log.tsv)" == "$(cat ref/logs/source_file_sent_log.tsv)" && "$(cat ref/logs/prev_script_log.tsv)" == "$(cat ref/logs/script_log.tsv)" ]];then
    echo "Source data or script unchanged. Moving on to domain availability check..."
else
    echo "Source data or script changed. Recompiling source data..."
    # Clear tmp files
    rm -r tmp_sents/*

    # Pour source texts into one file
    FILES=data/*.*
    for f in $FILES
    do
    cat ${f} \
    >> tmp_sents/alltext_sents.tsv
    echo "" >> tmp_sents/alltext_sents.tsv
    done

    # Generate word list from source text
    # Words to be sorted by POS, length and other factors in the future to accomodate more complex name-generating algorithms.
    echo "Creating word list..."
    python3 scripts/keyword_generator.py \
        tmp_sents/alltext_sents.tsv \
        tmp_sents/words_sents.json

    # Generate names
    echo "Initiating name generator script..."
    python3 scripts/name_generator.py \
        tmp_sents/words_sents.json \
        tmp_sents/potential_names_sents.tsv
    
    cat ref/logs/source_file_sent_log.tsv > ref/logs/prev_source_file_sent_log.tsv
    cat ref/logs/script_log.tsv > ref/logs/prev_script_log.tsv
fi

# Check domains 
# To make sure we don't overuse the API, the loop breaks after finding 10 available domains. You can change the limit by changing the "limit" variable defined below.
echo "Choosing names and initiating domain availability check..."
echo ""
dt=$(gdate '+%Y%m%d_%H%M%S')
limit=10
python3 scripts/domain_checker.py \
    tmp_sents/potential_names_sents.tsv \
    results/names_sent_${dt}.tsv \
    ${limit}

# Calculate time elapsed
end_time=`gdate +%s%3N`
min_elapsed=$(echo "scale=0; (${end_time}-${start_time})/1000/60" | bc )
sec_elapsed=$(echo "scale=3; ((${end_time}-${start_time})/1000)-(${min_elapsed}*60)" | bc )
echo "All files processed. Total: ${min_elapsed}min, ${sec_elapsed}sec." 
date
