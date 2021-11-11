from lxml import html
from typing import Dict

def get_page_object(html_str: str) -> Dict:
    '''Take an html string and return and object listing content with interesting properties'''
    doc = html.fromstring(html_str)

    return {
        'type': 'page',
        'dimensions': [doc.xpath('//page')[0].get('width'), doc.xpath('//page')[0].get('height')],
        'content': [{
            'type': 'block',
            'bounding_box': [bloc.get('xmin'), bloc.get('xmax'), bloc.get('ymin'), bloc.get('ymax')],
            'content': [
                {
                    'type': 'line',
                    'bounding_box': [line.get('xmin'), line.get('xmax'), line.get('ymin'), line.get('ymax')],
                    'line_content': ' '.join(word.text for word in line.getchildren()),
                    'content': [
                        {
                            'type': 'word',
                            'bounding_box': [word.get('xmin'), word.get('xmax'), word.get('ymin'), word.get('ymax')],
                            'content': word.text
                        } for word in line.getchildren()
                    ]
                } for line in bloc.getchildren()
                ]
            } for bloc in doc.xpath("//block")
        ]
    }