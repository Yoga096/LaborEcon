import pandas as pd   

# 讀取並合併範圍相同的成績及個資
p1 = pd.read_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/player_data_qq.csv')  
p2 = pd.read_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/fielder_all.csv')
pwage = pd.read_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/player_salary.csv')
p3 = pd.merge(p1, p2, left_on="name", right_on="name")
#p4 = pd.concat([p3, pwage], join='inner', ignore_index=True)
p4 = pd.merge(left=p3,
         right=pwage,
         how="right", # left outer join
         on=["name", "year"], # 透過此欄位合併
         indicator=True # 顯示結果中每一列的來源
)

## 刪除無用的欄
#p4 = p4.drop("Unnamed: 0_x", axis = 1)
#p4 = p4.drop("Unnamed: 0_y", axis = 1)
#p4 = p4.drop("url_y", axis = 1)

## 更改檔名存檔並顯示完成
p4.to_csv('C:/Users/Yoga/Desktop/Labor Econ/project/data/data_all_fielder3.csv', encoding = 'utf_8_sig', index = False)
print("complete")