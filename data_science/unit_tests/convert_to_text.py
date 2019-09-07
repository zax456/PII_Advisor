import unittest
import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os


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
        
    def contains_word(s, w):
        return f' {w} ' in f' {s} '

    def test_1(self):
        actual = convert_to_text(directory + '/sample_resumes/' + "kh_resume.pdf")
#        this is 1 test case that will pass the test case
#        actual = "Ang Kian Hwee Blk123 Choa Chu Kang Loop #02-34 S680341 Email: angkianhwee@u.nus.edu EDUCATION \
#        National University of Singapore (NUS) Bachelor of Science (Business Analytics), Honours \
#        Aug 2016 – present 25 years old NRIC: S1234567A Relevant Coursework: Data Management and Chinese, \
#        Business and Technical Communication, Application Systems Development for Business Analytics, Regression Analysis,\
#        Data Structure & Algorithms (Python, Java), Mining Web Data for Business Insights, Operations Research, Capstone Project,\
#        Computational Methods for BA Expected Date of Graduation: December 2019"
        actual = actual.lower()
        found = True
        phrases = ['ang kian hwee', 'blk123 choa chu kang loop #02-34 s680341', 'email: angkianhwee@u.nus.edu', 'education',
           'national university of singapore (nus)', 'bachelor of science (business analytics), honours', 'aug 2016 – present',
           '25 years old', 'nric: s1234567a', 'relevant coursework: data management and chinese,', 'business and technical communication,',
           'application systems development for business analytics,', 'regression analysis,', 'data structure & algorithms (python, java),',
           'mining web data for business insights, operations research,', 'capstone project,', 
           'computational methods for ba', 'expected date of graduation: december 2019']
        for p in phrases:
            print(p)
            found = contains_word(actual, p) and found
            
            if not found:
                break
        self.assertTrue(found)
        
unittest.main(verbosity=2)
