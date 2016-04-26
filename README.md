# Gateway to Research Pilot

This repository contains the code and instructions required to setup the Gateway to Research database and keep it up to date as well as notebooks containing analyses carried out on the data.

There are a number of steps required.

1. Install dependencies using `pip install -r requirements.txt`
2. Run the script `setup_db.py` (Make sure you have a postgres instance running and a database with the same name as that in your config file). This will create a schema with the relevant tables setup to receive data.
3. Run each of the files insert.py singularly. These also require the config file to be set up. These scripts will iterate through the Gateway to Research data, adding each page of returned data to the specified database.
