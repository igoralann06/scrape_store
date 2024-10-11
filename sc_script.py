import requests
import json
import xlwt
from bs4 import BeautifulSoup
import urllib.parse
import time

root_url = "https://ubereats.com"
hasMore = True
url = "https://www.ubereats.com/_p/api/getFeedV1"
offset = 0
store_urls = []
result = []
section_id = 1
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,ar;q=0.8,ko;q=0.7",
    "cache-control": "no-cache",
    "content-length": "709",
    "content-type": "application/json",
    "cookie":
    'uev2.id.xp=413406bd-84a3-4835-b96a-737addf5f39c; dId=98b24b9c-4cd6-43e1-a856-24d0b60bbc7f; uev2.id.session=26f8a4cc-786d-481b-8e4e-bb0d8ae400cc; uev2.ts.session=1728338883406; uev2.diningMode=DELIVERY; uev2.loc=%7B%22address%22%3A%7B%22address1%22%3A%2213659%20SW%20159th%20Ave%22%2C%22address2%22%3A%22Miami%2C%20FL%22%2C%22aptOrSuite%22%3A%22%22%2C%22eaterFormattedAddress%22%3A%2213659%20SW%20159th%20Ave%2C%20Miami%2C%20FL%2033196-1829%2C%20US%22%2C%22subtitle%22%3A%22Miami%2C%20FL%22%2C%22title%22%3A%2213659%20SW%20159th%20Ave%22%2C%22uuid%22%3A%22%22%7D%2C%22latitude%22%3A25.638959%2C%22longitude%22%3A-80.451453%2C%22reference%22%3A%22890a8d95-2587-5bd4-1d8d-7a3a97ad027a%22%2C%22referenceType%22%3A%22uber_places%22%2C%22type%22%3A%22uber_places%22%2C%22addressComponents%22%3A%7B%22city%22%3A%22Miami%22%2C%22countryCode%22%3A%22US%22%2C%22firstLevelSubdivisionCode%22%3A%22FL%22%2C%22postalCode%22%3A%2233196-1829%22%7D%2C%22categories%22%3A%5B%22street_address%22%2C%22LANDMARK%22%2C%22RESIDENCE%22%2C%22AREAS_AND_BUILDINGS%22%5D%2C%22originType%22%3A%22user_autocomplete%22%2C%22source%22%3A%22rev_geo_reference%22%2C%22userState%22%3A%22Unknown%22%7D; _ua={"session_id":"d6df1dc6-111f-44b0-8631-fd7841c0580c","session_time_ms":1728338883538}; marketing_vistor_id=1d327665-c4d7-4ae4-9660-3ccc17c9828f; jwt-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNsYXRlLWV4cGlyZXMtYXQiOjE3MjgzNDA2ODM1Mzd9LCJpYXQiOjE3MjgzMzg4ODMsImV4cCI6MTcyODQyNTI4M30.foe5X4nKXdOfDXSZdaFpvea5b77TDJBr0StPfC8-cJ8; uev2.gg=true; utag_main__sn=1; utag_main_ses_id=1728338903298%3Bexp-session; utm_medium=undefined; fm_conversion_id=undefined; utm_source=undefined; CONSENTMGR=c1:1%7Cc2:1%7Cc3:1%7Cc4:1%7Cc5:1%7Cc6:1%7Cc7:1%7Cc8:1%7Cc9:1%7Cc10:1%7Cc11:1%7Cc12:1%7Cc13:1%7Cc14:1%7Cc15:1%7Cts:1728338903307%7Cconsent:true; utag_main__ss=0%3Bexp-session; _scid=l5Qy4HN-hc-akbJllx0PwLGp_mrpsqws; _ScCbts=%5B%5D; _gid=GA1.2.1472499788.1728338912; _sctr=1%7C1728277200000; _gcl_au=1.1.880605592.1728338914; _fbp=fb.1.1728338914054.247873903790952932; _yjsu_yjad=1728338914.614d76a7-7e7d-40c6-86d3-0dbb44f87835; utag_main__pn=2%3Bexp-session; _scid_r=oBQy4HN-hc-akbJllx0PwLGp_mrpsqwsUgUcDw; _userUuid=; utag_main__se=6%3Bexp-session; utag_main__st=1728340730756%3Bexp-session; _ga=GA1.2.777607682.1728338909; _uetsid=af743f5084f811ef8a1e7b552fb25cd0; _uetvid=af74592084f811ef9d8b7bd94414eafe; _tt_enable_cookie=1; _ttp=s2bm_LQvW-iMaDVVhwCbn4NF69L; _clck=l1of1z%7C2%7Cfpt%7C0%7C1741; _ga_P1RM71MPFP=GS1.1.1728338909.1.1.1728339839.60.0.0',
    "origin": "https://www.ubereats.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer":
    "https://www.ubereats.com/feed?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMjEzNjU5JTIwU1clMjAxNTl0aCUyMEF2ZSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMjg5MGE4ZDk1LTI1ODctNWJkNC0xZDhkLTdhM2E5N2FkMDI3YSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJ1YmVyX3BsYWNlcyUyMiUyQyUyMmxhdGl0dWRlJTIyJTNBMjUuNjM4OTU5JTJDJTIybG9uZ2l0dWRlJTIyJTNBLTgwLjQ1MTQ1MyU3RA%3D%3D",
    "sec-ch-prefers-color-scheme": "light",
    "sec-ch-ua":
    '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent":
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    "x-csrf-token": "x",
    "x-uber-client-gitref": "x"
}

