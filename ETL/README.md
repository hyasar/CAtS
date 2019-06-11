# ETL for Controller Data
## Database Schema
There are two tables for database "cats": 
### Table1: groups
* gid: group id, varchar(5), primary key, external key, not null
* title: group title, varchar(100), not null
### Table2: controllers
* cid: controller id, varchar(10), primary key, not null
* gid: group id, varchar(5), external key, not null
* pid: parent controller id(only valid for subcontrollers), varchar(10)
* title: controller title, varchar(100), not null
* classinfo: controller class, varchar(32)
* parameters: json
* properties: json
* links: json
* parts: json
* high: controller priority, boolean
* moderate: controller priority, boolean
* low: controller priority, boolean

## How to dump and restore database?
To dump database:
```
pg_dump -U cats cats > controller_db_dump.sql
```
To restore database:
```
psql -U cats cats < controller_db_dump.sql
```

## How to load data from raw json file?
* Create a virtual environment
```
virtualenv venv
source venv/bin/activate
```
* Install dependencies

  If postgresql has not been installed, run
  ```
  sudo apt-get install postgresql
  ```

  Then install other dependencies
  ```
  sudo apt-get install python-psycopg2
  sudo apt-get install libpq-dev
  pip install psycopg2
  pip install sqlalchemy
  ```
  
* Run script to automatically build table "groups" and "controllers"
```
python load_data_catagory.py
```
