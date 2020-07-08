import pandas as pd # 引用套件並縮寫為 pd  

p1 = pd.read_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/pitcher_1.csv')  
p2 = pd.read_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/pitcher_os.csv')
p3 = pd.read_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/pitcher_rakuten.csv')

df = p1.append(p2, ignore_index = True)
df = df.append(p3, ignore_index = True)

df = df.drop("Unnamed: 0", axis = 1)

df.to_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/pitcher_all.csv', encoding = 'utf_8_sig') # 檔名
print("complete")
