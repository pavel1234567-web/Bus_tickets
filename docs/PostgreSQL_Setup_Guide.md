# PostgreSQL Setup Guide for Bus Tickets System

This guide will help you set up PostgreSQL and migrate from SQLite to PostgreSQL for the Bus Tickets System.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Install PostgreSQL](#install-postgresql)
3. [Configure PostgreSQL](#configure-postgresql)
4. [Create Database](#create-database)
5. [Configure Django Settings](#configure-django-settings)
6. [Install Required Packages](#install-required-packages)
7. [Run Migrations](#run-migrations)
8. [Migrate Data from SQLite](#migrate-data-from-sqlite)
9. [Load Sample Data](#load-sample-data)
10. [Test the System](#test-the-system)
11. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.8+ installed
- Django project already set up
- Administrative access to your system
- Internet connection for package installation

## Install PostgreSQL

### Windows

1. **Download PostgreSQL Installer**
   - Visit [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
   - Download the latest stable version
   - Run the installer

2. **Installation Steps**
   - Choose installation directory (default: `C:\Program Files\PostgreSQL\XX`)
   - Select components (keep defaults)
   - Set data directory (default: `C:\Program Files\PostgreSQL\XX\data`)
   - Set password for `postgres` user (remember this password!)
   - Set port (default: 5432)
   - Complete installation

3. **Add PostgreSQL to PATH**
   - Add `C:\Program Files\PostgreSQL\XX\bin` to system PATH
   - Restart command prompt

### macOS

```bash
# Using Homebrew (recommended)
brew install postgresql
brew services start postgresql

# Or download from official site
# https://www.postgresql.org/download/macosx/
```

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Configure PostgreSQL

### 1. Set Password for postgres User

```bash
# Switch to postgres user
sudo -u postgres psql

# Inside PostgreSQL shell
ALTER USER postgres PASSWORD 'your_password_here';
\q
```

### 2. Create Database User (Optional)

```bash
# Create dedicated user for the application
sudo -u postgres createuser --interactive

# Or create with SQL
sudo -u postgres psql
CREATE USER bus_tickets_user WITH PASSWORD 'your_password';
ALTER USER bus_tickets_user CREATEDB;
\q
```

## Create Database

### Option 1: Using Command Line

```bash
# Create database
sudo -u postgres createdb bus_tickets_db

# Or with specific user
sudo -u postgres createdb -O bus_tickets_user bus_tickets_db
```

### Option 2: Using SQL

```bash
sudo -u postgres psql
CREATE DATABASE bus_tickets_db;
\q
```

### Option 3: Using Python Script

The project includes a migration script that creates the database automatically:

```bash
python scripts/migrate_to_postgresql.py
```

## Configure Django Settings

### 1. Install Required Packages

```bash
# Install psycopg2 for PostgreSQL support
pip install psycopg2-binary

# Or if you encounter issues on Windows
pip install psycopg2
```

### 2. Update .env File

Edit `.env` file in project root:

```env
# Database Configuration
USE_SQLITE=False

# PostgreSQL Database Settings
DB_NAME=bus_tickets_db
DB_USER=postgres
DB_PASSWORD=your_actual_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

### 3. Verify Settings

The `settings.py` file is already configured to switch between SQLite and PostgreSQL based on the `USE_SQLITE` setting.

## Install Required Packages

```bash
# Install all required packages
pip install -r requirements.txt

# Additional packages for PostgreSQL
pip install psycopg2-binary python-decouple
```

## Run Migrations

### 1. Test Database Connection

```bash
# Test PostgreSQL connection
python manage.py dbshell --database=default

# If connected successfully, you'll see PostgreSQL prompt
```

### 2. Run Django Migrations

```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate
```

## Migrate Data from SQLite

### Option 1: Using Automated Script

```bash
# Run the migration script
python scripts/migrate_to_postgresql.py
```

### Option 2: Manual Migration

1. **Export SQLite Data**

```bash
# Export data from SQLite
python manage.py dumpdata --natural-foreign --natural-primary > sqlite_data.json
```

2. **Import to PostgreSQL**

```bash
# Switch to PostgreSQL in .env (USE_SQLITE=False)
# Run migrations first
python manage.py migrate

# Import data
python manage.py loaddata sqlite_data.json
```

### Option 3: Using SQL Scripts

```bash
# Export SQLite data
sqlite3 db.sqlite3 .dump > sqlite_dump.sql

# Convert and import to PostgreSQL
# (Manual conversion may be required for some data types)
```

## Load Sample Data

After migration, you can load sample data:

```bash
# Load all sample data at once
psql -U postgres -d bus_tickets_db -f sql/00_all_sample_data.sql

# Or load individual tables
psql -U postgres -d bus_tickets_db -f sql/01_routes_sample_data.sql
psql -U postgres -d bus_tickets_db -f sql/02_buses_sample_data.sql
# ... continue with other files
```

## Test the System

### 1. Create Superuser

```bash
python manage.py createsuperuser
```

### 2. Test Database Operations

```bash
# Test Django shell
python manage.py shell

# In shell:
from tickets.models import Route, Bus, Schedule
print(f"Routes: {Route.objects.count()}")
print(f"Buses: {Bus.objects.count()}")
print(f"Schedules: {Schedule.objects.count()}")
```

### 3. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000/admin/` to test the system.

## Switching Between Databases

### Switch to PostgreSQL

Edit `.env`:
```env
USE_SQLITE=False
```

### Switch back to SQLite

Edit `.env`:
```env
USE_SQLITE=True
```

## Production Configuration

### 1. Environment Variables

For production, set environment variables instead of `.env`:

```bash
export USE_SQLITE=False
export DB_NAME=bus_tickets_production
export DB_USER=bus_tickets_user
export DB_PASSWORD=secure_password
export DB_HOST=localhost
export DB_PORT=5432
```

### 2. Security Settings

```python
# settings.py for production
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'OPTIONS': {
            'MAX_CONNS': 20,
            'MIN_CONNS': 5,
        }
    }
}
```

## Troubleshooting

### Common Issues

#### 1. Connection Refused

**Error**: `could not connect to server: Connection refused`

**Solution**:
- Check if PostgreSQL is running: `sudo systemctl status postgresql`
- Verify port: `netstat -an | grep 5432`
- Check firewall settings

#### 2. Authentication Failed

**Error**: `FATAL: password authentication failed for user "postgres"`

**Solution**:
- Verify password in `.env` file
- Reset PostgreSQL password:
  ```bash
  sudo -u postgres psql
  ALTER USER postgres PASSWORD 'new_password';
  ```

#### 3. Database Doesn't Exist

**Error**: `FATAL: database "bus_tickets_db" does not exist`

**Solution**:
- Create database: `sudo -u postgres createdb bus_tickets_db`
- Check database name in `.env`

#### 4. Permission Denied

**Error**: `permission denied for database`

**Solution**:
- Grant permissions to user:
  ```sql
  GRANT ALL PRIVILEGES ON DATABASE bus_tickets_db TO bus_tickets_user;
  ```

#### 5. psycopg2 Installation Issues

**Windows**: Install Visual C++ Build Tools or use `psycopg2-binary`

**Linux**: Install development packages:
```bash
sudo apt install libpq-dev python3-dev
```

### Debug Connection Issues

```python
# Test connection script
import psycopg2

try:
    conn = psycopg2.connect(
        dbname='bus_tickets_db',
        user='postgres',
        password='your_password',
        host='localhost',
        port='5432'
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
```

### Reset Everything

If you need to start over:

```bash
# Drop database
sudo -u postgres dropdb bus_tickets_db

# Recreate database
sudo -u postgres createdb bus_tickets_db

# Run migrations
python manage.py migrate

# Load sample data
psql -U postgres -d bus_tickets_db -f sql/00_all_sample_data.sql
```

## Performance Optimization

### 1. Database Configuration

Edit `postgresql.conf`:
```ini
# Memory settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB

# Connection settings
max_connections = 100
```

### 2. Django Settings

```python
# Connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bus_tickets_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'MAX_CONNS': 20,
            'MIN_CONNS': 5,
        }
    }
}
```

### 3. Indexing

Add indexes to frequently queried fields:

```python
# In models.py
class Route(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    departure_city = models.CharField(max_length=100, db_index=True)
    arrival_city = models.CharField(max_length=100, db_index=True)
```

## Backup and Recovery

### 1. Backup Database

```bash
# Full backup
pg_dump -U postgres -d bus_tickets_db > backup.sql

# Compressed backup
pg_dump -U postgres -d bus_tickets_db | gzip > backup.sql.gz
```

### 2. Restore Database

```bash
# Restore from backup
psql -U postgres -d bus_tickets_db < backup.sql

# Restore from compressed backup
gunzip -c backup.sql.gz | psql -U postgres -d bus_tickets_db
```

### 3. Automated Backup

Create backup script `backup_db.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="bus_tickets_backup_$DATE.sql"

pg_dump -U postgres -d bus_tickets_db > $BACKUP_FILE
gzip $BACKUP_FILE

echo "Backup completed: $BACKUP_FILE.gz"
```

Add to crontab for daily backups:
```bash
0 2 * * * /path/to/backup_db.sh
```

---

## Summary

After completing these steps:

1. PostgreSQL is installed and configured
2. Database `bus_tickets_db` is created
3. Django is configured to use PostgreSQL
4. Data is migrated from SQLite (if applicable)
5. Sample data is loaded
6. System is tested and working

Your Bus Tickets System is now running on PostgreSQL with better performance, scalability, and reliability compared to SQLite.
