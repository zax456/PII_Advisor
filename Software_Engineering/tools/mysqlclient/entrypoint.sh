#!/bin/sh
set +ex;
INTERVAL=3;

function run_migrations {
  if [ -d /migrations ]; then
    # read
    mysql -u${READ_DB_USER} -p${READ_DB_PASSWORD} -P${READ_DB_PORT} -h${READ_DB_HOST} ${READ_DB_DATABASE} < /migrations/prod/201910241022_001_create_jobseeker_documents.sql;
    # write
    mysql -u${WRITE_DB_1_USER} -p${WRITE_DB_1_PASSWORD} -P${WRITE_DB_1_PORT} -h${WRITE_DB_1_HOST} ${WRITE_DB_1_DATABASE} < /migrations/prod/201910241022_001_create_jobseeker_documents.sql;
    mysql -u${WRITE_DB_1_USER} -p${WRITE_DB_1_PASSWORD} -P${WRITE_DB_1_PORT} -h${WRITE_DB_1_HOST} ${WRITE_DB_1_DATABASE} < /migrations/prod/201910241022_000_create_tmp.sql;
    # pii storage
    mysql -u${WRITE_DB_2_USER} -p${WRITE_DB_2_PASSWORD} -P${WRITE_DB_2_PORT} -h${WRITE_DB_2_HOST} ${WRITE_DB_2_DATABASE} < /migrations/pii/201910241026_000_create_pii.sql;
  fi;
}

while :; do
  ## read-only db
  echo 'SELECT 1' | mysql \
    -u${READ_DB_USER} \
    -p${READ_DB_PASSWORD} \
    -P${READ_DB_PORT} \
    -h${READ_DB_HOST} \
    ${READ_DB_DATABASE} \
  >/dev/null;
  READ_DB=$?;
  ## writable db
  echo 'SELECT 1' | mysql \
    -u${WRITE_DB_1_USER} \
    -p${WRITE_DB_1_PASSWORD} \
    -P${WRITE_DB_1_PORT} \
    -h${WRITE_DB_1_HOST} \
    ${WRITE_DB_1_DATABASE} \
  >/dev/null;
  WRITE_DB_1=$?;
  ## pii
  echo 'SELECT 1' | mysql \
    -u${WRITE_DB_2_USER} \
    -p${WRITE_DB_2_PASSWORD} \
    -P${WRITE_DB_2_PORT} \
    -h${WRITE_DB_2_HOST} \
    ${WRITE_DB_2_DATABASE} \
  >/dev/null;
  WRITE_DB_2=$?;
  echo "[DB status]: READ/WRITE/PII:${READ_DB}/${WRITE_DB_1}/${WRITE_DB_2}";
  if [ "${READ_DB}" = "0" ] && [ "${WRITE_DB_1}" = "0" ] && [ "${WRITE_DB_2}" = "0" ]; then
    printf -- 'all databases successfully connected\n';
    # run the migrations
    run_migrations;
    INTERVAL=10;
  fi;
  sleep ${INTERVAL};
done;
