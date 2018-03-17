import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from random import randint


LINK = "https://www.coursera.org/sitemap~www~courses.xml"


def get_courses_list():
    response_xml_urls = requests.get(LINK).text
    parse_object = BeautifulSoup(response_xml_urls, "lxml")
    urls_list = [
        url_with_tag.get_text() for url_with_tag in parse_object.findAll("loc")
    ]
    return urls_list


def get_course_info(course_url):
    response = requests.get(course_url)
    response.encoding = "UTF-8"
    response = response.text
    parse_object = BeautifulSoup(response, "html.parser")

    course_name_tag = parse_object.findAll(
        "h2", {"class": "headline-4-text course-title"}
    )
    course_language_tag = parse_object.findAll(
        "div", {"class": "rc-Language"}
    )
    course_start_date_tag = parse_object.findAll(
        "div", {"class": "startdate rc-StartDateString caption-text"}
    )
    course_rating_tag = parse_object.findAll(
        "div", {"class": "ratings-text bt3-visible-xs"}
    )
    course_name = course_name_tag[0].get_text()
    course_language = course_language_tag[0].get_text()
    course_start_date = course_start_date_tag[0].get_text()
    if course_rating_tag:
        course_rating = course_rating_tag[0].get_text()
    else:
        course_rating = None
    return (
        course_name,
        course_language,
        course_start_date,
        course_rating,
        course_url
    )


def output_courses_info_to_xlsx(data):
    xlsx_book = Workbook()
    xlsx_book_filename = "coursera_courses_info.xlsx"
    xlsx_book_sheet = xlsx_book.active
    xlsx_book_sheet.append(["Name", "Language", "Start date","Rating", "URL"])
    for row in data:
        xlsx_book_sheet.append(row)
    xlsx_book.save(filename=xlsx_book_filename)


if __name__ == "__main__":
    count_courses_to_xlsx = 20
    course_url_list = get_courses_list()
    data_to_xlsx_export = []
    for i in range(count_courses_to_xlsx):
        random_number = randint(0, len(course_url_list))
        data_to_xlsx_export.append(
            get_course_info(course_url_list[random_number])
        )
    output_courses_info_to_xlsx(data_to_xlsx_export)

