
def input_html_representation(file_name: str):
    """
    Loads the file for the given html file name, and transforms its content into a use-friendly object
    """
    with open(file_name, 'r') as f:   
        data = f.read()
        return(data)