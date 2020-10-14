from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen
import pandas as pd
import re
import urllib.request, urllib.error
import csv
import sys
import numpy as np

def commented_table(soup, id):
    id = '#' + id
    if(soup.select_one(id)):
        table = soup.select_one(id)
    else:
        # print('nah')
        return False
    comments = table.find(string=lambda text:isinstance(text,Comment))
    s = BeautifulSoup(comments, 'html.parser')
    return s

def get_text(s, feature):
    if(s.find('td', {'data-stat': feature})):
        cell = s.find('td', {'data-stat': feature})
        a = cell.text.strip().encode()
        text=a.decode("utf-8")
        return text
    else:
        return False

def is_champ(soup):
    info = soup.select_one('#info')
    if (soup.select_one('#bling')):
        bling = info.select_one('#bling')
        tip = bling.select_one('li')
        a = tip.text.strip().encode()
        text=a.decode("utf-8")
        if (text == 'NBA Champions'):
            return 1
    return 0

def is_playoffs(soup):
    if(commented_table(soup, 'all_playoffs_totals')):
        return 1
    return 0

def team_misc_table(soup, line):
    team_misc = commented_table(soup, 'all_team_misc')
    wins = get_text(team_misc, 'wins')
    losses = get_text(team_misc, 'losses')
    ortg = get_text(team_misc, 'off_rtg')
    efg = get_text(team_misc, 'efg_pct')
    line.append(wins)
    line.append(losses)
    line.append('{:.3f}'.format(int(wins)/(int(wins)+int(losses))))
    line.append(ortg)
    line.append(efg)

def d_player(val, total):
    return (val/total)*np.log2((val/total))

def point_balance(soup):
    table = commented_table(soup, 'all_totals')
    body = table.find('tbody')
    footer = table.find('tfoot')

    d_min_arr = []
    d_pts_arr = []

    tmin = int(get_text(footer, 'mp'))
    tpts = int(get_text(footer, 'pts'))

    rows = body.find_all('tr')
    for row in rows:
        pts = int(get_text(row, 'pts'))
        min = int(get_text(row, 'mp'))

        if(pts == 0):
            continue
        d_pts_arr.append(d_player(pts, tpts))
        d_min_arr.append(d_player(min, tmin))

    return '{:.3f}'.format(sum(d_pts_arr)/sum(d_min_arr))

def main(argvs):

    filename = argvs[0]

    teams = ['MIL', 'TOR', 'BOS', 'IND', 'MIA', 'PHI', 'BRK', 'NJN', 'ORL', 'CHO', 'CHA', 'WAS', 'CHI', 'NYK', 'DET', 'ATL',
            'CLE', 'LAL', 'LAC', 'DEN', 'HOU', 'OKC', 'UTA', 'DAL', 'POR', 'MEM', 'PHO', 'SAS', 'SAC', 'NOP', 'NOH', 'MIN', 'GSW']
    years = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    base = 'https://www.basketball-reference.com/teams/'

    data = {'year': [], 'team': [], 'wins': [], 'losses': [], 'wpct': [], 'ortg': [], 'eFG%': [], 'pb': [], 'playoffs': [], 'champions': []}
    final_df = pd.DataFrame(data)

    for year in years:
        for team in teams:
            url = base + team + '/' + year + '.html'
            try:
                page = urlopen(url).read()
            except urllib.error.HTTPError as e:
                print("Does not work: ", url)
                continue
            line = [year, team]

            soup = BeautifulSoup(page, 'html.parser')
            # print(soup)
            pb = point_balance(soup)
            team_misc_table(soup, line)
            line.append(pb)
            line.append(is_playoffs(soup))
            line.append(is_champ(soup))
            final_df = final_df.append({'year':line[0], 'team':line[1], 'wins':line[2], 'losses':line[3], 'wpct':line[4],
                                        'ortg':line[5], 'eFG%':line[6], 'pb':line[7], 'playoffs':line[8], 'champions':line[9]},
                                        ignore_index=True)
            # print(final_df)

    final_df.to_csv(filename, index=False)

if __name__ == "__main__":
	main(sys.argv[1:])
