# 抓野手歷年打擊成績數據 ：
# 從隊伍編號及年份調整目標網址
# 從網頁依序抓取每位選手資料
# 將抓下來的數據做格式調整後，依序加入各項清單
# 將清單合成一個dict
# 將dict轉為Dataframe
# 將DataFrame存成csv檔
# 需分三批次處理(t = 10 時網頁不存在) : 
#   1. t = 376 (樂天隊), 
#   2. t in range(11:13) (11:歐力士、12:軟銀), 
#   3. t in range(1: 10) (其他9隊)
# 每批次須調整 1.網址(82行), 2.隊名(98行), 3.檔名(204行)
# 處理樂天隊時隊名為team[0]
# 存好3個csv檔後用合併的.py檔合併
# 清單跟dict登錄的數據名稱有一點出入，懶得改了，自己注意一下就好 ><


import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


# 檢驗數據編號(26次一循環)
def is_n(xx, xxi) :
    return (xx-xxi) % 26 == 0

# 檢驗數據是否為浮點數，否則紀錄為"-"
def is_float(xx) :
    try :
        xx = float(xx)
        return xx
    except ValueError :
        return "-"

# 檢驗數據是否為整數，否則紀錄為"-"
def is_int(xx) :
    try :
        xx = int(xx)
        return xx
    except ValueError :
        return "-"


# 建立各項數據清單
year = []           # 年分    
player_name = []    # 姓名 
player_number = []  # 背號       
player_team = []    # 球隊     
player_url = []     # 網址 
player_game = []    # 出賽     
player_pa = []      # 打席 
player_ab = []      # 打數 
player_r = []       # 得分 
player_h = []       # 安打數 
player_2b = []      # 二壘安
player_3b = []      # 三壘安
player_hr = []      # 全壘打
player_tb = []      # 壘打數
player_rbi = []     # 打點       
player_k = []       # 三振 
player_bb = []      # 四壞 
player_ibb = []     # 敬遠         
player_hbp = []     # 觸身                    
player_sh = []      # 犧牲觸擊 
player_sf = []      # 高飛犧牲
player_sb = []      # 盜壘
player_cs = []      # 被阻殺 
player_dp = []      # 雙殺
player_e = []       # 失誤 
player_avg = []     # 打擊率         
player_slg = []     # 長打率 (壘打數/打數)      
player_obp = []     # 上壘率  
player_ops = []     # 攻擊指數 (上壘率+長打率)


# 隊名list
team = ["楽天", "巨人", "ヤクルト", "DeNA", "中日", "阪神", "広島", "西武", "日本ハム", "ロッテ", "", "オリックス", "ソフトバンク"]


# (！)從t調整隊伍編號，從y調整年份(2014~2019年)
for t in range(376, 377) :
    for y in range(2014, 2020) :

        # 將網頁內容get下來
        res = requests.get('http://www.baseball-lab.jp/player/batter/' + str(t) + '/' + str(y) + '/') # 調整網址
        soup = BeautifulSoup(res.text)

        # 紀錄網頁上每位選手的網址(被<a>標籤包起來的網址中包含"detail"者)
        for player in soup.find_all("a") :
            x = player.get('href')
            if "detail" in x :
                # 紀錄網址時一併紀錄隊名、年份
                year.append(y)
                player_url.append("http://www.baseball-lab.jp" + x)
                # (！)在此處調整隊名
                player_team.append(team[0]) # 隊名

        # 數據編號i預設為1
        i = 1
        # 尋找所有被<td>標籤包起來的元素
        for player in soup.select("td"):
            # 擷取文字部分，並移除空格、換行等
            x = player.get_text()
            x = re.sub("[\n\u3000 &nbsp;]", "", x)

            # 將抓下來的數據依照編號加進清單
            if is_n(i, 1) :
                player_number.append(is_int(x))
            elif is_n(i, 2) :
                player_name.append(x)
            elif is_n(i, 3) :
                player_game.append(is_int(x))
            elif is_n(i, 4) :
                player_pa.append(is_int(x))
            elif is_n(i, 5) :
                player_ab.append(is_int(x))
            elif is_n(i, 6) :
                player_r.append(is_int(x))
            elif is_n(i, 7) :
                player_h.append(is_int(x))
            elif is_n(i, 8) :
                player_2b.append(is_int(x))
            elif is_n(i, 9) :
                player_3b.append(is_int(x))
            elif is_n(i, 10) :
                player_hr.append(is_int(x))
            elif is_n(i, 11) :
                player_tb.append(is_int(x))
            elif is_n(i, 12) :
                player_rbi.append(is_int(x))
            elif is_n(i, 13) :
                player_k.append(is_int(x))
            elif is_n(i, 14) :
                player_bb.append(is_int(x))
            elif is_n(i, 15) :
                player_ibb.append(is_int(x))
            elif is_n(i, 16) :
                player_hbp.append(is_int(x))
            elif is_n(i, 17) :
                player_sh.append(is_int(x))
            elif is_n(i, 18) :
                player_sf.append(is_int(x))
            elif is_n(i, 19) :
                player_sb.append(is_int(x))
            elif is_n(i, 20) :
                player_cs.append(is_int(x))
            elif is_n(i, 21) :
                player_dp.append(is_int(x))
            elif is_n(i, 22) :
                player_e.append(is_int(x))
            elif is_n(i, 23) :
                player_avg.append(is_float(x))
            elif is_n(i, 24) :
                player_slg.append(is_float(x))
            elif is_n(i, 25) :
                player_obp.append(is_float(x))
            elif is_n(i, 26) :
                player_ops.append(is_float(x))
                
            # 數據編號 += 1
            i += 1

        # 休息3秒防止被網站誤認為攻擊       
        time.sleep(3)    


# 建立dict
dict = {"year" : year,
        "team" : player_team,
        "number" : player_number,
		"name" : player_name, 
        "url" : player_url, 
	    "b_game" : player_game,
        "b_pa" : player_pa,
        "b_ab" : player_ab, 
        "b_r" : player_r, 
        "b_h" : player_h, 
        "b_2b" : player_2b, 
        "b_3b" : player_3b, 
        "b_hr" : player_hr, 
        "b_tb" : player_tb, 
        "b_rbi" : player_rbi,
        "b_k" : player_k,
        "b_bb" : player_bb,
        "b_ibb" : player_ibb,
        "b_hbp" : player_hbp,
        "b_sh" : player_sh,
        "b_sf" : player_sf,
        "b_sb" : player_sb,
        "b_cs" : player_cs, 
        "b_dp" : player_dp, 
        "b_e" : player_e,    
        "b_avg" : player_avg,
        "b_slg" : player_slg,
        "b_obp" : player_obp,
        "b_ops" : player_ops}       


# 將dict轉乘dataframe並存成csv檔
player_data = pd.DataFrame(dict)
# (！)在此處調整檔名
player_data.to_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/fielder_rakuten.csv', encoding = 'utf_8_sig')
# 顯示完成
print("complete")