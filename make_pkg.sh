#!/bin/bash

PACKAGE=budget_site.zip
TEMP_DIRECTORY=temp
CERTIFICATE_DIRECTORY=$TEMP_DIRECTORY/certificates
BUDGET_SITE_DIRECTORY=$TEMP_DIRECTORY/site

#Create the zip directories
rm -rf $TEMP_DIRECTORY
mkdir $TEMP_DIRECTORY
mkdir $CERTIFICATE_DIRECTORY
mkdir $BUDGET_SITE_DIRECTORY

#Copy everything over to the temporary directory structure
cp $BUDGET_TRACKER_CERTIFICATE $CERTIFICATE_DIRECTORY
cp -r budget_tracking_tool/ $BUDGET_SITE_DIRECTORY
cp budget_tracking_tool.fcgi $BUDGET_SITE_DIRECTORY
cp Requirements*.txt $TEMP_DIRECTORY

#Create a text file with the new environment variables to be loaded by the .bashrc on the server.
echo 'export BUDGET_TRACKER_CERTIFICATE="~/certificates/BudgetTracker-secret.json"' > $TEMP_DIR/budget_variables.sh
echo 'export BUDGET_TRACKER_SECRET_KEY="$BUDGET_TRACKER_SECRET_KEY"' >> $TEMP_DIR/budget_variables.sh

zip -r $PACKAGE $TEMP_DIRECTORY



