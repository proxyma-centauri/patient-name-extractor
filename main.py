from os import listdir
from os.path import isfile, join

from decouple import config
from collections import Counter

import pandas as pd

from preprocessing.io.input_html_representation import input_html_representation
from preprocessing.html_to_object.html_to_object import get_page_object
from preprocessing.object_to_text.html_object_to_text_representation import html_object_to_text_representation
from preprocessing.locality_info.get_entity_locality_info import get_entity_locality_info
from preprocessing.locality_info.get_all_dates_localisations import get_all_dates_localisations

from ner.find_entities import find_person_entities

from feature_engineering.distances.distance_to_closest_date import get_distance_to_closest_date
from feature_engineering.associations.association_with_medical_title import get_association_with_medical_title
from feature_engineering.associations.association_with_indicators import get_association_with_indicators


def main(args):
    """"""
    # Get files list
    files = [join(args.get("MEDICAL_DATA_FOLDER"), f) for f in listdir(args.get("MEDICAL_DATA_FOLDER")) if isfile(join(args.get("MEDICAL_DATA_FOLDER"), f))]

    data = pd.DataFrame()

    # First preprocessing and NER for each document
    for file_name in files:
        html_representation = input_html_representation(file_name)
        html_object = get_page_object(html_representation)
        
        text_representations = html_object_to_text_representation(html_object, return_dict=True)

        # NER on by-line representation
        # TODO: add text preprocessing(removing phone, emails) 
        person_entities = find_person_entities(text_representations.get("by_line"))

        # Get count of occurences of each entity
        # TODO: extend to take into account variants
        entities_count = Counter(person_entities)

        # Get all dates localisation
        dates_locs = get_all_dates_localisations(html_object)

        # Feature engineering for each person entity
        for person_entity in person_entities:
            person = person_entity.text

            # Get entity HTML coords localisation and closest words
            entity_loc, closest_words = get_entity_locality_info(person, html_object)
            
            # Birth date intuition → Measure distance from closest date 
            distance_to_closest_date = get_distance_to_closest_date(entity_loc, dates_locs)
            
            # “Not a doctor” → Non-association with medical titles (Dr, Pr, etc), either distance or categorical from threshold
            association_to_medical_title = get_association_with_medical_title(person, closest_words)

            # “Patient-ness” indicators → Association with keywords
            # TODO: extend to coordinate closeness
            association_to_indicators = get_association_with_indicators(closest_words)

            # Nb of occurrences
            nb_occurences = entities_count.get(person_entity)

            # Appending to dataframe (document_path is for data keeping purposes, not a feature)
            new_row = {
                "xmin": entity_loc[0],
                "xmax": entity_loc[1],
                "ymin": entity_loc[2],
                "ymax": entity_loc[3],
                "distance_closest_date": distance_to_closest_date,
                "association_to_medical_title": association_to_medical_title,
                "association_to_indicators": association_to_indicators,
                "nb_occurences": nb_occurences,
                "document_path": file_name
            }
            data = data.append(new_row, ignore_index=True)

    data.to_csv(args["FEATURES_DATA_FOLDER"] + 'features.csv')

    # After this point, only the architceture headlines are mentionned as TODO comments

    # TODO : preprocessing on extracted features
    #   - standardisation
    #   - encoding categorical data
    #   - depending on traning mode, load the corresponding objects or fit them

    # TODO : depending on args["TRAINING"], train the model(s) or not
    #   - if there is training:
    #       - build target vector: from (document, patient name) association, 
    #           build corresponding (engineered features, is a patient) matching for each row of the dataframes
    #       - train/val/ test split, taking into account class imbalance
    #       - training
    #       - make predictions per Person entity
    #       - aggregate in Patient Name predictions, and document-wise ranking
    #       - compute metrics (F1, rank-based)
    #       - save the model's weights
    #   - if there is no training:
    #       - load model(s)
    #       - make predictions per Person entity
    #       - aggregate in Patient Name predictions, and document-wise ranking


if __name__ == "__main__":


    args = {}

    args["MEDICAL_DATA_FOLDER"] = config("MEDICAL_DATA_FOLDER",
                                    default="./data/medical_reports",
                                    cast=str)

    args["FEATURES_DATA_FOLDER"] = config("FEATURES_DATA_FOLDER",
                                    default="./data/features",
                                    cast=str) 

    args["TRAINING"] = config("TRAINING",
                                    default=True,
                                    cast=bool) 

    main(args)                              
