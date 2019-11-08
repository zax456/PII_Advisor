import unittest
import phonenumbers
import re
from textblob import TextBlob
import spacy
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from pdfminer.pdfpage import PDFPage
#from io import StringIO
from db_connection_WRITE import db_connection_WRITE
db_function_write = db_connection_WRITE("database_WRITE_config.ini")

def process_string(raw_text):
    """
    Takes in a string and outputs a parsed string. Calls flagging() and parsing() functions to identify PIIs and mask the data respectively. 
    
    The raw string, Output from flagging(), Output from parsing() will be upsert into 3 different columns (Raw Contents, PIIs, Parsed Contents)
    for the record with the same uuid in database.

    Input:
      text: String output from convert_to_text()

    Main Output:
      Returns HTTP status code 201 and indication msg to signify processing was done successfully. Upserts the values into database.

      Secondary (Indirect) Output:
      The raw resume string, Output from flagging(), Output from parsing() will be upsert into 3 different columns for the record with the same uuid in database. 
    """
    try:
        PIIs = flagging(raw_text)
        parse_text = parsing(raw_text, PIIs)
        return PIIs, parse_text
    except Exception as e: 
        tmp = {
        "file_path": "process_string function",
        "data": e
        }
        db_function_write._insert_tmp(tmp)
        return
    # return ("Successfully processed and uploaded resume into database!")

def flagging(raw_text):
    """
      Sub-function within process_string

      Input: Output from convert_to_text()

      Output: returns an array of unique PIIs / returns a dictionary of lists of PIIs (there might be more than 1 value for 1 key, for exmaple giving home + personal phone number)
    """
    try:
        nric = re.findall('(?i)[SFTG]\d{7}[A-Z]', raw_text)
        email_address = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", raw_text)
        phone_number = [phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164) for match in phonenumbers.PhoneNumberMatcher(raw_text, "SG")] 
        search_physical_address = re.search('([A-Za-z]{2,6}[\s]?|)[\d]{1,4}' + # block/street number (e.g. Blk 123, Street 52, 133, St 55)
                                            '[\s]?' +
                                            '[A-Za-z]{,2}' + # block suffix (e.g. the 'A' in Block 60A)
                                            '[\s]' +
                                            '[\D]{5,}.+' + # road/street name (e.g. Kent Ridge Drive)
                                            '[Ss][A-Za-z]{,8}[\s]?[\d]{6}' # postal code (e.g. S123456, Singapore 123456)
                                            , raw_text)
        physical_address = search_physical_address.group() if search_physical_address is not None else ''
        name = process_name(raw_text).strip() if type(raw_text) == str else ''
        return {'nric':nric,
                'email':email_address,
                'phone':phone_number,
                'address':[physical_address] if physical_address else [],
                'name':[name] if name else []
                }
    except Exception as e: 
        tmp = {
        "file_path": "flagging function",
        "data": e
        }
        db_function_write._insert_tmp(tmp)
        return

def parsing(raw_text, dic):
    """
      Sub-function within process_string. Mask each pii with a <pii: category>, where category is the group which the pii belongs to. 

      Input:
          raw_text: Output from convert_to_text(), String
          dic: Output from flagging(), list/dict

      Output: 
      Entire string from convert_to_text() <pii: nric> labels over sensitive information.
    """
    try:
        processed_text = raw_text
        # Removing hard PIIs by default: NRIC, email address, phone, physical address
        processed_text = re.sub("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", '<pii_email>', processed_text)
        processed_text = re.sub('(?i)[SFTG]\d{7}[A-Z]', '<pii_nric>', processed_text)
        phone_number_raw = [match.raw_string for match in phonenumbers.PhoneNumberMatcher(processed_text, "SG")] 
        for num in phone_number_raw:
            processed_text=processed_text.replace(num, "<pii_phone>")
        processed_text = re.sub('([A-Za-z]{2,6}[\s]?|)[\d]{1,4}' + # block/street number (e.g. Blk 123, Street 52, 133, St 55)
                                '[\s]?' +
                                '[A-Za-z]{,2}' + # block suffix (e.g. the 'A' in Block 60A)
                                '[\s]' +
                                '[\D]{5,}.+' + # road/street name (e.g. Kent Ridge Drive)
                                '[Ss][A-Za-z]{,8}[\s]?[\d]{6}' # postal code (e.g. S123456, Singapore 123456)
                                , '<pii_address>'
                                , processed_text)
        if dic['name'] != []:
            processed_text = re.sub(dic['name'][0], '<pii_name>', processed_text)
        processed_text = " ".join(processed_text.split())
        processed_text = processed_text.replace("#", '') # remove redundant characters
        # if PIIs then remove 
        return processed_text
    except Exception as e: 
        tmp = {
        "file_path": "parsing function",
        "data": e
        }
        db_function_write._insert_tmp(tmp)
        return

def process_name(raw_text):
    """
      Sub-function within flagging. Identifies Name by extracting the first string of noun/ "JJ" included for Indian Names

      Input:
          raw_text: Output from convert_to_text(), String Type

      Output: 
      Name of string type
      """
    try:
        nlp = spacy.load("model_building/model")
        doc = nlp(raw_text)
        for ent in doc.ents:  
            if ent.label_ == "NAME":
                return ent.text
    except Exception as e: 
        tmp = {
        "file_path": "process_name function",
        "data": e
        }
        db_function_write._insert_tmp(tmp)
        return