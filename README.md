# Page crawler

A playwright script to get FIBA game match results from FIBA World Cup 2023.

## Setup

1. Install latest Python
2. Clone this repo with `git clone https://github.com/fsmosca/page-crawler.git`
3. cd to page-crawler
4. Create a `data` folder
5. Install dependencies with `pip install -r requirements.txt`
6. Run the script with `python matchup.py`

Crawled match results will be saved under the data folder with filenames such as ANG.csv, USA.csv and others. Step 4 is important, don't miss it.

**Typical output**

ANG.csv
```
C1,C1S,C2,C2S
ANG,67,ITA,81
PHI,70,ANG,80
ANG,67,DOM,75
ANG,76,CHN,83
ANG,78,SSD,101

where:
C1 = the country code at the left side of the page
C1S = the score of C1
C2 = similar to C1 but at right
C2S = the score of C2
```

## Credits
* [FIBA - Basketball](https://www.fiba.basketball/)
* [Playwright - browser automator](https://playwright.dev/python/)
* [Pandas - data manipulation tool](https://pandas.pydata.org/)
