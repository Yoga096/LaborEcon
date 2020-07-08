import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


# 檢驗姓名是否附有漢字的讀音，有的話去掉
def try_sup(so, xxn) :
    try :
        xsup = so.find("sup").get_text()
        xsup = re.sub("[\n\u3000 &nbsp;]", "", xsup)
        xxn = re.sub(xsup, "", xxn)
        return xxn
    except AttributeError :
        return xxn

# 建立各項資訊清單
player_name = []    # 姓名   
player_url = []     # 網址 
player_pos = []     # 守備位置
born_year = []      # 生年   
hometown = []       # 出身地        
height = []         # 身高
weight = []         # 體重(?)
blood_type = []     # 血型
throw_side = []     # 投
bat_side = []       # 打  
draft_year = []     # 選秀年    
draft_round = []    # 選秀順位  
education = []      # 學經歷
koshien = []        # 甲子園出場經歷
  

# 讀取檔案並濾出不重複的url
p3 = pd.read_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/pitcher_rakuten.csv') # 檔案
urls = p3.drop_duplicates(subset = "url", keep='first', inplace=False)


for url in urls["url"] :
    # 將網頁內容get下來
    res = requests.get(url) 
    soup = BeautifulSoup(res.text)

    # 尋找被<strong>標籤包起來的球員姓名文字
    xname = soup.find("strong").get_text()
    # 調整文字格式
    xname = re.sub("[\n\u3000 &nbsp;]", "", xname)
    xname = try_sup(soup, xname)
    # 印出球員姓名及url    
    print(xname, url)
    
    # 尋找被<i class="i-pos-l active">標籤包起來的守備位置
    for x in soup.find("i", {'class':'i-pos-l active'}) :
        xpos = re.sub("[\n\u3000 &nbsp;]", "", x)[-1]

    # 數據編號i預設為1
    i = 1
    # 尋找所有被<td>標籤包起來的元素
    for thing in soup.select("td"):
        # 擷取文字部分，並移除空格、換行等
        x = thing.get_text()
        x = re.sub("[\n\u3000 &nbsp;\xa0]", "", x)
        
        # 將抓下來的資訊依照編號加進清單
        if i == 1 :
            player_name.append(xname)
            player_url.append(url)
            player_pos.append(xpos)
            born_year.append(x[:4])
        elif i == 2 :
            hometown.append(x)
        elif i == 3 :
            x1 = x.split("/")
            x2 = x1[1].split("（")
            x3 = re.sub("[）]", "", x2[1])
            height.append(x1[0])
            weight.append(x2[0])
            blood_type.append(x3)
        elif i == 4 :                
            throw_side.append(x[0])
            bat_side.append(x[3])  
        elif i == 5 :
            if "年" in x :
                x1 = x.split("年")
                xa = x1[0]
                xb = x1[1]
            else :
                xa = ""
                xb = ""
            draft_year.append(xa)    
            draft_round.append(xb)
        elif i == 7 :                    
            if "（甲）" in x :
                koshien.append(True)
            else :
                koshien.append(False)           
            x = re.sub("[（甲）]", "", x)
            education.append(x)

        # 取完前7項元素後結束迴圈
        elif i >= 8 :
            break
        
        i += 1

    # 休息1秒防止被網站誤認為攻擊
    time.sleep(1)        


# 建立dict
dict = {"name" : player_name,
        "url" : player_url,
        "position" : player_pos,
        "born_year" : born_year,
        "hometown" : hometown,
        "height" : height,
        "weight" : weight,
        "blood_type" : blood_type, 
        "throw_side" : throw_side, 
        "bat_side" : bat_side,
        "draft_year" : draft_year, 
        "draft_round" : draft_round,
        "education" : education,
        "koshien" : koshien}


# 將dict轉乘dataframe並存成csv檔
player_data = pd.DataFrame(dict)
# (！)在此處調整檔名及檔案位置
player_data.to_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/player_data_qq.csv', encoding = 'utf_8_sig')
# 顯示完成
print("complete")
            