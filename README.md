# Auto Ria Test Task

The test scraping written on Python


### Installing using GitHub

- Python3 must be already installed
- Install PostgreSQL and create db

```shell
git clone https://github.com/Viktor-Beniukh/auto_ria_test_task.git
cd auto_ria_test_task
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python insert_or_update_data_to_db.py

```
You need to create `.env` file and add there the variables with your according values:
- `POSTGRES_DB`: this is databases name;
- `POSTGRES_USER`: this is username for databases;
- `POSTGRES_PASSWORD`: this is username password for databases;
- `POSTGRES_HOST`: this is host name for databases;
- `POSTGRES_PORT`: this is port for databases;
- `CELERY_BROKER_URL`: this is url redis broker;
- `CELERY_RESULT_BACKEND`: this is redis data to save of data on backend.


## Run with docker

Docker should be installed

- Create docker image: `docker-compose build`
- Run docker app: `docker-compose up`
