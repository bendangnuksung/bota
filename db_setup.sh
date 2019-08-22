# Refernce to install postgres
# https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04

# Install DB requirements
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo apt-get install libpq-dev python-dev
sudo pip3 install psycopg2

# Default password for user postgres
echo "Setting up Postgres password, database and table"
password="bota@123"
sudo -u postgres psql -c "ALTER USER postgres PASSWORD '$password';"
sudo -u postgres psql -c "CREATE DATABASE bota;"
sudo -u postgres psql -d bota -c "create table user_info (discord_id bigint unique,discord_name text,steam_id bigint, language text, others jsonb);"
sudo -u postgres psql -d bota -c "create table alias (alias_name text unique,steam_id bigint, discord_id bigint);"