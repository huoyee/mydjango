from celery.task import Task
import requests
from bs4 import BeautifulSoup
import time
import random
import os

class MeiziTask(Task):

    def __init__(self):
        #任务名称
        self.name = 'MeiziTask'
        #是否下载到本地
        self.is_down = False
        #存放目录，默认当前data下
        self.root_dir = 'data'
        #headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        #分类地址
        self.classify_urls = {
            'xinggan': 'https://www.mzitu.com/xinggan/',
            'japan': 'https://www.mzitu.com/japan/',
            'taiwan': 'https://www.mzitu.com/taiwan/',
            'mm': 'https://www.mzitu.com/mm/'
        }
    def run(self, *args, **kwargs):
        self.get_cfy_images()

    #获取所有图片数据
    def get_all_images(self):
        all_images = []
        for classify, url in self.classify_urls.items():
            images = {}
            classify_items, classify_totle = self.get_classify(url,classify)
            images['items'] = classify_items
            images['totle'] = classify_totle
            images['classify'] = classify

        with open('data/image.json', 'w') as f:
            f.write(all_images)

    # 获取分类数据
    def get_classify(self,url,save_dir):
        # pages = bs.select("a[class='page-numbers']")
        # pagenumbers = int(pages[len(pages)-1].get_text())
        html = requests.get(url, headers=self.headers)
        classify_bs = BeautifulSoup(html.text, 'lxml')
        classify_pages = classify_bs.find_all(name='a', attrs={'class': 'page-numbers'})
        page_numbers = int(classify_pages[-2].get_text())
        classify_totle = 0
        classify_items = []
        for index in range(1, page_numbers + 1):
            page_html = requests.get('{}{}'.format(url, '%d/'), headers=self.headers)
            page_bs = BeautifulSoup(page_html.text, 'lxml')
            page_bs = page_bs.find(id='pins')
            pins = page_bs.find_all('li')
            images = {}
            for pin in pins:
                pin_url = pin.a['href']
                pin_name = pin.img['alt']
                pin_time = pin.find(name='span', attrs={'class': 'time'}).text
                pin_imgs, totle = self.get_images(pin_url,'{}/{}'.format(save_dir,pin_name))
                images['images'] = pin_imgs
                images['name'] = pin_name
                images['time'] = pin_time
                images['totle'] = totle
                print(index, pin_name, totle)
                classify_totle += totle
            classify_items.append(images)
        return classify_items, classify_totle

    #获取单组图片数据
    def get_images(self,pin_url,save_dir):
        # pin_url = 'https://www.mzitu.com/200529'
        pin_html = requests.get(pin_url, headers=self.headers)
        pin_bs = BeautifulSoup(pin_html.text, 'lxml')

        pin_pages = pin_bs.find(name='div', attrs={'class': 'pagenavi'}).find_all('a')[4].span.text
        pin_images = []
        totle = 0
        for index in range(1, int(pin_pages) + 1):
            try:
                #防止封ip
                time.sleep(random.randint(1, 2))
                totle += 1
                pin_image = {}
                pin_html = requests.get("{}/{}".format(pin_url, index), headers=self.headers)
                pin_bs = BeautifulSoup(pin_html.text, 'lxml')
                #图片数据 <div class='main-image'>
                pin_data = pin_bs.find(name='div', attrs={'class': 'main-image'})
                pin_image['src'] = pin_data.img['src']       #image 地址
                pin_image['width'] = pin_data.img['width']   #image 宽度
                pin_image['height'] = pin_data.img['height'] #image 高度
                #print("{}/{}".format(pin_url, index), pin_data.img['src'])
                pin_images.append(pin_image)
                self.save_image('',pin_image['src'],save_dir)
            except:
                print("{}/{}".format(pin_url, index),pin_html.status_code)
        return pin_images, totle

    #保存图片
    def save_image(self,image_url,save_dir):
        if self.is_down:
            html = requests.get(image_url,headers = self.headers, stream=True)

            if html.status_code == 200:
                save_dir = os.path.join(self.root_dir,save_dir)
                if not os.path.isdir(save_dir):
                    os.makedirs(save_dir)
                image_name = os.path.basename(image_url)
                with open(os.path.join(self.root_dir,save_dir,image_name),'wb') as imgfile:
                    imgfile.write(html.content)