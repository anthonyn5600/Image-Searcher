import PySimpleGUI as gui
import flickrapi
import urllib.request
import os
from PIL import Image

api_key=u'f757ef7772aa181fa3d1e6e352c5e679'
api_secret=u'53b88aa38bcd94e'
flickr = flickrapi.FlickrAPI(api_key, api_secret,format='parsed-json')
directory = "C:\\Users\\Anthony Ngon\\Downloads\\New folder (2)" #change this to a directory such as a empty folder so the program would be able to download the images.

a_col = [[gui.Input(key='submit'),gui.Button('Enter')]]

b_col =[[gui.Image(key='0',size=(300,300)),gui.Image(key='1',size=(300,300))],
      [gui.Image(key='2',size=(300,300)),gui.Image(key='3',size=(300,300))],
      [gui.Image(key='4',size=(300,300)),gui.Image(key='5',size=(300,300))]]

gui.theme('DarkGrey8')
layout = [[gui.Text('Enter a object')],
          [gui.Column(a_col)],
          [gui.Text('You are viewing',key='consume',size=(20,1))],
          [gui.Column(b_col,key='col',size=(630,300),scrollable=True,vertical_scroll_only=True,expand_x=True,element_justification='center',visible=False)],
          [gui.Exit()]]
window = gui.Window('Image Searcher',layout)

while True:
    event, values = window.read()

    #delete the images after the user press the exit button
    if event == gui.WIN_CLOSED or event == 'Exit': 
        for file in os.listdir(directory):
            find_file = directory + f'\\{file}'
            os.remove(find_file)
        break

    if event == 'Enter':
        urls = 'url_c'
        apple = flickr.photos.search(text=values['submit'], per_page=10, page=1, extras=urls, safe_search=1, sort='relevance')

        n_photos = len(apple['photos']['photo'])

        #convert the url into a image file .jpeg into the download folder
        s_picture = 0
        for x in range(0, n_photos):
            if urls in apple['photos']['photo'][x]:
                photo = directory + f"\\picture_{str(s_picture)}.jpeg"
                urllib.request.urlretrieve(apple['photos']['photo'][x][urls],photo) #how you want to save the image from the url
                s_picture += 1

        #convert the .jpeg in the folder to .png so it be read into the image element 
        s_picture = 0
        for file in os.listdir(directory):
            if file.endswith('.jpeg'):
                window['col'].update(visible=True)
                find_file = directory + f'\\{file}'
                image = Image.open(find_file)
                image = image.resize((300, 300))
                image.save(find_file.replace('.jpeg','.png'))#save the file into the downloads folder with the new extension
                if s_picture <= 5:
                    if file.find(str(s_picture)):
                        window[str(s_picture)].update(find_file.replace('.jpeg','.png')) #find the file with the .png in the file type and put it in the image
                        s_picture += 1
window.close()


