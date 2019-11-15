# Software Engineering

# Development

## Building the Image

Run the following to build the Docker image:

```sh
make build;
```

## Starting a complete environment

Run the following to run the image with a complete expected setup:

```sh
make start;
```

To run a sample:

```sh
curl -vv localhost:5000/0011.doc;
```

To connect to the various MySQL databases, run the following from your host machine:

- READ DB `mysql -ureader -ppassword -h127.0.0.1 -P13306 read`
- WRITE DB `mysql -uwriter -ppassword -h127.0.0.1 -P23306 write`
- PII DB `mysql -ushh -ppassword -h127.0.0.1 -P33306 results`

# Usage

## Retrieving parsed content of an uploaded resume

> PREREQ: for the following example to work, you should have run `make start` so that the application is listening on your host machine at port 5000.

```sh
curl -H "Content-Type: application/json" "http://localhost:5000/parsed_content/pdf/0001.pdf"
```

# Deployment

## Environment Variables

To facilitate testing, we have split up the database into 3 parts, 1 for READ, and 2 for WRITE. 

| Key | Description |
| --- | --- |
| PRODUCTION | If set to `"false"`, enables the debug mode |
| DATA_DIR | Absolute path to the directory that stores the resumes |
| SERVER_ADDRESS | Defines the IP address interface for the server to bind to |
| SERVER_PORT | Defines the port on which the service should listen on |
| PROD_HOST | DB hostname for READ DB |
| PROD_USER | Username for READ DB |
| PROD_PORT | Port number for READ DB |
| PROD_PASSWORD | Password for READ DB |
| PROD_DBNAME | DB database name for READ DB |
| PROD_TABLENAME | DB table name for READ DB |
| PROD_SEP_HOST | DB hostname for WRITE DB 1 |
| PROD_SEP_USER | Username for WRITE DB 1 |
| PROD_SEP_PORT | Port number for WRITE DB 1 |
| PROD_SEP_PASSWORD | Password for  WRITE DB 1 |
| PROD_SEP_DBNAME | DB database name for WRITE DB 1 |
| PROD_SEP_TABLENAME | DB table name for masked data for WRITE DB 1 |
| PROD_SEP_TABLENAME_2 | DB table name for logs for WRITE DB 1 |
| PII_DB_HOST | DB hostname for WRITE DB 2 |
| PII_DB_USER | Username for WRITE DB 2 |
| PII_DB_PORT | Port number for WRITE DB 2 |
| PII_DB_PASSWORD | Password for WRITE DB 2 |
| PII_DB_DBNAME | DB database name for WRITE DB 2 |
| PII_DB_TABLENAME | DB table name for WRITE DB 2 |

Below is the description of 3 sets of database environmental variables.

# Details

## READ Database (`READ DB`)

The READ should be from GovTech's database that contains the resume details such as filenames and filepaths, and is prefixed with `PROD` in the env variables as [`PROD_HOST`, `PROD_USER`, `PROD_PORT`, `PROD_PASSWORD`, `PROD_DBNAME`, `PROD_TABLENAME`].

## WRITE Database 1 (`WRITE DB 1`)

The 1st WRITE should also be to GovTech's database that contains the WRITE location for the output of the Docker functions, i.e the masked resume. This might have the same credentials as the READ database above, but the choice of decoupling is available here. 

The variables are [`PROD_SEP_HOST`, `PROD_SEP_USER`, `PROD_SEP_PORT`, `PROD_SEP_PASSWORD`, `PROD_SEP_DBNAME`, `PROD_SEP_TABLENAME`, `PROD_SEP_TABLENAME_2`].

`PROD_SEP_TABLENAME` is the table that contains the masked resume data.

`PROD_SEP_TABLENAME_2` contains the logs from the exceptions, or function errors in Docker during the masking. They are meant for debugging, especially without access to the raw resume files.

The schema for this `PROD_SEP_TABLENAME_2` table, which is currently named `tmp` can be created by running the scripts at [./db/migrations/prod/201910241022_000_create_tmp.sql](./db/migrations/prod/201910241022_000_create_tmp.sql).

## WRITE Database 2 (`WRITE DB 2`)

The 2nd WRITE should be to GovTech's database that contains the location to store extracted PII data contained inside a dictionary. Using this dictionary, we can see what data was extracted for each of the PII types, such as name and address.

For example, a typical output here looks like:

`{"name": ["Ang Kian"], "nric": ["S4254566Z"], "email": ["angkian@u.nus.edu"], "phone": [], "address": ["Blk456 Choa Chu Kang Loop S680345"]}`

The variables are [`PII_DB_HOST`, `PII_DB_USER`, `PII_DB_PORT`, `PII_DB_PASSWORD`, `PII_DB_DBNAME`, `PII_DB_TABLENAME`].

This might have the same credentials as the READ database above, but the choice of decoupling is available here. 

The schema for this `PII_DB_TABLENAME` table, which is currently named `pii`, can be created by running the script at [./db/migrations/prod/201910241026_000_create_pii.sql](./db/migrations/prod/201910241026_000_create_pii.sql).

## How Files Integrate Together

