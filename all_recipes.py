import requests
import json
from bs4 import BeautifulSoup
from model import Model

def get_recipe_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    recipe_links = []

    for link in links:
        href = link['href']
        if href.startswith('https://www.allrecipes.com/recipe') and href not in recipe_links:
            recipe_links.append(href)

    return recipe_links


def scrape_recipe(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting recipe name
    recipe_name_element = soup.find('h1', class_='article-heading type--lion')
    recipe_name = recipe_name_element.get_text().strip() if recipe_name_element else 'Unknown'

    # Extracting ingredients
    ingredients = []
    ingredients_list = soup.find('ul', class_='mntl-structured-ingredients__list')
    if ingredients_list:
        ingredient_items = ingredients_list.find_all('li', class_='mntl-structured-ingredients__list-item')
        for item in ingredient_items:
            ingredient = item.get_text().strip()
            ingredients.append(ingredient)

    # Extracting image URL
    image_url_element = soup.find('img', class_='universal-image__image')
    image_url = image_url_element['data-src'] if image_url_element else 'Unknown'

    # Extracting cuisine
    cuisine_element = soup.find('span', class_='toggle-similar__title')
    cuisine = cuisine_element.get_text().strip() if cuisine_element else 'Unknown'

    # Extracting cooking time
    cooking_time_label = "Cook Time:"
    cooking_time_element = soup.find('div', string=cooking_time_label)
    if cooking_time_element:
        cooking_time = cooking_time_element.find_next_sibling('div', class_='mntl-recipe-details__value').get_text().strip()
    else:
        cooking_time = 'Unknown'

    # Extracting nutrition info
    nutrition_info = []
    nutrition_table = soup.find('div', class_='mntl-nutrition-facts-summary')
    if nutrition_table:
        rows = nutrition_table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                nutrient_name = cells[0].get_text().strip()
                nutrient_value = cells[1].get_text().strip()
                nutrition_info.append(f"{nutrient_name}: {nutrient_value}")

    # Extract cooking directions
    directions_list = soup.find_all('p', class_='comp mntl-sc-block mntl-sc-block-html')
    cooking_directions = '\n'.join([direction.get_text().strip() for direction in directions_list])

    # Extract cooking notes
    cooking_notes_element = soup.find('p', class_='comp mntl-sc-block mntl-sc-block-html')
    cooking_notes = cooking_notes_element.get_text().strip() if cooking_notes_element else 'Unknown'

    return Model(name=recipe_name, url=url, ingredients=ingredients, image_url=image_url, cuisine=cuisine, cooking_time=cooking_time, nutrition_info=nutrition_info, cooking_directions=cooking_directions, cooking_notes=cooking_notes)

def scrape_and_store_recipe(url, recipes,num_of_pages,count_lock,scrape_count):
    recipe = scrape_recipe(url)
    if recipe:
        recipes.append(recipe.__dict__)

        recipe_links = get_recipe_links(url)
        for link in recipe_links:
            with count_lock:
                if scrape_count[0]>num_of_pages[0]:
                    break
                scrape_count[0]+=1
            # print(link)
            scrape_and_store_recipe(link, recipes,num_of_pages,count_lock,scrape_count)

def scrape_all_recipes(baseUrl,num_of_pages,count_lock,scrape_count):
    recipes = []
    scrape_and_store_recipe(baseUrl, recipes,num_of_pages,count_lock,scrape_count)
    with open('data5.json', 'w') as f:
        json.dump(recipes, f, indent=4)

# if _name_ == "_main_":
#     main()