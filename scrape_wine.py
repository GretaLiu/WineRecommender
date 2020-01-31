from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import math


def scrape (url_list: list):
    mydata = {}
    wine_name = ""
    wine_region = ""
    wine_country = ""
    wine_type = ""
    winery = ""
    grapes = ""
    wine_name_array = []
    wine_region_array = []
    wine_country_array = []
    wine_type_array = []
    winery_array = [] 
    grapes_array = []
    chrome_options = Options()
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    chrome_options.add_argument('start-maximized')

    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)
    for i in range(0,len(url_list)):
        driver.get(url_list[i])

        try: #wine name
            wine_0 = driver.find_element_by_xpath("//div[@class='winePageHeader__pageHeader--11AWt']/h1")
            wine_name = wine_0.text
        except NoSuchElementException:
            wine_name = ""
        try: #wine region 
            wine_1 = driver.find_element_by_xpath("//div[@class='wineLocationHeader__text--3irYN']/a[1]")
            wine_region = wine_1.text
        except NoSuchElementException:
            wine_region = ""
        try: #wine country 
            wine_2 = driver.find_element_by_xpath("//div[@class='wineLocationHeader__text--3irYN']/a[2]")
            wine_country = wine_2.text
        except NoSuchElementException:
            wine_country = ""
        try: #wine type
            wine_3 = driver.find_element_by_xpath("//div[@class='wineLocationHeader__text--3irYN']/span[1]")
            wine_type = wine_3.text
        except NoSuchElementException:
            wine_type = ""
        try: #winery
            wine_4 = driver.find_element_by_xpath("//div[@class='wineFacts__container--eIljB'][1]/div[2]/a")
            winery = wine_4.text
        except NoSuchElementException:
            winery = ""
        try: #grapes
            wine_5 = driver.find_element_by_xpath("//div[@class='wineFacts__container--eIljB'][1]/div[2]/a")
            grapes = wine_5.text
        except NoSuchElementException:
            grapes = ""
        wine_name_array.append(wine_name)
        wine_region_array.append(wine_region)
        wine_country_array.append(wine_country)
        wine_type_array.append(wine_type)
        winery_array.append(winery) 
        grapes_array.append(grapes)
        time.sleep(3)
    mydata["wine_name"]=wine_name_array
    mydata["wine_region"] = wine_region_array
    mydata["wine_country"] = wine_country_array
    mydata["wine_type"] = wine_type_array
    mydata["winery"]= winery_array
    mydata["grapes"] = grapes_array
    mydataframe = pd.DataFrame(mydata)

    return mydataframe

