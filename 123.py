import requests
import re
import base64
from Crypto.Cipher import AES
from concurrent.futures import ThreadPoolExecutor, as_completed

# 定义频道URL数组
n = {
    '爱尔达影剧': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/aierdayingju.html',#爱尔达影剧
    'AFC亚洲旅游': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/AFCyazhoulüyoutai.html',#AFC亚洲旅游
    '爱尔达综合': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/aierdazonghetai.html',#爱尔达综合
    '星空电影': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/xingkongdianyingtai.html',#星空电影
    '星卫电影': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/xingweidianying.html',#星卫电影
    '美亚电影': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/meiyadianying.html',#美亚电影
    '东森幼幼': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/dongsenyouyouYoyoTV.html',#东森幼幼
    'EYETV戏剧': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/EYETVxiju.html',#EYETV戏剧
    'EYETV旅游': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/EYETVlüyou.html',#EYETV旅游
    '卫视电影': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/weishidianyingtai.html',#卫视电影
    '卫视中文': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/weishizhongwentaiStarMoviesChinese.html',#卫视中文
    'MTVLive': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/MTVLive.html',#MTVLive
    '博斯无限': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/bosiwuxian.html',#博斯无限
    '博斯网球': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/bosiwangqiu.html',#博斯网球
    '博斯高球2': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/bosigaoqiu2.html',#博斯高球2
    '博斯运动2': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/bosiyundong2.html',#博斯运动2
    '博斯运动1': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/bosiyundong1.html',#博斯运动1
    '阿里郎': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/alilangArirang.html',#阿里郎
    '靖天卡通': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/jingtiankatongtai.html',#靖天卡通
    '龙详时代': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/longxiangshidai.html',#龙详时代
    'AFC亚洲旅游(备)': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/yazhoulüyouTLCAsia.html',#AFC亚洲旅游(备)
    '美食星球': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/meishixingqiu.html',#美食星球
    '亚洲美食': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/yazhoumeishi.html',#亚洲美食
    '龙华洋片': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/longhuayangpianLunghuaWestern.html',#龙华洋片
    '好消息2': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/haoxiaoxi2.html',#好消息2
    '纬来精彩': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/weilaijingcai.html',#纬来精彩
    '纬来育乐': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/weilaiyule.html',#纬来育乐
    '纬来综合': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/weilaizonghetai.html',#纬来综合
    '纬来戏剧': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/weilaixijutai.html',#纬来戏剧
    '纬来体育': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/weilaitiyutai.html',#纬来体育
    '纬来电影': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/weilaidianyingtai.html',#纬来电影
    '纬来日本': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/weilairibentai.html',#纬来日本
    '年代新闻': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/niandaixinwen.html',#年代新闻
    '靖天咨询': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/jingtianzixuntai.html',#靖天咨询
    '靖天国际': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/jingtianguojitai.html',#靖天国际
    '龙华电影': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/longhuadianyingLunghuaMovie.html',#龙华电影
    '龙华偶像': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/longhuaouxiang.html',#龙华偶像
    '龙华经典': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/longhuajingdiantai.html',#龙华经典
    '龙华戏剧': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/longhuaxijutai.html',#龙华戏剧
    '非凡新闻': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/feifanxinwentai.html',#非凡新闻
    '大爱1': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/daai1tai.html',#大爱1
    '寰宇新闻': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/huanyuxinwentai.html',#寰宇新闻
    '寰宇财经': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/huanyucaijing.html',#寰宇财经
    '东森财经': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/dongsencaijingxinwenETTVBusiness.html',#东森财经
    '东森超视': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/dongsenchaoshi.html',#东森超视
    '东森戏剧': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/dongsenxijuETTVDrama.html',#东森戏剧
    '东森综合': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/dongsenzongheETTVMetro.html',#东森综合
    '东森洋片': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/dongsenyangpianETTVWestern.html',#东森洋片
    '东森电影': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/dongsendianyingETTVMovie.html',#东森电影
    '东森新闻': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/dongsenxinwenETTVNews.html',#东森新闻
    '三立都会': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/sanlidouhuitai.html',#三立都会
    '三立综合': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/sanlizongheSanliMetro.html',#三立综合
    '三立戏剧': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/sanlixijutai.html',#三立戏剧
    '三立台湾': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/sanlitaiwanSanliTaiwan.html',#三立台湾
    'CatchPlay电影': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/CatchPlaydianyingtai.html',#CatchPlay电影
    'AXNTaiwan': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/AXNTaiwan.html',#AXNTaiwan
    'CINEMAX': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/CINEMAX.html',#CINEMAX
    'HollywoodMovies': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/HollywoodMovies.html',#HollywoodMovies
    'HBO_HITS': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/HBO_HITS.html',#HBO_HITS
    'HBO_': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/HBO_HD.html',#HBO_
    '八大娱乐': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/badayuleGTVEntertainment.html',#八大娱乐
    '八大戏剧': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/badaxijuGTVDrama.html',#八大戏剧
    '八大综合': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/badazongheGTVMetro.html',#八大综合
    '八大第一': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/badadiyiGTVFirst.html',#八大第一
    '公视': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/gongshiCTV.html',#公视
    '华视': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/huashiCTS.html',#华视
    '民视台湾': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/minshitaiwantai.html',#民视台湾
    '民视新闻': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/minshixinwentaiFTVNews.html',#民视新闻
    '民视': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/minshi.html',#民视
    '中视新闻': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/zhongshixinwentai.html',#中视新闻
    '中视': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/zhongshi.html',#中视
    '台视综合': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/taishizonghetai.html',#台视综合
    '台视新闻': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/taishixinwentai.html',#台视新闻
    '台视TTV': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/taishiTTV.html',#台视TTV
    '中天亚洲': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/zhongtianyazhoutai.html',#中天亚洲
    '中天综合': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/zhongtianzongheCTIMetro.html',#中天综合
    '中天娱乐': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/zhongtianyuleCTIEntertaiment.html',#中天娱乐
    '中天新闻': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/zhongtianxinwen.html',#中天新闻
    'TVBS': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/TVBS.html',#TVBS
    'TVBS欢乐台': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/TVBShuanletai.html',#TVBS欢乐台
    'TVBS新闻': 'https://www.chaojidianshi.net//zhibo/gangtaizhibo/TVBSNewsxinwentai.html',#TVBS新闻
    'BBC News': 'https://www.chaojidianshi.net//zhibo/490579.html',#BBC News
    'CNN': 'https://www.chaojidianshi.net//zhibo/490578.html',#CNN
    'Discovery Turbo': 'https://www.chaojidianshi.net//zhibo/490577.html',#Discovery Turbo
    'DMAX': 'https://www.chaojidianshi.net//zhibo/490576.html',#DMAX
    'Discovery Science': 'https://www.chaojidianshi.net//zhibo/490575.html',#Discovery Science
    'Discovery Channel': 'https://www.chaojidianshi.net//zhibo/490574.html',#Discovery Channel
    'Discovery Asia': 'https://www.chaojidianshi.net//zhibo/490573.html',#Discovery Asia
    'HBO Signature': 'https://www.chaojidianshi.net//zhibo/490572.html',#HBO Signature
    'HBO Hits': 'https://www.chaojidianshi.net//zhibo/490571.html',#HBO Hits
    'HBO ': 'https://www.chaojidianshi.net//zhibo/490570.html',#HBO 
    'HBO Family': 'https://www.chaojidianshi.net//zhibo/490569.html',#HBO Family
    '寰宇新闻(备)': 'https://www.chaojidianshi.net//zhibo/85.html',#寰宇新闻(备)
    '寰宇新闻2': 'https://www.chaojidianshi.net//zhibo/84.html',#寰宇新闻2
    '中视(备)': 'https://www.chaojidianshi.net//zhibo/47.html',#中视(备)
    '华视(备)': 'https://www.chaojidianshi.net//zhibo/46.html',#华视(备)
    '台视': 'https://www.chaojidianshi.net//zhibo/45.html',#台视
    '民视(备)': 'https://www.chaojidianshi.net//zhibo/44.html',#民视(备)
    '公视(备)': 'https://www.chaojidianshi.net//zhibo/43.html',#公视(备)
    '中天新闻(备)': 'https://www.chaojidianshi.net//zhibo/42.html',#中天新闻(备)
    '中天综合(备)': 'https://www.chaojidianshi.net//zhibo/41.html',#中天综合(备)
    '中天娱乐(备)': 'https://www.chaojidianshi.net//zhibo/40.html',#中天娱乐(备)
    '中天亚洲(备)': 'https://www.chaojidianshi.net//zhibo/39.html',#中天亚洲(备)
    'TVBS新闻(备)': 'https://www.chaojidianshi.net//zhibo/38.html',#TVBS新闻(备)
    'TVBS综合': 'https://www.chaojidianshi.net//zhibo/37.html',#TVBS综合
    'TVBS欢乐': 'https://www.chaojidianshi.net//zhibo/36.html',#TVBS欢乐
    '壹综合': 'https://www.chaojidianshi.net//zhibo/35.html',#壹综合
    '壹新闻': 'https://www.chaojidianshi.net//zhibo/34.html',#壹新闻
    '东森新闻(备)': 'https://www.chaojidianshi.net//zhibo/33.html',#东森新闻(备)
    '东森综合(备)': 'https://www.chaojidianshi.net//zhibo/32.html',#东森综合(备)
    '东森幼幼(备)': 'https://www.chaojidianshi.net//zhibo/31.html',#东森幼幼(备)
    '东森亚洲': 'https://www.chaojidianshi.net//zhibo/30.html',#东森亚洲
    '东森电影(备)': 'https://www.chaojidianshi.net//zhibo/29.html',#东森电影(备)
    '东森洋片(备)': 'https://www.chaojidianshi.net//zhibo/28.html',#东森洋片(备)
    '东森财经(备)': 'https://www.chaojidianshi.net//zhibo/27.html',#东森财经(备)
    '三立新闻': 'https://www.chaojidianshi.net//zhibo/26.html',#三立新闻
    '三立都会(备)': 'https://www.chaojidianshi.net//zhibo/25.html',#三立都会(备)
    '三立台湾(备)': 'https://www.chaojidianshi.net//zhibo/24.html',#三立台湾(备)
    '三立国际': 'https://www.chaojidianshi.net//zhibo/23.html',#三立国际
    '八大综合(备)': 'https://www.chaojidianshi.net//zhibo/22.html',#八大综合(备)
    '八大第一(备)': 'https://www.chaojidianshi.net//zhibo/21.html',#八大第一(备)
    '八大娱乐(备)': 'https://www.chaojidianshi.net//zhibo/20.html',#八大娱乐(备)
    '中视新闻(备)': 'https://www.chaojidianshi.net//zhibo/19.html',#中视新闻(备)
    '中视综合': 'https://www.chaojidianshi.net//zhibo/18.html',#中视综合
    '中视综艺': 'https://www.chaojidianshi.net//zhibo/17.html',#中视综艺
    '卫视电影(备)': 'https://www.chaojidianshi.net//zhibo/16.html',#卫视电影(备)
    '天映电影': 'https://www.chaojidianshi.net//zhibo/15.html',#天映电影
    '龙祥电影': 'https://www.chaojidianshi.net//zhibo/14.html',#龙祥电影
    '龙祥时代': 'https://www.chaojidianshi.net//zhibo/13.html',#龙祥时代
    '纬来综合(备)': 'https://www.chaojidianshi.net//zhibo/12.html',#纬来综合(备)
    '纬来体育(备)': 'https://www.chaojidianshi.net//zhibo/11.html',#纬来体育(备)
    '纬来日本(备)': 'https://www.chaojidianshi.net//zhibo/10.html',#纬来日本(备)
    '纬来电影(备)': 'https://www.chaojidianshi.net//zhibo/9.html',#纬来电影(备)
    '年代新闻(备)': 'https://www.chaojidianshi.net//zhibo/7.html',#年代新闻(备)
    '非凡新闻(备)': 'https://www.chaojidianshi.net//zhibo/6.html',#非凡新闻(备)
    '民视新闻(备)': 'https://www.chaojidianshi.net//zhibo/5.html',#民视新闻(备)
    '卫视中文(备)': 'https://www.chaojidianshi.net//zhibo/4.html',#卫视中文(备)
    '星空国际': 'https://www.chaojidianshi.net//zhibo/3.html',#星空国际
    '凤凰中文台': 'https://www.chaojidianshi.net//zhibo/100.html',#凤凰中文台
    '凤凰资讯台': 'https://www.chaojidianshi.net//zhibo/99.html',#凤凰资讯台
    '凤凰香港台': 'https://www.chaojidianshi.net//zhibo/98.html',#凤凰香港台
    'RHK32': 'https://www.chaojidianshi.net//zhibo/97.html',#RHK32
    'RHK31': 'https://www.chaojidianshi.net//zhibo/96.html',#RHK31
    '香港开电视': 'https://www.chaojidianshi.net//zhibo/95.html',#香港开电视
    'ViuTv': 'https://www.chaojidianshi.net//zhibo/94.html',#ViuTv
    '香港卫视': 'https://www.chaojidianshi.net//zhibo/93.html',#香港卫视
    '香港有线603': 'https://www.chaojidianshi.net//zhibo/92.html',#香港有线603
    '天映经典': 'https://www.chaojidianshi.net//zhibo/90.html',#天映经典
    '美亚电影台': 'https://www.chaojidianshi.net//zhibo/89.html',#美亚电影台
    'TVB经典台': 'https://www.chaojidianshi.net//zhibo/88.html',#TVB经典台
    'TVB娱乐新闻台': 'https://www.chaojidianshi.net//zhibo/87.html',#TVB娱乐新闻台
    '无线财经台': 'https://www.chaojidianshi.net//zhibo/79.html',#无线财经台
    'TVB翡翠台': 'https://www.chaojidianshi.net//zhibo/78.html',#TVB翡翠台
    'TVB明珠台': 'https://www.chaojidianshi.net//zhibo/77.html',#TVB明珠台
    'TVB星河台': 'https://www.chaojidianshi.net//zhibo/76.html',#TVB星河台
    'TVB Plus': 'https://www.chaojidianshi.net//zhibo/74.html',#TVB Plus
    '无线新闻台': 'https://www.chaojidianshi.net//zhibo/73.html',#无线新闻台
    'TVB功夫台': 'https://www.chaojidianshi.net//zhibo/72.html',#TVB功夫台
    '有线新闻台': 'https://www.chaojidianshi.net//zhibo/62.html',#有线新闻台
    '有线电影台': 'https://www.chaojidianshi.net//zhibo/61.html',#有线电影台
    '有线18台': 'https://www.chaojidianshi.net//zhibo/59.html',#有线18台
    '有线财经台': 'https://www.chaojidianshi.net//zhibo/58.html',#有线财经台
    '香港国际财经台': 'https://www.chaojidianshi.net//zhibo/57.html',#香港国际财经台
    '奇妙资讯': 'https://www.chaojidianshi.net//zhibo/56.html',#奇妙资讯
    'Viu Six': 'https://www.chaojidianshi.net//zhibo/55.html',#Viu Six
    'now爆谷星影台': 'https://www.chaojidianshi.net//zhibo/54.html',#now爆谷星影台
    'now財經台': 'https://www.chaojidianshi.net//zhibo/53.html',#now財經台
    'now新闻台': 'https://www.chaojidianshi.net//zhibo/52.html',#now新闻台
    'now直播台': 'https://www.chaojidianshi.net//zhibo/51.html',#now直播台
    'now Sports': 'https://www.chaojidianshi.net//zhibo/50.html',#now Sports
    '澳视生活': 'https://www.chaojidianshi.net//zhibo/49.html',#澳视生活
    '澳视卫星台MACAU': 'https://www.chaojidianshi.net//zhibo/48.html',#澳视卫星台MACAU

}

