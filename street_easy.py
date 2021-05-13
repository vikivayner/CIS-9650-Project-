def(url, headers):
    house = {"Name":[], "Address":[], "Price":[], "Bed":[],"Bath":[],"Sqft":[]}
    url_list = ["{}?page={}".format(url, str(page)) for page in range(1, 6)]
    for url in url_list:
        src = requests.get(url, headers = headers).content
        soup_exploration = BeautifulSoup(src, 'html.parser')
        street_easy_rentals = soup_exploration.find_all('li', class_="searchCardList--listItem")

        for rental in street_easy_rentals: 
            house["Name"].append(rental.find('p', class_='listingCardLabel-grey').text.strip('\n').strip())
            house["Address"].append(rental.find('address', class_='listingCard-addressLabel').text.strip('\n').strip())
            house["Price"].append(rental.find('span', class_='price listingCard-priceMargin').text)
    
  
            room = rental.find("div", class_='listingDetailDefinitions')#.text.strip('\n').strip()
            house["Bed"].append(room.contents[1].text.strip('\n').strip())
    
            house["Bath"].append(room.contents[5].text.strip('\n').strip())
    
        try:
            sqft =  re.sub('\s+',' ',room.contents[9].text)
        
        except IndexError:
            sqft = 'N/A'
    
        house["Sqft"].append(sqft)
    house_df=pd.DataFrame.from_dict(house)
return(house_df)