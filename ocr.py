import easyocr
import numpy as np
import pandas as pd
import os, shutil
from google_images_search import GoogleImagesSearch
from dotenv import load_dotenv

load_dotenv()
GCS_DEVELOPER_KEY =os.getenv('GCS_DEVELOPER_KEY')
GCS_CX = os.getenv('GCS_CX')
gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)
df = pd.read_csv('Dish.csv')


#returns a list of every food item that was 
#filtered out from the list of words from easyocr 
def getItems(pathname: str) -> list:
    reader = easyocr.Reader(['en'])

    result = reader.readtext(pathname)
    
    items=[]

    for i in result:
        items.append(i[1])
        
    items=filterItems(items)
    return(items)


#returns a filtered list of only food items from initial list 
#using a dataset to compare if the word is a valid food
def filterItems(items: list) -> list:
    filteredItems = []
    
    for food in items:
        food=food.replace("/", " ")
        food=food.replace(":", " ")
        spaceSeparation = food.split(" ")
        
        for subword in spaceSeparation:
            if len(df[df["name"] == subword])>0:
                filteredItems.append(food)
                break
                
    if len(filteredItems) == 0:
        return ["null"]
    
    return filteredItems

#returns void, creates out file with images
#uses Google Images API to store an image of each food item into out file
def obtainImages(items: list):
    shutil.rmtree("./out/") #empties out file 
    
    for item in items[0:10]: #only do first 10 item(s) because google api is cringe
        gis.search(search_params = {'q':item, 'fileType': 'jpg'}, path_to_dir= "./out/", custom_image_name=item)