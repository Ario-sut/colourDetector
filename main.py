import cv2
import pandas as pd
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i','--image', required=True, help='Image Path')
args=vars(ap.parse_args())
img_path= args['image']

img = cv2.imread(img_path)

clicked =False
r=g=b=xpos=ypos=0

index=['color', 'color_name', 'hex', 'R', 'G','B']
csv= pd.read_csv('colors.csv', names=index, header=None)

def getColorName(R,G,B): # To obtain a color name and code at a certain position in a picture
    minimum=1000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,'R'])) + abs(G- int(csv.loc[i,'G'])) + abs(B- int(csv.loc[i,'B']))
        if d<= minimum:
            minimum=d
            cname = csv.loc[i,'color_name']
    return cname

def draw_function(event,x,y): # Declare global variables to store the color values and position of the clicked pixel
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos,clicked
        clicked =True # set the clicked flag to true
        xpos=x # store the x coordinates of the clicked pixel
        ypos=y # store the y coordinates of the clicked pixel
        b,g,r = img[x,y] # get the color values of the clicked pixel
        b = int(b) # convert the color values to integers
        g = int(g) # convert the color values to integers
        r = int(r) # convert the color values to integers

cv2.namedWindow('image') # create new window called "image"
cv2.setMouseCallback('image', draw_function) # setting the "draw_function" as the callback for mouse events on the image on the window 
                
while(1):
    cv2.imshow('image', img)
    if clicked:
        cv2.rectangle(img, (20,20), (750,60), (b,g,r), -1)
        text = getColorName(r,g,b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' +str(b)
        cv2.putText(img, text, (50,50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    if r+g+b>=600:
        cv2.putText(img, text, (50,50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked=False

# break the loop if user pressed 'esc' button
    if cv2.waitKey(20) & 0xFF ==27:
        break

cv2.destroyAllWindows()
