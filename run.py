import os
import logging
import configparser
import pytesseract
from PIL import Image

# Logging and config init
logging.basicConfig(level=logging.INFO)
config = configparser.ConfigParser()
config.read('config.ini')

# Paths
raw_corpus_path = config['DEFAULT']['RawPath']
training_corpus_path = config['DEFAULT']['TrainingPath']

# Input image file list
raw_corpus_file_list = os.listdir(raw_corpus_path)


def ocr_core(filename):
    """
    Tesseract bind
    :param filename: image file path + name
    :return: extracted text from image file
    """
    text = pytesseract.image_to_string(Image.open(filename))
    return text


def save_text_file(content, new_file_path):
    """
    Saves text to .txt file
    :param content: text to be added to the .txt file
    :param new_file_path: .txt file path + name
    :return:
    """
    logging.info(" Now saving {}".format(new_file_path))

    try:
        with open(new_file_path, "w") as text_file:
            text_file.write("%s" % content)
    except Exception as ex_io:
        logging.error(" Error {}".format(str(ex_io)))


# Run
for raw_file in raw_corpus_file_list:

    logging.info(" Now processing {}".format(os.path.join(raw_corpus_path, raw_file)))
    training_file_path = os.path.splitext(os.path.join(training_corpus_path, raw_file))[0] + '.txt'

    try:
        text = ocr_core(os.path.join(raw_corpus_path, raw_file))
        save_text_file(text, training_file_path)
    except Exception as ex:
        logging.error(" Error {}".format(str(ex)))
