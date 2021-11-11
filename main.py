from os import listdir
from os.path import isfile, join

from decouple import config

from preprocessing.io.input_html_representation import input_html_representation
from preprocessing.html_to_object.html_to_object import get_page_object
from preprocessing.object_to_text.html_object_to_text_representation import html_object_to_text_representation

from ner.find_entities import find_person_entities

def main(args):
    """"""
    # Get files list
    files = [f for f in listdir(args.get("MEDICAL_DATA_FOLDER")) if isfile(join(args.get("MEDICAL_DATA_FOLDER"), f))]

    # First preprocessing and NER for each document
    for file_name in files:
        html_representation = input_html_representation(file_name)
        html_object = get_page_object(html_representation)
        
        text_representations = html_object_to_text_representation(html_object, return_dict=True)

        # NER on by-line representation
        person_entities = find_person_entities(text_representations.get("by_line"))

        # Feature engineering

if __name__ == "__main__":


    args = {}

    args["MEDICAL_DATA_FOLDER"] = config("MEDICAL_DATA_FOLDER",
                                    default="./data/medical_reports",
                                    cast=str)

    args["FEATURES_DATA_FOLDER"] = config("FEATURES_DATA_FOLDER",
                                    default="./data/features",
                                    cast=str)                               