while(hasMore == True):
    payload = {
        "cacheKey":
        "JTdCJTIyYWRkcmVzcyUyMiUzQSUyMjEzNjU5JTIwU1clMjAxNTl0aCUyMEF2ZSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMjg5MGE4ZDk1LTI1ODctNWJkNC0xZDhkLTdhM2E5N2FkMDI3YSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJ1YmVyX3BsYWNlcyUyMiUyQyUyMmxhdGl0dWRlJTIyJTNBMjUuNjM4OTU5JTJDJTIybG9uZ2l0dWRlJTIyJTNBLTgwLjQ1MTQ1MyU3RA==/DELIVERY///0/0//JTVCJTVE/undefined//////HOME////////",
        "feedSessionCount": {
            "announcementCount": 0,
            "announcementLabel": ""
        },
        "userQuery": "",
        "date": "",
        "startTime": 0,
        "endTime": 0,
        "carouselId": "",
        "sortAndFilters": [],
        "billboardUuid": "",
        "feedProvider": "",
        "promotionUuid": "",
        "targetingStoreTag": "",
        "venueUUID": "",
        "selectedSectionUUID": "",
        "favorites": "",
        "vertical": "",
        "searchSource": "",
        "serializedRequestContext": "",
        "pageInfo": {
            "offset": offset,
            "pageSize": 300
        },
    }

    response = requests.post(url, headers=headers, json=payload)
    store_data = response.json()
    store_array = store_data["data"]["feedItems"]

    for item in store_array:
        try:
            stores = item["carousel"]["stores"]
            for i in stores:
                store_urls.append(root_url + i["actionUrl"])        
        except:
            print("No stores")
        try:
            store = item["store"]
            store_urls.append(root_url + store["actionUrl"])        
        except:
            print("No carousel stores")
        
    hasMore = store_data["data"]["meta"]["hasMore"]
    offset = offset + 300

with requests.Session() as session:
    for store_url in store_urls:
        try:
            store_headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = session.get(store_url, headers=store_headers, timeout=10)

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the script tag with the specified type and id
            script_tag = soup.find('script', type='application/json', id='__REACT_QUERY_STATE__')

            titleData = ["id","Store URL", "Store_name", "Address", "Phone_number", "Rating", "Rating Count", "Categories"]
            widths = [30,150,80,80,50,30,30,100]

            style = xlwt.easyxf('font: bold 1; align: horiz center')
            
            if script_tag:
                script_content = script_tag.string
                decoded_content = urllib.parse.unquote(script_content)
                json_string = decoded_content.replace('\\u0022', '"').replace('\\u005C', '\\').replace('\\u2019', "'")
            
                json_data = json.loads(json_string)
                store_title = json_data["queries"][0]["state"]["data"]["title"]
                
                store_rating = ""
                store_review_number = ""
                address = ""
                phone_number = ""
                categories = []
                
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
                    categories = json_data["queries"][0]["state"]["data"]["categories"]
                except:
                    categories = ""
                    
                record = [
                    str(section_id),
                    store_url,
                    store_title,
                    address,
                    phone_number,
                    store_rating,
                    store_review_number,
                    ",".join(str(category) for category in categories)
                ]
                
                print(record)
                result.append(record)
                section_id = section_id + 1
                
            response.close()
        except:
            print("Fetching data failed")
        
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
workbook.save("stores.xls")