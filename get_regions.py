import requests
from bs4 import BeautifulSoup

# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cache-Control': 'no-cache',
#     'Pragma': 'no-cache',
#     'Proxy-Connection': 'keep-alive',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
#     # 'Cookie': 'route=0ac454e771f6298414c35589736677d2; _yfxkpy_ssid_10005562=%7B%22_yfxkpy_firsttime%22%3A%221747726897562%22%2C%22_yfxkpy_lasttime%22%3A%221747794108810%22%2C%22_yfxkpy_visittime%22%3A%221747825146022%22%2C%22_yfxkpy_cookie%22%3A%2220250520154137563895918365727635%22%2C%22_yfxkpy_returncount%22%3A%221%22%7D',
# }
#
# response = requests.get(
#     'http://www.innocom.gov.cn/gqrdw/c101481/list_gsgg_l2.shtml',
#     headers=headers,
#     verify=False,
# )
#
# soup = BeautifulSoup(response.text, 'html.parser')
# div = soup.find('div', attrs={'class': 'fl subnav'})
# dds = div.find_all('dd')
# regions = []
# for dd in dds:
#     a = dd.find('a')
#     regions.append({"region": a.get('title'), "url": a.get('href')})
# print(regions)

regions = [{'region': '北京市', 'url': '/gqrdw/c101443/list_gsgg_l3.shtml'}, {'region': '天津市', 'url': '/gqrdw/c101444/list_gsgg_l3.shtml'}, {'region': '河北省', 'url': '/gqrdw/c101445/list_gsgg_l3.shtml'}, {'region': '山西省', 'url': '/gqrdw/c101446/list_gsgg_l3.shtml'}, {'region': '内蒙古自治区', 'url': '/gqrdw/c101447/list_gsgg_l3.shtml'}, {'region': '辽宁省', 'url': '/gqrdw/c101448/list_gsgg_l3.shtml'}, {'region': '大连市', 'url': '/gqrdw/c101449/list_gsgg_l3.shtml'}, {'region': '吉林省', 'url': '/gqrdw/c101450/list_gsgg_l3.shtml'}, {'region': '黑龙江省', 'url': '/gqrdw/c101451/list_gsgg_l3.shtml'}, {'region': '上海市', 'url': '/gqrdw/c101452/list_gsgg_l3.shtml'}, {'region': '江苏省', 'url': '/gqrdw/c101453/list_gsgg_l3.shtml'}, {'region': '浙江省', 'url': '/gqrdw/c101454/list_gsgg_l3.shtml'}, {'region': '宁波市', 'url': '/gqrdw/c101455/list_gsgg_l3.shtml'}, {'region': '安徽省', 'url': '/gqrdw/c101456/list_gsgg_l3.shtml'}, {'region': '福建省', 'url': '/gqrdw/c101457/list_gsgg_l3.shtml'}, {'region': '厦门市', 'url': '/gqrdw/c101458/list_gsgg_l3.shtml'}, {'region': '江西省', 'url': '/gqrdw/c101459/list_gsgg_l3.shtml'}, {'region': '山东省', 'url': '/gqrdw/c101460/list_gsgg_l3.shtml'}, {'region': '青岛市', 'url': '/gqrdw/c101461/list_gsgg_l3.shtml'}, {'region': '河南省', 'url': '/gqrdw/c101462/list_gsgg_l3.shtml'}, {'region': '湖北省', 'url': '/gqrdw/c101463/list_gsgg_l3.shtml'}, {'region': '湖南省', 'url': '/gqrdw/c101464/list_gsgg_l3.shtml'}, {'region': '广东省', 'url': '/gqrdw/c101465/list_gsgg_l3.shtml'}, {'region': '深圳市', 'url': '/gqrdw/c101466/list_gsgg_l3.shtml'}, {'region': '广西壮族自治区', 'url': '/gqrdw/c101467/list_gsgg_l3.shtml'}, {'region': '海南省', 'url': '/gqrdw/c101468/list_gsgg_l3.shtml'}, {'region': '重庆市', 'url': '/gqrdw/c101469/list_gsgg_l3.shtml'}, {'region': '四川省', 'url': '/gqrdw/c101470/list_gsgg_l3.shtml'}, {'region': '贵州省', 'url': '/gqrdw/c101471/list_gsgg_l3.shtml'}, {'region': '云南省', 'url': '/gqrdw/c101472/list_gsgg_l3.shtml'}, {'region': '西藏自治区', 'url': '/gqrdw/c101473/list_gsgg_l3.shtml'}, {'region': '陕西省', 'url': '/gqrdw/c101474/list_gsgg_l3.shtml'}, {'region': '甘肃省', 'url': '/gqrdw/c101475/list_gsgg_l3.shtml'}, {'region': '青海省', 'url': '/gqrdw/c101476/list_gsgg_l3.shtml'}, {'region': '宁夏回族自治区', 'url': '/gqrdw/c101477/list_gsgg_l3.shtml'}, {'region': '新疆维吾尔自治区', 'url': '/gqrdw/c101478/list_gsgg_l3.shtml'}]
BASE_URL = 'http://www.innocom.gov.cn/'

regs = ['北京市', '天津市', '河北省', '山西省', '内蒙古自治区', '辽宁省', '大连市', '吉林省', '黑龙江省', '上海市', '江苏省', '浙江省', '宁波市', '安徽省', '福建省', '厦门市', '江西省', '山东省', '青岛市', '河南省', '湖北省', '湖南省', '广东省', '深圳市', '广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省', '云南省', '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区']

def get_number_url(url, num):
    url = BASE_URL + url[1:]

    if num == 1:
        return url
    else:
        return url[:-6] + f'_{num}' + url[-6:]

def get_links(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        # 'Cookie': 'route=0ac454e771f6298414c35589736677d2; _yfxkpy_ssid_10005562=%7B%22_yfxkpy_firsttime%22%3A%221747726897562%22%2C%22_yfxkpy_lasttime%22%3A%221747794108810%22%2C%22_yfxkpy_visittime%22%3A%221747825146022%22%2C%22_yfxkpy_cookie%22%3A%2220250520154137563895918365727635%22%2C%22_yfxkpy_returncount%22%3A%221%22%7D',
    }

    response = requests.get(
        url,
        headers=headers,
        verify=False,
    )
    if response.status_code == 404:
        return False

    soup = BeautifulSoup(response.text, 'html.parser')

    div = soup.find('div', attrs={'class': 'column-list'})

    lis = div.find_all('li')

    links = []
    for li in lis:
        title = li.find('a')['title']
        url = li.find('a')['href']
        time = li.find('span').text.strip()
        links.append({'title': title, 'link': url, 'time': time})

    return links
links = []

for region in regions:
    for i in range(1, 56):
        link = get_links(get_number_url(region['url'], i))
        if not link:
            break
        links += link

print(len(links))
print(links)