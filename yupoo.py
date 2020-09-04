import requests
import sys
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen

'''
    How to use this script?
    Just run python3 yupoo.py "https://xxxx.x.yupoo.com/xxxxxxx"
    Make sure you pass the URL argument inside double brackets!
'''


# Function to download a single images by url
def download_photo(url, picture_url):
    with requests.Session() as c:
        c.get(url)
        c.headers.update({'referer': url})
        res = c.get(picture_url)
        if res.status_code == 200:
            return res.content


# Lets read the url as HTML
def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html)


# Get all the images url location to list from the given urls
def get_all_pics(url):
    soup = make_soup(url)
    images = [img for img in soup.findAll('img')]
    print(str(len(images)) + "images found.")
    urls = [each.get('src') for each in images]
    final_urls = []
    for i in urls:
        if "jpg" in str(i):
            this_url = "http:" + i
            final_urls.append(this_url)
    return final_urls


# Download each url location into a new pictures folder
def download_to_dir(url, images_urls):
    # First create dir if not exists
    uuid = url[::-1].split("=")[0][::-1]
    print("UUID of this URL is :" + uuid)
    directory = "pictures/" + uuid + "/"
    print("The directory to hold the downloaded files are: " + directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    index = 0
    for i in images_urls:
        with open(directory + 'photo{}.jpg'.format(index), 'wb') as f:
            f.write(download_photo(url, i))
        index += 1


# Main func of the script
def main_func(url):
    print("Starting to download from " + url)
    images_urls = get_all_pics(url)
    print("The images going to be downloaded are:" + str(images_urls))
    download_to_dir(url, images_urls)


# Must be given a single argument of the url
if __name__ == "__main__":
    if len(sys.argv) != 2 or (str(sys.argv[1]).endswith("/")):
        print("\nPlease enter valid site\n")
    else:
        main_func(str(sys.argv[1]))
