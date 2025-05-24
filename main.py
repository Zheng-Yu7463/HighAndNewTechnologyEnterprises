
import requests
from bs4 import BeautifulSoup
import os

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'http://www.innocom.gov.cn/gqrdw/c101445/list_gsgg_l3.shtml',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        # 'Cookie': 'route=634dba88966acd81013e6f242d3f0153; _yfxkpy_ssid_10005562=%7B%22_yfxkpy_firsttime%22%3A%221747726897562%22%2C%22_yfxkpy_lasttime%22%3A%221747726897562%22%2C%22_yfxkpy_visittime%22%3A%221747726897562%22%2C%22_yfxkpy_cookie%22%3A%2220250520154137563895918365727635%22%7D',
    }
BASE_URL = 'http://www.innocom.gov.cn/'
url = 'http://www.innocom.gov.cn/gqrdw/c101445/201511/f754853f18ab4de1a6460590de5e6054.shtml'

def parse_detail_page(url):
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        div = soup.find('div', attrs={'class': 'fjjian'})

        container = soup.find('div', attrs={'class': 'container bg-white padd20'})
        title = container.find_all('h2')[0].text

        file_name = div.find('a').get('href')
        last_slash_index = url.rfind('/')

        file_url = url[:last_slash_index + 1] + file_name
        type = file_url[file_url.rfind('.'):]
    except AttributeError:
        container = soup.find('div', attrs={'class': 'container bg-white padd20'})
        title = container.find_all('h2')[0].text
        try:
            file_name = soup.find('a', attrs={'type': 'file'}).get('href')
            last_slash_index = url.rfind('/')
        except AttributeError:
            file_name = soup.find('div', attrs={'id': 'detailContent'}).find('a').get('href')
            last_slash_index = url.rfind('/')

        file_url = url[:last_slash_index + 1] + file_name
        type = file_url[file_url.rfind('.'):]


    return file_url, type, title


def parse_detail_page_2017(url):
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    container = soup.find('div', attrs={'class': 'container bg-white padd20'})
    title = container.find_all('h2')[0].text

    file_name = container.find('a', attrs={'target': '_blank'}).get('href')

    file_url = BASE_URL + file_name[1:]
    type = file_url[file_url.rfind('.'):]



    return file_url, type, title

def download_file(url, file_name):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查HTTP请求是否成功 (200 OK)

        with open(f"results/{file_name}", 'wb') as f:
            f.write(response.content)
        print(f"文件 '{file_name}' 已成功保存！")

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    except IOError as e:
        print(f"保存文件失败: {e}")

download_file('http://www.innocom.gov.cn/754853f18ab4de1a6460590de5e6054/files/e3d3b3c398db496b89c74bd8bbd9ca1d.doc', '关于河北省2015年第一批复审高新技术企业备案的复函&2015-11-23.doc')
print(parse_detail_page_2017(url))

