def scrape_URLs(cards):
    URLs = []
    for card in cards:
        element = card.find_element(By.CLASS_NAME, 'Listing_link__6Z504')
        url = element.get_attribute('href')
        URLs.append(url)
    return URLs

def get_next_page_button(driver):
    # Get the next page button
    next_page_button = driver.find_element(By.CSS_SELECTOR, "a[data-e2e='pagination-next']")
    return next_page_button

def scrape_car(URL):

    driver.get(URL)

    time.sleep(1)

    # Find and click the "Show all details" button
    try:
        driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[3]/div[2]/div[2]/article/main/div[7]/div/button').click()
    except:
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[3]/div[2]/div[2]/article/main/div[6]/div/button').click()
            driver.find_element(By.XPATH, '// *[ @ id = "root"] / div[2] / div[3] / div[2] / div[2] / article / main / div[6] / div / button[1]').click()
            driver.find_element(By.XPATH,'// *[ @ id = "root"] / div[2] / div[3] / div[2] / div[2] / article / main / div[6] / div / button').click()
        except:
            print("Button 'Vis alle detaljer' not found.")


    content = driver.find_elements(By.CLASS_NAME, "bas-MuiVipPageComponent-main")

    if len(content) == 0:
        return {}

    #car info is seperated by '\n' character
    details = re.findall('.*\n', content[0].text)
    details = [detail.strip('\n') for detail in details]

    # Dictionary for current car
    car = {}

    try:

        try:
            make = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[3]/div[2]/div[2]/div[5]/div[1]/nav/ol/li[1]/a').text
        except:
            try:
                make = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[3]/div[2]/div[2]/div[4]/div[1]/nav/ol/li[1]/a')
                make = make.text
            except:
                make = None

        try:
            model = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[3]/div[2]/div[2]/div[5]/div[1]/nav/ol/li[3]/a').text
        except:
            try:
                model = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[3]/div[2]/div[2]/div[4]/div[1]/nav/ol/li[3]/a')
                model = model.text
            except:
                model = None
        try:
            configuration = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[3]/div[2]/div[2]/div[5]/div[1]/nav/ol/li[5]/a').text
        except:
            try:
                configuration = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[3]/div[2]/div[2]/div[4]/div[1]/nav/ol/li[5]/a')
                configuration = configuration.text
            except:
                configuration = None

        rating = details[3]
        try:
            price = details[details.index("Kontantpris") + 1]
        except:
            try:
                price = details[details.index("Kontantpris(Sælges for kunde)") + 1]
            except:
                pass

        registered = details[details.index("1. registrering") + 1]
        kilometers = details[details.index("Kilometertal") + 1]
        fuel = details[details.index("Drivmiddel") + 1]
        consumption = details[details.index("Brændstofforbrug") + 1]
        try:
            range = details[details.index("Rækkevidde") + 1]
            battery = details[details.index("Batterikapacitet") + 1]
            electric_consumption = details[details.index("Energiforbrug") + 1]
            car["Range"] = range
            car["Battery"] = battery
            car["Electric Consumption"] = electric_consumption
        except:
            car["Range"] = None
            car["Battery"] = None
            car["Electric Consumption"] = None
        tax = details[details.index("Periodisk afgift") + 1]
        power = details[details.index("Ydelse") + 1]
        transmission = details[details.index("Geartype") + 1]
        tow_capacity = details[details.index("Trækvægt") + 1]
        price_new = details[details.index("Nypris") + 1]
        trunk = details[details.index("Bagagerumsstørrelse") + 1]
        width = details[details.index("Bredde") + 1]
        try:
            length = details[details.index("Længde") + 1]
            height = details[details.index("Højde") + 1]
        except:
            length = None
            height = None
    except:
        pass

    # Dictionary for current car
    car = {
        'Make': make,
        'Model': model,
        'Configuration': configuration,
        'Rating': rating,
        'Price': price,
        'Registered': registered,
        'Kilometers': kilometers,
        'Fuel': fuel,
        'Consumption': consumption,
        'Tax': tax,
        'Power': power,
        'Transmission': transmission,
        'TowCapacity': tow_capacity,
        'PriceNew': price_new,
        'Trunk': trunk,
        'Width': width,
        'Length': length,
        'Height': height
    }

    return car