For this solution to work, Docker has to be connected to a SQL database based on `config.py` and `docker-compose.yml` credentials. These credentials should correspond to the READ & WRITE Database as mentioned from the previous section.

The SQL statements that are ran can be found in `database_READ_config.ini` and `database_WRITE_config.in`, which interacts heavily with `db_connection_READ.py` and `db_connection_WRITE.py` respectively to run SELECT/ INSERT statements that interface with the database.

`main_functions` is where the API routes are implemented, written in python Flask. It executes the data science functions from `convert_to_text.py` and `process_string.py` in the same directory.

Whenever exceptions occur with the API routes, there are 2 places to debug information:
- Immediate output from terminal (or wherever CURL request is called)
- tmp database where error logs are stored

Docker configurations and settings can be found in `Dockerfile` and `Makefile`

## Directory Descriptions

- [data](./data) - Sample resumes as test inputs
- [db/migrations](./data/migrations) - SQL CREATE TABLE statements to initalise new database to interact with Docker functions
- [model_building](./model_building) - Productionsed Dataturks (NLP model) solution

## Endpoints

1) `upload`
##### @app.route('/upload/<jobseeker_document_id>', methods=['POST', 'GET'])

Parameters:
jobseeker_document_id: Primary key of the `jobseeker_documents` table where we want to 
conduct the masking for. 

Function:
    Responds with a string if 2 database insertions are successful:
    `'Success. Parsed contents and PIIs inserted into 2 tables.`
    1 insertion is into the `jobseeker_documents` table, namely the `parsed_content_v2` column, while the other insertion is into the `pii` table, where the `pii_json` column stores the PIIs extracted. 

This takes in a jobseeker_document_id and performs insertion of masked resume and PIIs into the database.

If there are errors, they will be returned to the terminal, and the error message would also be inserted into `tmp` table, which stores log messages for such situations.

```sh
curl localhost:5000/upload/ -d '{"filepath": "bar"}' -H 'Content-Type: application/json'
```

2) `parsed_content`
##### @app.route('/parsed_content/<file_ext>/<file_path>', methods=['GET'])

Parameters:
file_ext: file extension (pdf, doc, docx, odt)
file_path: The file name, without any upstream directories (any upstream directories should be configured in config.py file, under `data_directory` variable)

Function:
    Responds with a JSON structure containing 2 keys:
    1. "content"
    2. "piis"

The "content" key contains the parsed content while the "piis" key contains the mapped PIIs. Call this function to retrieve the parsed content of a pre-existing file that the service has access to. If there is an error, it will be returned to the terminal/ curl request source. 

Given that a local file resume_name.pdf is present in the same directory, run this command:
```sh
curl localhost:5000/parsed_content/pdf/resume_name -H 'Content-Type: application/json'
```

3) `directory_scan`
#### @app.route('/directory_scan/', methods=['GET'])

Parameters:
(None)

Function:
    Responds with a string 
    `'Finished scanning resume directory.`

This function iterates through a directory of resumes and runs the `parsed_content` function, which outputs the masked content and PIIs. Essentially, this allows for an iterative, scalable approach for a large amount of resumes from legacy to be updated, instead of from a singular, real-time approach from the job portal.

If there are errors, the error message would also be inserted into `tmp` table, which stores log messages for such situations.

Due to changing requirements, the function is not fully implemented, and could run `upload` instead of `parsed_content` as per requirements in future changes.

```sh
curl localhost:5000/directory_scan/ -H 'Content-Type: application/json'
```

4) `cron_scan`

Parameters:
Time Duration of how far back in time (relative to now) to filter for recently uploaded resumes from the real-time resume database. Represented in terms of hours.

Function:
    Responds with a dictionary of high-level aggregate metrics for the results from scanning resumes from a timeboxed period. 

If there are errors, the error message would also be inserted into `tmp` table, which stores log messages for such situations.

An example of the output is shown here, for example from resumes uploaded to the database within the last 30 mins:

```
result = {
    "name": 20,
    "nric": 15,
    "email": 17,
    "phone": 14,
    "address": 10
    }
```
    
This shows that among those resumes in the last 30min, how many PIIs of each type (soft/ hard) were found. Over time, more useful metrics could be included, such as:

- number of resumes scanned
- time elapsed
- ids of those resumes with zero outputs (flag for manual inspections)

```sh
curl -X GET localhost:5000/cron_scan/ -d '{"time_duration":438}' -H 'Content-Type: application/json'
```

## Setting up DataTurks on Docker

Prerequiste: Docker is Installed on the machine

1. Start the Docker Service (sudo service docker start)
2. Download the DataTurk Image (curl -o dataturks_docker.tar.gz https://s3-us-west-2.amazonaws.com/images.onprem.com.dataturks/dataturks_docker_3_3_0.tar.gz)
3. Extract the docker (tar -xvzf dataturks_docker.tar.gz)
4. Load dataturks docker image (sudo docker load --input ./dataturks_docker.tar)
5. Start the docker image (sudo docker run -d -p 80:80 dataturks/dataturks:3.3.0)
6. http://localhost (Open Browser)

