def handle_cookies():
    try:
        # Switch into cookies iframe
        iframe = wait.until(
            EC.presence_of_element_located((By.ID, "sp_message_iframe_1274315"))
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

def get_next_page_button(driver):
    # Get the next page button
    next_page_button = driver.find_element(By.CSS_SELECTOR, "a[data-e2e='pagination-next']")
    return next_page_button

def scrape_cards(car_cards):
    # list to store cars info
    cars = []
    for card in car_cards:
        # car info is seperated by '\n' character
        details = re.findall('.*\n', card.text)

        # get rid of '\n' character
        details = [detail.strip('\n') for detail in details]

        # Some adverts had an additional field because they were added recently
        if details[0] == 'Ny annonce':
            details.pop(0)  # remove that field

        if len(details) == 8:  # Expecting 8 pieces of information
            make = details[0]
            config = details[1]
            price = details[2].strip(' kr.').replace('.', '')
            year = details[3]
            km = details[4].strip(' km').replace('.', '')
            fuel_consumption = details[5].strip(' km/l').replace(',', '.')
            transmission = details[6]
            fuel_type = details[7]

            # Dictionary for the current car
            car = {
                'Make': make,
                'Configuration': config,
                'Price (DKK)': price,
                'Year': year,
                'Kilometers': km,
                'Fuel Consumption (km/l)': fuel_consumption,
                'Transmission': transmission,
                'Fuel Type': fuel_type
            }

            # Appendind current car to the list 'cars'
            cars.append(car)

    return cars

if __name__ == '__main__':
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.devtools.v133.debugger import pause
    from selenium.webdriver.support.wait import WebDriverWait
    import pandas as pd
    import time
    import re

    # Use Brave browser for scraping
    scrape_options = Options()
    scrape_options.binary_location = "/snap/brave/current/opt/brave.com/brave/brave"
    scrape_service = Service(executable_path="/home/anders-eriksen/Downloads/chromedriver-linux64/chromedriver")

    # Start driver and go to website
    URL = "https://www.bilbasen.dk/brugt/bil/citro%C3%ABn/c4?pricetype=Retail&removabletowbar&swingawaytowbar&swingawaytowbarelectric&towbar"
    driver = webdriver.Chrome(service=scrape_service, options=scrape_options)
    driver.get(URL)

    wait = WebDriverWait(driver, 15)

    # Handle the 'Accept Cookies' prompt that shows when opening the site
    handle_cookies()

    # Not all adverts are shown on one page. Getting number of pages to scrape through.
    n_pages = driver.find_element(By.CLASS_NAME, "Pagination_pagination__GywrN") # Container for the page index
    n_pages = int(n_pages.text[-1]) # The number of pages is the last letter in the string, cast to int for looping

    # Scraping through pages
    current_page = 0
    list_of_cars = []

    while current_page < n_pages:
        current_page = current_page + 1;
        car_cards = driver.find_elements(By.CLASS_NAME, "Listing_listing__XwaYe") # Each advert is shown as a card
        list_of_cars.extend(scrape_cards(car_cards)) # Scrape cars and append to list_of_cars
        get_next_page_button(driver).click() # Click to get next page

    # After looping, load list of cars into a dataframe
    df = pd.DataFrame(list_of_cars)

    # Save to CSV
    df.to_csv('/home/anders-eriksen/Documents/GitHub/data-projects/citroen-c4-project/bilbasen_scrape.csv', index=False)

    print("Saved to bilbasen_scrape.csv!")


