import requests
from bs4 import BeautifulSoup

link = "https://www.coursera.org/sitemap~www~courses.xml"

def get_courses_list():

    response_xml_urls = requests.get(link).text
    parse_object = BeautifulSoup(response_xml_urls, "lxml")
    urls_list = [
        url_with_tag.get_text() for url_with_tag in parse_object.findAll("loc")
    ]
    return urls_list


def get_course_info(link = "https://www.coursera.org/learn/programming-in-python"):
    response = requests.get(link).text
    parse_object = BeautifulSoup(response, 'html.parser')
    x = parse_object.findAll("div", {"class": "rc-Language"})

    print(x)
    print(x[0].get_text())

    

def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    x = get_courses_list()
    #print(requests.get(x[0]).headers)

    headers = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'youremail@domain.com'
    }
    #print(x[0])
    #response = requests.get(x[0], headers=headers)
    #print(response.content)

    #for i in x:
    #   print(i)
    get_course_info()