if __name__ == "__main__":
    url_list = ['https://www.vivino.com/kim-crawford-sauvignon-blanc/w/66534?ref=nav-search',
    'https://www.vivino.com/de-deinhard-mosel-saal-ruwer-piesporter-goldtropfchen-riesling/w/2408352',
    'https://www.vivino.com/jacob-s-creek-shiraz-cabernet/w/2693',
    'https://www.vivino.com/santa-margherita-pinot-grigio-valdadige/w/1184502',
    'https://www.vivino.com/lindemans-bin-45-cabernet-sauvignon/w/3776',
    'https://www.vivino.com/brotte-la-fiole-du-pape-chateauneuf-du-pape/w/2374392',
    'https://www.vivino.com/finca-villacreces-pruno-ribera-del-duero/w/1141810',
    'https://www.vivino.com/lindemans-bin-65-chardonnay/w/2153',
    'https://www.vivino.com/cupcake-chardonnay/w/99562',
    'https://www.vivino.com/lindemans-bin-50-shiraz/w/2156',
    'https://www.vivino.com/gekkeikan-japanese-caramel/w/2503563',
    'https://www.vivino.com/cupcake-red-velvet/w/1140866',
    'https://www.vivino.com/torres-vina-esmeralda/w/2628',
    'https://www.vivino.com/ruffino-chianti/w/2186',
    'https://www.vivino.com/san-pedro-central-valley-gato-negro-cabernet-sauvignon/w/3565573',
    'https://www.vivino.com/monseran-garnacha/w/1160055',
    'https://www.vivino.com/copper-moon-moonlight-harvest-merlot/w/1184253',
    'https://www.vivino.com/peter-lehmann-layers-red/w/1374567',
    'https://www.vivino.com/georges-duboeuf-beaujolais-villages/w/79407',
    'https://www.vivino.com/michel-torino-cuma-organic-torrontes/w/1145296',
    'https://www.vivino.com/rosemount-shiraz-cabernet/w/2448166',
    'https://www.vivino.com/luc-belaire-gold-brut/w/5599160',
    'https://www.vivino.com/gallo-family-vineyards-cabernet-sauvignon/w/3380',
    'https://www.vivino.com/wolf-blass-yellow-label-chardonnay/w/1130017',
    'https://www.vivino.com/barone-montalto-nero-d-avola-cabernet-sauvignon/w/1505448',
    'https://www.vivino.com/beringer-vineyards-main-vine-white-zinfandel-california/w/5443473',
    'https://www.vivino.com/sawmill-creek-sauvignon-blanc/w/1174142',
    'https://www.vivino.com/gray-monk-okanagan-valley-red-pinot-noir/w/2113245',
    'https://www.vivino.com/jose-maria-da-fonseca-periquita-tinto-original/w/1635822',
    'https://www.vivino.com/j-lohr-estates-riverstone-chardonnay/w/1717479',
    'https://www.vivino.com/rosemount-chardonnay-diamond-label/w/68254',
    'https://www.vivino.com/wine-o-clock-pinot-grigio/w/1394894',
    'https://www.vivino.com/georges-duboeuf-beaujolais-villages/w/79407',
    'https://www.vivino.com/dom-perignon-brut-champagne/w/86684',
    'https://www.vivino.com/san-pedro-central-valley-gato-negro-cabernet-sauvignon/w/3565573',
    'https://www.vivino.com/penfolds-koonunga-hill-shiraz-cabernet/w/1306',
    'https://www.vivino.com/it-masi-bonacosta-valpolicella-classico/w/21975',
    'https://www.vivino.com/gallo-family-vineyards-white-zinfandel/w/1156607',
    'https://www.vivino.com/jacob-s-creek-chardonnay/w/2706',
    'https://www.vivino.com/joseph-drouhin-beaujolais-villages/w/24062',
    'https://www.vivino.com/stoneleigh-vineyards-sauvignon-blanc/w/23834',
    'https://www.vivino.com/baltasar-gracian-calatayud-el-politico-garnacha/w/4175593',
    'https://www.vivino.com/rosemount-diamond-label-shiraz/w/67884',
    'https://www.vivino.com/cono-sur-tocornal-sauvignon-blanc/w/73388',
    'https://www.vivino.com/prospect-ogopogo-s-lair-pinot-grigio-okanogan-valley/w/1676582',
    'https://www.vivino.com/matua-valley-sauvignon-blanc-hawke-s-bay/w/1224837',
    'https://www.vivino.com/j-lohr-estates-seven-oaks-cabernet-sauvignon/w/4343',
    'https://www.vivino.com/oyster-bay-sauvignon-blanc/w/9530',
    'https://www.vivino.com/it-masi-costasera-amarone-della-valpolicella-classico/w/21929',
    'https://www.vivino.com/carlo-rossi-blush/w/2003479',
    'https://www.vivino.com/penfolds-koonunga-hill-chardonnay/w/1989',
    'https://www.vivino.com/trapiche-oak-cask-cabernet-sauvignon/w/1141324',
    'https://www.vivino.com/oyster-bay-chardonnay/w/9528',
    'https://www.vivino.com/hess-select-cabernet-sauvignon/w/1639306',
    'https://www.vivino.com/two-oceans-sauvignon-blanc/w/62804',
    'https://www.vivino.com/trapiche-oak-cask-malbec/w/1135810',
    'https://www.vivino.com/louis-moreau-chablis/w/779318',
    'https://www.vivino.com/fetzer-vineyards-gewurztraminer/w/6678000',
    'https://www.vivino.com/la-crema-sonoma-coast-chardonnay/w/9103',
    'https://www.vivino.com/kendall-jackson-vintner-s-reserve-chardonnay/w/2132',
    'https://www.vivino.com/kendall-jackson-vintner-s-reserve-sauvignon-blanc/w/1399107',
    'https://www.vivino.com/anna-spinato-prosecco-organic/w/1983803',
    'https://www.vivino.com/louis-bernard-cotes-du-rhone-villages/w/75920',
    'https://www.vivino.com/ricasoli-brolio-chianti-classico/w/1166103',
    'https://www.vivino.com/taittinger-brut-reserve-champagne/w/1129619',
    'https://www.vivino.com/two-oceans-sauvignon-blanc/w/62804',
    'https://www.vivino.com/bogle-old-vine-zinfandel/w/622',
    'https://www.vivino.com/michael-david-winery-petite-petit/w/1144063',
    'https://www.vivino.com/luigi-bosca-malbec-mendoza-red-wine/w/2141966',
    'https://www.vivino.com/st-francis-cabernet-sauvignon/w/7873',
    'https://www.vivino.com/bogle-merlot/w/620',
    'https://www.vivino.com/ecco-domani-pinot-grigio/w/1730840',
    'https://www.vivino.com/screw-it-malbec/w/4027556',
    'https://www.vivino.com/ruffino-riserva-ducale-chianti-classico/w/1137925',
    'https://www.vivino.com/banrock-station-shiraz/w/84335',
    'https://www.vivino.com/mark-west-winery-california-pinot-noir/w/779298',
    'https://www.vivino.com/pelee-island-winery-merlot-cc77e/w/1676659',
    'https://www.vivino.com/zenato-ripassa-valpolicella-ripasso-superiore/w/1380075?year=U.V.',
    'https://www.vivino.com/luigi-bosca-malbec-mendoza-red-wine/w/2141966?year=U.V.',
    'https://www.vivino.com/woodbridge-by-robert-mondavi-cabernet-sauvignon/w/5806?year=U.V.',
    'https://www.vivino.com/domaine-gayda-figure-libre-freestyle-rouge/w/2503569?year=U.V.',
    'https://www.vivino.com/carlo-rossi-paisano/w/1133636?year=U.V.',
    'https://www.vivino.com/trivento-bodegas-y-vinedos-sa-reserve-cabernet-malbec/w/14379?year=U.V.',
    'https://www.vivino.com/the-bend-in-the-river-riesling-rheinhessen/w/2381988?year=U.V.',
    'https://www.vivino.com/farnese-fantini-sangiovese-terre-di-chieti/w/1512980?year=U.V.',
    'https://www.vivino.com/mission-hill-family-estate-five-vineyards-chardonnay/w/5701?year=U.V.',
    'https://www.vivino.com/barossa-valley-estate-gsm-grenache-shiraz-mourvedre/w/2756195?year=U.V.',
    'https://www.vivino.com/tinhorn-creek-vineyards-gewurztraminer/w/1567927?year=U.V.',
    'https://www.vivino.com/tinhorn-creek-vineyards-pinot-gris/w/85252?year=U.V.']
    scrape(url_list).to_csv("winefeature.csv", mode="a", sep=",",header=False)
