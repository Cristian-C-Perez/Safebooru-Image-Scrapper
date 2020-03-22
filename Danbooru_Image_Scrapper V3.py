"""
End user License Agreement goes here, need help on making this happen.
"""

import os
from bs4 import BeautifulSoup
import requests
import json
import concurrent.futures
import time

def char_case(argument): 
    # ---Function to clean the character's names when searching in Danbooru---
    # Checks the text inputted to see if it's in the JSON:

    try:
        with open("characters.json") as chars_in_jason:
            switcher = json.load(chars_in_jason)
    except FileNotFoundError as e:
        print("JSON file not found, please place the file in the same folder/directory as this program")
        print(e)
        end = input("Press Enter to end the program \n")
  
    # get() method of dictionary data type returns  
    # the value of passed argument if it is found within  
    # the JSON, otherwise the second argument will 
    # be assigned as default value of passed argument in which case it's the same thing as inputted.
    # Without the JSON, the program fails to work.
    return switcher.get(argument, argument)

# The search engine where you input the character's name, switches any space to underscore and lowercases the string.
character_source = input("What character would you like to search: \n").lower()
character_source = character_source.replace(" ","_")
character_source = char_case(character_source)
if (character_source == "exit"):
    exit()
print(character_source)

start_time = time.perf_counter()

# Then it takes the tag and adds it to the full https link to use it to parse.
source = requests.get(f"https://safebooru.donmai.us/posts?tags={character_source}").text

# This is where BeautifulSoup comes into play for parsing the sections necessary till it narrows it down to the images section.
soup = BeautifulSoup(source, 'lxml')
body = soup.body
img = body.find('div', id='page')
c_post = img.find('div', id='c-posts')
a_index = c_post.find('div', id='a-index')
main_content = a_index.find('section', id='content')
posts_1 = main_content.find('div', id='posts')
posts_2 = posts_1.find('div', id='posts-container')

# This piece here checks if there are any images at all on the webpage. Then makes a directory if not existing.
if(len(posts_2) > 5):
    try:
        os.mkdir(character_source)
        print("Directory " , character_source ,  " has been created.\n") 
    except FileExistsError:
        print("Directory " , character_source ,  " already exists.\n")
else:
    # Kills the program because no results were found.
    print("No images found.")
    end = input("Press Enter to end the program \n")
    exit()


# The section which nets all the images and puts it in the directory the program utilizes.
def download_images(character_images):
    x = character_images['data-file-url']
    filename = x.split('/')
    if os.path.exists(f"{character_source}\\" + filename[4]):
        print(f"File {x} already Exist.")
    else:
        # The downloading segment.
        print(f"Downloading {x}...")
        second_request = requests.get(x)
        with open(f"{character_source}\\" + filename[4], 'wb') as f:
            f.write(second_request.content)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download_images, posts_2.find_all('article'))

# End of the line.
end_time = time.perf_counter()
print(f"all possible images have successfully been downloaded in {round(end_time-start_time, 2)} seconds.")
end = input("Press Enter to end the program \n")