def handle_cookies():
    try:
        # Switch into cookies iframe
        iframe = wait.until(
            EC.presence_of_element_located((By.ID, "sp_message_iframe_1298334"))
        )
        driver.switch_to.frame(iframe)

        # Find and click the "Accept necessary cookies" button
        accept_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Kun nødvendige")]'))
        )
        accept_button.click()

        # Switch back to main page
        driver.switch_to.default_content()
    except Exception as e:
        print("Failed at cookie handling:", e)

    time.sleep(3)

if __name__ == '__main__':
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    #from selenium.webdriver.common.devtools.v133.debugger import pause
    from selenium.webdriver.support.wait import WebDriverWait
    import pandas as pd
    import time
    import re
    import os.path

    # Script options
    create_URLs = False;

    # Use Brave browser for scraping
    scrape_options = Options()
    scrape_options.binary_location = "/snap/brave/current/opt/brave.com/brave/brave"
    scrape_service = Service(executable_path="/home/anders-eriksen/Downloads/chromedriver-linux64/chromedriver")

    # Start driver and go to website
    URL = "https://www.bilbasen.dk/brugt/bil?doors=5%2c6&greentaxto=2000&hpfrom=95&kmlfrom=25&mintow=1000&newandused=2&priceto=300000&pricetype=Retail&regfrom=2009-01&regto=2021-12"
    URLs_filepath = "/home/anders-eriksen/Documents/GitHub/data-projects/Bilbasen Project/URLs.csv"
    cars_filepath = "/home/anders-eriksen/Documents/GitHub/data-projects/Bilbasen Project/bilbasen_scrape.csv"
    driver = webdriver.Chrome(service=scrape_service, options=scrape_options)
    driver.get(URL)

    wait = WebDriverWait(driver, 15)

    # Handle the 'Accept Cookies' prompt that shows when opening the site
    handle_cookies()

    # Not all adverts are shown on one page. Getting number of pages to scrape through.
    n_pages = driver.find_element(By.CLASS_NAME, "Pagination_pagination__GywrN") # Container for the page index
    txt = n_pages.text
    i = -1;
    while 1:
        index = txt.find(" ", i+1)
        if index == -1:
            break
        else:
            i = index


    n_pages = int(txt[i+1:]) # The number of pages is the last letter in the string, cast to int for looping

    # Scraping through pages
    current_page = 0

    progression = 0;
    #Load existing data to build upon it
    if os.path.exists(cars_filepath):
        list_of_cars = pd.read_csv(cars_filepath).to_dict(orient='records')
        progression = len(list_of_cars)

    # Create list of URLs or load list from csv
    if create_URLs:
        list_of_URLs = []

        while current_page < n_pages:
            current_page = current_page + 1;
            car_cards = driver.find_elements(By.CLASS_NAME, "Listing_listing__XwaYe") # Each advert is shown as a card
            list_of_URLs.extend(scrape_URLs(car_cards)) # Scrape cars and append to list_of_cars
            get_next_page_button(driver).click() # Click to get next page

        df = pd.DataFrame(list_of_URLs)
        df.to_csv(URLs_filepath, index=False)
    else:
        list_of_URLs = pd.read_csv(URLs_filepath)
        column_header = list_of_URLs.columns.values[0]
        list_of_URLs = list_of_URLs[column_header].tolist()
        n_cars = len(list_of_URLs);
        list_of_URLs = list_of_URLs[progression:n_cars]


    for url in list_of_URLs:
        list_of_cars.append(scrape_car(url))
        progression += 1
        print("Progression: ", progression, "/", n_cars)

        if progression % 10 == 0:
            df = pd.DataFrame(list_of_cars)
            df.to_csv(cars_filepath, index=False)

    # After looping, load list of cars into a dataframe
    df = pd.DataFrame(list_of_cars)

    # Save to CSV
    df.to_csv(cars_filepath, index=False)

    print("Saved to bilbasen_scrape.csv!")