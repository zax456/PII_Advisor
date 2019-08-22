import unittest


def convert_to_text(filepath):
    pass


def convert_to_text_dir(dir, directory = True):
    pass


def flagging(raw_text):
    return [""]


def parsing(raw_text, PIIs):
    return ""


def process_string(raw_text):
    PIIs = flagging(raw_text)
    parse_text = parsing(raw_text, PIIs)
    return 201

# Tests

class Test(unittest.TestCase):
    def convert_to_text(self):
        self.assertEqual(convert_to_text, "test")

    def convert_to_text_dir(self):
        self.assertEqual(convert_to_text_dir, "test")

    def flagging(self):
        self.assertEqual(flagging, "expected")
    
    def parsing(self):
        self.assertEqual(parsing, "expected")

    def process_string(self):
        self.assertEqual(process_string, "expected")

unittest.main(verbosity=2)