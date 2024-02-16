from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json

def scrape_veg_recipes(baseUrl,num_of_pages,count_lock,scrape_count):
    s = HTMLSession()
    r = s.get(baseUrl)
    sourceSoup = BeautifulSoup(r.text, 'html.parser')
    links = {}
    for l in sourceSoup.findAll('div' , {'class': 'glossary-section'}):
        for i in l.findAll('li'):
            links[i.find('a').get('href')] = False

    recipe_list = []
    for k,v in links.items():
        with count_lock:
            if scrape_count[0]>num_of_pages[0]:
                break
            scrape_count[0]+=1 
        recipe = s.get(k)
        soupRecipe = BeautifulSoup(recipe.text, 'html.parser')
        ing = []
        # print(k)
        if soupRecipe.find('ul', {'class': 'wprm-recipe-ingredients'}) != None:
            for i in soupRecipe.find('ul', {'class': 'wprm-recipe-ingredients'}).findAll('li', {'class': 'wprm-recipe-ingredient'}):
                ing.append(i.find('span', {'class':'wprm-recipe-ingredient-name'}).text)
        name = soupRecipe.find('h2',{'class': 'wprm-recipe-name wprm-block-text-normal'})
        img = soupRecipe.find('div',{'class': 'wprm-recipe-image wprm-block-image-normal'}).find('img') if soupRecipe.find('div',{'class': 'wprm-recipe-image wprm-block-image-normal'}) != None else  " "
        cuisine = soupRecipe.find('span', {'class': 'wprm-recipe-cuisine wprm-block-text-bold'})
        cook = soupRecipe.find('span', {'class': 'wprm-recipe-time wprm-block-text-bold'})
        obj = {
            "name": name.text if name != None else " " ,
            "url": k,
            "ingredients":ing,
            "image_url": img.get('data-lazy-src') if img != " " else " ",
            "cuisine": cuisine.text if cuisine != None else " ",
            "cooking_time": cook.text if cook != None else " "
        }
        recipe_list.append(obj)
    
    with open('data4.json', 'w') as f:
        json.dump(recipe_list, f, indent=4)

# veg_recipes('https://www.vegrecipesofindia.com/glossary/')