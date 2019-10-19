# Software Engineering

# Development

## Building the Image

Run the following to build the Docker image:

```sh
make build;
```

## Running the Image as a Container

Run the following to run the image as a container:

```sh
make run;
```

# Deployment

## Environment Variables

To facilitate testing, we have split up the database into 3 parts, 1 for READ, and 2 for WRITE. 

Below is the description of 3 sets of database environmental variables.

## READ Database

The READ should be from GovTech's database that contains the resume details such as filenames and filepaths, and is prefixed with `PROD` in the env variables as [`PROD_HOST`, `PROD_USER`, `PROD_PORT`, `PROD_PASSWORD`, `PROD_DBNAME`, `PROD_TABLENAME`].

## WRITE Database 1

The 1st WRITE should also be to GovTech's database that contains the WRITE location for the output of the Docker functions, i.e the masked resume. This might have the same credentials as the READ database above, but the choice of decoupling is available here. 

The variables are [`PROD_SEP_HOST`, `PROD_SEP_USER`, `PROD_SEP_PORT`, `PROD_SEP_PASSWORD`, `PROD_SEP_DBNAME`, `PROD_SEP_TABLENAME`, `PROD_SEP_TABLENAME_2`].

`PROD_SEP_TABLENAME` is the table that contains the masked resume data.

`PROD_SEP_TABLENAME_2` contains the logs from the exceptions, or function errors in Docker during the masking. They are meant for debugging, especially without access to the raw resume files.

The schema for this `PROD_SEP_TABLENAME_2` table, which is currently named `tmp`:

```sh
create table tmp
(
  tmp_id     int auto_increment primary key,
  created_at datetime      null,
  file_path  varchar(500)  null,
  data       varchar(5000) not null
);
```

## WRITE Database 2

The 2nd WRITE should be to GovTech's database that contains the location to store extracted PII data contained inside a dictionary. Using this dictionary, we can see what data was extracted for each of the PII types, such as name and address.

For example, a typical output here looks like:

`{"name": ["Ang Kian"], "nric": ["S4254566Z"], "email": ["angkian@u.nus.edu"], "phone": [], "address": ["Blk456 Choa Chu Kang Loop S680345"]}`

The variables are [`PII_DB_HOST`, `PII_DB_USER`, `PII_DB_PORT`, `PII_DB_PASSWORD`, `PII_DB_DBNAME`, `PII_DB_TABLENAME`].

This might have the same credentials as the READ database above, but the choice of decoupling is available here. 

The schema for this `PII_DB_TABLENAME` table, which is currently named `pii`:

```sh
create table pii
(
  id              int          auto_increment primary key,
  js_documents_id varchar(256) not null,
  individual_id   char(36)     not null,
  pii_json        json         null
);
```

| Key | Description |
| --- | --- |
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

