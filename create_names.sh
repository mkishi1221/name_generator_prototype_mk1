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
python3 scripts/word_list_generator.py \
    tmp/alltext.tsv \
    tmp/words.json

#Generate word list from source text
#Words to be sorted by POS, length and other factors in the future to accomodate more complex name-generating algorithms.
echo "Initiating name generator script..."
python3 scripts/name_generator.py \
    tmp/words.json \
    tmp/potential_names.tsv

#Check domains 
#To make sure we don't overuse the API, the loop breaks after finding 10 available domains
echo "Choosing names and checking their domain availability..."
echo ""
counter=0
available=0
limit=10
file="tmp/tmp.tsv"
> results/names.tsv

while IFS= read -r line; do

    if [ "${available}" -eq "${limit}" ]
    then
        break
    else
        domain="${line}.com"
        echo "checking ${domain}..."
        whois ${domain} > ${file}
        if grep -q '^No match\|^NOT FOUND\|^Not fo\|AVAILABLE\|^No Data Fou\|has not been regi\|No entri' "${file}"
        then
            echo "${line}\t${domain}" >> results/names.tsv
            echo "${line} available"
            ((available++))
        else
            echo "${line} not available"
        fi
    fi

    ((counter++))
    echo "Names processed: ${counter}"
    echo "Names available: ${available}"
    echo ""

done < tmp/potential_names.tsv

#Calculate time elapsed
end_time=`gdate +%s%3N`
min_elapsed=$(echo "scale=0; (${end_time}-${start_time})/1000/60" | bc )
sec_elapsed=$(echo "scale=3; ((${end_time}-${start_time})/1000)-(${min_elapsed}*60)" | bc )
echo "All files processed. Total: ${min_elapsed}min, ${sec_elapsed}sec." 
date