# 定义 IV 和 KEY
iv = "TTDNwyJtHesysVPN".encode('utf-8')
key = "12345678988baixh".encode('utf-8')

def get_response(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    return response.text

def decrypt(ciphertext, key, iv):
    ciphertext = base64.b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted.decode('utf-8', errors='ignore').rstrip('\0')

def remove_control_chars(s):
    return ''.join(c for c in s if ord(c) >= 32 and ord(c) <= 126)

def get_video_url(id):
    url = n[id]
    response = get_response(url)
    
    pattern = re.compile(r'<div class="ad"><a href="(.*?)"')
    match = pattern.search(response)
    channel_url = 'https://www.chaojidianshi.net' + match.group(1)
    
    two_response = get_response(channel_url)
    pattern = re.compile(r'none;">(.*?)</div>')
    match = pattern.search(two_response)
    encrypted_text = match.group(1)
    
    decrypted_text = decrypt(encrypted_text, key, iv)
    pattern = re.compile(r'https://[^\s]+')
    match = pattern.search(decrypted_text)
    if match:
        video_url = match.group(0)
    else:
        video_url = "No URL found"
    
    # 移除控制字符
    video_url = remove_control_chars(video_url)
    
    return id, video_url

# 使用多线程获取所有频道的 video_url 并写入文件
with ThreadPoolExecutor(max_workers=10) as executor, open('nntv.txt', 'w', encoding='utf-8') as file:
    futures = {executor.submit(get_video_url, id): id for id in n}
    for future in as_completed(futures):
        id = futures[future]
        try:
            id, video_url = future.result()
            file.write(f"{id},{video_url}\n")
            print(f"{id},{video_url}\n")
        except Exception as e:
            file.write(f"Error fetching video URL for ID {id}: {e}\n")
            print(f"Error fetching video URL for ID {id}: {e}")
