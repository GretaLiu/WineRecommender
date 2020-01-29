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

def scrape_this_page ( url ):
    mydata = {}
    reviewer_names_array =[]
    reviewer_info_array = []
    review_date_array = []
    comments_array = []
    star_rating = [] 
    mydataframe = pd.DataFrame(mydata)
    chrome_options = Options()
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    chrome_options.add_argument('start-maximized')

    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)
    driver.get(url)

    try: 
        wine = driver.find_element_by_xpath("//div[@class='winePageHeader__pageHeader--11AWt']/h1")
        wine_name = wine.text
    except NoSuchElementException:
        wine_name = ""
    try:
        number_of_reviews_str  = (driver.find_element_by_xpath("//div[@class='vivinoRatingWide__basedOn--s6y0t']")).text
        number_of_reviews_str = number_of_reviews_str[:-8]
        number_of_reviews = int(number_of_reviews_str)
        number_of_clicks = math.floor(number_of_reviews/3)
        if (number_of_clicks >200):
            number_of_clicks = 200
        for i in range(0, number_of_clicks):
        #click next link
            try:
                element = wait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="anchor__anchor--2QZvA communityReviews__showMore--2yihj"]')))
                element.click() 
                time.sleep(2)
            except (TimeoutException, ElementClickInterceptedException) as e:
                break
        
        
        containers = driver.find_elements_by_xpath("//div[@class='pageSectionColumns__pageSectionColumns--31LI3']/div[1]/div")
        for items in containers:
            try:
                name = items.find_element_by_xpath(".//div[@class='communityReviewer__userSection--yV9wt']/div[2]/a[1]")
                reviewer_names_array.append(name.text)    
            except:
                reviewer_names_array.append("NaN")
            try:
                user_num_rating = items.find_element_by_xpath(".//div[@class='communityReviewer__userSection--yV9wt']/div[2]/span[1]")
                reviewer_info_array.append(user_num_rating.text)
            except:
                reviewer_info_array.append("NaN")
            try:
                review_date = items.find_element_by_xpath(".//div[@class='communityReviewer__userSection--yV9wt']/div[2]/a[2]")
                review_date_array.append(review_date.text)
            except:
                review_date_array.append("NaN")
            try:
                star_rating_content = items.find_elements_by_xpath(".//div[@class='rating__rating--ZZb_x rating__user--15hMB']/i")
                i = 1 
                temp_rating = 0
                for it in star_rating_content:
                    if(it.get_attribute("class") == "rating__icon--2T9_0 rating__icon100--2vw_3"):
                        temp_rating +=1
                    elif (it.get_attribute("class") == "rating__icon--2T9_0 rating__icon50--3xGES"):
                        temp_rating +=0.5
                    
                    if(i%5==0):
                        star_rating.append(temp_rating)
                        temp_rating = 0
                    i = i+1
            except:
                star_rating.append("NaN")
            try:
                rating_text = items.find_element_by_xpath(".//div[@class='communityReview__textSection--vu-i-']/p[1]")
                comments_array.append(rating_text.text)
            except:
                comments_array.append("NaN")
        mydata["wine_name"] = [wine_name]*len(reviewer_names_array)
        mydata["reviewer_names"] = reviewer_names_array
        mydata["reviewing_date"] = review_date_array
        mydata["reviewer_num_rating"] = reviewer_info_array
        mydata["star_rating"] =star_rating 
        mydata["text_rating"] = comments_array

    except NoSuchElementException:
        mydata["wine_name"] = []
        mydata["reviewer_names"] = []
        mydata["reviewing_date"] = []
        mydata["reviewer_num_rating"] = []
        mydata["star_rating"] = []
        mydata["text_rating"] = []
    
    mydataframe = pd.DataFrame(mydata)

    return mydataframe



if __name__ == "__main__":
    long = ['https://www.vivino.com/kim-crawford-sauvignon-blanc/w/66534?ref=nav-search'] 
    short = ['https://www.vivino.com/de-deinhard-mosel-saal-ruwer-piesporter-goldtropfchen-riesling/w/2408352']
    
    list4 = ['https://www.vivino.com/zenato-ripassa-valpolicella-ripasso-superiore/w/1380075?year=U.V.',
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
        'https://www.vivino.com/tinhorn-creek-vineyards-pinot-gris/w/85252?year=U.V.' ]

    for i in range(0,len(list4)):
        scrape_this_page(list4[i]).to_csv("ratings3000.csv", mode="a", sep=",",header=False)
    
    #print(scrape_this_page('https://www.vivino.com/kim-crawford-sauvignon-blanc/w/66534?ref=nav-search'))
    
    '''
    list1 = ['https://www.vivino.com/kim-crawford-sauvignon-blanc/w/66534?ref=nav-search',
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
    'https://www.vivino.com/torres-vina-esmeralda/w/2628']

    list2 = ['https://www.vivino.com/ruffino-chianti/w/2186',
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
    'https://www.vivino.com/beringer-vineyards-main-vine-white-zinfandel-california/w/5443473']

    list3 = ['https://www.vivino.com/sawmill-creek-sauvignon-blanc/w/1174142',
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
    'https://www.vivino.com/jacob-s-creek-chardonnay/w/2706']

    list4 = ['https://www.vivino.com/joseph-drouhin-beaujolais-villages/w/24062',
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
    'https://www.vivino.com/oyster-bay-chardonnay/w/9528']

    list5 = ['https://www.vivino.com/hess-select-cabernet-sauvignon/w/1639306',
    'https://www.vivino.com/two-oceans-sauvignon-blanc/w/62804',
    'https://www.vivino.com/trapiche-oak-cask-malbec/w/1135810',
    'https://www.vivino.com/louis-moreau-chablis/w/779318',
    'https://www.vivino.com/fetzer-vineyards-gewurztraminer/w/6678000',
    'https://www.vivino.com/la-crema-sonoma-coast-chardonnay/w/9103',
    'https://www.vivino.com/kendall-jackson-vintner-s-reserve-chardonnay/w/2132',
    'https://www.vivino.com/kendall-jackson-vintner-s-reserve-sauvignon-blanc/w/1399107',
    'https://www.vivino.com/anna-spinato-prosecco-organic/w/1983803']

    list6 = ['https://www.vivino.com/louis-bernard-cotes-du-rhone-villages/w/75920',
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
        'https://www.vivino.com/pelee-island-winery-merlot-cc77e/w/1676659']

    list7 = ['https://www.vivino.com/zenato-ripassa-valpolicella-ripasso-superiore/w/1380075?year=U.V.',
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
        'https://www.vivino.com/tinhorn-creek-vineyards-pinot-gris/w/85252?year=U.V.' ]'''


#user name, wine name, time stamp 
#1. feedback matrix (to figure out ?s) 
#2. collaborative filltering (user-user similarity, item-item similarity) 
#model 1: classifier:  accuracy
#model 2: regression binary target (0,1) threshold, then ?=probability accuracy = accuracy 
#split the data into training 70, testing 30 by time stamp by user
# Dec 23rd - Jan 1st