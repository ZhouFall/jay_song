import requests    #从网站上爬取数据
from time import sleep    #延时等待
import re,os    #正则表达式和系统文件操作
from datetime import datetime    #统计使用时长
from tqdm import tqdm    #进度条模块

headers = {
    'origin': 'https://y.qq.com',
    'referer': 'https://y.qq.com/',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
}
para = {
    'ct': '24',
    'qqmusic_ver': '1298',
    'new_json': '1',
    'remoteplace': 'txt.yqq.song',
    'searchid': '66253237842047499',
    't': '0',
    'aggr': '1',
    'cr': '1',
    'catZhida': '1',
    'lossless': '0',
    'flag_qc': '0',
    'p': '10',
    'n': '10',
    'w': '周杰伦',
    'g_tk_new_20200303': '5381',
    'g_tk': '5381',
    'loginUin': '0',
    'hostUin': '0',
    'format': 'json',
    'inCharset': 'utf8',
    'outCharset': 'utf-8',
    'notice': '0',
    'platform': 'yqq.json',
    'needNewCode': '0',
}
id_list = []
name_list = []

def get_song_list(url,para):
    # 调用get方法，下载这个字典
    res_music = requests.get(url=url,headers=headers,params=para)
    # 使用json()方法，将response对象，转为列表/字典
    json_music = res_music.json()
    list_music = json_music['data']['song']['list']
    for music in list_music:
        id_list.append(music['id'])
        name_list.append(music['name'])
    sleep(0.1)

def get_song_text():
    url_link = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_yqq.fcg'
    para1 = {
        'nobase64': '1',
        'musicid': '',
        '-': 'jsonp1',
        'g_tk_new_20200303': '5381',
        'g_tk': '5381',
        'loginUin': '0',
        'hostUin': '0',
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': ' utf-8',
        'notice': '0',
        'platform': 'yqq.json',
        'needNewCode': '0',
    }
    count = 0
    #创建歌词文件夹
    if not os.path.exists('./song_text/'):
        os.mkdir('./song_text/')
    print('开始爬取歌曲列表的歌词')
    sleep(0.2)
    for id in tqdm(id_list):
        para1['musicid'] = str(id)
        music_text = requests.get(url=url_link, headers=headers,params=para1)
        with open(r'song_text/{}.txt'.format(name_list[count]),'wb') as f:
            f.write(music_text.text.encode())
        # print('{},歌词爬取完毕'.format(name_list[count]))
        count = count + 1
        sleep(0.1)
    print('歌词爬取完毕')


# 查找当前路径下所有的txt文件
def walkFile(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.txt'):
                fullname = os.path.join(root, f)
                yield fullname

def parse_song_text():
    filepath = walkFile(r'song_text')
    for file in filepath:
        # print(file)
        #打开文件的时候加上打开编码格式
        with open(file,'r',encoding='utf-8') as f:
             text = f.read()
        text = re.sub(r"&#10;", "\n", text)
        text = re.sub(r"(\[.*]\n)|(\[.*])|(\"})|({.*:\")", "", text)
        text = re.sub(r"&#32;", " ",text)
        text = text.replace("&#40;", "(")
        text = text.replace("&#41;", ")")
        text = text.replace("&#45;", "-")
        # print(text)
        with open(file, 'wb') as f:
            f.write(text.encode('utf-8'))

if __name__ =="__main__":
    start = datetime.now()
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
    print('开始爬取歌词列表')
    for i in tqdm(range(1,11)):
        para['p'] = str(i)
        get_song_list(url, para)
    print('前10页歌曲列表爬取完毕')
    sleep(0.2)
    get_song_text()
    parse_song_text()
    end = datetime.now()
    print('一共用时：',end-start)


