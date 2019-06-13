import requests
from bs4 import BeautifulSoup
from time import sleep
import os

IMAGE_PATH = os.getcwd() + '/images/'


def header(referer):
    '''
    You should always update the referer, even when you are doing test
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36',
        'Referer': '{}'.format(referer),
    }
    return headers


def request_page(pageNum, referer):
    '''
    Get the certain page information
    '''
    baseUrl = 'https://www.mzitu.com/page/{}/'.format(pageNum)

    r = requests.get(baseUrl, headers=header(referer))
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


def get_images(blog_url, referer):
    print(requests.get((blog_url), headers=header(referer)))
    soup = BeautifulSoup(requests.get(
        blog_url, headers=header(referer)).text, features="html.parser")

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
    image_referer = referer
    for pic_index in range(1, int(pic_num) + 1):
        # setting the time gap is important, or it will meet the Max retries exceeded with url error
        sleep(1)
        pic_link = blog_url + '/' + str(pic_index)
        pic_cur_page = requests.get(pic_link, headers=header(image_referer))
        soup = BeautifulSoup(pic_cur_page.text, features="html.parser")
        pic_src = soup.find('div', 'main-image').find('img')['src']
        pic_name = pic_src.split('/')[-1]

        f = open(pic_name, 'wb')
        print("accessing {}".format(pic_src))
        f.write(requests.get(pic_src, headers=header(image_referer)).content)
        f.close()
        image_referer = pic_link  # update the referer
        print("finish {} image : {}".format(pic_index, pic_name))

    os.chdir(IMAGE_PATH)  # finish downloading, and get back


if __name__ == "__main__":
    '''
    remember to update the referer when you change the page number.
    '''
    header_referer = "https://www.mzitu.com/"

    # by setting the range, can scrape the images in the first n pages.
    for i in range(3):
        print("accessing the {} page...".format(i))
        r = request_page(i, referer=header_referer)
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
