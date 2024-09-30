### author : Igor

import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import xlwt
import imghdr
import re
import os
from datetime import datetime
from urllib.parse import urlparse
import uuid

def clean_filename(filename):
    pattern = r'[^A-Za-z0-9 ]'
    cleaned_filename = re.sub(pattern, '', filename)
    return cleaned_filename

store_urls = []

if(os.path.isfile("stores.txt")):
    with open('stores.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            cleaned_text = re.sub(r'\n', '', line)
            store_urls.append(cleaned_text)

if(not os.path.isdir("resources")):
    os.mkdir("resources")
    
# store_urls = []
# for i in range(0,1):
#     new_url = input("Enter the new url of Uber Eats Store: ")
#     store_urls.append(new_url)

now = datetime.now()
current_time = now.strftime("%m-%d-%Y-%H-%M-%S")
os.mkdir("resources/"+current_time)

for url in store_urls:
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the script tag with the specified type and id
    script_tag = soup.find('script', type='application/json', id='__REACT_QUERY_STATE__')

    titleData = ["Store page link", "Product item page link", "Store_name", "Category", "Product_description", "Product Name", "Weight/Quantity", "Units/Counts", "Price", "image_file_names", "Image_Link", "Store Rating", "Store Review number", "Product Rating", "Product Review number", "Address", "Phone number", "Latitude", "Longitude", "Description Detail"]
    widths = [150,150,60,45,70,35,25,25,20,130,130,30,30,30,30,60,50,60,60,80]
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
            
            store_rating = ""
            store_review_number = ""
            address = ""
            phone_number = ""
            latitude = ""
            longitude = ""
            parsed_url = urlparse(url)
            detail = ""
            
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
                phone_number = json_data["queries"][0]["state"]["data"]["phoneNumber"]
            except:
                phone_number = ""
                
            try:
                latitude = json_data["queries"][0]["state"]["data"]["location"]["latitude"]
            except:
                latitude = ""
                
            try:
                longitude = json_data["queries"][0]["state"]["data"]["location"]["longitude"]
            except:
                longitude = ""
                
            dir_path = 'resources/'+current_time+"/"+cleaned_store
            if(not os.path.isdir(dir_path)):
                os.mkdir(dir_path)
                os.mkdir(dir_path+"/images")
                
            with open('resources/'+current_time+"/"+cleaned_store+"/"+store_title+".json", 'w', encoding='utf-8') as file:
                json.dump(json_data, file, indent=4)
            
            for key, menu in metaData.items():
                for catalog in menu:
                    itemData = catalog["payload"]["standardItemsPayload"]
                    
                    for item in itemData["catalogItems"]:
                        image_url = item.get('imageUrl', "")
                        new_uuid = uuid.uuid4()
                        modctx = {
                            "storeUuid":json_data["queries"][0]["state"]["data"]["uuid"],
                            "sectionUuid":item["sectionUuid"],
                            "subsectionUuid":item["subsectionUuid"],
                            "itemUuid":item["uuid"],
                            "showSeeDetailsCTA":True
                        }
                        product_page = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "/" + item["sectionUuid"] + "/data/" + item["uuid"]
                        
                        try:
                            responseDetail = requests.get(product_page, headers=headers)
                            if responseDetail.status_code == 200:
                                soupDetail = BeautifulSoup(responseDetail.content, 'html.parser')
                                detail = soupDetail.find('p', {'aria-hidden': 'true'}).get_text()
                        except Exception as e:
                            detail = ""
                        
                        item_url = url + "&mod=quickView&modctx="+urllib.parse.quote(json.dumps(modctx))
                        file_url = ""
                        description = item.get('itemDescription', "")
                        weData = ""
                        unData = ""
                        rating = ""
                        review_number = ""
                        
                        
                        if(not description):
                            try:
                                description = item["itemThumbnailElements"][1]["payload"]["labelPayload"]["label"]["accessibilityText"]
                            except:
                                description = ""
                        
                        
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
                                    file_url = dir_path+"/images/"+str(new_uuid)+'.'+image_type
                                    with open(file_url, 'wb') as file:
                                        file.write(responseImage.content)
                            except Exception as e:
                                print(e)
                        
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
                            product_page,
                            store_title, # title
                            itemData.get("title", {"text":""})["text"],
                            description,
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
                            phone_number,
                            latitude,
                            longitude,
                            detail
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
            workbook.save('resources/'+current_time+"/"+cleaned_store+ "/" + store_title + ".xls")
        except Exception as error:
            print(error)
        
    
        
    