@echo off

REM Step 1: Set up PostgreSQL database
SET DB_USER=db2test
SET DB_PASSWORD=changeit
SET DB_NAME=finforecastdata
SET HOST=localhost
SET PORT=5432
SET DATABASE_URL=postgresql://%DB_USER%:%DB_PASSWORD%@%HOST%:%PORT%/%DB_NAME%
SET CONN_MAX_AGE=600

REM ********************************
REM DO NOT CHANGE THE FOLLOWING LINES
SET CONFIG_FILE="src\conf\config.ini"
if exist %CONFIG_FILE% del %CONFIG_FILE%
call venv\Scripts\activate.bat
REM ********************************

REM Step 1: Set up PostgreSQL database

psql -U postgres -c "CREATE USER %DB_USER% WITH PASSWORD '%DB_PASSWORD%';"
psql -U postgres -c "CREATE DATABASE %DB_NAME% ENCODING 'UTF8' OWNER %DB_USER%;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE %DB_NAME% TO %DB_USER%;"
psql -U postgres -d %DB_NAME% -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO %DB_USER%;"
psql -U %DB_USER% -d %DB_NAME% -f "install\postgres\create_tables.sql"


echo Database setup complete.
echo ********************************
echo *** updating the config file ***
echo ********************************

echo [database] > %CONFIG_FILE%
pause
echo DATABASE_URL = %DATABASE_URL% >> %CONFIG_FILE%
echo CONN_MAX_AGE = %CONN_MAX_AGE% >> %CONFIG_FILE%

echo ********************************
echo *** updating the config ok   ***
echo ********************************

REM Step 2: Run Django migrations
cd src
python manage.py makemigrations
python manage.py migrate

REM Step 3: Load initial data
python manage.py installation_import_institutions
python manage.py installation_import_indicators
python manage.py installation_import_areas

