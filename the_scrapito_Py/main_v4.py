import re
import csv
import requests as req
#import urllib2
#import datetime
from bs4 import BeautifulSoup as bsoup

#TODO: https://www.coursetalk.com/providers/.*/courses/.*?page=6#reviews
#TODO: For each Course node, extract the information - also multi pages

url = 'https://www.coursetalk.com/providers/coursera/courses/an-introduction-to-interactive-programming-in-python'
r = req.get(url)
soup = bsoup(r.content)

reviews = open("/home/laurita/Documents/reviews.csv.txt", "w")
page_count_links = soup.find_all("a", href=re.compile(r".*page=.*"))

try: # Make sure there are more than one page, otherwise, set to 1.
    num_pages = int(page_count_links[2].get_text()) #[3] = 278 the max number, 2 for 30
except IndexError:
    num_pages = 1

# Add 1 because Python range.
url_list = ["{}?page={}#reviews".format(url, str(page)) for page in range(1, num_pages + 1)]

with open("results2.txt","wb") as reviews:
    review_list = []
    for url_ in url_list: #url_ last url of the list
        print "Processing {}...".format(url_)
        r_new = req.get(url_)
        soup_new = bsoup(r_new.text)

        for item in soup_new.head:
            course_title = soup_new.head.title.text.encode('utf8')
            course_title = course_title.replace(' - online course reviews and ratings | CourseTalk','')
            course_provider_lookup = re.search('by.*', course_title)
            if course_provider_lookup:
                course_provider = course_provider_lookup.group().encode('utf8')
                course_provider = course_provider.replace('by','')
            course_title = re.sub('by .*','',course_title)

        for item in soup_new.body:
            # TODO test = soup.findChildren("a")[16]
            course_fee = soup_new.find_all("div", {"class" : "course-enrollment-details__detail--narrow course-enrollment-details__detail--cost"})[0].text.encode('utf8')
            course_instructor = soup_new.find_all("div", {"class" : "course-info__academic__item"})[0].text.encode('utf8')
            course_instructor = course_instructor.replace('\n\nInstructors:\xc2\xa0\n                            ','')
            course_stage = soup_new.find_all("span", {"class" : re.compile("^review-body-info__course-stage")})[0].text.encode('utf8')
            course_school = soup_new.find_all("div", {"class" : "course-info__academic__item"})[1].text.encode('utf8')
            course_school = course_school.replace('\n\nSchool:\xc2\xa0\n                                ','')

            # TODO course_content =
            course_description = soup.find_all("div", {"class" : "course-info__academic__item--extra-whitespace"})[0].text.encode('utf8')
            # TODO course_provider =


        for item in soup_new.find_all("div", {"class": "review js-review"}):
        #TODO:in same tg extract the review id
            try:
                username = item.contents[1].find_all("p", {"class" : "userinfo__username"})[0].text.encode('utf8')
                #TODO: Convert date into numerical
                date = item.contents[1].find_all("time", {"class" : "review-body-info__pubdate"})[0].text.encode('utf8')
                rating = item.contents[1].find_all("span", {"class" : "sr-only"})[0].text.encode('utf8')
                status = item.contents[1].find_all("span", {"class" : re.compile("^review-body-info__course-stage")})[0].text.encode('utf8')
                review = item.contents[1].find_all("div", {"class" : "review-body__content"})[0].text.encode('utf8')
                reviews_count = item.contents[1].find_all("li", {"class" : "userinfo-activities__item--reviews-count"})[0].text.encode('utf8')
                completed_count = item.contents[1].find_all("li", {"class" : "userinfo-activities__item--courses-complited"})[0].text.encode('utf8')
            except:
                pass

            review_each = [course_provider, course_title, course_instructor, course_stage, course_school, course_description, date, username,status,rating,reviews_count,completed_count,review]
            review_list.append(review_each)
            #print(review_list)
            # reviews.write(", ".join(review_list) + '\n')

    with open ('reviews4.csv','wb') as file:
        writer = csv.writer(file)
        for row in review_list:
            writer.writerow(row)
