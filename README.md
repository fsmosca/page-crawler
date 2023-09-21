# Page crawler

A playwright script to get FIBA game match results from FIBA World Cup 2023 and Olympics 2020.

## Files

#### 1. worldcup2023.py

Used to get match result from the world cup 2023 games. Results are saved in csv file. You need to create a folder path `data/worldcup/2023` to save the csv file.

#### 2. olympics2020.py

Used to get match result from the Tokyo olympics 2020 games. Results are saved in csv file. You need to create a folder path `data/olympics/2020` to save the csv file.

#### 3. worldcup2019.py

Used to get match results from world cup 2019. Results are saved in csv file. You need to create a folder path `data/worldcup/2019` to save the csv file.

#### 4. worldcup2014.py

Used to get match results from world cup 2014. Results are saved in csv file. You need to create a folder path `data/worldcup/2014` to save the csv file.

## Setup

1. Install latest Python
2. Clone this repo with `git clone https://github.com/fsmosca/page-crawler.git`
3. cd to page-crawler
4. Create a folder path `data/worldcup/2023` similar to this repository
5. Install dependencies with `pip install -r requirements.txt`
6. Run the script with `python worldcup2023.py`

Crawled match results will be saved under the data folder with filenames such as ANG.csv, USA.csv and others. Step 4 is important, don't miss it.

**Typical output**

ANG.csv
```
C1,C1S,C2,C2S,GI,DP
ANG,67,ITA,81,1,2023.08.25
PHI,70,ANG,80,2,2023.08.27
ANG,67,DOM,75,3,2023.08.29
ANG,76,CHN,83,4,2023.08.31
ANG,78,SSD,101,5,2023.09.02

where:
C1 = the country code at the left side of the page
C1S = the score of C1
C2 = similar to C1 but at right
C2S = the score of C2
DI = Game index
DP = Date played
```

## Credits
* [FIBA - Basketball](https://www.fiba.basketball/)
* [Playwright - browser automator](https://playwright.dev/python/)
* [Pandas - data manipulation tool](https://pandas.pydata.org/)
