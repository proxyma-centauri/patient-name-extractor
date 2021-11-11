

def get_association_with_medical_title(person: str, closest_words: str):
    """
    Returns 0 if no medical title is detected in the neighbourhood and 1 if there is
    """
    medical_titles = ["Dr", "Dr.", "Pr.", 'Pr']

    association = 0

    if any(medical_title in person for medical_title in medical_titles):
        association = 1
    elif any(medical_title in closest_words for medical_title in medical_titles):
        association = 1
    elif any(medical_title in ''.join(closest_words) for medical_title in medical_titles):
        association = 1

    return association