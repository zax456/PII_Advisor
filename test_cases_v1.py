"""
pip install spacy
python -m spacy download en
python -m spacy download xx
pip install pdfminer.six
pip install nltk
"""
import unittest
import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def convert_to_text(filepath):
    """
    Function:
	  Takes in a file and converts contents to python strings. 
	
    Input:
	  filepath: 1 file of (PDF/ doc format) in a directory

    Output:
    A giant string (in UTF-8 format) containing all the text found, in “sequential” order (Text should be split by 1 whitespace)
    """

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(filepath, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def convert_to_text_dir(dir, directory = True):
    """
	Takes in a directory and outputs all the strings found while processing the contents of each resume.

	Input:
	filepath: A directory of files of (PDF/ doc format)’s location in a directory

	Output:
    An array of raw string (in UTF-8 format) containing all the text found, in “sequential” order (Text should be split by 1 space)
	"""    
    return ["",""]


def flagging(raw_text):
    """
      Sub-function within process_text

      Input: Output from convert_to_text()

      Output: returns an array of unique PIIs / returns a dictionary PIIs 
	  """
    nric = re.findall('(?i)[SFTG]\d{7}[A-Z]', raw_text)
    email_address = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", raw_text)
    return {'nric':nric, 'email':email_address} #e.g. {'email': ['angkianhwee@u.nus.edu'], 'nric': ['S1234567A']}


def parsing(raw_text, PIIs):
    """
      Sub-function within process_text. Mask each pii with a <pii: category>, where category is the group which the pii belongs to. 

      Input:
          Text: Output from convert_to_text(), String
          flagged: Output from flagging(), list/dict

      Output: 
      Entire string from convert_to_text() <pii: nric> labels over sensitive information.
    """
    processed_text = raw_text
    # Removing hard PIIs by default: NRIC, email address, phone, physical address
    processed_text = re.sub("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", '<pii: email>', processed_text)
    processed_text = re.sub('(?i)[SFTG]\d{7}[A-Z]', '<pii: nric>', processed_text)
    # if PIIs then remove 
    return processed_text


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

# Tests

# class Test(unittest.TestCase):

#     def test_convert_to_text(self):
#         actual = convert_to_text("test_resume.pdf")
#         expected = "Not sure what your python lib to parse pdf to text will return"
#         self.assertEqual(actual, expected)

#     def test_convert_to_text_dir(self):
#         actual = convert_to_text_dir("/test_folder")
#         expected = ["Not sure what your python lib to parse pdf to text will return", 
#                     "Not sure what your python lib to parse pdf to text will return"]
#         self.assertEqual(actual, expected)

#     def test_flagging(self):
#         actual = flagging("Name: Ang Kian Hwee \nAge: 25 \nNRIC: S1234567A \nSkills: Blah blah \nWorking Experience: Blah Blah")
#         expected = ["Ang Kian Hwee", "25", "S1234567A"]
#         self.assertEqual(actual, expected)
    
#     def test_parsing(self):
#         actual = parsing("Name: Ang Kian Hwee \nAge: 25 \nNRIC: S1234567A \nSkills: Blah blah \nWorking Experience: Blah Blah", 
#                         flagging("Name: Ang Kian Hwee \nAge: 25 \nNRIC: S1234567A \nSkills: Blah blah \nWorking Experience: Blah Blah"))

#         expected = "Name: <pii: Name> \nAge: <pii: Age> \nNRIC: <pii: NRIC> \nSkills: Blah blah \nWorking Experience: Blah Blah"
#         self.assertEqual(actual, expected)

#     def test_process_string(self):
#         raw = convert_to_text("test_resume.pdf")
#         actual = process_string(raw)
#         expected = "Successfully processed and uploaded resume into database!"
#         self.assertEqual(actual, expected)

#unittest.main(verbosity=2)

pdf1_text = convert_to_text("test_folder/test_resume_pdf1.pdf")
print("#################  CONVERT TO TEXT 1 ##################")
print(pdf1_text)
pdf2_text = convert_to_text("test_folder/test_resume_pdf2.pdf")
print("#################  CONVERT TO TEXT 2 ##################")
print(pdf2_text)
flag_pdf2_text = flagging(pdf2_text)
print("#################  FLAG 1 ##################")
print(flag_pdf2_text)
parse_pdf2_text = parsing(pdf2_text,flag_pdf2_text)
print("#################  PARSE 1 ##################")
print(parse_pdf2_text)