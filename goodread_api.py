import os, sys
import requests
import xml.etree.ElementTree as ET
import json

"""
export KEY="opHVu3oUSvCR9lympPZ5Bw"
xml docs ---> 'https://docs.python.org/3/library/xml.etree.elementtree.html'
requests docs ---> http://docs.python-requests.org/en/master/
"""

def send_req(query):
    try:
        r = requests.get('https://www.goodreads.com/search.xml', params={'key' : os.getenv('KEY'), 'q' : query})
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit(1)
    else:
        return r

def get_cover_image(query='0553803700'):
    root = ET.fromstring(send_req(query).content)
    try:
        image_tag = root.find('search').find('results').find('work').find('best_book').find('image_url')
    except AttributeError as err:
        return 'None image'
    else:
        return image_tag.text

def get_avg_rate(query='1416949658'):
    root = ET.fromstring(send_req(query).content)
    try:
        rate_tag = root.find('search').find('results').find('work').find('average_rating')
    except AttributeError as err:
        return 'None rate'
    else:
        return rate_tag.text

def get_total_rated(query='0553803700'):
    root = ET.fromstring(send_req(query).content)
    try:
        ratings_count = root.find('search').find('results').find('work').find('ratings_count')
    except AttributeError as err:
        return 'None rated total'
    else:
        return ratings_count.text

def get_reviews_count_on_goodread(query='0553803700'):
    root = ET.fromstring(send_req(query).content)
    try:
        reviews_count = root.find('search').find('results').find('work').find('text_reviews_count')
    except AttributeError as err:
        return 'None reviews_count'
    else:
        return reviews_count.text

def get_pub_date(query='0553803700'):
    root = ET.fromstring(send_req(query).content)
    try:
        year = root.find('search').find('results').find('work').find('original_publication_year')
    except AttributeError as err:
        year_replace = 'None'
    else:
        year_replace = year.text
    try:
        month = root.find('search').find('results').find('work').find('original_publication_month')
    except AttributeError as err:
        month_replace = 'None'
    else:
        month_replace = month.text
    try:
        day = root.find('search').find('results').find('work').find('original_publication_day')
    except AttributeError as err:
        day_replace = 'None'
    else:
        day_replace = day.text
    return '{d}-{m}-{y}'.format(d = day_replace, m = month_replace, y = year_replace)

def search_book(query='rowling'):
    '''search for books with query'''
    json_template = {
        'books' : []
    }

    element = {
                'title' : None,
                'rate' : {
                    'ratings_count' : None,
                    'average_rating' : None
                },
                'author' : {
                    'name' : None
                },
                'image' : {
                    'image_url' : None
                }
            }

    root = ET.fromstring(send_req(query).content)
    list_books = root.find('search').find('results')
    for book in list_books:
        element['title'] = book.find('best_book').find('title').text
        element['rate']['ratings_count'] = book.find('ratings_count').text
        element['rate']['average_rating'] = book.find('average_rating').text
        element['author']['name'] = book.find('best_book').find('author').find('name').text
        element['image']['image_url'] = book.find('best_book').find('image_url').text
        json_template['books'].append(element)
    return json.dumps(json_template, indent=2)

if __name__ == "__main__":
    print('image url : {}'.format(get_cover_image()))
    print('average rate : {}'.format(get_avg_rate()))
    print('total rates : {}'.format(get_total_rated()))
    print('total reviews : {}'.format(get_reviews_count_on_goodread()))
    print('date pb : {}'.format(get_pub_date()))
    print('search : {}'.format(search_book()))
