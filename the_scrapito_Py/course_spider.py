import scrapy
from scrapy.http import Request
import urlparse
import re
from CourseTalk.items import CoursetalkItem

class CoursetalkSpider(scrapy.Spider):
    name = 'coursetalk'
    allowed_domains = ['coursetalk.com']
    start_urls = ['https://www.coursetalk.com/search']

    def parse(self, response):
        for course in response.xpath('//a[@class=\'link-unstyled js-course-search-result\']'):
            print 'processing'
            course_url = ''.join(course.xpath('./@href').extract()).strip()
            if course_url:
                course_url = urlparse.urljoin(response.url, course_url)
            meta = {'course_url': course_url}
            yield scrapy.Request(
                course_url,
                callback=self.parse_coursecontent,
                dont_filter=True,
                meta=meta)
        # turn page:
        next_page = ''.join(response.xpath('//div[@class=\'js-course-pagination\']//li/a[@aria-label=\'Next\']//@href').extract()).strip()
        next_page_num = response.xpath('//div[@class=\'js-course-pagination\']//li/a[@aria-label=\'Next\']//@data-page-number').extract()
        page_limit = response.xpath('//div[@class=\'js-course-pagination\']//li//a/@data-page-number').extract()[-2]
        if next_page_num <= page_limit:
            next_page = urlparse.urljoin(response.url, next_page)
            yield scrapy.Request(
                next_page,
                callback=self.parse,
                dont_filter=True,
            )
        else:
            pass
    def parse_coursecontent(self, response):
        course_url = response.meta['course_url']
        course_name = ''.join(response.xpath('//h1[@class=\'course-header__name__title\']//text()').extract()).strip()
        course_price = ''.join(response.xpath('//div[@class=\'course-enrollment-details__detail--narrow course-enrollment-details__detail--cost\']//text()').extract()).strip()
        course_desc = ''.join(response.xpath('//div[@class=\'course-info__academic__item--extra-whitespace\']//text()').extract()).strip()
        course_university = ''.join(response.xpath('//i[@class=\'course-info__academic__school-icon\']/../text()').extract()).strip()
        course_instructor = ''.join(response.xpath('//i[@class=\'course-info__academic__instuctor-icon\']/../text()').extract()).strip()
        course_provider = ''.join(response.xpath('//div[@class=\'course-enrollment-details course-enrollment-details--dashed\']/div[@itemprop=\'seller\']//a/img/@alt').extract()).strip()
        course_review_num = ''.join(response.xpath('//div[@itemprop=\'aggregateRating\']/div[@class=\'course-rating__count\']/span[@class=\'course-additional-info__reviews-count\']//text()').extract()).strip()
        course_rating = ''.join(response.xpath('//div[@itemprop=\'aggregateRating\']/div[@class=\'course-rating__stars\']//meta[@itemprop=\'ratingValue\']/@content').extract()).strip()
        item = CoursetalkItem()

        item['course_url'] = course_url
        item['course_name'] = course_name
        item['course_price'] = course_price
        item['course_desc'] = course_desc
        item['course_university'] = course_university
        item['course_instructor'] = course_instructor
        item['course_provider'] = course_provider
        item['course_review_num'] = course_review_num
        item['course_rating'] = course_rating
        yield item

# scrapy crawl coursetalk -o data.csv -t csv
# url_data.csv is the file to be processed next

import pandas as pd
import numpy as np
import requests as req
import csv
from bs4 import BeautifulSoup as bsoup

class ReviewSpider:
    courses_df = pd.read_csv('/home/laurita/PycharmProjects/CourseTalk/clean_data.csv', header=True, names=['course_instructor','course_name','course_rating','course_university','course_review_num','course_desc','course_url','course_provider', 'course_price'])
    reviewed_courses_df = courses_df[courses_df.course_review_num != '0 reviews']
    next(reviewed_courses_df)
    for line in reviewed_courses_df:
        r = req.get(line)
        soup = bsoup(r.content)

        reviews = open('/home/laurita/Documents/reviews.csv.txt', 'w')
        page_count_links = soup.find_all('a', href=re.compile(r'.*page=.*'))

# Multipages

            try: # Make sure there are more than one page, otherwise, set to 1.
                num_pages = int(page_count_links[2].get_text()) #[3] = 278 the max number, 2 for 30
            except IndexError:
                num_pages = 1

            url_list = ['{}?page={}#reviews'.format(reviewed_url, str(page)) for page in range(1, num_pages + 1)]

            with open('results.txt','wb') as reviews:
                review_list = []
                for url_ in url_list:
                    print 'Processing {}...'.format(url_)
                    r_new = req.get(url_)
                    soup_new = bsoup(r_new.text)

                    for item in soup_new.head:
                        course_title = soup_new.head.title.text.encode('utf8')
                        course_title = course_title.replace(' - online course reviews and ratings | CourseTalk','')
                        course_provider_lookup = re.search('by.*', course_title)

                        if course_provider_lookup:
                            course_provider = course_provider_lookup.group().encode('utf8')
                            course_provider = course_provider.replace('by','')

                        course_title = re.sub('by.*','',course_title)

                        for item in soup_new.body:
                            course_fee = soup_new.find_all('div', {'class' : 'course-enrollment-details__detail--narrow course-enrollment-details__detail--cost'})[0].text.encode('utf8')
                            course_instructor = soup_new.find_all('div', {'class' : 'course-info__academic__item'})[0].text.encode('utf8')
                            course_instructor = course_instructor.replace('\n\nInstructors:\xc2\xa0\n                            ','')
                            course_stage = soup_new.find_all('span', {'class' : re.compile('^review-body-info__course-stage')})[0].text.encode('utf8')
                            course_school = soup_new.find_all('div', {'class' : 'course-info__academic__item'})[1].text.encode('utf8')
                            course_school = course_school.replace('\n\nSchool:\xc2\xa0\n','')
                            course_description = soup.find_all('div', {'class' : 'course-info__academic__item--extra-whitespace'})[0].text.encode('utf8')

                    for item in soup_new.find_all('div', {'class': 'review js-review'}):
                    #TODO:in same tg extract the review id
                        try:
                            username = item.contents[1].find_all('p', {'class' : 'userinfo__username'})[0].text.encode('utf8')
                            #TODO: Convert date into numerical
                            date = item.contents[1].find_all('time', {'class' : 'review-body-info__pubdate'})[0].text.encode('utf8')
                            rating = item.contents[1].find_all('span', {'class' : 'sr-only'})[0].text.encode('utf8')
                            status = item.contents[1].find_all('span', {'class' : re.compile('^review-body-info__course-stage')})[0].text.encode('utf8')
                            review = item.contents[1].find_all('div', {'class' : 'review-body__content'})[0].text.encode('utf8')
                            reviews_count = item.contents[1].find_all('li', {'class' : 'userinfo-activities__item--reviews-count'})[0].text.encode('utf8')
                            completed_count = item.contents[1].find_all('li', {'class' : 'userinfo-activities__item--courses-complited'})[0].text.encode('utf8')
                        except:
                            pass

                    review_each = [course_provider, course_title, course_instructor, course_stage, course_school, course_description, date, username,status,rating,reviews_count,completed_count,review]
                    review_list.append(review_each)
                        #print(review_list)
                        # reviews.write(', '.join(review_list) + '\n')

            with open ('reviews4.csv','wb') as file:
                writer = csv.writer(file)
                for row in review_list:
                    writer.writerow(row)
