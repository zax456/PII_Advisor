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

###################################################################

directory = os.getcwd()
directory

class Test(unittest.TestCase):

    def test_convert_to_text(self):
        actual = convert_to_text(directory + '/sample_resumes/' + "kh_resume_pdf1.pdf")
        expected = "Ang Kian Hwee Blk123 Choa Chu Kang Loop #02-34 S680341 Email: angkianhwee@u.nus.edu EDUCATION \
        National University of Singapore (NUS) Bachelor of Science (Business Analytics), Honours \
        Aug 2016 – present 25 years old NRIC: S1234567A Relevant Coursework: Data Management and Chinese, \
        Business and Technical Communication, Application Systems Development for Business Analytics, Regression Analysis,\
        Data Structure & Algorithms (Python, Java), Mining Web Data for Business Insights, Operations Research, Capstone Project,\
        Computational Methods for BA Expected Date of Graduation: December 2019"
        self.assertEqual(actual, expected)

    def test_convert_to_text_dir(self):
        actual = convert_to_text_dir("/test_folder")
        expected = ["Not sure what your python lib to parse pdf to text will return", 
                    "Not sure what your python lib to parse pdf to text will return"]
        self.assertEqual(actual, expected)
        
unittest.main(verbosity=2)
