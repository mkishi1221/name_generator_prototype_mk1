#!/bin/bash
# Calculate time elapsed
date
start_time=`gdate +%s%3N`

#Clear tmp files
rm -r tmp/*

#Create required folders
mkdir -p tmp
mkdir -p ref
mkdir -p results

#Reset source file
> tmp/alltext.tsv

#Pour source texts into one file
FILES=data/*.*
for f in $FILES
do
cat ${f} \
>> tmp/alltext.tsv
echo "" >> tmp/alltext.tsv
done

#Generate word list from source text
#Words to be sorted by POS, length and other factors in the future to accomodate more complex name-generating algorithms.
echo "Creating word list..."
python3 scripts/keyword_generator.py \
    tmp/alltext.tsv \
    tmp/words.json

#Generate names
echo "Initiating name generator script..."
python3 scripts/name_generator.py \
    tmp/words.json \
    tmp/potential_names.tsv

#Check domains 
#To make sure we don't overuse the API, the loop breaks after finding 10 available domains. You can change the limit by changing the "limit" variable defined below.
echo "Choosing names and checking their domain availability..."
echo ""
dt=$(gdate '+%Y%m%d_%H%M%S')
limit=10
python3 scripts/domain_checker.py \
    tmp/potential_names.tsv \
    results/names_sent_${dt}.tsv \
    ${limit}

#Calculate time elapsed
end_time=`gdate +%s%3N`
min_elapsed=$(echo "scale=0; (${end_time}-${start_time})/1000/60" | bc )
sec_elapsed=$(echo "scale=3; ((${end_time}-${start_time})/1000)-(${min_elapsed}*60)" | bc )
echo "All files processed. Total: ${min_elapsed}min, ${sec_elapsed}sec." 
date