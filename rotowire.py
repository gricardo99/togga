#python3
import requests
import regex
from bs4 import BeautifulSoup

start_week = "2017-08-11" 
cur_week = 1 

def get_cur_week():
	return cur_week

def get_team_img_status(img_name):
	if regex.match(r'.*lineup-green\.png', img_name):
		return 'green'
	if regex.match(r'.*lineup-yellow\.png', img_name):
		return 'yellow'
	if regex.match(r'.*lineup-black\.png', img_name):
		return 'black'
	return 'unknown'

roto_lineup_url = str('http://www.rotowire.com/soccer/soccer-lineups.htm?league=EPL&week=')
this_week = get_cur_week()

cur_lineup_url = roto_lineup_url+str(this_week)

r = requests.get(cur_lineup_url)
data = r.text

lineup_div_tag = "span15 offset1"
home_div_tag = "home_lineup"
away_div_tag = "visit_lineup"

soup = BeautifulSoup(data, "html5lib")

starting_players = []
home_lineup = None
away_lineup = None
home_p_info = None
p_name_attr = None
lineups = soup.find_all('div', class_=lineup_div_tag)
for lineup in lineups:
	teams = lineup.find_all('img')
	if len(teams)==4: #we're good with the parsing 
		home_team_name = teams[0].attrs['alt']
		home_team_status = get_team_img_status(teams[1].attrs['src'])
		away_team_name = teams[3].attrs['alt']
		away_team_status = get_team_img_status(teams[2].attrs['src'])
		print("home team:"+home_team_name + " status:"+ home_team_status)
		print("away team:"+away_team_name + " status:"+ away_team_status)
		print("")
		home_lineup=lineup.find('div',class_=home_div_tag)
		away_lineup=lineup.find('div',class_=away_div_tag)
		for player_info in home_lineup.find_all('div', class_='dlineups-vplayer'):
			pos = regex.sub('.*([GDMF/]+).*', r'\g<1>', player_info.find('div', class_='dlineups-pos').text).strip()
			p_name =player_info.find('a').attrs['title']
			home_p_info=player_info
			print("home player:"+p_name + " position:"+ pos)
			starting_players.append(p_name+","+pos)
		for player_info in away_lineup.find_all('div', class_='dlineups-vplayer'):
			pos = regex.sub('.*([GDMF/]+).*',r'\g<1>', player_info.find('div', class_='dlineups-pos').text).strip()
			p_name =player_info.find('a').attrs['title']
			print("away player:"+p_name + " position:"+ pos)
			starting_players.append(p_name+","+pos)
	else:
		print("Error parsing team lineup images")
