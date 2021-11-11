

def get_entity_locality_info(person: str, html_object: dict, closest_threshold: int= 2):
    """"""
    coords = []
    closest_words = []

    content = html_object.get('content')
    size_content = len(content)

    # Find coordinates for the two elements of the name
    for i_content in range(size_content):
        inner_content = content[i_content].get('content')
        size_inner_content = len(inner_content)

        for i_inner_content in range(size_inner_content):

            # We use sets to see if name + first names are in this line
            line_content = inner_content[i_inner_content].get('line_content')

            person_components = set(person.split(' '))
            p_c_l = len(person_components)
            line_components = set(line_content.split())

            intersection = person_components.intersection(line_components)
            intersection_len = len(intersection)

            condition = (person in line_content.replace(',', '')) or (p_c_l >= 2 and intersection_len >= 2) or (p_c_l == 1 and intersection_len == 1)

            if condition:
                content_of_line_content = inner_content[i_inner_content].get('content')
                size_inner_content = len(content_of_line_content)

                # Coordinates
                for i_line_content in range(size_inner_content):
                    word = content_of_line_content[i_line_content].get('content')

                    if word in person:
                        coords.append(content_of_line_content[i_line_content].get('bounding_box'))

                # Closest words
                try:
                    [before, after] = line_content.split(person)
                    after = after.split(' ')
                    before = before.split(' ')

                    if len(before) >= closest_threshold:
                        closest_words += before[-closest_threshold:-1]
                    else:
                        closest_words += before
                    if len(after) >= closest_threshold:
                        closest_words += after[:closest_threshold]
                    else:
                        closest_words += after

                # Fallback case is to add the whole line to closest_words
                except ValueError:
                    closest_words += line_content



    # Merge the coordinates
    try:
        final_coordinates = coords[0]
    # TODO: have a better fallback
    except IndexError:
        final_coordinates = [0, html_object.get("dimensions")[0], 0, html_object.get("dimensions")[0]]

    if len(coords) > 1:
        for coord in coords[1:]:
            final_coordinates = [min(coord[0], final_coordinates[0]), 
                                max(coord[1], final_coordinates[1]), 
                                min(coord[2], final_coordinates[2]), 
                                max(coord[3], final_coordinates[3])]
    return(final_coordinates, closest_words)

