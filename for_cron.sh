#! /bin/bash

# Activate the virtual environment
cd /home/gg/Dev/ethicalCommittee_aws/
source ./ec/bin/activate

# run the python script
date >> ./log1
python3 ./backup_creatpdf_uploadpdf.py >> ./log1
