import requests
from bs4 import BeautifulSoup
import re


def find_facts():
    url = "https://www.onthisday.com/"  # "https://www.onthisday.com/"
    response = requests.get(url)

    list_of_fact = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        events = soup.find_all("li", class_="event")
        for i, event in enumerate(events):
            date_element = event.find("a", class_="date")
            if date_element:
                date = date_element.text.strip()
                text_elements = [
                    element
                    for element in event.contents
                    if element.name != "div"
                    or "event-photo" not in element.get("class", [])
                ]
                text = " ".join(
                    element.get_text(strip=True)
                    for element in text_elements
                    if element != date_element
                )
                text = re.sub(r"^\s+", "", text)
                text = re.sub(r"\s+([,\.])", r"\1", text)

                event_dict = {"date": date, "text": text}
                list_of_fact.append(event_dict)

    else:
        print(f"Failed to retrieve the page. Status code: \
              {response.status_code}")
        list_of_fact = None

    return list_of_fact
