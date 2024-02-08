import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import datetime
from PIL import Image
from io import BytesIO
import requests
import random
import numpy as np

def crop_image(image):
    width, height = image.size
    img_array = np.array(img)
    x1 = width - 1
    x2 = 0
    y1 = height - 1
    y2 = 0
    for y in range(height):
        for x in range(width):
            pixel_value = img_array[y, x]
            if pixel_value[1] == 255:
                x1 = min(x1, x)
                x2 = max(x2, x)
                y1 = min(y1, y)
                y2 = max(y2, y)



    return image.crop((x1, y1, x2, y2))

def add_white_background(image):
    width, height = image.size
    background = Image.new("RGB", (width, height), "white")
    background.paste(image, (0, 0),image)
    return background
        
words = ['ذرة', 'طفل', 'يد', 'ثمرة', 'فول', 'رمان', 'قرد', 'بيت', 'أرز', 'تمساح', 'موز', 'بنت', 'علم', 'عنب', 'غراب', 'نار', 'دار', 'جزر', 'ثعلب']
for word in words:
    script_directory = os.path.dirname(__file__)
    
    folder_path = os.path.join(script_directory,word)
    
    
    os.mkdir(folder_path)
    driver = webdriver.Chrome()
    
    
    for page in range(1,20):
        url = f'https://www.myfonts.com/collections/tags/arabic-fonts?page={page}'
        driver.get(url)
        time.sleep(1)
        input_field = None
        time.sleep(10)
        inputs = driver.find_elements(By.TAG_NAME,"input")
        for i in inputs:
            if i.get_attribute("placeholder") == "Type your own text":
                input_field = i;
                break;
        input_field.clear()
        input_field.send_keys(word)
    
        time.sleep(3)
        for i in range(10):
            driver.execute_script("window.scrollBy(0,1000);")
            time.sleep(1)
        time.sleep(3)
        imgs = driver.find_elements(By.TAG_NAME,"img")
    
        for img in imgs:
            src = img.get_attribute("src")
            if src.startswith("https://sig.monotype.com/"):
                filename = os.path.join(folder_path,f"{random.randint(0,100000000)}.jpg")
                response = requests.get(src)
    
                if response.status_code == 200:
                    with Image.open(BytesIO(response.content)) as img:
                        try:
                            img = crop_image(img)
                            img = add_white_background(img)
                            img.save(filename,format="JPEG")
                        except:
                            pass

     
                
driver.quit()