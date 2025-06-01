import requests
from bs4 import BeautifulSoup
import urllib.parse
import html
import re


class PageDataCollector:
    def __init__(self, page_id):
        self.url = f"https://www.kolzchut.org.il/w/he/api.php?action=parse&format=xml&pageid={page_id}&redirects=1&prop=text%7Clinks%7Cexternallinks%7Cheadhtml"
        self.page_id = page_id
        self.soup = ""
        self.first_split = []
        self.result = ""
        self.result_summary = ""
        self.result_content = ""
        self.title = ""
        self.result_sources = ""
        self.another_resources = []
        self.result_contacts_centers = ""

    def get_page(self):
        response = requests.get(self.url)
        self.soup = BeautifulSoup(html.unescape(response.text), features="xml")
        text = self.soup.find("text").get_text()
        headhtml = self.soup.find("headhtml")
        title_data = str(headhtml.find("title"))
        self.title = title_data[title_data.rfind("(") + 1 : title_data.rfind(")")]
        if "title" in self.title:
            self.title = "None"
        headhtml.decompose()
        self.first_split = [i for i in text.split("\n\n\n\n\n") if i]

    def get_summary(self):
        self.result_summary = "תקציר: "
        summary = self.first_split[0]
        summary_array = summary.split("\n\n\n\n")
        for i in summary_array:
            self.result_summary += "\n" + i + "."
        self.result_summary += "\n\n"
        if len(self.first_split) == 1:
            self.result_summary = ""

    def get_content(self):
        if len(self.first_split) == 1:
            content = self.first_split[0][13:]
        else:
            content = self.first_split[1][13:]
        if "פרטים" in content:
            content = content.replace("פרטים", "פרטים[עריכה]")
        elif "פרטי" in content:
            content = content.replace("פרטי", "פרטים[עריכה]")
        content_data = {"סָעִיף": ""}
        article_now = "סָעִיף"
        result_content = "תוכן:\n"
        roe_gam = False
        splitted = content.split("\n")
        for text_block in splitted:
            if roe_gam:
                self.another_resources.append(text_block)
                continue
            if "[עריכה]" in text_block:
                article_now = text_block.replace("[עריכה]", "")
                content_data[article_now] = ""
            else:
                if "תוכן עניינים" in text_block:
                    continue
                if "ראו גם" in text_block:
                    text_block = text_block[: text_block.find("ראו גם")]
                    roe_gam = True
                text_in_data = content_data[article_now]
                if text_block:
                    text_in_data += text_block
                    text_in_data += "\n"
                content_data[article_now] = text_in_data
        for i in content_data:
            result_content += f"{i}: {content_data[i]}\n\n"
        self.result_content = result_content

    def get_sources(self):
        another_resources = [i for i in self.another_resources if i]
        self.result_sources = "מקורות: "
        sources_started = False
        resources_array = []
        for block in range(0, len(another_resources)):
            if sources_started:
                if "[עריכה]" not in another_resources[block]:
                    resources_array.append(another_resources[block])
                continue
            if "מקורות משפטיים ורשמיים[עריכה]" in another_resources[block]:
                sources_started = True
        for source in resources_array:
            self.result_sources += f"\n{source}. "

    def get_tables(self):
        contacts_centers_table_array = self.soup.find_all("table")
        result_contacts_centers_array = []
        if contacts_centers_table_array:
            for contacts_centers_table in contacts_centers_table_array:
                try:
                    if "simple" in contacts_centers_table["class"]:
                        continue
                except KeyError:
                    pass
                rows = contacts_centers_table.find_all("tr")
                result = []
                for row in rows:
                    cells = row.find_all(["td", "th"])
                    row_data = []
                    for cell in cells:
                        link = cell.find("a")
                        if link:
                            text = link.get_text(strip=True)
                            href = link.get("href", "#")
                            if href.startswith("/he/"):
                                href = "https://www.kolzchut.org.il" + href
                            cell_data = f"{text} [{href}]"
                        else:
                            cell_data = cell.get_text(strip=True)
                        row_data.append(cell_data)
                    result.append(" | ".join(row_data))
                result_contacts_centers_array.append("\n".join(result))
            self.result_contacts_centers = "\n\n".join(result_contacts_centers_array)

    def get_links(self):
        links_soup = self.soup.find("links")
        links_array = []
        for link in links_soup.children:
            links_array.append(link.get_text())
        for link in links_array:
            text_link = f"https://www.kolzchut.org.il/he/{urllib.parse.quote(link)}"
            self.result = self.result.replace(link, f"({link})[{text_link}] ")

    def analyze_page(self):
        functions = [
            self.get_page,
            self.get_summary,
            self.get_content,
            self.get_sources,
            self.get_tables,
        ]
        # try:
        for func in functions:
            func()
        # except Exception as e:
        #     print(self.page_id, e)
        else:
            self.result = (
                "סוּג: "
                + self.title
                + "\n"
                + self.result_summary
                + self.result_content
                + self.result_sources
                + "\nשולחנות:\n"
                + self.result_contacts_centers
            )
            self.get_links()
            print(f"Success {self.page_id}")
        return self.result

    def print_result(self):
        print(self.result)


if __name__ == "__main__":
    obj = PageDataCollector(page_id=11340)
    obj.analyze_page()
    obj.print_result()
