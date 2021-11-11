from typing import List
import spacy


def find_entities(text: List[str], language_model: str="fr_core_news_md"):
    """
    Returns all identifies entities of the input text, for the given language model
    """
    nlp = spacy.load(language_model)

    # Minimal preprocessing
    ner_results = [nlp(str(x).replace(',', '')) for x in text]

    return [entity for ner_result in ner_results for entity in ner_result.ents ]


def find_person_entities(text: List[str], language_model: str="fr_core_news_md"):
    """
    Returns only PER entities
    """
    entities = find_entities(text, language_model=language_model)

    return [entity for entity in entities if entity.label_ == "PER"]