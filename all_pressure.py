# import libraries
from bs4 import BeautifulSoup
import pandas as pd
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

parser = argparse.ArgumentParser()
parser.add_argument('--year', default=2018, type=int)

args = parser.parse_args()
# change this for a stat of different year
YEAR = args.year

# this link gets stat of ratings for the particular year
link = f'https://www.atptour.com/en/stats/leaderboard?boardType=pressure&timeFrame={YEAR}&surface=hard&versusRank=all&formerNo1=false'

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument(f'user-agent={YEAR}-{str(YEAR)[::-1]}')

browser = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
browser.get(link)

html = browser.page_source

soup = BeautifulSoup(html, 'html.parser')
player_tbls = soup.find(id="statsListingTableContent").find('table')

browser.quit()

thead_child = player_tbls.find('thead').find_all(recursive=False)

tbody_child = player_tbls.find('tbody').find_all(recursive=False)


thead = player_tbls.find('thead')
for child in thead_child:
    thead.append(child)

tbody = player_tbls.find('tbody')
for child in tbody_child:
    tbody.append(child)

df = pd.read_html(str(player_tbls))[0]


df.columns = ['rank', 'name', 'pressure_rating', 'break_pts_converted%',
              'break_pts_saved%', 'tie_breaks%', 'deciding_sets%']

# merge with the original set of stats
main_df = pd.read_csv(f'./data/aus-open-player-stats-{YEAR}.csv')
main_df = main_df.merge(df, left_on='name', right_on='name', how='left')

# this link fetches the career ratings of players to fill for players whose
# yearly rating was unavailable
link = f'https://www.atptour.com/en/stats/leaderboard?boardType=pressure&timeFrame=Career&surface=hard&versusRank=all&formerNo1=false'

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')

browser = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
browser.get(link)

html = browser.page_source

soup = BeautifulSoup(html, 'html.parser')
player_tbls = soup.find(id="statsListingTableContent").find('table')

browser.quit()

thead_child = player_tbls.find('thead').find_all(recursive=False)

tbody_child = player_tbls.find('tbody').find_all(recursive=False)

thead = player_tbls.find('thead')
for child in thead_child:
    thead.append(child)

tbody = player_tbls.find('tbody')
for child in tbody_child:
    tbody.append(child)


df = pd.read_html(str(player_tbls))[0]


no_stats = main_df.loc[main_df['pressure_rating'].isna(), 'name']

df.columns = ['rank', 'name', 'pressure_rating', 'break_pts_converted%',
              'break_pts_saved%', 'tie_breaks%', 'deciding_sets%']

df = df[df['name'].isin(no_stats)].copy(deep=True).reset_index(drop=True)

main_df.set_index('name', inplace=True)
df.set_index('name', inplace=True)

main_df['pressure_rating'].fillna(df['pressure_rating'], inplace=True)
main_df.reset_index(inplace=True)

main_df.to_csv(f'data/aus-open-player-stats-{YEAR}.csv', index=False)