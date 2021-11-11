

def get_association_with_indicators(closest_words: str):
    """
    Returns 0 if no indicators are detected in the neighbourhood and 1 if there is
    """
    medical_titles = ["Concerne", "concerne", "Patient", 'patient']

    association = 0

    if any(medical_title in closest_words for medical_title in medical_titles):
        association = 1
    elif any(medical_title in ''.join(closest_words) for medical_title in medical_titles):
        association = 1

    return association