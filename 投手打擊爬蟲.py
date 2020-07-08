# 爬取投手打擊成績：
# 從投手檔案中過濾出所有不重複的url
# 從每個url的網頁依序抓取成績 
# (開了很多網頁 耗時會較久 可以斟酌要不要分批再合併)
# 將抓下來的數據做格式調整後，依序加入各項清單
# 將清單合成一個dict
# 將dict轉為Dataframe
# 將DataFrame存成csv檔(250行)
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

# 檢驗姓名是否附有漢字的讀音，有的話去掉
def try_sup(so, xxn) :
    try :
        xxx = xxn
        xsup = so.find("sup").get_text()
        xsup = re.sub("[\n\u3000 &nbsp;]", "", xsup)
        xxx = re.sub(xsup, "", xxx)
        return xxx
    except AttributeError :
        return xxn


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


# 隊名dict
team = {"E" : "楽天", 
        "G" : "巨人", 
        "S" : "ヤクルト",      
        "DB" : "DeNA",
        "D" : "中日",
        "T" : "阪神",
        "C" : "広島",
        "L" : "西武",
        "F" : "日本ハム",
        "M" : "ロッテ",
        "B" : "オリックス", 
        "H" : "ソフトバンク"}


# 讀取檔案並濾出不重複的url
p3 = pd.read_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/pitcher_rakuten.csv') 
urls = p3.drop_duplicates(subset = "url", keep='first', inplace=False)


# 若要分批就改成urls["url"][? : ?]
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

    # 在網頁中有一軍及二軍的投球成績及打擊成績，需檢驗抓到的數據是否為一軍打擊成績
    # f_flag: 是否有一軍成績 (預設有 = 0)  
    f_flag = 0
    for thing in soup.select("#player-results-recently") : 
        x = thing.get_text()
        x = re.sub("[\n\u3000 &nbsp;\xa0]", "", x)
        if "データはありません" in x :
            f_flag = 1
            break

    # 若無一軍成績則跳過本次迴圈
    if f_flag == 1 :
        print("pass")
        continue

    # b_flag: 是否為打擊成績 (預設不是 = 0)
    b_flag = 0
    # 數據編號i預設為1
    i = 1
    # 尋找所有被<td>標籤包起來的元素
    for thing in soup.select("td"):
        x = thing.get_text()
        x = re.sub("[\n\u3000 &nbsp;]", "", x)

        # 找到第一個"通算後"進入打擊成績紀錄範圍
        if "通算" in x :
            b_flag += 1

        elif b_flag == 1 :
            # 從b_flag為1後第29項數據開始進入目標範圍
            if i >= 29 : 
                # 將抓下來的數據依照編號加進清單
                if is_n(i, 3) :        
                    year.append(is_int(x))
                    player_name.append(xname)
                    player_url.append(url)
                elif is_n(i, 4) :
                    player_team.append(team[str(x)])
                elif is_n(i, 5) :
                    player_game.append(is_int(x))
                elif is_n(i, 6) :
                    player_pa.append(is_int(x))
                elif is_n(i, 7) :
                    player_ab.append(is_int(x))
                elif is_n(i, 8) :
                    player_r.append(is_int(x))
                elif is_n(i, 9) :
                    player_h.append(is_int(x))
                elif is_n(i, 10) :
                    player_2b.append(is_int(x))
                elif is_n(i, 11) :
                    player_3b.append(is_int(x))
                elif is_n(i, 12) :
                    player_hr.append(is_int(x))
                elif is_n(i, 13) :
                    player_tb.append(is_int(x))
                elif is_n(i, 14) :
                    player_rbi.append(is_int(x))
                elif is_n(i, 15) :
                    player_k.append(is_int(x))
                elif is_n(i, 16) :
                    player_bb.append(is_int(x))
                elif is_n(i, 17) :
                    player_ibb.append(is_int(x))
                elif is_n(i, 18) :
                    player_hbp.append(is_int(x))
                elif is_n(i, 19) :
                    player_sh.append(is_int(x))
                elif is_n(i, 20) :
                    player_sf.append(is_int(x))                
                elif is_n(i, 21) :
                    player_sb.append(is_int(x))
                elif is_n(i, 22) :
                    player_cs.append(is_int(x))
                elif is_n(i, 23) :
                    player_dp.append(is_int(x))
                elif is_n(i, 24) :
                    player_e.append(is_int(x))
                elif is_n(i, 25) :
                    player_avg.append(is_float(x))
                elif is_n(i, 26) :
                    player_slg.append(is_float(x))
                elif is_n(i, 27) :
                    player_obp.append(is_float(x))
                elif is_n(i, 28) :
                    player_ops.append(is_float(x))

            i += 1
    
        # 遇到第二次"通算"後結束迴圈
        elif b_flag >= 1 :
            break

    # 休息1秒防止被網站誤認為攻擊 
    time.sleep(1)        


# 建立dict
dict = {"year" : year,
        "team" : player_team,
        #"number" : player_number,
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
# (！)在此處調整檔名及檔案位置
player_data.to_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/pitcher_bat_rakuten.csv', encoding = 'utf_8_sig')
# 顯示完成
print("complete")