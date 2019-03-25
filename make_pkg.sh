#!/bin/bash

PACKAGE=budget_site.zip
TEMP_DIRECTORY=temp
CERTIFICATE_DIRECTORY=$TEMP_DIRECTORY/certificates
BUDGET_SITE_DIRECTORY=$TEMP_DIRECTORY/budget_tracking_tool

#Create the zip directories
rm -rf $TEMP_DIRECTORY
mkdir $TEMP_DIRECTORY
mkdir $CERTIFICATE_DIRECTORY
mkdir $BUDGET_SITE_DIRECTORY

#Copy everything over to the temporary directory structure
cp $BUDGET_TRACKER_CERTIFICATE $CERTIFICATE_DIRECTORY
cp -r budget_tracking_tool $TEMP_DIRECTORY
cp requirements.txt $TEMP_DIRECTORY
cp app.yaml $TEMP_DIRECTORY
cp budget_tracking_tool.py $TEMP_DIRECTORY

#Create a text file with the new environment variables to be loaded by the .bashrc on the server.
echo 'export BUDGET_TRACKER_CERTIFICATE="$HOME/certificates/BudgetTracker-secret.json"' > $TEMP_DIRECTORY/budget_variables.sh
echo "export BUDGET_TRACKER_SECRET_KEY='$BUDGET_TRACKER_SECRET_KEY'" >> $TEMP_DIRECTORY/budget_variables.sh
chmod 755 $TEMP_DIRECTORY/budget_variables.sh
#For google app engine, adjust the variables in the yaml app file
sed -i 's@bt_certificate@$HOME/certificates/BudgetTracker-secret.json@g' $TEMP_DIRECTORY/app.yaml
sed -i 's@bt_secret_key@'"$BUDGET_TRACKER_SECRET_KEY"'@g' $TEMP_DIRECTORY/app.yaml

cd $TEMP_DIRECTORY
zip -r $PACKAGE .
mv $PACKAGE ..
