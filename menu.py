
import requests
import sys
import json

# 5-C6TATK5WT3NWJA
def fetch_menu(merchant_id: str):
    url: str = f"https://portal.grab.com/foodweb/v2/merchants/{merchant_id}"   
    res: requests.Response = requests.get(url=url)
    if not res.status_code in range(200,299):
        print("Request err")
        sys.exit(1)
    return res.json()["merchant"]["menu"]

def export_menu_for_ot(menu: any):
    for category in menu["categories"]:
        print(category["name"])
    

if __name__ == "__main__":
    print("Start fetch menu of merchant Grab food")
    merchant_id: str = input("Please input merchant ID: ")
    menu: any = fetch_menu(merchant_id=merchant_id)
    org_code: str = input("Please input org code: ")
    if org_code == "ot":
        export_menu_for_ot(menu=menu)
    # define new ot