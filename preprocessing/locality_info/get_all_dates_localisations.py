import datetime

from datefinder import find_dates


def get_all_dates_localisations(html_object: dict):
    """
    Parses textual data to find coordinates of dates
    """
    dates_localisations = {}

    content = html_object.get('content')
    size_content = len(content)

    for i_content in range(size_content):
        inner_content = content[i_content].get('content')
        size_inner_content = len(inner_content)

        for i_inner_content in range(size_inner_content):
            line_content = inner_content[i_inner_content].get('line_content')

            dates = find_dates(line_content)

            if dates:
                content_of_line_content = inner_content[i_inner_content].get('content')
                size_inner_content = len(content_of_line_content)

                # Coordinates
                for date in dates:
                    for i_line_content in range(size_inner_content):
                        word = content_of_line_content[i_line_content].get('content')

                        if date.strftime('%d/%m/%Y') in word or date.strftime('%m/%d/%Y') in word:
                            dates_localisations[date.strftime('%d/%m/%Y')] = content_of_line_content[i_line_content].get('bounding_box')

    return(dates_localisations)
