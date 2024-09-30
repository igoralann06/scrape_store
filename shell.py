### author : Igor

import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import xlwt
import imghdr
import re
import os
import time

def clean_filename(filename):
    pattern = r'[^A-Za-z0-9 ]'
    cleaned_filename = re.sub(pattern, '', filename)
    return cleaned_filename

store_urls = [
    "https://www.ubereats.com/store/fit4u-healthy-spot/rm5TYx__UoS9jK3ezuVGyQ",
    "https://www.ubereats.com/store/cuencos/MyP7s9Y7TNSYeZtyoyTmxA",
    "https://www.ubereats.com/store/tropical-smoothie-13550-sw-120th-st-452/5NOKHNZzQ_uBBumSmx3EpQ",
    "https://www.ubereats.com/store/express-subs-%26-pasta-energy-bar/dpisAiPISEaNixGnG9cQJA",
    "https://www.ubereats.com/store/subway-14713-sw-42nd-st/_Iqb-s9vS_Cf8vzQnMF90w",
    "https://www.ubereats.com/store/ernies-acai-laguna-st/t24lYs38VFS9-bWAnUdUrg?diningMode=PICKUP",
    "https://www.ubereats.com/store/sweet-natura/oYGWxohZRvGNifhvb39hbQ?diningMode=PICKUP",
    "https://www.ubereats.com/store/walgreens-16690-sw-88th-st/K_8rOU92TZOcTIl2ysBWrQ",
    "https://www.ubereats.com/store/la-siete-cafe/od14VgtDRUytIQcMVD6KnA",
    "https://www.ubereats.com/store/the-ice-cream-shop/bnIhrvxsSuGJBH1vGlKqVA",
    "https://www.ubereats.com/store/joshs-premium-meats/juP_W7vhUrOx5rCuGe1a6Q",
    "https://www.ubereats.com/store/sabores-market-kendall/C9zkPlhGUCqozREP2bnQJA",
    "https://www.ubereats.com/store/edible-arrangements-13746-n-kendall-drive/qQ93kZxGW1q1glIo7oIJ2A",
    "https://www.ubereats.com/store/target-kendall/rOqbSmhRVgam9bWrgbK_KA",
    "https://www.ubereats.com/store/fresco-y-mas-14655-sw-104th-st/3wiGH6W9X56IQSHmJJrHXA",
    "https://www.ubereats.com/store/magic-city-perks/sTeGNdVsSbSmc8xrqzO3_w",
    "https://www.ubereats.com/store/divas-nectar-bar/9_otlnD7WoK4ivjFsUIa-A",
    "https://www.ubereats.com/store/jamba-juice-dadeland/LDH9_2sjRZqIfI0R5FxESQ",
    "https://www.ubereats.com/store/myroots-juice-bar-%26-kitchen-kendall/8b6G2s8dRiWRmtdjXqnLsg",
    "https://www.ubereats.com/store/luka-restaurant-doral/idMuaIzWRNC0Ymx4nY-44w",
    "https://www.ubereats.com/store/carne-asada/kh5dmXezXTih_5djtVkWOg",
    "https://www.ubereats.com/store/mayas-kitchen-305/2Hn7KwdVTa636iqJ3wCuVQ",
    "https://www.ubereats.com/store/fritanga-masayita-nica/2trPslpeTyGQNBkYg_asuQ",
    "https://www.ubereats.com/store/el-rinconcito-latino/8yf9E4LdRXe0LMT22U3cSg",
    "https://www.ubereats.com/store/delicias-pizzeria-cubana/sDJLDS3jQZiL81oGv4aK4w",
    "https://www.ubereats.com/store/office-depot-officemax-8950-sw-137th-avenue/IpWOrCZxXvm3ElaNzt_b6g",
    "https://www.ubereats.com/store/staples-13640-north-kendall-drive/Sw2pSJWiWlaRCbTVrOm-Jw",
    "https://www.ubereats.com/store/target-kendall/rOqbSmhRVgam9bWrgbK_KA",
    "https://www.ubereats.com/store/rinconcito-latino/KR_JgVRaQrmJgRtWj2x6jA",
    "https://www.ubereats.com/store/sprouts-farmers-market-12690-sw-88th-street/JE1PKkKDU7SGl25SA7zdSQ",
    "https://www.ubereats.com/store/lowes-9191-sw-137th-avenue/X9c62vzyU3KVLJoNcig5zw"
]

if(not os.path.isdir("resources")):
    os.mkdir("resources")
if(not os.path.isdir("json")):
    os.mkdir("json")
    
# store_urls = []
# for i in range(0,1):
#     new_url = input("Enter the new url of Uber Eats Store: ")
#     store_urls.append(new_url)

