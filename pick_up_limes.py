import requests
from model import Model
from bs4 import BeautifulSoup
import json
import model_to_dict

def scrape_pick_up_limes(baseUrl,num_of_pages,count_lock,scrape_count):
# baseUrl = "https://www.pickuplimes.com"
    links_in_page = []
    for page in range(1,35):
        r= requests.get(f'https://www.pickuplimes.com/recipe/?page={page}')
        soup = BeautifulSoup(r.content,'lxml')
        # getting the hrefs of each dishes
        dishes = soup.find_all('li', class_="flex-item slide-up-ani")
        for dish in dishes:
            for hrefs in dish.find_all('a', href=True):
                if 'video' not in hrefs['href']: 
                    links_in_page.append(baseUrl+hrefs['href'])
    pick_up_limes = []
    for link in links_in_page:
        with count_lock:
            if scrape_count[0]>num_of_pages[0]:
                break
            scrape_count[0]+=1 
        # print(link)
        req= requests.get(link)
        soup2 = BeautifulSoup(req.content,'lxml')
        ingredients_raw = []
        ingredient_span = soup2.find_all('span', class_='ingredient-name-text')
        dish_name = soup2.find('h1').text
        div_tags = soup2.find('div', class_='col-lg-5')
        img_div = div_tags.find('img',class_='img-fluid')
        img_src = img_div['src']
                # print(img['src'])
                # print("dish name = ",dish_name.text)
        for item in ingredient_span:
            ingredients_raw.append(item.text)
        time_div = soup2.find_all('div', class_="col")
        cooking_time = time_div[1].find('span')
        ingredients = [str(ingredient) for ingredient in ingredients_raw]
            #directions
        span_tag = soup2.find_all("span",class_="direction")
        directions= ''
        for span in span_tag:
            directions+=span.text
        model_instance = Model(str(dish_name),str(link),ingredients,str(img_src)," ",str(cooking_time),directions," "," ")
        pick_up_limes.append(model_instance)
        
    
    pick_up_limes_dict = []

    for obj in pick_up_limes:
        model_dict = model_to_dict.convertModelToDict(obj)
        pick_up_limes_dict.append(model_dict)
    #writing to a json file 
    with open("data1.json", "w") as json_file:
        json.dump(pick_up_limes_dict, json_file, indent=4)

