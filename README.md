# name_generator_prototype_mk1
This is the first terminal based prototype of name-generator (mark 1). 

This script is the first attempt at aiding the creative process of creating a name for the potential business, product or brand. The vast majority of name generators currently on the market require users to manually provide a list of words or potential names which can be tedious, labor intensive and time-consuming. In worst case scenarios, months of thinking could yield no results. This script attempts to address that issue by asking users to collect existing text that they find relevant to their business, product or brand they wish to create as raw data to generate potential names. The script then takes the text and transforms them into hundreds of thousands of potential names. The names are then filtered based on it's length and if the .com domain is available and the results presented to the user as name recommendations. 

This script performs the following processes.
1. Takes the text files in the "data" folder and generates a list of words.
2. Combines the list of words to generate a range of potential "names".
3. Creates a list of potential names based on the availability of the .com domain.

# Requirements
This script uses bash and python coding. The script also requires an internet connection to check available domains.

### Bash Requirements

#### Pararell
Build and run commands in parallel
https://www.gnu.org/software/bash/manual/html_node/GNU-Parallel.html
https://formulae.brew.sh/formula/parallel

#### GNU Coreutils
Install and Use GNU Command Line Tools on macOS/OS X
https://formulae.brew.sh/formula/coreutils#default

#### gdate
gdate is not available on linux systems. A quick fix / hack is to symlink gdate to date:  
`sudo ln -s $(which date) /bin/gdate`

#### Bash
This script uses the latest version of bash
https://formulae.brew.sh/formula/bash#default

### Python Requirements

#### Python 3.0
This script uses the latest version of python 3.0
https://www.python.org/downloads/

#### Regex
If an older version of Python is pre-installed, make sure to install regex for python 3.0
https://pypi.org/project/regex/

#### Spacy
This script also uses spaCy's "en_core_web_lg" English model. Run `python3 -m spacy download en_core_web_lg` to install the required model.
https://spacy.io/models/en

#### Whois (PythonWhois Domain Checker)
Checks domain availability
https://pypi.og/project/python-whois/

- Documentation on Spacy attributes: https://spacy.io/api/annotation#pos-tagging
- Information on dependancy tokens: https://nlp.stanford.edu/software/dependencies_manual.pdf
- For more info on Spacy attributes and tokens: https://stackoverflow.com/questions/40288323/what-do-spacys-part-of-speech-and-dependency-tags-mean

#### Json
Most tmp data will be processed using json format.

#### itertools
The generate_names.py module uses itertools
https://pypi.org/project/more-itertools/

#### sys
Uses sys to import values (eg. filepath) from terminal Command

#### time
Uses time to stop the script for a specific period of time (used for whois domain checker to prevent request overload)

#### random
Uses random to shuffle the generated names

#### datetime
Uses datetime to log current time and date (Used to log when the domain was checked)

# Manual

To run the script, do the following steps:
1. Open Terminal.
2. Change the current working directory to the location where you want to clone the create_names repository.
3. Type `git clone https://github.com/mkishi1221/name_generator_prototype_mk1.git`
4. Press Enter to create your local clone.
5. To use sentences as source data, provide text files in the "data" folder and the names will be generated from the keywords in the provided sentences. Currently accepts English sentences only. (For testing purposes, use the text files provided.)
6. To use keywords as source data, provide text files in the "data/keywords" folder and the names will be generated from those keywords. (For testing purposes, use the text files provided.)
7. Run `create_names_from_sentences.sh` to generate names from sentences.
8. Run `create_names_from_keywords.sh` to generate names from keywords.
9. Check the results using the "names" file in the "results" folder with the current date and time. Names generated using sentences will be named "names_sent_date_time.tsv" and names generated using keywords will be named "names_keyw_date_time.tsv"