for url in store_urls:
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the script tag with the specified type and id
    script_tag = soup.find('script', type='application/json', id='__REACT_QUERY_STATE__')

    titleData = ["Store page link", "Product item page link", "Store_name", "Category", "Product_description", "Product Name", "Weight/Quantity", "Units/Counts", "Price", "image_file_names", "Image_Link", "Store Rating", "Store Review number", "Product Rating", "Product Review number", "Address", "Phone number"]
    widths = [150,150,60,45,70,35,25,25,20,130,130,30,30,30,30,60,50]
    result = []

    style = xlwt.easyxf('font: bold 1; align: horiz center')

    if script_tag:
        try:
            script_content = script_tag.string
            decoded_content = urllib.parse.unquote(script_content)
            json_string = decoded_content.replace('\\u0022', '"').replace('\\u005C', '\\').replace('\\u2019', "'")
            
            # Load the JSON string into a Python dictionary
            json_data = json.loads(json_string)
            
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(json_data, file, indent=4)
            
            metaData = json_data["queries"][0]["state"]["data"]["catalogSectionsMap"]
            store_title = json_data["queries"][0]["state"]["data"]["title"]
            cleaned_store = clean_filename(store_title)
            
            with open('json/'+store_title+".json", 'w', encoding='utf-8') as file:
                json.dump(json_data, file, indent=4)
            
            store_rating = ""
            store_review_number = ""
            address = ""
            phone_number = ""
            
            # store_rating, store_review_number
            try:
                store_rating = json_data["queries"][0]["state"]["data"]["rating"]["ratingValue"]
                store_review_number = json_data["queries"][0]["state"]["data"]["rating"]["reviewCount"]
            except:
                store_rating = ""
                store_review_number = ""
            
            try:
                address = json_data["queries"][0]["state"]["data"]["location"]["address"]
            except:
                address = ""
                
            try:
                phone_number = json_data["queries"][0]["state"]["data"]["phoneNumber"];
            except:
                phone_number = ""
                
            dir_path = 'resources/'+cleaned_store
            if(not os.path.isdir(dir_path)):
                os.mkdir(dir_path)
                os.mkdir(dir_path+"/images")
            for key, menu in metaData.items():
                for catalog in menu:
                    itemData = catalog["payload"]["standardItemsPayload"]
                    
                    for item in itemData["catalogItems"]:
                        image_url = item.get('imageUrl', "")
                        modctx = {
                            "storeUuid":json_data["queries"][0]["state"]["data"]["uuid"],
                            "sectionUuid":item["sectionUuid"],
                            "subsectionUuid":item["subsectionUuid"],
                            "itemUuid":item["uuid"],
                            "showSeeDetailsCTA":True
                        }
                        item_url = url + "&mod=quickView&modctx="+urllib.parse.quote(json.dumps(modctx))
                        file_url = ""
                        weData = ""
                        unData = ""
                        rating = ""
                        review_number = ""
                        
                        pattern = r'\((.*?)\)'
                        matches = re.findall(pattern, item["title"])
                        if(len(matches) == 1):
                            lowered_str = matches[0].lower()
                            if(lowered_str.find("per") == -1 and lowered_str.find("each") == -1):
                                weData = matches[0]
                                unData = ""
                            else:
                                weData = ""
                                unData = matches[0]
                        elif(len(matches) == 2):
                            weData = matches[0]
                            unData = matches[1]
                        
                        if(image_url):
                            try:
                                responseImage = requests.get(image_url, headers=headers)
                                image_type = imghdr.what(None, responseImage.content)
                                if responseImage.status_code == 200:
                                    cleaned_url = clean_filename(item["title"])
                                    file_url = dir_path+"/images/"+cleaned_url+'.'+image_type
                                    with open(file_url, 'wb') as file:
                                        file.write(responseImage.content)
                            except:
                                print("Downloading error occured")
                        
                        ### price
                        price = item.get("priceTagline", {"text": ""})["text"]
                        if(not price):
                            price_value = float(item.get("price"))/100.0
                            price = '$'+ str(price_value)
                        
                        # rating, review_number
                        try:
                            rating = item["catalogItemAnalyticsData"]["endorsementMetadata"]["rating"]
                            review_number = item["catalogItemAnalyticsData"]["endorsementMetadata"]["numRatings"]
                        except:
                            rating = ""
                            review_number = ""
                        
                        record = [
                            url,
                            item_url,
                            store_title, # title
                            itemData.get("title", {"text":""})["text"],
                            item.get('itemDescription', ""),
                            item["title"],
                            weData,
                            unData,
                            price,
                            file_url,
                            image_url,
                            store_rating,
                            store_review_number,
                            rating,
                            review_number,
                            address,
                            phone_number
                        ]
                        print(record)
                        result.append(record)
            
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet('Sheet1')

            for col_index, value in enumerate(titleData):
                first_col = sheet.col(col_index)
                first_col.width = 256 * widths[col_index]  # 20 characters wide
                sheet.write(0, col_index, value, style)
                
            for row_index, row in enumerate(result):
                for col_index, value in enumerate(row):
                    sheet.write(row_index+1, col_index, value)

            # Save the workbook
            workbook.save('resources/'+cleaned_store+ "/" + store_title + ".xls")
        except:
            print("Fetching error occured")
        
    
        
    