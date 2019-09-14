FROM python:3-onbuild

ADD . D:\AKH_Folder/Work/University/Year 4 Sem 1/BT3101 Business Analytics Capstone Project/pii/data_science/unit_tests/sample_resumes/

COPY convert_to_text.py convert_to_text.py
COPY process_string.py process_string.py
COPY db_connection.py db_connection.py

EXPOSE 5000

# ENTRYPOINT python run.py
CMD [ "python", "run.py" ]