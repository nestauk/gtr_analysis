# Gateway to Research Pilot

This directory contains the code required to setup the Gateway to Research database. There are a number of steps required to get the data into the required format.

1. Install dependencies using `pip install -r setup-requirements.txt`
2. Create a config.json file in the `scripts/` directory in the format:
```javascript
{
  "database": "DATABASE_NAME",
  "schema": "SCHEMA_NAME",
  "user": "USER_NAME",
  "host": "HOST",
  "port": "PORT_NUMBER",
  "passw": "PASSWORD"
}
```
2. `chmod +x` each of the `.py` files in `scripts/` to make them executable.
3. Run the script `db_init.py`. Make sure you have a postgres instance running and a database with the same name as that in your config file. This will create a schema with the relevant tables setup to receive the data.
4. Run each of the scripts named `insert_*.py`. Allow each one to finish before starting the next. These scripts will iterate through the Gateway to Research data, adding each page of returned data to the specified database. This can take some time to complete.
