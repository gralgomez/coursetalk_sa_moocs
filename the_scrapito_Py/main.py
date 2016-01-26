import re
import csv
import requests as req
import urllib2
import datetime
from bs4 import BeautifulSoup as bsoup

 #--------------------------------
url = 'https://www.coursetalk.com/providers/coursera/courses/an-introduction-to-interactive-programming-in-python'
r = req.get(url)
soup = bsoup(r.content)

review_list = []
  #--------------------------------
  # TODO Resolving pagination ---> Solved!
  # https://www.coursetalk.com/providers/coursera/courses/an-introduction-to-interactive-programming-in-python?page=276
  # var new_url = '/providers/coursera/courses/an-introduction-to-interactive-programming-in-python' + page_string + sort_string + '#reviews';

  #should have as output total number of pages i.e int
page_count_links = soup.find_all("a", href=re.compile(r".*page=.*"))
try: # Make sure there are more than one page, otherwise, set to 1.
    num_pages = int(page_count_links[1].get_text()) #[3] = 278 the max number
except IndexError:
    num_pages = 1

# Add 1 because Python range.
url_list = ["{}?page={}#reviews".format(url, str(page)) for page in range(1, num_pages + 1)]

with open("results.txt","wb") as acct:
    for url_ in url_list:
        print "Processing {}...".format(url_)
        r_new = req.get(url_)
        soup_new = bsoup(r_new.text)
        for tr in soup_new.find_all('tr', align='center'):
            stack = []
            for td in tr.findAll('td'):
                stack.append(td.text.replace('\n', '').replace('\t', '').strip())
            acct.write(", ".join(stack) + '\n')
  #--------------------------------

  #   g_data refers to general data per page (course page)
g_data = soup.find_all("div", {"class": "review js-review"})

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
