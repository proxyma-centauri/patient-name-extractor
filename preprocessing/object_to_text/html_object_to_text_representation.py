

def html_object_to_text_representation(html_object: dict, return_dict: bool = False):
    """
    Returns two representation of the text contained in the given html_object, as well
    as optionaly the dictionary used to build the line based representation.
    """
    all_text_representation = []
    line_text_representation_dict = {}

    content = html_object.get('content')
    size_content = len(content)

    for i_content in range(size_content):
        inner_content = content[i_content].get('content')
        size_inner_content = len(inner_content)

        for i_inner_content in range(size_inner_content):
            line_content = inner_content[i_inner_content].get('line_content')
            all_text_representation.append(line_content)

            if line_text_representation_dict.get(i_content):
                line_text_representation_dict[i_content].append(line_content)
            else:
                line_text_representation_dict[i_content] = [line_content]

    
    line_text_representation = [' '.join(text_line) for _, text_line in line_text_representation_dict.items()]

    representations = {"all": all_text_representation, 
                        "by_line": line_text_representation
                    }
    if return_dict:
        representations["dict"] = line_text_representation_dict

    return representations