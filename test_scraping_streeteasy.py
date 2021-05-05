from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

streeteasy_url = 'https://streeteasy.com/2-bedroom-apartments-for-sale/murray-hill/price:-2000000'

req = Request(streeteasy_url, headers={'User-Agent': 'Chrome/90.0.4430.93'})
make_request = urlopen(req)
read_html = make_request.read()

html_soup = BeautifulSoup(read_html, 'html.parser')

apts_for_sale = html_soup.find_all('li', class_='searchCardList--listItem')

filename = 'test_scrape_streeteasy.csv'
f = open(filename, 'w')

headers = 'Title, Address, Price \n'
f.write(headers)

for listing in apts_for_sale:
    title = listing.find('p', class_='listingCardLabel-grey').text
    address = listing.find('address', class_='listingCard-addressLabel').text
    pricelist = listing.find('span', class_='price').text.strip('$').split(',')
    price = ''.join(pricelist)

    f.write(title + ',' + address + ',' + price + ',')

f.close()