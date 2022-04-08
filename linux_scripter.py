from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from pyquery import PyQuery as pq


class JD_Spider:
    def __init__(self, item_id, item_name, txt_path, browser, wait):
        self.txt_file = open(txt_path, encoding='utf-8', mode='a')
        self.item_name = item_name
        self.item_id = item_id
        self.browser = browser
        self.wait = wait

    def run(self):
        """登陆接口"""
        try:
            browser.implicitly_wait(5)
            input_edit = self.browser.find_element(By.CSS_SELECTOR, '#key')
            input_edit.clear()
            input_edit.send_keys(self.item_name)
            input_edit.send_keys(Keys.ENTER)
        except Exception as e:
            print('Not found this item', e)
        # 向下翻页
        self.browser.execute_script(js)
        time.sleep(1.5)

        html = self.browser.page_source  # 获取html
        item_count = self.parse_html(html)
        current_url = self.browser.current_url  # 获取当前页面 url
        initial_url = str(current_url).split('&pvid')[0]
        if item_count >= 60:
            # 这样每个产品会有120个. 2页，每页60个
            for i in range(1, 2):
                try:
                    next_page_url = initial_url + '&page={}&s={}&click=0'.format(str(i * 2 + 1), str(i * 60 + 1))
                    self.browser.get(next_page_url)
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList > ul > li')))
                    # 向下翻页
                    browser.execute_script(js)
                    time.sleep(1.5)
                    html = self.browser.page_source
                    self.parse_html(html)  # 对 html 网址进行解析
                    print('{}% finish'.format(str(50 * i)))
                    time.sleep(0.1)  # 设置频率
                except Exception as e:
                    print('Error Next page', e)
                    self.txt_file.close()

    def parse_html(self, html):
        doc = pq(html)
        items = doc('#J_goodsList > ul > li').items()
        item_count = 0
        for item in items:
            try:
                product = {
                    'name': item.find('div > div.p-name > a > em').text().replace('\n', '\t') if item.find(
                        'div > div.p-name > a > em').text() else "None"
                }
                if product['name'] is None:
                    return False
                else:
                    product_name = product['name'].replace('\t', '')
                    product_item = item_id + '\t' + product_name + '\n'
                    self.txt_file.write(product_item)
                    item_count += 1
            except Exception as e:
                print('Error {}'.format(e))
        print("number of items in 1 page: ", item_count)
        return item_count


if __name__ == '__main__':
    query_file_path = r"/home/akira/桌面/train.query.txt"
    txt_name = 'jd_item.txt'
    url = 'https://www.jd.com/'  # 登录网址
    options = webdriver.ChromeOptions()  # 谷歌浏览器
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(executable_path=r"/home/akira/桌面/chromedriver", options=options)
    wait = WebDriverWait(browser, 2)
    browser.get(url)
    # 将滚动条移动到页面底部
    js = 'var q=document.documentElement.scrollTop=100000'

    with open(query_file_path, 'r') as query_file:
        # 需要查询的数据行数目
        count = 1000
        # 初始化中断点的地址
        interpret = 0
        # 停止节点, 每30个停止10秒，最后一行可以设置
        stop_flag = 30
        while count > 0:
            data = query_file.readline()
            count -= 1
            interpret += 1
            if interpret <= 357:
                pass
            else:
                item_id, item_name = data.split('\t', 1)  # 防止名字中有\t影响命名
                print('------解析第{}个query------'.format(str(item_id)))
                start_time = time.time()
                spider = JD_Spider(item_id, item_name, txt_name, browser, wait)
                spider.run()
                end_time = time.time()
                print(int(end_time-start_time), 'seconds')
                print("***Done***")
                if count % stop_flag == 0:
                    print("Take a rest man!")
                    time.sleep(10)
