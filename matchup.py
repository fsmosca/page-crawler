"""Crawl match results of each team in FIBA site.

Results are taken from FIBA men world cup 2023.
base_url = 'https://www.fiba.basketball/basketballworldcup/2023/'
"""


import random
import os.path
import time

from playwright.sync_api import sync_playwright
import pandas as pd


SLEEP_TIME_REPEAT_INTERVAL = 5  # SEC


USER_AGENTS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
]

COUNTRIES = ['Angola', 'Brazil', 'Cape-Verde', 'Cote-d-Ivoire', 'Egypt',
             'France', 'Germany', 'Iran', 'Japan', 'Latvia', 'Lithuania',
             'Montenegro', 'Philippines', 'Serbia', 'South-Sudan', 'USA',
             'Australia', 'Canada', 'China', 'Dominican-Republic',
             'Finland', 'Georgia', 'Greece', 'Italy', 'Jordan', 'Lebanon',
             'Mexico', 'New-Zealand', 'Puerto-Rico', 'Slovenia', 'Spain',
             'Venezuela']

CTY_TO_IOC = {'Angola': 'ANG', 'Brazil': 'BRA', 'Cape-Verde': 'CPV', 'Cote-d-Ivoire': 'CIV',
              'Egypt': 'EGY', 'France': 'FRA', 'Germany': 'GER', 'Iran': 'IRI', 'Japan': 'JPN',
              'Latvia': 'LAT', 'Lithuania': 'LTU', 'Montenegro': 'MNE', 'Philippines': 'PHI',
              'Serbia': 'SRB', 'South-Sudan': 'SSD', 'USA': 'USA', 'Australia': 'AUS',
              'Canada': 'CAN', 'China': 'CHN', 'Dominican-Republic': 'DOM',
              'Finland': 'FIN', 'Georgia': 'GEO', 'Greece': 'GRE', 'Italy': 'ITA',
              'Jordan': 'JOR', 'Lebanon': 'LBN', 'Mexico': 'MEX',
              'New-Zealand': 'NZL', 'Puerto-Rico': 'PUR', 'Slovenia': 'SLO',
              'Spain': 'ESP', 'Venezuela': 'VEN'}


def build_url(country):
    """Creates a url from the given country."""
    return f'https://www.fiba.basketball/basketballworldcup/2023/team/{country}#|tab=games_and_results'


# Define a function to get the matchup and team results
def get_results(url):
    with sync_playwright() as p:

        # If there is failure, re-crawl. Sleep for some time to not
        # hammer the server of too many requests.
        repeat = 0
        while True:
            try:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                ua = USER_AGENTS[random.randint(0, 4)]
                page.set_extra_http_headers({"User-Agent": ua})
                page.goto(url, timeout=30000)
                a = page.query_selector('div.schedule_list.gmt')
                b = a.query_selector('ul')
                c = b.query_selector_all('div.game_item')        
            except Exception as exc:
                repeat += 1
                print(f'{repr(exc)}')
                browser.close()
                time.sleep(SLEEP_TIME_REPEAT_INTERVAL)
            else:
                break        

        team_left, team_right, points = [], [], []
        for g in c:
            tl = g.query_selector('table.country.left')
            d = tl.query_selector('div.name')
            team_left.append(d.inner_text())

            pt = g.query_selector('table.points')
            divs = pt.query_selector_all('div.number')
            pp = []
            for p in divs:
                n = p.inner_text()
                pp.append(n)
            points.append(pp)

            tr = g.query_selector('table.country.right')
            d = tr.query_selector('div.name')
            team_right.append(d.inner_text())

        browser.close()

        data = []
        for l, p, r in zip(team_left, points, team_right):
            if len(p):
                data.append([l, p[0], r, p[1]])

        df = pd.DataFrame(data, columns=['C1', 'C1S', 'C2', 'C2S'])
        return df


# Entry point
for c in COUNTRIES:
    url = build_url(c)
    cc = CTY_TO_IOC[c]

    # Important you need to create a data folder manually
    fpath = f'./data/{cc}.csv'
    is_file = os.path.isfile(fpath)

    # Do not crawl twice.
    if is_file:
        continue

    df = get_results(url)

    # Save so that we will not attempt to crawl it again
    # later when there is failure.
    df.to_csv(fpath, index=False)   
