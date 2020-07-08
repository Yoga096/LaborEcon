import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


def is_n(xx, xxi) :
    return (xx-xxi) % 26 == 0

def is_float(xx) :
    try :
        xx = float(xx)
        return xx
    except ValueError :
        return "-"

def is_int(xx) :
    try :
        xx = int(xx)
        return xx
    except ValueError :
        return "-"


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

p3 = pd.read_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/pitcher_rakuten.csv')
bb = p3.drop_duplicates(subset = "url", keep='first', inplace=False)
print(bb)
