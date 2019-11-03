import unittest
import re
import os
import docx2txt
from odf import text, teletype
from odf.opendocument import load

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

#remaining to test: doc, txt

def convert_to_text(filename, file_extension):
    """
    file_extension e.g. "doc", "pdf", "odt", "odtx", "txt"
    filename e.g. kh_resume, without any file extension
    """
    try:
        
        filepath = filename + "." + file_extension
        if file_extension=='pdf':
            return getPDFcontent(filepath)
        elif file_extension=='odt':
            return getODTContent(filepath)
        elif file_extension=='doc':
            return getDOCcontent(filepath)
        elif file_extension=='txt':
            return getTXTcontent(filepath)
        elif file_extension=='docx':
            return getDocxContent(filepath)
        else:
            print("Please Verify that file extension is PDF, Doc, Docx, odt, txt")
    except:
        return "Verify file_name does not contain file_extension information"


def getDOCcontent(filepath):    #couldnt find a way for Windows so i converted the file, but for mac there is antiword/textract     
    docx_file = '{0}{1}'.format(filepath, 'x')
    content = getDocxContent(docx_file)
    return content

def getTXTcontent(filepath):
    content = open(filepath, "r")
    return content

def getPDFcontent(filepath):
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
    laparams = LAParams(line_margin=0.1)
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

def getDocxContent(filename):
    DocxText = docx2txt.process(filename)
    return DocxText

def getODTContent(filename):
    list=[]
    textdoc = load(filename)
    allparas = textdoc.getElementsByType(text.P)
    for i in range(len(allparas)):
        list.append(teletype.extractText(allparas[i]))
    return ' '.join(list)

def convert_to_text_dir(dir, directory = True):
    """
    Takes in a directory and outputs all the strings found while processing the contents of each resume.

    Input:
    filepath: A directory of files of (PDF/ doc format)’s location in a directory

    Output:
    An array of raw string (in UTF-8 format) containing all the text found, in “sequential” order (Text should be split by 1 space)
    """    
    return ["",""]

