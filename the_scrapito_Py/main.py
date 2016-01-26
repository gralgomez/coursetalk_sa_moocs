import re
import csv
import requests as req
import urllib2
import datetime
from bs4 import BeautifulSoup as bsoup

 #--------------------------------
url = urllib2.urlopen('https://www.coursetalk.com/providers/coursera/courses/an-introduction-to-interactive-programming-in-python').read()
r = req.get(url)
soup = bsoup(r.content)

review_list = []
  #--------------------------------
  # TODO Resolving pagination
  # var new_url = '/providers/coursera/courses/an-introduction-to-interactive-programming-in-python' + page_string + sort_string + '#reviews';
  # page_string and page_sort are the kay variables

  #should have as output total number of pages i.e int
page_count_links = soup.find_all("a", href=re.compile('?page=.*'))
print(page_count_links)

try: # Make sure there are more than one page, otherwise, set to 1.
    num_pages = int(page_count_links[-1].get_text())   #should have as output 278

except IndexError:
    num_pages = 1

url_list = ["{}&pageNum={}".format(url, str(page)) for page in range(1, num_pages + 1)]
  #--------------------------------

  #   g_data refers to general data per page (course page)
g_data = soup.find_all("div", {"class": "review js-review"}) #"row" contains userinfo and review_body #works fine!

for item in g_data:

  #   1 datetime="X" is the one targeted!
  #     try:
  #         date = item.contents[1].find_all("time", {"class" : "review-body-info__pubdate"},recursive=True)[0].text
  #     except:
  #         pass
  #   2 username
    try:
        username = item.contents[1].find_all("p", {"class" : "userinfo__username"})[0].text
    except:
        pass
  #   3 rating
    try:
        rating = item.contents[1].find_all("span", {"class" : "sr-only"})[0].text
    except:
        pass
  #   4 status (ue re.compile for regeX)
    try:
        status = item.contents[1].find_all("span", {"class" : re.compile("^review-body-info__course-stage")})[0].text
    except:
        pass
  #   5 review_body
    try:
        review = item.contents[1].find_all("div", {"class" : "review-body__content"})[0].text
    except:
        pass
  #         # print item.contents[1].find_all("div", {"class" : ""}).text
    review_each = [username,status,rating,review]
    review_list.append(review_each)
  #  self.writer.writerow([unicode(s).encode("utf-8") for s in row])
  #  print review_list

with open ('reviews.csv','wb') as file:
     writer = csv.writer(file)
     for row in review_list:
         writer.writerow(row)
