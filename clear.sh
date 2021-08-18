# load database credentials
if [[ -f db_creds.env ]]; then
  export $(cat db_creds.env | xargs)
fi
python3 drop_all_lists.py
rm -rf tmp ref