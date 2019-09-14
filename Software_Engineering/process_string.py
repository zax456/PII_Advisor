import unittest

import re

#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from pdfminer.pdfpage import PDFPage
#from io import StringIO

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
    PIIs = flagging(raw_text)
    parse_text = parsing(raw_text, PIIs)
    return PIIs, parse_text # for testing purposes only...remove this after confirming process_string works
    # return ("Successfully processed and uploaded resume into database!")

def flagging(raw_text):
    """
      Sub-function within process_string

      Input: Output from convert_to_text()

      Output: returns an array of unique PIIs / returns a dictionary of lists of PIIs (there might be more than 1 value for 1 key, for exmaple giving home + personal phone number)
	"""
    nric = re.findall('(?i)[SFTG]\d{7}[A-Z]', raw_text)
    email_address = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", raw_text)
    return {'email': [email_address], 'nric': [nric]}

def parsing(raw_text, dic):
    """
      Sub-function within process_string. Mask each pii with a <pii: category>, where category is the group which the pii belongs to. 

      Input:
          raw_text: Output from convert_to_text(), String
          dic: Output from flagging(), list/dict

      Output: 
      Entire string from convert_to_text() <pii: nric> labels over sensitive information.
    """
    processed_text = raw_text
    # Removing hard PIIs by default: NRIC, email address, phone, physical address
    processed_text = re.sub("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", '<pii_email>', processed_text)
    processed_text = re.sub('(?i)[SFTG]\d{7}[A-Z]', '<pii_nric>', processed_text)
    # if PIIs then remove 
    return processed_text

###################################################################

class Test(unittest.TestCase):
    
    def test_1(self):
        raw_text = "Ang Kian Hwee Blk123 Choa Chu Kang Loop #02-34 S680341 \
        Email: angkianhwee@u.nus.edu EDUCATION \
        National University of Singapore (NUS)"
        dic, parsed_string = process_string(raw_text)
        
        # match each key to each value
        test_dic = {'name': ['Ang Kian Hwee'], 'address': ['Blk123 Choa Chu Kang Loop #02-34 S680341'], 
                    'email': ['angkianhwee@u.nus.edu']}
        dic_check = True
        pii_keys = ['name', 'address', 'email', 'nric', 'phone']
        for key in pii_keys:
            if dic[key] != test_dic[key]:
                dic_check = False
                break
            
        test_string = "<pii_name> <pii_address> Email: <pii_email> EDUCATION National University of Singapore (NUS)"
        if parsed_string == test_string:
            parsed_string_check = True
        else:
            parsed_string_check = False
        self.assertTrue(parsed_string_check and dic_check)
        
        
        
    def test_2(self):
        raw_text = "ALICE TAN MING NI S4598004D 16 JIAK CHUAN RD, SINGAPORE 089267 \
        +65 9722 4728 FUNNYGIRL111@AOL.COM HTTPS://LINKEDIN.COM/ALICEELIOT Summary\
        Experienced Server bringing enthusiasm, dedication and an exceptional work ethic.\
        Trained in customer service with knowledge of Italy cuisine. High energy and outgoing\
        with a dedication to positive guest relations. High volume dining customer service, and\
        cash handling background."
        dic, parsed_string = process_string(raw_text)
        
        # match each key to each value
        test_dic = {'name': ['ALICE TAN MING NI'], 'nric': ['S4598004D'], 'address': ['16 JIAK CHUAN RD, SINGAPORE 089267'], 
                    'email': ['angkianhwee@u.nus.edu'], 'phone': ['+65 9722 4728']}
        dic_check = True
        pii_keys = ['name', 'address', 'email', 'nric', 'phone']
        for key in pii_keys:
            if dic[key] != test_dic[key]:
                dic_check = False
                break
            
        test_string = "<pii_name> <pii_nric>  <pii_address> \
        <pii_phone> <pii_email> HTTPS://LINKEDIN.COM/ALICEELIOT Summary\
        Experienced Server bringing enthusiasm, dedication and an exceptional work ethic.\
        Trained in customer service with knowledge of Italy cuisine. High energy and outgoing\
        with a dedication to positive guest relations. High volume dining customer service, and\
        cash handling background."
        if parsed_string == test_string:
            parsed_string_check = True
        else:
            parsed_string_check = False
        self.assertTrue(parsed_string_check and dic_check)
   
# run this line
# unittest.main(verbosity=2)

        