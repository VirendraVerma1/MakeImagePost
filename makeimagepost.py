from jinja2 import Environment, BaseLoader
from PIL import ImageFilter
import imgkit
import random
import requests
import json
from PIL import Image
import os
from os import listdir
from os.path import isfile, join
import random
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


message_list=[
    "Life is waiting for you <br>Give your best Shot."
]

is_author=True
author_name="-Sandeep Maheshwari"
is_author_pic=False
author_pic="https://i.pinimg.com/originals/d2/cd/59/d2cd59ec667f39bfa65a1fcaf90434ac.png"

#number of images
total_samples=2
random_sample=True

#text colors
custom_text_color=False
text_color="white"

#text alignment
left__margin="100px"
bottom__margin="330px"
font__family="Merriweather"
font__size="40px"
is_border=False
border_color="black"

#image filter
gaussian_blur=1






current_post_id=""









unsortedimage="D:\\Programs\\MakeImagePost\\UnSortedImage"
imagetocropdirpath="D:\\Programs\\MakeImagePost\\ImagesToCrop"
croppedimagedirpath="D:\\Programs\\MakeImagePost\\CropedImage"
completedpostdirpath="D:\\Programs\\MakeImagePost\\CompletedPost"
author_imagepath="D:\\Programs\\MakeImagePost\\Author"
downloadedpostdirpath="D:\\Programs\\MakeImagePost\\DownloadedImage"

path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
html_location='D:\\Programs\\MakeImagePost\\basichtml.html'

def read_and_store_all_the_files(fromfolder):
    onlyfiles = [f for f in listdir(fromfolder) if isfile(join(fromfolder, f))]
    return onlyfiles

def remove_all_files(directory):
    onlyfiles=read_and_store_all_the_files(directory)
    for i in onlyfiles:
        os.remove(directory+"\\"+i)

def getcolordict(im):
    w,h = im.size
    colors = im.getcolors(w*h)
    colordict = { x[1]:x[0] for x in colors }
    return colordict


def isimageBlack(imagefileWithPath):
    im = Image.open(imagefileWithPath).convert('L')
    pixels = im.getdata()          # get the pixels as a flattened sequence
    black_thresh = 50
    nblack = 0
    for pixel in pixels:
        if pixel < black_thresh:
            nblack += 1
    n = len(pixels)

    if (nblack / float(n)) > 0.01:
        return True
    else:
        return False


def makeimagecropfromfolder():
    onlyfiles=read_and_store_all_the_files(imagetocropdirpath)
    remove_all_files(croppedimagedirpath)
    counter=1
    for i in onlyfiles:
        try:
            img = Image.open(imagetocropdirpath+"\\"+i)
            width, height = img.size
            size_height=height
            size_width=width

            min_width_size=(width/2.0)-540
            min_height_size=(height/2.0)-540


            #print(size_width-min_size,min_size,size_height)
            img_left_area = (min_width_size,min_height_size, min_width_size+1080, min_height_size+1080)
            img_left = img.crop(img_left_area)

            img_left = img_left.filter(ImageFilter.GaussianBlur(gaussian_blur))
            img_left.save(croppedimagedirpath+"\\"+str(counter)+".jpg")
            counter+=1
        except:
            pass
        
    
def rename_all_the_files():
    onlyfiles=read_and_store_all_the_files(unsortedimage)

    for i in range(0,len(onlyfiles)):
        os.rename(unsortedimage+"\\"+onlyfiles[i],imagetocropdirpath+"\\"+str(i+1)+".jpg") 



