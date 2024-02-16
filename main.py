from model import Model
import south_indian
import pick_up_limes
import food_network
import vegrecipes
import all_recipes
from model import Model
from bs4 import BeautifulSoup
import json
from threading import Thread, Lock

# num_of_pages = [5]

num_of_pages_input = input("Enter the number of pages to scrape: ")
num_of_pages = [int(num_of_pages_input)]

count_lock = Lock()
scrape_count = [0]
pick_up_limes_base_url = "https://www.pickuplimes.com"
south_indian_base_url = "https://www.sailusfood.com/categories/south_indian_food_recipes/page/"
food_network_base_url = "https://www.foodnetwork.com/recipes/recipes-a-z/123"
all_recipes_base_url = "https://www.allrecipes.com/"
veg_recipes_base_url = "https://www.vegrecipesofindia.com/glossary/"

tr1 = Thread(target=pick_up_limes.scrape_pick_up_limes,args=(pick_up_limes_base_url,num_of_pages,count_lock,scrape_count))
tr2 = Thread(target=south_indian.scrape_south_indian, args=(south_indian_base_url,num_of_pages,count_lock,scrape_count))
tr3 = Thread(target=food_network.scrape_food_network,args=(food_network_base_url,num_of_pages,count_lock,scrape_count))
tr4 = Thread(target =vegrecipes.scrape_veg_recipes, args=(veg_recipes_base_url,num_of_pages,count_lock,scrape_count))
tr5 = Thread(target=all_recipes.scrape_all_recipes, args=(all_recipes_base_url,num_of_pages,count_lock,scrape_count))

#start the threads
tr1.start()
tr2.start()
tr3.start()
tr5.start()
tr4.start()

#wait until all threads are finished
tr1.join()
tr2.join()
tr3.join()
tr5.join()
tr4.join()