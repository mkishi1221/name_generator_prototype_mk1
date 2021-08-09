#!/bin/bash
# load database credentials
echo "Loading mongo creds..."
if [[ -f db_creds.env ]]; then
  export $(cat db_creds.env | xargs)
fi