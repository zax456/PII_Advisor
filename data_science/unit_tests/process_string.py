import unittest
import phonenumbers
import re
from textblob import TextBlob

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
    phone_number = [phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164) for match in phonenumbers.PhoneNumberMatcher(raw_text, "SG")] 
    search_physical_address = re.search('([A-Za-z]{2,6}[\s]?|)[\d]{1,4}' + # block/street number (e.g. Blk 123, Street 52, 133, St 55)
                                        '[\s]?' +
                                        '[A-Za-z]{,2}' + # block suffix (e.g. the 'A' in Block 60A)
                                        '[\s]' +
                                        '[\D]{5,}.+' + # road/street name (e.g. Kent Ridge Drive)
                                        '[Ss][A-Za-z]{,8}[\s]?[\d]{6}' # postal code (e.g. S123456, Singapore 123456)
                                        , raw_text)
    physical_address = [search_physical_address.group() if search_physical_address is not None else '']
    name = process_name(raw_text).strip()
    return {'nric':nric,
            'email':email_address,
            'phone':phone_number,
            'address':physical_address,
            'name':[name]
            }

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
    processed_text = re.sub(dic['name'][0], '<pii_name>', processed_text) 
    processed_text = " ".join(processed_text.split())  
    processed_text = processed_text.replace("#", '') # remove redundant characters
    # if PIIs then remove 
    return processed_text

def process_name(raw_text):
    """
      Sub-function within flagging. Identifies Name by extracting the first string of noun/ "JJ" included for Indian Names

      Input:
          raw_text: Output from convert_to_text(), String Type

      Output: 
      Name of string type
      """  
    sentences = raw_text.split('\n')
    for i in sentences:
        blob = TextBlob(i)
        if len(blob.tags) >=2 and all(tag in ("NNP","NNS", "NN", "JJ") for words,tag in blob.tags):
            return i    

###################################################################

class Test(unittest.TestCase):
    
    def test_1(self):
        raw_text = "Ang Kian Hwee \n Blk123 Choa Chu Kang Loop #02-34 S680341 \n \
        \nEmail: angkianhwee@u.nus.edu \n\n EDUCATION\n \
        National University of Singapore (NUS)"
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
        dic, parsed_string = process_string(raw_text)
        
        # match each key to each value
        test_dic = {'name': ['Ang Kian Hwee'], 'address': ['Blk123 Choa Chu Kang Loop #02-34 S680341'], 
                    'email': ['angkianhwee@u.nus.edu'], 'nric':[], 'phone':[]}
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
        raw_text = "ALICE TAN MING NI  \n\n  S4598004D \n\n16 JIAK CHUAN RD, SINGAPORE 089267 \n\n\
                    +65 9722 4728 # FUNNYGIRL111@AOL.COM # HTTPS://LINKEDIN.COM/ALICEELIOT \n\n \n\nSummary \n\
                    Experienced Server bringing enthusiasm, dedication and an exceptional work ethic. \
                    Trained in customer \n service with knowledge of Italy cuisine. High energy and outgoing \
                    with a dedication to positive guest \nrelations. High volume dining customer service, and \
                    cash handling background."

        dic, parsed_string = process_string(raw_text)
        
        # match each key to each value
        test_dic = {'name': ['ALICE TAN MING NI'], 'nric': ['S4598004D'], 'address': ['16 JIAK CHUAN RD, SINGAPORE 089267'], 
                    'email': ['FUNNYGIRL111@AOL.COM'], 'phone': ['+6597224728']}
        dic_check = True
        pii_keys = ['name', 'address', 'email', 'nric', 'phone']       
        for key in pii_keys:
            if dic[key] != test_dic[key]:
                dic_check = False
                break
            
        test_string = "<pii_name> <pii_nric> <pii_address> \
        <pii_phone> <pii_email> HTTPS://LINKEDIN.COM/ALICEELIOT Summary\
        Experienced Server bringing enthusiasm, dedication and an exceptional work ethic.\
        Trained in customer service with knowledge of Italy cuisine. High energy and outgoing\
        with a dedication to positive guest relations. High volume dining customer service, and\
        cash handling background."
        
        # replace multiple spaces between text with single space
        test_string = re.sub(' +', ' ', test_string)
        parsed_string = re.sub(' +', ' ', parsed_string)        
        if parsed_string == test_string:
            parsed_string_check = True
        else:
            parsed_string_check = False   
        self.assertTrue(parsed_string_check and dic_check)
   
# run this line
unittest.main(verbosity=2)

        