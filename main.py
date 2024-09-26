### author : Igor

import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import xlwt
import imghdr
import re
import os

def clean_filename(filename):
    pattern = r'[^A-Za-z0-9 ]'
    cleaned_filename = re.sub(pattern, '', filename)
    return cleaned_filename

def scrape_store(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the script tag with the specified type and id
    script_tag = soup.find('script', type='application/json', id='__REACT_QUERY_STATE__')

    titleData = ["Store page link", "Product item page link", "Store_name", "Category", "Product_description", "Product Name", "Weight/Quantity", "Units/Counts", "Price", "image_file_names", "Image_Link", "Store Rating", "Store Review number", "Product Rating", "Product Review number"]
    widths = [150,150,60,45,70,35,25,25,20,130,130,30,30,30,30]
    result = []

    style = xlwt.easyxf('font: bold 1; align: horiz center')

    if script_tag:
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
        
        # store_rating, store_review_number
        try:
            store_rating = json_data["queries"][0]["state"]["data"]["rating"]["ratingValue"]
            store_review_number = json_data["queries"][0]["state"]["data"]["rating"]["reviewCount"]
        except:
            store_rating = ""
            store_review_number = ""
        
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
                            responseImage = requests.get(image_url)
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
        
    
        
    