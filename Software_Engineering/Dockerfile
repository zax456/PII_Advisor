FROM python:3-onbuild

COPY convert_to_text.py convert_to_text.py
COPY process_string.py process_string.py
COPY db_connection_READ.py db_connection_READ.py
COPY db_connection_WRITE.py db_connection_WRITE.py

EXPOSE 5000

# ENTRYPOINT python run.py
CMD [ "python", "run.py" ]