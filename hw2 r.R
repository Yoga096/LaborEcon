library(readxl)
library(tidyverse)
library(ggplot2)
library(plm)

# 1.
fielder_raw <- read_excel("fielder_data_all.xlsx")

# 2.
summary(fielder_raw)

# 3.
## 1. 
fielder_data1 <- fielder_raw %>%
  
  mutate(year_2014 = ifelse(year == 2014, 1, 0),
         year_2015 = ifelse(year == 2015, 1, 0),
         year_2016 = ifelse(year == 2016, 1, 0),
         year_2017 = ifelse(year == 2017, 1, 0),
         year_2018 = ifelse(year == 2018, 1, 0),
         year_2019 = ifelse(year == 2019, 1, 0),
         height = as.numeric(substr(height, start = 1, stop = 3)),
         weight = as.numeric(substr(weight,start = 1,stop = nchar(weight) - 2)),
         age = year - born_year,
         age2 = age**2,
         lwage = log(salary),
         bat_r = ifelse(bat_side == "左", 0, 1),
         bat_l = ifelse(bat_side == "右", 0, 1),
         throw_r = ifelse(throw_side == "左", 0, 1),
         throw_l = ifelse(throw_side == "右", 0, 1),
         ifer = ifelse(position %in% c("内"), 1, 0),
         ofer = ifelse(position == "外", 1, 0),
         catcher = ifelse(position == "捕", 1, 0),
         giant = ifelse(team == "巨人", 1, 0)) %>%
  
  group_by(name) %>%  
  arrange(desc(year)) %>% 
  mutate(i = as.numeric(row_number()),
         s_change = ifelse(i >= 1, salary - salary[i+1], NA)) %>%
  arrange(year) %>% 
  ungroup() %>% 
  
  filter(exp >= 0) %>% 
  
  select("year", "name", "height", "weight", "age", "age2", 
         "year_2014", "year_2015", "year_2016", "year_2017", 
         "year_2018", "year_2019", "married", "treat",
         "salary", "s_change", "lwage", "position",
         "b_game", "b_pa", "b_avg", "b_slg", "b_ops",
         "b_hr", "b_rbi", "b_sb", "b_ab", "giant",
         "bat_r", "bat_l", "throw_r", "throw_l",
         "ifer", "ofer", "catcher", "league",
         "exp", "exp2") 

## 2.
sum1 <- fielder_data1 %>%
  group_by(married) %>% 
  summarise(nPlayer = n(),
            mean_salary = mean(salary),
            mean_change = mean(s_change, na.rm = TRUE))


## 3.
fielder_data2 <- fielder_data1 %>%
  full_join(sum1, by = "married")


# 4.
plot2 <- fielder_data2 %>%
  filter((s_change >= 0) | (s_change < 0))
qplot(age, s_change, data = plot2, color = married)

# 5.
result <- lm(lwage ~ treat + married + age + age2 + exp + exp2 +
             bat_r + bat_l +b_game + b_avg + 
             b_hr + b_sb + b_rbi + ofer + league + giant, 
             data = fielder_data1)
summary(result)