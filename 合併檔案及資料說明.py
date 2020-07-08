# 檔案總共有5種 :
# 1. 2014到2018年間結婚選手名單 (非爬蟲取得)
# 2. 各隊各年投手投球成績(分３次抓取後合併)
# 3. 各隊各年野手打擊成績(分３次抓取後合併)
# 4. 各投手歷年打擊成績(僅一軍出賽過選手)
# 5. 各選手個人資料
# 第2、3類可直接爬取
# 建議先將第2、3類合併後濾出所有不重複url清單並存成檔案
# 再利用此檔案爬取第4、5類
# 最後將所有檔案(2、3、4、5)合併
# 合併不同類型檔案可依據 :
# 2. year、name、url
# 3. year、name、url
# 4. year、name、url
# 5. name、url


import pandas as pd  


# 讀取要合併的檔案
p1 = pd.read_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/pitcher_1.csv')  
p2 = pd.read_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/pitcher_os.csv')
p3 = pd.read_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/pitcher_rakuten.csv')


# 依次加入新檔案中
df = p1.append(p2, ignore_index = True)
df = df.append(p3, ignore_index = True)


# 刪除無用的欄
df = df.drop("Unnamed: 0", axis = 1)


# 存檔並顯示完成
df.to_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/pitcher_all.csv', encoding = 'utf_8_sig') # 檔名
print("complete")
