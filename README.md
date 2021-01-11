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

#### Whois domain checker
Check domain registration using the terminal
https://www.howtogeek.com/680086/how-to-use-the-whois-command-on-linux/
https://www.computerhope.com/unix/uwhois.htm
https://formulae.brew.sh/formula/whois

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

- Documentation on Spacy attributes: https://spacy.io/api/annotation#pos-tagging
- Information on dependancy tokens: https://nlp.stanford.edu/software/dependencies_manual.pdf
- For more info on Spacy attributes and tokens: https://stackoverflow.com/questions/40288323/what-do-spacys-part-of-speech-and-dependency-tags-mean

#### Json
Most tmp data will be processed using json format.

#### itertools
The generate_names.py module uses itertools
https://pypi.org/project/more-itertools/

# Manual

To run the script, do the following steps:
1. Open Terminal.
2. Change the current working directory to the location where you want to clone the create_names repository.
3. Type `git clone https://github.com/mkishi1221/name_generator_prototype_mk1.git`
4. Press Enter to create your local clone.
5. In the "data" folder, provide text files the names will be generated from. (For testing purposes, use the text files provided.)
6. Run `sh create_names.sh`
7. Check the results using the "names.tsv" file in the "results" folder.
