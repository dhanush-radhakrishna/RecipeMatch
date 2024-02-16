import requests
from model import Model
from bs4 import BeautifulSoup
import json
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor

def scrape_website(link,links_lock,food_network_lock,links,food_network):
    # global food_network
    # global links
    # global links_lock
    # global food_network_lock

    with links_lock:
        if links[link] == True:
            return
        links[link] = True

    req3 = requests.get(link)
    soup3 = BeautifulSoup(req3.content, 'lxml')
    # print(link)

    name_tag = soup3.find_all('span', class_="o-AssetTitle__a-HeadlineText")
    if len(name_tag) > 1:
        name = name_tag[1].text
    else:
        name = name_tag[0].text

    cooking_time = soup3.find('span', class_="o-RecipeInfo__a-Description m-RecipeInfo__a-Description--Total")
    if cooking_time is None:
        cooking_time = ""
    else:
        cooking_time = str(cooking_time.text)

    nutrition = ""
    ingredients = []
    spans = soup3.find_all('span', class_="o-Ingredients__a-Ingredient--CheckboxLabel")
    for i in range(1, len(spans)):
        ingredients.append(spans[i].text)

    li = soup3.find_all('li', class_="o-Method__m-Step")
    directions = ""
    for i in li:
        directions += i.text

    notes_tag = soup3.find_all("p", class_="o-ChefNotes__a-Description")
    notes = ""
    if len(notes) > 0:
        notes = notes_tag[0].text

    raw_data = {
        "name": name,
        "cooking_time": cooking_time,
        "nutrition": nutrition,
        "ingredients": ingredients,
        "directions": directions,
        "notes": notes
    }
    with food_network_lock:
        food_network.append(raw_data)
#initialize locks
def scrape_food_network(baseUrl,num_of_pages,count_lock,scrape_count):
    food_network_lock = Lock()
    links_lock = Lock()
    # baseUrl = "https://www.foodnetwork.com/recipes/recipes-a-z/123"
    pages = []
    req1= requests.get(baseUrl)
    soup = BeautifulSoup(req1.content,'lxml')
    food_network = []
    alphabet = soup.find_all('a', class_="o-IndexPagination__a-Button")
    for i in alphabet:
        pages.append("https:"+i['href'])
    links = {}
    for page in pages:
    # page = pages[0]
        req2 = requests.get(page)
        soup2 = BeautifulSoup(req2.content,'lxml')
        li = soup2.find_all('li', class_="m-PromoList__a-ListItem")
        for i in li:
            hrefs = i.find('a',href=True)
            # print("https:"+str(hrefs['href']))
            links["https:"+str(hrefs['href'])] = False
            #storing it in a dict so that there wont be duplicates
        #value = false for all keys (cuz they are not scraped yet)
    #multithreading function to scrape
    # links = dict(list(links.items())[:100])

    with ThreadPoolExecutor(max_workers=5) as executor:
    # Submit scraping tasks to the executor
        for link in links:
            with count_lock:
                if scrape_count[0]>num_of_pages[0]:
                    break
                scrape_count[0]+=1
            executor.submit(scrape_website, link, links_lock, food_network_lock, links, food_network)

    with open("data3.json", "w") as json_file:
        json.dump(food_network, json_file, indent=4)