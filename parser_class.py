import requests
import random
import re
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint
from mongo_class import Mongo_class


class Parser_class:
    def __init__(self):
        self.agent = UserAgent()
        self.mongo_db = Mongo_class()
        self.session = requests.session()
        self.page_counter = 1
        self.max_interested_pages = 1
        self.all_posts = []
        self.url = ""
        self.headers = ""

    def random_agent(self):
        list_of_agents = [self.agent.chrome, self.agent.safari, self.agent.firefox]
        return random.choice(list_of_agents)

    def grab_number(self, word):
        result = 0
        try:
            result = int(re.findall(r"[0-9]+", word)[0])
        except:
            result = "nothing is"
        return result

    def parsing_start(self):
        while self.page_counter <= self.max_interested_pages:
            response = self.session.get(
                self.url + f"catalogue/page-{self.page_counter}.html",
                headers=self.headers,
            )
            soup = BeautifulSoup(response.text, "html.parser")
            dirty_posts = soup.find_all("article", {"class": "product_pod"})

            if not dirty_posts:
                break

            for post in dirty_posts:
                try:
                    post_info = {}
                    name_info = post.find("h3").findChildren("a")
                    post_info["name"] = name_info[0].get("title")

                    price_info = post.find(
                        "div", {"class": "product_price"}
                    ).findChildren("p", {"class": "price_color"})
                    post_info["price"] = (
                        f"{price_info[0].getText()[1]} {float(price_info[0].getText()[2:])}"
                    )

                    core_info = requests.get(
                        self.url + "catalogue/" + name_info[0].get("href"),
                        headers=self.headers,
                    )
                    core_soup = BeautifulSoup(core_info.text, "html.parser")
                    stock_info = (
                        core_soup.find("p", {"class": "instock availability"})
                        .getText()
                        .strip()
                    )
                    post_info["in stock"] = (
                        f"In stock ({self.grab_number(stock_info)} available)"
                    )

                    description_info = (
                        core_soup.find("article", {"class": "product_page"})
                        .findChildren("p")[3]
                        .getText()
                    )
                    post_info["description"] = description_info
                    self.all_posts.append(post_info)
                except:
                    print("Пропуск...")

            print(f"отработана страница: {self.page_counter}")
            self.page_counter += 1

        print(len(self.all_posts))
        self.show_info()

    def show_info(self):
        print("Что делать с данными?")

        answer = int(
            input(
                "Введите 1 для отправки данных в монго или 0 для отображения данных: "
            )
        )

        if answer == 1:
            self.mongo_db.add_to_db(self.all_posts)
        else:
            self.mongo_db.get_from_db()

    def start(self, num):
        match num:
            case 1:
                self.url = "http://books.toscrape.com/"
                self.headers = {"User-Agent": self.random_agent()}
                answer = self.session.get(
                    self.url + "catalogue/page-1.html", headers=self.headers
                )

                print(self.headers)
                print(answer)

                if answer.status_code == 200:
                    self.parsing_start()
                    
            case 0:
                self.mongo_db.get_from_db()
            case _:
                print("Ошибка ввода")
