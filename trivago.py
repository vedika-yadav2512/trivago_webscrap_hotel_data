import time
import calendar
import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

options = Options()
# options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-cookies')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

########## en-IN/osr - It redirect to the form page #######
driver.get('https://www.trivago.in/en-IN/osr')

destination = 'Delhi'
input_loc = driver.find_element(By.ID, 'input-auto-complete').send_keys(destination)
time.sleep(2)

suggestion_select = driver.find_element(By.ID, 'suggestion-list').find_elements(By.CLASS_NAME, 'cursor-pointer')[
    0].click()
time.sleep(2)

start_date = '15-06-2023'
end_date = '30-06-2023'
print(start_date, end_date)


def calender(start, end):
    ############## START DATE ############
    day_start = start_date.split('-')[0]
    month_start = start_date.split('-')[1]
    year_start = start_date.split('-')[2]

    ############### END DATE ##########
    day_end = end_date.split('-')[0]
    month_end = end_date.split('-')[1]
    year_end = end_date.split('-')[2]

    check_in_month = \
    driver.find_element(By.CSS_SELECTOR, 'div[data-testid="calendar-popover"]').find_elements(By.TAG_NAME, 'h3')[1].text
    check_out_month = \
    driver.find_element(By.CSS_SELECTOR, 'div[data-testid="calendar-popover"]').find_elements(By.TAG_NAME, 'h3')[2].text
    print("check in month ::::", check_in_month.split(' ')[0], ",", "year::", check_in_month.split(' ')[1])
    print("check out month ::::", check_out_month.split(' ')[0], ",", "year::", check_out_month.split(' ')[1])

    months_calender = list(calendar.month_name)[1:]
    print(months_calender)
    month_start = str(months_calender[int(month_start) - 1])
    month_end = str(months_calender[int(month_end) - 1])
    format_string = "%d-%m-%Y"
    print("Start date :::", start_date)
    print("End date :::", end_date)
    # Convert the string to a datetime object
    date1 = datetime.datetime.strptime(start_date, format_string)
    date2 = datetime.datetime.strptime(end_date, format_string)

    difference_in_year = int(str(date2).split('-')[0]) - int(str(date1).split('-')[0])

    ### check in date code ##########
    if int(difference_in_year) < 1:
        if str(year_start) == str(check_in_month.split(' ')[1]):
            for month in range(0, 4):

                if str(check_in_month.split(' ')[0]).lower() == str(month_start).lower():
                    time.sleep(2)
                    tb = driver.find_element(By.CSS_SELECTOR,
                                             'div[class="grid grid-cols-7 gap-y-1 CalendarMonth_scrollWrapper__wErGe px-5 pt-2"]')

                    for td in tb.find_elements(By.TAG_NAME, 'button'):
                        if str(td.text) == str(day_start):
                            td.click()
                            print('clicked check in')

                            break
                    break
                try:
                    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="calendar-button-next"]').click()
                except:
                    print('Not found')

            driver.find_element(By.CSS_SELECTOR, 'button[data-testid="calendar-button-next"]').send_keys(Keys.ESCAPE)

            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, 'button[data-testid="search-form-calendar-checkout"]').click()

            ########### check out date ############
            print('-------------------')
            print(check_out_month.split(' ')[0])
            print(month_end)
            print('------------------')
            if str(check_out_month.split(' ')[0]).lower() == str(month_end).lower():
                tb1 = driver.find_element(By.CSS_SELECTOR,
                                          'div[class="grid grid-cols-7 gap-y-1 CalendarMonth_scrollWrapper__wErGe px-5 pt-2"]')

                for td1 in tb1.find_elements(By.TAG_NAME, 'button'):
                    if str(td1.text) == str(day_end):
                        td1.click()
                        print('clicked check out')
                        break


print(calender(start_date, end_date))

time.sleep(3)

submit = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="search-button"]').click()


time.sleep(40)
try:
    submit = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="search-button"]').click()
except:
    print('er')
time.sleep(3)

Data = []
ol = driver.find_element(By.TAG_NAME, 'ol')
for li in ol.find_elements(By.TAG_NAME, 'li'):
    try:
        title = li.find_element(By.TAG_NAME, 'h2').text
        distance = li.find_element(By.CSS_SELECTOR, 'button[data-testid="distance-label-section"]').text
        rating = li.find_element(By.CSS_SELECTOR, 'button[data-testid="rating-section"]').text
        price_booking = li.find_element(By.CSS_SELECTOR, 'span[data-testid="price-label"]').text
        pricelow = li.find_element(By.CSS_SELECTOR, 'span[data-testid="cheapest-price-label"]').text
        img = li.find_element(By.CSS_SELECTOR, 'img[data-testid="accommodation-main-image"]').get_attribute('src')
        Data.append((start_date, end_date, destination, title, distance, rating, price_booking, pricelow, img))
    except:
        print('err')

import pandas as pd

df = pd.DataFrame(Data,
                  columns=['checkin_date', 'checkout_date', 'Destination', 'Title', 'Distance', 'Rating', 'Price_book',
                           'Price_low', 'Image'])
df.to_csv('Trivago.csv')


