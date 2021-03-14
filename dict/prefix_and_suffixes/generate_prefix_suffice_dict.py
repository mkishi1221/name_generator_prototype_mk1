import regex as re
import sys
import json

def generate_json_dict(filepath, word_type, output_path):
    
    # Open file
    with open(filepath) as raw_data:
        raw_data = raw_data.read()
        raw_data_list = raw_data.split("\n")

    raw_data_list.pop(0)
    
    data_list = []
    count = 1
    num_lines = len(raw_data_list)
    for line in raw_data_list:
        if count != num_lines:
            print("Processing line " + str(count) + " out of " + str(num_lines) + "...", end='\r')
        else:
            print("Completed processing line " + str(count) + " out of " + str(num_lines))

        if line != "":
            split_data = line.split('\t')
            no_data = ''

            try:
                word = re.sub(r"\"", "", split_data[0])
                if len(word) == 0:
                    word = no_data
            except IndexError:
                word = no_data

            try:
                word_len = re.sub(r"\"", "", split_data[1])
                if len(word_len) == 0:
                    word_len = no_data
            except IndexError:
                word_len = no_data

            try:
                meaning = re.sub(r"\"", "", split_data[2])
                if len(meaning) == 0:
                    meaning = no_data
            except IndexError:
                meaning = no_data
            
            try:
                examples = re.sub(r"\"", "", split_data[3])
                if len(examples) == 0:
                    examples = no_data
            except IndexError:
                examples = no_data

            dict_data = {
            word_type:word,
            'word_len':word_len,
            'definition':meaning,
            'examples':examples,
            }

            if dict_data not in data_list and word != "":
                data_list.append(dict_data) 
        
        count = count + 1

    with open(output_path, "w+") as out_file:
        json.dump(data_list, out_file, ensure_ascii=False, indent=1)

    print("")

if __name__ == "__main__":
    generate_json_dict(sys.argv[1], sys.argv[2], sys.argv[3])

