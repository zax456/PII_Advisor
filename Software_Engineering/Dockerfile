FROM python:3-onbuild

ENV PROD_HOST=bt3101-govtech.cu5hwpemnxbf.ap-southeast-1.rds.amazonaws.com
ENV PROD_USER=admin
ENV PROD_PORT=3306
ENV PROD_PASSWORD=capstone123!
ENV PROD_DBNAME=govtech_external
ENV PROD_TABLENAME=jobseeker_documents

ENV PROD_SEP_HOST=bt3101-govtech.cu5hwpemnxbf.ap-southeast-1.rds.amazonaws.com
ENV PROD_SEP_USER=admin
ENV PROD_SEP_PORT=3306
ENV PROD_SEP_PASSWORD=capstone123!
ENV PROD_SEP_DBNAME=govtech_external
ENV PROD_SEP_TABLENAME=jobseeker_documents_2
ENV PROD_SEP_TABLENAME_2=tmp

ENV PII_DB_HOST=bt3101-govtech.cu5hwpemnxbf.ap-southeast-1.rds.amazonaws.com
ENV PII_DB_USER=admin
ENV PII_DB_PORT=3306
ENV PII_DB_PASSWORD=capstone123!
ENV PII_DB_DBNAME=govtech_external
ENV PII_DB_TABLENAME=pii

COPY convert_to_text.py convert_to_text.py
COPY process_string.py process_string.py
COPY db_connection_READ.py db_connection_READ.py
COPY db_connection_WRITE.py db_connection_WRITE.py

EXPOSE 5000

# ENTRYPOINT python run.py
CMD [ "python", "run.py" ]