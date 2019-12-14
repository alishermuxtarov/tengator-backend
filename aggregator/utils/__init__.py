from hashlib import md5
from textract import process


def get_text_from_file(filename):
    try:
        return process(filename).decode('utf-8')
    except:
        return ''


def md5_text(text):
    return md5(text.encode('utf-8')).hexdigest()
