# Car data mini-project
I want to get some data on cars for sale, to see if I can make an informed decision on which car to buy. I have an idea that the Citroën C4 would be a good fit, as it is economical, reasonably priced, can be equipped with a tow hook and more. To get an idea of the market, I set out to scrape Bilbasen.dk, one of the major online used-car dealing sites, to see if I can learn something about the market.

## Data scraping with Python and Selenium

I used Python for the data scraping. The script is available to look at in the file `C4scraping.py`, and the resulting dataset is available to look at in the CSV file `bilbasen_scrape.csv`.

### Starting a driver for scraping
I use the **[Selenium](https://www.selenium.dev)** package for scraping. I choose to use Brave Browser, which is a privacy oriented browser based on Chromium, which is supported by Selenium. I configure the selenium.options(), such that it has the location of Brave on my PC. I have made an initial query on the website with a few filters to get started, such that the URL I provide goes directly to the results of that query.  
## Handling pop-up message
As for any website nowadays, you have to accept some level of cookies. The driver needs to handle this as well. The pop-up message is a seperate iframe from the main site, so I switch into that frame, find the "Only Necessary" button by inspection of the HTML, and commands the driver to click the button. Finally, we switch back to the main sites iframe.


![Cookie window](graphics/cookie-window.png)
### Getting advert details
The website contains a number of cards, each card being an advert for a car on sale. The card has the data we are looking for for now. More information could be scraped by clicking and opening each advert, but for this project, I leave additional data out.

The scraper searches through the HTML, as can be seen by inspecting an element on the website. A card is found by looking for class name "Listing_listing_XwaYe", of which there are several, one for each card/advert. The data can be extracted as one string with `element.text`, and seperated by splitting where there is a `'\n'` character.


![Car advert and corresponding HTML](graphics/HTML_car_card.png)

### Saving data in csv file
The scraping ends up with me having a list of dictionaries, each one having the data of an advert. Bilbasen returned 62 cars on my initial query, why I have a list of length 62. I use **Pandas** to export the list to a CSV file, which I will use for data analysis later on.

## Power BI
I'm still very early in my Power BI adventures, but I loaded the csv file into Power BI to do some transformations, visualizations and reporting, and this is what came out:

![Power BI Report](graphics/PBI_CitroenC4-1.png)

Several factors affects the cost of owning a car, most notably its fuel consumption and annual tax (grøn ejerafgift). The annual tax is determined on basis of the fuel economy of the vehicle. To add complexity, cars registered after 3/10/17 will have a different set of tax brackets. In general cars from before this date are cheaper in tax, as technology has progressed and what was once a very economical car is now a moderately economical car, and the tax levels follow. By quick research, insurance (not included in data set) does not seem to change much, unless you choose to buy the newest edition of the C4 with the BlueHDi 1.5 engine.

The C4 has been sold for many years, and as such, many engine configurations across 
gas (benzin) and diesel has been offered. A diagram shows the maximum fuel efficiency a particular engine has been listed with. There can be variation across models with the same engine, so one would have to refer to the individual advert, but the data shows the general trend.

From the dataset we can also see what the minimum amount is to enter the market based on the asking price of cars with particular engine configurations. The 100 horsepower BlueHDi is the cheapest, leaving out the e-HDi 115, which is the predecessor to the BlueHDi generation of engines. As such, it is found only in older cars.

Lastly, the trendlines of the scatterplot suggest that the BlueHDi will hold its value better. Using a linear fit for this is however questionable, but it is the only fit currently offered in Power BI. See MATLAB analysis for more on this.

From these insights, I would recommend a car with the BlueHDi 100 from before 3/10/2017, if economy is the prime objective in this purchase.

## MATLAB analysis
This is under development. I plan to do some model fitting in MATLAB, as Power BI currently only supports linear fits, and preliminary analysis shows that an exponential fit of **price** as a dependent variable on independent variables **kms driven** and **age** shows good fit.