## PSQL Migration 
Postgres instructions to export and import DB  

### Export tables
```bash
# login to postgres user psql
sudo -u postgres psql

# once you inside psql command line, connect to bota DB
\c bota

# Copy tables to /tmp/ 
COPY user_info TO '/tmp/user_info.csv' DELIMITER ',' CSV HEADER;
COPY alias TO '/tmp/alias.csv' DELIMITER ',' CSV HEADER;
```

### Import tables
If PSQL is not setup do run `sh db_setup.sh` then the following:
```bash
# login to postgres user psql
sudo -u postgres psql

# once you inside psql command line, connect to bota DB
\c bota

# Copy tables from /tmp/
# Make sure the tables does not have duplicates with the csv or it will fail 
COPY user_info FROM '/tmp/user_info.csv' DELIMITER ',' CSV HEADER;
COPY alias FROM '/tmp/alias.csv' DELIMITER ',' CSV HEADER;
```
