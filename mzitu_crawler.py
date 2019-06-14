import requests
from bs4 import BeautifulSoup
from time import sleep
import os
import random
from fake_useragent import UserAgent

IMAGE_PATH = os.getcwd() + '/images/'


def header(fake_ua, referer):
    '''
    Using the fake_useragent to randomly choose your useragent to avoid the anti-spider tech.
    You should always update the referer, even when you are doing test.
    '''
    headers = {
        'User-Agent': fake_ua,
        'Referer': '{}'.format(referer),
    }
    return headers


def request_page(pageNum, fake_ua, referer):
    '''
    Get the certain page information
    '''
    baseUrl = 'https://www.mzitu.com/page/{}/'.format(pageNum)

    r = requests.get(baseUrl, headers=header(fake_ua, referer))
    print(r)  # check the response
    return r


def extract_links(response_info):
    '''
    Extract the all the links from one certain page.
    '''
    soup = BeautifulSoup(response_info.text, features='html.parser')
    preview_link_list = soup.find(id='pins').find_all(
        'a', target='_blank')[1::2]
    link_list = [preview_link['href'] for preview_link in preview_link_list]
    return link_list


def random_sleep_time():
    '''
    random generate the time of sleeping when doing the scraping work
    '''
    possibility_like = random.random()
    if possibility_like < 0.2:
        sleep_time = random.randint(10, 20)
    else:
        sleep_time = random.randint(1, 10)
    return sleep_time


def get_images(blog_url, referer):
    # ---- Every time when choosing girl, randomly choose one useragent ----
    fake_ua = UserAgent()
    user_agent = fake_ua.random

    blog_first_r = requests.get(
        (blog_url), headers=header(user_agent, referer))
    print(blog_first_r)
    soup = BeautifulSoup(blog_first_r.text, features="html.parser")

    # ---- get the number of images ----
    pic_num = soup.find('div', class_='pagenavi').find_all('a')[4].get_text()
    title = soup.find("h2", class_='main-title').get_text()
    print("{}:{}".format(title, pic_num))

    # ---- make the dir ----
    # make the directory and store the images
    dir_name = "【{}P】{}".format(pic_num, title)
    pic_path = IMAGE_PATH + str(dir_name)
    if os.path.exists(pic_path):
        print('directory exist!')
    else:
        os.mkdir(pic_path)
    os.chdir(pic_path)  # access the dir and download images
    print('downloading' + dir_name + '...')

    # ---- downloading the images ----
    # download the first image
    image_referer = blog_url
    pic_src = soup.find('div', 'main-image').find('img')['src']
    pic_name = pic_src.split('/')[-1]

    sleep(random_sleep_time())
    f = open(pic_name, 'wb')
    print("accessing {}".format(pic_src))
    f.write(requests.get(pic_src, headers=header(
        user_agent, image_referer)).content)
    f.close()
    print("finish the first image : {}".format(pic_name))

    for pic_index in range(2, int(pic_num) + 1):
        # setting the time gap is important, or it will meet the Max retries exceeded with url error
        sleep(random_sleep_time())
        pic_link = blog_url + '/' + str(pic_index)
        pic_cur_page = requests.get(
            pic_link, headers=header(user_agent, image_referer))
        soup = BeautifulSoup(pic_cur_page.text, features="html.parser")
        pic_src = soup.find('div', 'main-image').find('img')['src']
        pic_name = pic_src.split('/')[-1]

        f = open(pic_name, 'wb')
        print("accessing {}".format(pic_src))
        f.write(requests.get(pic_src, headers=header(
            user_agent, image_referer)).content)
        f.close()
        image_referer = pic_link  # update the referer
        print("finish {} image : {}".format(pic_index, pic_name))

    os.chdir(IMAGE_PATH)  # finish downloading, and get back the dir


if __name__ == "__main__":
    '''
    remember to update the referer when you change the page number.
    '''
    header_referer = "https://www.mzitu.com/"

    # by setting the range, can scrape the images in the first n pages.
    for i in range(3, 4):
        print("accessing the {} page...".format(i))
        fake_ua = UserAgent()
        user_agent = fake_ua.random

        r = request_page(i, user_agent, header_referer)
        current_page = 'https://www.mzitu.com/page/{}/'.format(i)
        header_referer = current_page
        # ---- extract all the links from one page----
        link_list = extract_links(r)
        print(
            "extracted all the links in page {}.".format(i))
        for link in link_list:
            # print(link)
            # ---- get all the images and store ----
            get_images(link, current_page)
