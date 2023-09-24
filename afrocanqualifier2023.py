"""Crawl match results in the FIBA Afrocan qualifier 2023 games.

The base url is 'https://www.fiba.basketball/afrocan/2023/qualifiers'.
Match results are saved in a csv file per team.
"""


import random
import os.path
import time
from datetime import datetime

from playwright.sync_api import sync_playwright
import pandas as pd


output_folder = './data/afrocanqualifier/2023'


SLEEP_TIME_REPEAT_INTERVAL = 5  # SEC


USER_AGENTS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
]


CTY_TO_IOC = {'Algeria': 'ALG', 'Benin': 'BEN', 'Burundi': 'BDI', 'Cameroon': 'CMR',
              'Central-African-Rep-': 'CAF', 'Chad': 'CHA', 'Cote-d-Ivoire': 'CIV',
              'Equatorial-Guinea': 'GEQ', 'Eritrea': 'ERI', 'Gabon': 'GAB', 'Guinea': 'GUI',
              'Mozambique': 'MOZ', 'Nigeria': 'NGR', 'Rwanda': 'RWA', 'South-Sudan': 'SSD',
              'Tanzania': 'TAN', 'Tunisia': 'TUN', 'Zambia': 'ZAM', 'Zimbabwe': 'ZIM'}


def build_url(country):
    """Creates a url from the given country."""
    return f'https://www.fiba.basketball/afrocan/2023/qualifiers/team/{country}#|tab=games_and_results'


def simple_date(date_value):
    date_format = '%A %d %B %Y'
    date_obj = datetime.strptime(date_value, date_format)
    return date_obj.strftime('%Y.%m.%d')


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
                a = page.query_selector('div.qualifiers_games_and_results_content.local')
                c = a.query_selector_all('div.games_list')        
            except Exception as exc:
                repeat += 1
                print(f'{repr(exc)}')
                browser.close()
                time.sleep(SLEEP_TIME_REPEAT_INTERVAL)
            else:
                break        

        team_left, team_right, points, game_date = [], [], [], []
        for g in c:
            # Save the date played
            date_str = g.query_selector('h4').inner_text()
            sd = simple_date(date_str)
            game_date.append(sd)

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
        gi = 0
        for l, p, r, d in zip(team_left, points, team_right, game_date):
            if len(p):
                gi += 1
                data.append([l, p[0], r, p[1], gi, d])

        df = pd.DataFrame(data, columns=['C1', 'C1S', 'C2', 'C2S', 'GI', 'DP'])
        return df


# Entry point
for c in list(CTY_TO_IOC.keys()):
    url = build_url(c)
    cc = CTY_TO_IOC[c]

    # Important you need to create a data folder manually
    fpath = f'{output_folder}/{cc}.csv'
    is_file = os.path.isfile(fpath)

    # Do not crawl twice.
    if is_file:
        continue

    df = get_results(url)

    # Save so that we will not attempt to crawl it again
    # later when there is failure.
    df.to_csv(fpath, index=False)   
