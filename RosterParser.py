from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd

# world_ids = [183,102,191,131,178,11,96,188,70,214,61,8,20,225,99]
world_id = 86

levels = ['ML','AAA','AA','High A','Low A','Rookie']
#levels = ['All']
#positions = ['All Positions']
positions = ['C','DH','IF','OF']
pitchers = ['SP','RP']
#pitchers = ['All Pitchers']
hitters = []
throwers = []

driver = webdriver.Chrome('C:\\Users\\logan\\Downloads\\chromedriver_win32\\chromedriver.exe')
driver.get('Https://www.whatifsports.com')
driver.find_element_by_class_name('loginLnk').click()
driver.find_element_by_class_name('username').send_keys('')
driver.find_element_by_class_name('password').send_keys('')
driver.find_element_by_class_name('button').click()


# for world_id in world_ids:
world_path = 'https://www.whatifsports.com/hbd/Pages/World/Home.aspx?worldid=' + str(world_id)
driver.get(world_path)
driver.get('https://www.whatifsports.com/hbd/Pages/World/PlayerSearch.aspx')
#driver.get('https://www.whatifsports.com/hbd/Pages/GM/ViewRoster.aspx')
Select(driver.find_element_by_class_name('FranchiseDropDown')).select_by_visible_text('All Franchises')
#Select(driver.find_element_by_class_name('pageoptions')).select_by_visible_text('Current Ratings')

for level in levels:
    for position in positions:
        col_names = ['ID']
        Select(driver.find_element_by_class_name('PlayingLevelDropDown')).select_by_visible_text(level)
        Select(driver.find_element_by_class_name('PositionDropDown')).select_by_visible_text(position)
        driver.find_element_by_class_name('GoButton').click()
        source = driver.page_source
        soup = BeautifulSoup(source,'lxml')
        table = soup.find('table',id='GMPlayerListTable')
        header = table.find('tr',class_='makeStickyHeader')
        for column in header.find_all('th'):
            if 'rating' in column['class']:
                col_names.append(column.a.img['title'].strip())
            else:
                col_names.append(column.text.strip())
        for player in table.find_all('tr', class_=['odd','even']):
            player_info = []
            for attribute in player.find_all('td'):
                if 'playername' in attribute['class']:
                    player_info.append(attribute.a['href'].split('=')[-1])
                    player_info.append(attribute.text.strip())
                elif 'salary' in attribute['class']:
                    player_info.append(attribute.span.text)
                else:
                    player_info.append(attribute.text.strip())
            hitters.append(dict(zip(col_names, player_info)))

    for pitcher in pitchers:
        col_names = ['ID']
        Select(driver.find_element_by_class_name('PlayingLevelDropDown')).select_by_visible_text(level)
        Select(driver.find_element_by_class_name('PositionDropDown')).select_by_visible_text(pitcher)
        driver.find_element_by_class_name('GoButton').click()
        source = driver.page_source
        soup = BeautifulSoup(source, 'lxml')
        table = soup.find('table', id='GMPlayerListTable')
        header = table.find('tr', class_='makeStickyHeader')
        for column in header.find_all('th'):
            if 'rating' in column['class']:
                col_names.append(column.a.img['title'].strip())
            else:
                col_names.append(column.text.strip())
        for player in table.find_all('tr', class_=['odd','even']):
            player_info = []
            for attribute in player.find_all('td'):
                if 'playername' in attribute['class']:
                    player_info.append(attribute.a['href'].split('=')[-1])
                    player_info.append(attribute.text.strip())
                elif 'salary' in attribute['class']:
                    player_info.append(attribute.span.text)
                else:
                    player_info.append(attribute.text.strip())
            throwers.append(dict(zip(col_names, player_info)))

df = pd.DataFrame(hitters).set_index('ID')
path = 'HBD' + str(world_id) + 'Batters.csv'
cols = ['Player', 'Lvl', 'Frn', 'Pos', '%', 'Age', 'Durability', 'Health', 'Contact', 'Power', 'Batting Versus Left-Handed Pitching', 'Batting Versus Right-Handed Pitching', 'Batting Eye', 'Base Running', 'Speed', 'Range', 'Glove', 'Arm Strength', 'Arm Accuracy', 'Pitch Calling', '$']
#cols = ['Player', 'Lvl', 'Pos', 'Age', 'Durability', 'Health', 'Contact', 'Power', 'Batting Versus Left-Handed Pitching', 'Batting Versus Right-Handed Pitching', 'Batting Eye', 'Base Running', 'Speed', 'Range', 'Glove', 'Arm Strength', 'Arm Accuracy', 'Pitch Calling', '$']
df = df[cols]
df.to_csv(path)
df = pd.DataFrame(throwers).set_index('ID')
path = 'HBD' + str(world_id) + 'Pitchers.csv'
cols = ['Player', 'Lvl', 'Frn', 'Pos', '%', 'Age', 'Durability', 'Health', 'Stamina', 'Control', 'Effectiveness Versus Left-Handed Batting', 'Effectiveness Versus Right-Handed Batting', 'Velocity', 'Groundball/Flyball Tendency', 'Pitch 1', 'Pitch 2', 'Pitch 3', 'Pitch 4', 'Pitch 5', '$']
#cols = ['Player', 'Lvl', 'Pos', 'Age', 'Durability', 'Health', 'Stamina', 'Control', 'Effectiveness Versus Left-Handed Batting', 'Effectiveness Versus Right-Handed Batting', 'Velocity', 'Groundball/Flyball Tendency', 'Pitch 1', 'Pitch 2', 'Pitch 3', 'Pitch 4', 'Pitch 5', '$']
df = df[cols]
df.to_csv(path)


driver.close()