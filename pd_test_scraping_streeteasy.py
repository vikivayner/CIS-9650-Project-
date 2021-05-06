# Import required libraries
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd

# URL for Streeteasy with a search query of sales in Murray Hill, two bedrooms, less than $2,000,000 USD.
streeteasy_url = 'https://streeteasy.com/2-bedroom-apartments-for-sale/murray-hill/price:-2000000'

# Make request to webpage and read in the HTML.
req = Request(streeteasy_url, headers={'User-Agent': 'Chrome/90.0.4430.93'})
make_request = urlopen(req)
read_html = make_request.read()

html_soup = BeautifulSoup(read_html, 'html.parser')

# Each listing is stored in an unordered list and each listing card is a list item in this unordered list.
# We are grabbing each list item, li, that has the class searchCardList--listItem since those are the results of our search.

apts_for_sale = html_soup.find_all('li', class_='searchCardList--listItem')

# Iterating through each listing in apts_for_sale and grabbing the title of the listing, address, and the price.
# The title would be something along the lines of 'Condo in Murray Hill' or 'Apartment in Murray Hill.'

# Create column of indexes for dataframe.
streeteasy_df_columns = ['Title', 'Address', 'Price', 'Bedrooms', 'Bathrooms', 'Square Footage']

#Create lists to store all of the title, address, and price information
streeteasy_titles = []
streeteasy_addresses = []
streeteasy_prices = []
streeteasy_bedrooms = []
streeteasy_bathrooms = []
streeteasy_sq_footage = []

for listing in apts_for_sale:
    title = listing.find('p', class_='listingCardLabel-grey').text.strip('\n').strip()
    address = listing.find('address', class_='listingCard-addressLabel').text.strip('\n')
    pricelist = listing.find('span', class_='price').text.strip('$').split(',')
    price = ''.join(pricelist)

    # The spans that contain information on bathrooms, bedrooms, and square footage have the same class so find all spans.
    listDetailTexts = listing.find_all('span', class_='listingDetailDefinitionsText')

    streeteasy_titles.append(title)
    streeteasy_addresses.append(address)
    streeteasy_prices.append(price)
    streeteasy_bedrooms.append(listDetailTexts[0].text)
    streeteasy_bathrooms.append(listDetailTexts[1].text)
    if (len(listDetailTexts) > 2):
        sqft_of_listing = listDetailTexts[2].text.strip().split('\n')[0].split(',')
        streeteasy_sqft_value = ''.join(sqft_of_listing)
        streeteasy_sq_footage.append(streeteasy_sqft_value)
    else:
        streeteasy_sq_footage.append('NA')

streeteasy_data = [streeteasy_titles, streeteasy_addresses, streeteasy_prices, streeteasy_bedrooms, streeteasy_bathrooms, streeteasy_sq_footage]
# Create streeteasy dataframe to store our data and then save it as a csv.

streeteasy_dict ={
    streeteasy_df_columns[0]: streeteasy_titles,
    streeteasy_df_columns[1]: streeteasy_addresses,
    streeteasy_df_columns[2]: streeteasy_prices,
    streeteasy_df_columns[3]: streeteasy_bedrooms,
    streeteasy_df_columns[4]: streeteasy_bathrooms,
    streeteasy_df_columns[5]: streeteasy_sq_footage
}

streeteasy_df = pd.DataFrame(data=streeteasy_dict)

streeteasy_df


    