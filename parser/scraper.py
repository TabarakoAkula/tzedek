import requests
import json
import re
from bs4 import BeautifulSoup
from formatter import PageDataCollector


BASE_LINK = "https://www.kolzchut.org.il"

ap_continue = ""
pages_number = 1

pages = []


def get_all_pages():
    global ap_continue, pages_number

    if not ap_continue:
        link = (
            BASE_LINK + "/w/api.php?action=query&list=allpages&aplimit=max&format=json"
        )
        response = requests.get(link)
        data = response.json()
        ap_continue = data["continue"]["apcontinue"]
        with open(f"data/pages/page_{pages_number}.json", "w", encoding="utf-8") as f:
            json.dump(data["query"]["allpages"], f)
    else:
        link = (
            BASE_LINK
            + f"/w/api.php?action=query&list=allpages&aplimit=max&format=json&apcontinue={ap_continue}"
        )
        response = requests.get(link)
        data = response.json()
        ap_continue = data["continue"]["apcontinue"]
        with open(f"data/pages/page_{pages_number}.json", "w", encoding="utf-8") as f:
            json.dump(data["query"]["allpages"], f)
    print(ap_continue)
    pages_number += 1


def format_pages():
    for page_number in range(1, 22):
        with open(
            f"data/pages/page_{page_number}.json",
            "r",
            encoding="utf-8",
        ) as f:
            data = json.load(f)
            data = data["query"]["allpages"]

        with open(
            file=f"data/pages/clear_pages/page_{page_number}.json",
            mode="w",
            encoding="utf-8",
        ) as f:
            json.dump(data, f)


def all_pages_one_file():
    global pages
    for page_number in range(1, 22):
        with open(
            file=f"data/pages/clear_pages/page_{page_number}.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            data = json.load(f)
            pages.append(data)
    new_pages = []
    for i in pages:
        for j in i:
            new_pages.append(j)
    with open("data/pages/all_pages.json", "w", encoding="utf-8") as f:
        json.dump(new_pages, f)


def get_pages_content():
    with open(
        file=f"data/pages/all_pages.json",
        mode="r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)
        for page in data[:5]:
            page_id = page["pageid"]
            page_link = f"https://www.kolzchut.org.il/w/index.php?curid={page_id}"
            page_content_link = (
                BASE_LINK
                + f"/w/api.php?action=query&pageids={page_id}&prop=revisions&rvprop=content&format=json"
            )
            response_data = requests.get(page_content_link).json()
            data_pages = response_data["query"]["pages"]
            page_content = data_pages[str(page_id)]["revisions"][0]["*"]
            with open(
                file=f"data/pages_content/page_{page_id}.json",
                mode="w",
                encoding="utf-8",
            ) as f:
                result = {
                    "page_id": page_id,
                    "page_link": page_link,
                    "page_content": page_content,
                }
                json.dump(result, f)


def all_pages_with_uid():
    counter = 0
    new_data = []
    with open(f"data/pages/all_pages.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for page_data in data:
            counter += 1

            if counter < 7999:
                continue

            if counter % 100 == 0:
                print(new_data)

            page_id = page_data["pageid"]

            response = requests.get(
                f"https://www.kolzchut.org.il/w/he/index.php?curid={page_id}"
            )
            soup = BeautifulSoup(response.text, "html.parser")

            page_title = soup.title.string

            new_page_data = {
                "pageid": page_id,
                "title": page_data["title"],
                "page_title": page_title,
            }
            new_data.append(new_page_data)
            print(str(counter), "Finish №" + str(page_id))
    print("FINISH")
    print(new_data)
    with open("data/pages/all_pages_title.json", "w", encoding="utf-8") as f:
        json.dump(new_data, f)


def find_collisions():
    titles = []
    result = []
    counter = 0
    with open(
        file=f"data/pages/all_pages_title/all_pages_title.json",
        mode="r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)
        for i in data:
            if i["page_title"] in titles:
                counter += 1
            else:
                result.append(
                    {
                        "pageid": i["pageid"],
                        "title": i["title"],
                    }
                )
                titles.append(i["page_title"])
        print(counter)
    with open(
        file="data/pages/all_pages_title/all_pages_title_clear.json",
        mode="w",
        encoding="utf-8",
    ) as f:
        json.dump(result, f)


def convert_to_files():
    with open(f"data/green_links.json", "r", encoding="utf-8") as f:
        links = json.load(f)["links"]
        for link in links:
            page_id = link[(link.find("=")) + 1 :]
            collector = PageDataCollector(page_id=page_id)
            page_info = collector.analyze_page()

            with open(f"pages_data/page_{page_id}.txt", "w", encoding="utf-8") as f:
                f.writelines(page_info)


def get_all():
    with open(f"data/all_pages_title_clear.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for i in data:
            print("https://www.kolzchut.org.il/w/index.php?curid=" + str(i["pageid"]))
