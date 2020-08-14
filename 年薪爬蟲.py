import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
# 受傷對表現 薪資的影響

year = []
player_name = []
player_team = []
player_salary = []
player_url = []
# player_bat_throw = []
# player_born = []


for y in range(2013, 2020) :
    for i in range(1, 15) :
        page = 'https://www.gurazeni.com/ranking/' + str(i) + '/year:' + str(y)
        print(page)
        res = requests.get(page)
        soup = BeautifulSoup(res.text)

        # 球員姓名
        name_tag = "#player_name"
        for player in soup.select('{}'.format(name_tag)):
            year.append(y)
            name = player.get_text()
            name = re.sub("[\n\u3000 ]", "", name)
            player_name.append(name)
            
        for player in soup.find_all("a") :
            x = player.get('href')
            if "player" in x :
                player_url.append("https://www.gurazeni.com" + x)
            
       # 球員隊伍
        team_tag = "#team"
        for player in soup.select('{}'.format(team_tag)):
            team = player.get_text()
            team = re.sub("[\n\u3000 ]", "", team)
            player_team.append(team)	

        # 球員年薪
        uni_tag = "#uniform_number"

        for player in soup.select('{}'.format(uni_tag)):
            uni = player.get_text()

            if "円" in uni :
                if ("億" in uni) & ("万" in uni) : 
                    uni = re.sub("[\n\u3000 万円]", "", uni).split("億")
                    player_salary.append(int(uni[0]) * 10000 + int(uni[1]))
                elif "億" in uni :
                    uni = int(re.sub("[\n\u3000 億万円]", "", uni)) * 10000
                    player_salary.append(uni)
                else :
                    uni = int(re.sub("[\n\u3000 万円]", "", uni))
                    player_salary.append(uni)
       #elif "投" in uni :
       #   uni = re.sub("[\n\u3000 投げ打ち]", "", uni) 
       #   player_bat_throw.append(uni[0] + "/" + uni[1])
       #elif "年" in uni :
       #   uni = re.sub("[\n\u3000 ]", "", uni)
       #   uni = re.sub("[年月日]", "/", uni)
       #   player_born.append(uni)

    time.sleep(1)

dict = {"year" : year,
       "name" : player_name,  
       "team" : player_team, 
       "salary" : player_salary,
       "url" : player_url
       }
#
player_data = pd.DataFrame(dict)
player_data.to_csv('C:/Users/Yoga/Documents/GitHub/LaborEcon/new_salary.csv', encoding = 'utf_8_sig', index = False)  #存檔至player_data.csv中
print("complete")