import unittest
#import phonenumbers
#import re

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
    return ("Successfully processed and uploaded resume into database!")

def flagging(raw_text):
    """
      Sub-function within process_string

      Input: Output from convert_to_text()

      Output: returns an array of unique PIIs / returns a dictionary PIIs 
	"""
    nric = re.findall('(?i)[SFTG]\d{7}[A-Z]', raw_text)
    email_address = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", raw_text)
    phone_number = [phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164) for match in phonenumbers.PhoneNumberMatcher(text, "SG")] 

    return {'nric':nric, 'email':email_address, 'phone':phone_number} #e.g. {'email': ['angkianhwee@u.nus.edu'], 'nric': ['S1234567A']}



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
    processed_text = re.sub("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", '<pii: email>', processed_text)
    processed_text = re.sub('(?i)[SFTG]\d{7}[A-Z]', '<pii: nric>', processed_text)
    phone_number_raw = [match.raw_string for match in phonenumbers.PhoneNumberMatcher(text, "SG")] 
	for num in phone_number_raw:
    	processed_text=processed_text.replace(num, "<pii: phone>")

    # if PIIs then remove 
    return processed_text

###################################################################

class Test(unittest.TestCase):
    
    def test_process_string(self):
        raw_text = "Ang Kian Hwee Blk123 Choa Chu Kang Loop #02-34 S680341 \
        Email: angkianhwee@u.nus.edu EDUCATION \
        National University of Singapore (NUS)"
        actual = process_string(raw_text)
        expected = {'Ang Kian Hwee' : 'name', 'Blk123 Choa Chu Kang Loop #02-34' : 'address', 
                    'S680341' : 'nric', 'angkianhwee@u.nus.edu' : 'email'} , 
                    "<pii_name> <pii_address> <pii_nric> \
        Email: <pii_email> EDUCATION \
        National University of Singapore (NUS)"
        self.assertEqual(actual, expected)

# Still up for discussion
#    def test_parsing(self):
#        actual = parsing("Name: Ang Kian Hwee \nAge: 25 \nNRIC: S1234567A \nSkills: Blah blah \nWorking Experience: Blah Blah", 
#                        flagging("Name: Ang Kian Hwee \nAge: 25 \nNRIC: S1234567A \nSkills: Blah blah \nWorking Experience: Blah Blah"))
#
#        expected = "Name: <pii: Name> \nAge: <pii: Age> \nNRIC: <pii: NRIC> \nSkills: Blah blah \nWorking Experience: Blah Blah"
#        self.assertEqual(actual, expected)
#        
#    def test_flagging(self):
#        actual = flagging("Name: Ang Kian Hwee \nAge: 25 \nNRIC: S1234567A \nSkills: Blah blah \nWorking Experience: Blah Blah")
#        expected = ["Ang Kian Hwee", "25", "S1234567A"]
#        self.assertEqual(actual, expected)
        
        
unittest.main(verbosity=2)
