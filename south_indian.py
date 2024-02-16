import requests
from model import Model
from bs4 import BeautifulSoup
import json
import model_to_dict

def scrape_south_indian(baseUrl,num_of_pages,count_lock,scrape_count):
    # baseUrl = "https://www.sailusfood.com/categories/south_indian_food_recipes/"
    pages = []
    links_set = set()
    for page in range(1,4):
        r= requests.get(f'{baseUrl}/{page}/')
        soup = BeautifulSoup(r.content,'lxml')
        # getting the hrefs of each dishes
        dishes_url = soup.find_all('div', class_="media align-items-top container row")
        for url in dishes_url:
            for hrefs in url.find_all('a', href=True):
                links_set.add(hrefs['href'])
    links = list(links_set)
    south_indian_menu = []

    # req= requests.get(links[0])
    # soup2 = BeautifulSoup(req.content,'lxml')

    # for d in dir_tag:
    #     print(d)
    for link in links_set:
        with count_lock:
            if scrape_count[0]>num_of_pages[0]:
                break
            scrape_count[0]+=1 
        # print(link)
        req= requests.get(link)
        soup2 = BeautifulSoup(req.content,'lxml')
            #name
        name_tag = soup2.find_all('h1', class_="single-title")
        dish_name = str(name_tag[0].text)
                #ingredients
        ingredients = []
        ingredients_tag = soup2.find_all('span', itemprop='recipeIngredient')
        for i in ingredients_tag:
            ingredients.append(str(i.text.strip()))
                #url
        url = str(link)
                #image_url
        img_tag = soup2.find('div', class_="entry-content")
        img = img_tag.find('img')
        img_url = str(img['src'])
                #cuisine
        cuisine_tag = soup2.find_all('span', itemprop='recipeCuisine')
        cuisine = " "
        if len(cuisine_tag) > 0 :
            cuisine = str(cuisine_tag[0].text)
                #cooking_time
        prep_time_tag = soup2.find('time', itemprop="prepTime")
        cooking_time = ""
        if prep_time_tag is not None:
            cooking_time = str(prep_time_tag.text)
        dir_tag = soup2.find_all('span', itemprop="recipeInstructions")
        directions = ""
        for d in dir_tag:
            directions += d.text
        model_instance = Model(dish_name,link,ingredients,img_url,cuisine,cooking_time,directions," "," ")
        south_indian_menu.append(model_instance)

    south_indian_menu_dict = []
    for obj in south_indian_menu:
        model_dict = model_to_dict.convertModelToDict(obj)
        south_indian_menu_dict.append(model_dict)
    #writing to a json file 
    with open("data2.json", "w") as json_file:
        json.dump(south_indian_menu_dict, json_file, indent=4)