def createQuoteImg(msg_body,image_location,filename):
    onlyfiles=read_and_store_all_the_files(croppedimagedirpath)
    if(filename==False):
        if(image_location.find("https") == -1):
            backimage=croppedimagedirpath+"\\"+random.choice(onlyfiles)
        else:
            backimage=image_location
        print(backimage)
    else:
        backimage=croppedimagedirpath+"\\"+filename

    temptextcolor="black"
    imagecolor=isimageBlack(backimage)
    if(imagecolor):
        temptextcolor="white"
    else:
        temptextcolor="black"

    if(custom_text_color):
        temptextcolor=text_color

    temp__border=""
    if(is_border):
        temp__border="border: 4px solid "+border_color+";"
    
    temp__author=""
    if(is_author):
        temp__author='<p class="bottom-right">'+author_name+'</p>'

    temp__author_pic=""
    if(is_author_pic):
        temp__author_pic='<img src="'+author_pic+'" style="width:25%;height:20%">'


    content = dict(
        background_img_path=backimage,
        description=msg_body,
        textcolor=temptextcolor,
        left_margin=left__margin,
        bottom_margin=bottom__margin,
        font_family=font__family,
        font_size=font__size,
        temp_border=temp__border,
        temp_author=temp__author,
        temp_author_pic=temp__author_pic,
        )

    

    HTML="""
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="imgkit-format" content="png"/>
        <meta name="imgkit-orientation" content="Landscape"/>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Palette+Mosaic&display=swap" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;1,300&family=Palette+Mosaic&display=swap" rel="stylesheet">

        <style type="text/css">

        .bottom-left{
            position:absolute;
            bottom:250px;
            left:100px;
            width:60%;
            font-size:50px;
            line-height:150%;
            font-weight: bold;
            color:{{textcolor}};
        }
        .bottom-right{
            position:absolute;
            bottom: -50px;
            left:100px;
            width:90%;
            font-size:30px;
            line-height:100%;
            font-style: italic;
            color:{{textcolor}};
        }

        .bottom-center{
            position:absolute;
            float:right;
            bottom:{{bottom_margin}};
            left:{{left_margin}};
            align-content: center;
            width:80%;
            font-size:{{font_size}};
            line-height:150%;
            font-weight: bold;
            color:{{textcolor}};
            font-family: '{{font_family}}';
            
        }

        .top-right{
            position:absolute;
            top:60px;
            right:68px;
            width:100px;
        }
        </style>


        </head>
        <body >
        <div class="container">
            <img src="{{background_img_path}}" style="width:100%; {{temp_border}}">
            <div class="bottom-center" align="center">
            {{temp_author_pic}}
            <p>"{{description}}"</p>
            {{temp_author}}</div>
            
            
        </div>
        </body>
        </html>
        """

    # <div class="bottom-center"><p>"{{description}}"</p></div>  



    #imgkit.from_string(HTML, image_location, config=config)
     
    rtemplate = Environment(loader=BaseLoader).from_string(HTML)
    rendered_output = rtemplate.render(**content)
    #rendered_output=Environment().form_string(HTML).from_string(HTML).render(**content)

    with open(html_location,'w', encoding='utf8') as f:
        f.write(rendered_output)

    options={
            'encoding':"UTF-8",
            "enable-local-file-access":None,
            'custom-header':[
                ('Accept-Encoding','gzip')
            ],
        }

    imgkit.from_file(html_location,image_location,options)


def make_themes_from_message():
    onlyfiles=read_and_store_all_the_files(croppedimagedirpath)
    
    counter=random.randint(1111111,999999999)
    n=total_samples
    while(n>0):
        n-=1
        if(random_sample):
            for i in message_list:
                createQuoteImg(i,completedpostdirpath+"\\"+"motivational_quote_"+str(current_post_id)+"_"+str(counter)+".jpg",False)
                counter=random.randint(1111111,999999999)
        else:
            for i in message_list:
                for image in onlyfiles:
                    createQuoteImg(i,completedpostdirpath+"\\"+"motivational_quote_"+str(current_post_id)+"_"+str(counter)+".jpg",image)
                    counter=random.randint(1111111,999999999)
        

def download_more_images():
    print("--------downlaod start--------")
    url='https://www.freepik.com/search?dates=any&format=search&orientation=square&page=2&query=background&selection=1&sort=popular'
    driver = webdriver.Firefox(executable_path="D:\\Programs\\Python_private\\SeleniumBots\\Driver\\geckodriver.exe")
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)
    page = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(''.join(page), 'html.parser')
    # actions = ActionChains(driver)
    # for _ in range(8):
    #     actions.send_keys(Keys.SPACE).perform()
    #     time.sleep(1)
    img_all_links=soup.find_all("a",{"class":"showcase__link"})
    for i in img_all_links:
        try:
            imglink=i.find("img",{"class":"loaded"}).get('data-src')
            li=imglink.split('?')
            counter=0
            for i in message_list:
                
                print(li[0])
                createQuoteImg(i,li[0],False)
                counter+=1
        except:
            pass
    driver.close()
    driver.quit()

def set_author_pic(author_namee):
    onlyfiles=read_and_store_all_the_files(author_imagepath)
    author_namee=author_namee.lower()
    flag=False
    author_namee = author_namee.replace("-"," ")
    author_namee = author_namee.replace(" ","")
    current_file=""
    for i in onlyfiles:
        current_file=i
        i = i.replace("_"," ")
        i = i.replace(".png"," ")
        i = i.replace(" ","")
        if(i == author_namee):
            flag=True
            break
       
        print(i)
        print(author_namee)

    global author_pic
    author_pic=author_imagepath+"\\"+current_file
    global is_author_pic
    if(flag):
        is_author_pic=True
    else:
        is_author_pic=False

def getquotefromserverandpost():
    
    while(True):
        url="http://kreasaard.atwebpages.com/laravel/public/getquote"
        x = requests.get(url)
        if(x.text=="alldone"):
            break
        data=x.json()
        print(data)
        global current_post_id
        current_post_id=data["id"]
        global message_list
        message_list=[data["quote"]]
        global author_name
        author_name=data["author_name"]
        set_author_pic(author_name)
        global total_samples
        total_samples=1
        global font__family
        font__family=data["font"]
        make_themes_from_message()
        url="http://kreasaard.atwebpages.com/laravel/public/api/updatequote"
        myobj = {'id':data["id"]}
        x = requests.post(url, data = myobj)
        print(x.text)



remove_all_files(completedpostdirpath)
getquotefromserverandpost()
#rename_all_the_files()
#makeimagecropfromfolder()
#make_themes_from_message()
#download_more_images()