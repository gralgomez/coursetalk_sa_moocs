import re
import csv
import requests as req
#import urllib2
#import datetime
from bs4 import BeautifulSoup as bsoup

url = 'https://www.coursetalk.com/providers/coursera/courses/an-introduction-to-interactive-programming-in-python'
r = req.get(url)
soup = bsoup(r.content)

reviews = open("/home/laurita/Documents/reviews.csv.txt", "w")
page_count_links = soup.find_all("a", href=re.compile(r".*page=.*"))

try: # Make sure there are more than one page, otherwise, set to 1.
    num_pages = int(page_count_links[3].get_text()) #[3] = 278 the max number
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

        for item in soup_new.find_all("div", {"class": "review js-review"}):
            try:
                username = item.contents[1].find_all("p", {"class" : "userinfo__username"})[0].text.encode('utf8')
            except:
                pass
  #   3 rating
            try:
                rating = item.contents[1].find_all("span", {"class" : "sr-only"})[0].text.encode('utf8')
            except:
                pass
  #   4 status (ue re.compile for regeX)
            try:
                status = item.contents[1].find_all("span", {"class" : re.compile("^review-body-info__course-stage")})[0].text.encode('utf8')
            except:
                pass
  #   5 review_body
            try:
                review = item.contents[1].find_all("div", {"class" : "review-body__content"})[0].text.encode('utf8')
            except:
                pass

            review_each = [username,status,rating,review]
            review_list.append(review_each)
            #print(review_list)
            # reviews.write(", ".join(review_list) + '\n')

    with open ('reviews2.csv','wb') as file:
        writer = csv.writer(file)
        for row in review_list:
            writer.writerow(row)
