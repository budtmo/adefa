#!/bin/bash

WHEELHOUSE_FOLDER=wheelhouse
ZIP_FILE=test_scripts_app.zip

# Remove old files
rm -rf $WHEELHOUSE_FOLDER && rm -f $ZIP_FILE

# Create wheel archive
pip wheel --wheel-dir wheelhouse -r requirements.txt

# Zip tests/, wheelhouse/, and requirements.txt
zip -r $ZIP_FILE tests/ $WHEELHOUSE_FOLDER/ requirements.txt
