import requests
import random
import sys
from bs4 import BeautifulSoup
from openpyxl import Workbook


def get_urls_course_list(text):
    xml_4parse = BeautifulSoup(text, "lxml")
    urls_list = [
        url_with_tag.get_text() for url_with_tag in xml_4parse.find_all("loc")
    ]
    return urls_list


def get_course_info(html_page_text, course_url):
    html_page_4parse = BeautifulSoup(html_page_text, "html.parser")
    course_name = html_page_4parse.find(
        "h2", {"class": "headline-4-text course-title"}
    ).get_text()
    course_language = html_page_4parse.find(
        "div", {"class": "rc-Language"}
    ).get_text()
    course_start_date = html_page_4parse.find(
        "div", {"class": "startdate rc-StartDateString caption-text"}
    ).get_text()
    course_rating = html_page_4parse.find(
        "div", {"class": "ratings-text bt3-visible-xs"}
    )
    course_duration = len(
        html_page_4parse.findAll("div", {"class": "week"})
    )
    if course_rating:
        course_rating = course_rating.get_text()
    else:
        course_rating = None
    return {
        "course_url": course_url,
        "course_name": course_name,
        "course_language": course_language,
        "course_start_date": course_start_date,
        "course_rating": course_rating,
        "course_duration": course_duration
    }


def output_courses_info_to_xlsx(courses_info_list):
    xlsx_book = Workbook()
    xlsx_book_sheet = xlsx_book.active
    xlsx_book_sheet.append(
        ["Name", "Language", "Start date", "Rating", "Course duration", "URL"]
    )
    for course_info in courses_info_list:
        xlsx_book_sheet.append(
            (
                course_info["course_name"],
                course_info["course_language"],
                course_info["course_start_date"],
                course_info["course_rating"],
                course_info["course_duration"],
                course_info["course_url"]
            )
        )
    return xlsx_book


if __name__ == "__main__":
    count_courses_to_xlsx = 20
    url = "https://www.coursera.org/sitemap~www~courses.xml"
    try:
        output_file_name = sys.argv[1]
    except IndexError:
        exit("The file name is not specified")
    coursera_feed = requests.get(url).text
    course_urls_list = get_urls_course_list(coursera_feed)
    data_to_xlsx_export = []
    random_courses_list = random.sample(course_urls_list, count_courses_to_xlsx)
    for course_url in random_courses_list:
        html_page = requests.get(course_url)
        html_page.encoding = "UTF-8"
        course_info = get_course_info(html_page.text, course_url)
        data_to_xlsx_export.append(course_info)
    xslx_courses_book = output_courses_info_to_xlsx(data_to_xlsx_export)
    xslx_courses_book.save(filename=output_file_name)
