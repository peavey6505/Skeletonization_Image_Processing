import numpy as np
from prettytable import PrettyTable
import cv2
from skimage.util import invert
from skimage.morphology import skeletonize
import matplotlib.pyplot as plt

####### Wczytywanie obrazu, ustawienie tabeli wyników
img = cv2.imread('fingerprint2.png',0)

cv2.imshow('image',img)

table = PrettyTable()
np.set_printoptions(threshold=np.nan)
table.field_names = ["Nr. punktu","Y","X"]

print(img.ndim)
numrows = len(img)
numcols = len(img[0])
print("rzedy")
print(numrows)
print("kolumny")
print(numcols)
print(img[12][40])


####### Binaryzacja obrazu 
for x in range(numrows):
    for y in range(numcols):
        if(img[x][y] > 230):
            img[x][y] = 0
        else:
            img[x][y] = 1

        
print(img[12][40])
skeleton = skeletonize(img)

branchCounter=0
tempCounter=0

dlugosc=0
######## Wyznaczanie długości szkieletu
for x in range(numrows):
    for y in range(numcols):
        if(skeleton[x][y]==True):
            dlugosc=dlugosc+1
            


print("Obwod: ")
print(dlugosc)
print("################################SKELETON ######################")
print(skeleton[2][2])
print("Punkt  |  X  |  Y  " )

######## Wyznacznanie rozgałęzień szkieletu
for x in range(numrows):
    for y in range(numcols):
      if (x>0 and y>0 and x< numrows-1 and y < numcols-1):
       if(skeleton[x][y]==True):
        
        tempArray = [ skeleton[x-1][y+1], skeleton[x][y+1], skeleton[x+1][y+1], skeleton[x+1][y], skeleton[x+1][y-1], skeleton[x][y-1], skeleton[x-1][y-1], skeleton[x-1][y], skeleton[x-1][y+1] ]
        tempCounter=0
        
        if(skeleton[x-1][y+1]==True):
            for i in range(7):
                if(tempArray[i] == True and tempArray[i+1] ==False):
                    tempCounter = tempCounter+1
        else:
            for i in range(7):
                if(tempArray[i] == False and tempArray[i+1] ==True):
                    tempCounter = tempCounter+1
        if(tempCounter>2):
               
                branchCounter = branchCounter+1
                table.add_row([branchCounter,x,y])                            


print(branchCounter)
print(table)


######## Wyświetlanie wyników
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4),
                         sharex=True, sharey=True)

ax = axes.ravel()

ax[0].imshow(img, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('Original Black-White Zoom ', fontsize=20)
ax[1].imshow(skeleton, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('Skeletonized Zoom', fontsize=20)
fig.tight_layout()
plt.show()
