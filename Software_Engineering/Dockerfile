FROM python:3-onbuild

COPY convert_to_text.py convert_to_text.py
COPY process_string.py process_string.py
COPY db_connection.py db_connection.py

EXPOSE 5000

# ENTRYPOINT python run.py
CMD [ "python", "run.py" ]