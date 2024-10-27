import requests
import xlsxwriter
import string
import itertools
from datetime import datetime

colors = [
    "#facc15",
    "#a3e635",
    "#4ade80",
    "#0891b2",
    "#2563eb",
    "#7c3aed",
    "#db2777",
    "#f43f5e",
]

clc = list(
    itertools.chain(
        string.ascii_uppercase,
        ("".join(pair) for pair in itertools.product(string.ascii_uppercase, repeat=2)),
    )
)


def sum_items(menu: any, idx: int) -> int:
    result = 0
    for i in range(0, idx):
        result = result + len(menu["categories"][i]["items"])
    return result


def fetch_menu(merchant_id: str):
    url: str = f"https://portal.grab.com/foodweb/v2/merchants/{merchant_id}"
    res: requests.Response = requests.get(url=url)
    if not res.status_code in range(200, 299):
        raise Exception("Request err")
    return res.json()["merchant"]["menu"]


# 5-C6TATK5WT3NWJA
def export_categories(categories: any):
    workbook = xlsxwriter.Workbook("export.xlsx")
    worksheet_name: str = datetime.today().strftime("%Y-%m-%d")
    worksheet = workbook.get_worksheet_by_name(worksheet_name)
    if worksheet is None:
        worksheet = workbook.add_worksheet(worksheet_name)

    for i, category in enumerate(categories):
        s_color = colors[i % (len(colors) - 1)]
        fm_category_name = workbook.add_format(
            {
                "bold": 1,
                "align": "center",
                "valign": "vcenter",
                "fg_color": s_color,
                "font_name": "Times New Roman",
                "text_wrap": 1,
            }
        )

        fm_item_name = workbook.add_format(
            {
                "bold": 1,
                "align": "center",
                "valign": "vcenter",
                "font_name": "Time New Roman",
                "text_wrap": 1,
                "font_size": 10,
            }
        )
        sum_i = sum_items(menu=menu, idx=i)

        x = clc[sum_i]
        y = clc[sum_i + len(category["items"]) - 1]

        worksheet.set_column(sum_i, sum_i + len(category["items"]) - 1, 25)
        # worksheet.set_row(0, 20)
        worksheet.set_row(1, 45)

        if x == y:
            worksheet.write(f"{x}1", category["name"], fm_category_name)
        else:
            worksheet.merge_range(f"{x}1:{y}1", category["name"], fm_category_name)

        for ioi, item in enumerate(category["items"]):
            worksheet.write(f"{clc[sum_i+ioi]}2", item["name"], fm_item_name)
    workbook.close()


if __name__ == "__main__":
    print("Start fetch menu of merchant Grab food")
    merchant_id: str = input("Please input merchant ID: ")
    menu: any = fetch_menu(merchant_id=merchant_id.strip())
    categories = []
    for _, category in enumerate(menu["categories"]):
        option: str = input(
            f"You want export category {category["name"]} to sheet (yes/no) default no: "
        )
        option = option.strip().lower()
        if option == "yes" or option == "y":
            if len(category["items"]) > 0:
                categories.append(category)
        elif option == "no" or option == "n" or option == "":
            continue
        else:
            raise Exception(f"Invalid option {option}.Please enter (yes/no)")

    export_categories(categories=categories)
