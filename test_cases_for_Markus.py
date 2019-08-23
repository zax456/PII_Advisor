import unittest


def convert_to_text(filepath):
    """
    Function:
	Takes in a file and converts contents to python strings. 
	
    Input:
	filepath: 1 file of (PDF/ doc format) in a directory

    Output:
    A giant string (in UTF-8 format) containing all the text found, in “sequential” order (Text should be split by 1 whitespace)
    """
    return ""


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
    return [""]


def parsing(raw_text, PIIs):
    """
      Sub-function within process_text. Mask each pii with a <pii: category>, where category is the group which the pii belongs to. 

      Input:
          Text: Output from convert_to_text(), String
          flagged: Output from flagging(), list/dict

      Output: 
      Entire string from convert_to_text() <pii: nric> labels over sensitive information.
    """
    return ""


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

class Test(unittest.TestCase):

    def test_convert_to_text(self):
        actual = convert_to_text("test_resume.pdf")
        expected = ""
        self.assertEqual(actual, expected)

    def test_convert_to_text_dir(self):
        actual = convert_to_text_dir("test_resume.pdf")
        expected = "An arry of text"
        self.assertEqual(actual, expected)

    def test_flagging(self):
        actual = flagging("Some text")
        expected = ""
        self.assertEqual(actual, expected)
    
    def test_parsing(self):
        actual = parsing("test_resume.pdf", flagging("Some text"))
        expected = ""
        self.assertEqual(actual, expected)

    def test_process_string(self):
        actual = process_string("test_resume.pdf")
        expected = "Successfully processed and uploaded resume into database!"
        self.assertEqual(actual, expected)

unittest.main(verbosity=2)