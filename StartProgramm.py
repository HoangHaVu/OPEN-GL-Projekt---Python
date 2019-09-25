from RenderWindow import RenderWindow
from FileReader import FileReader
from OpenGL.arrays import vbo
from numpy import array
import numpy as np


"""By Hoang Ha Vu"""


punkte = {}
dreiecke = []
data = []
normalen = {}
texturen = {}

WIDTH= 600
HEIGHT = 600
myvbo = None

#def readData(arg):
#
#    global myvbo,punkte,dreiecke,data,normalen,texturen
#    lines = open(arg).read().split("\n")

#    counterP = 1
#    counterN = 1
#    counterT = 1
#    for line in lines:
#        l = line.split()
#        if(len(l)>2):
#            if (l[0]=="v"):
#                x = float(l[1])
#                y = float(l[2])
#                z = float(l[3])
#                punkte[counterP] = [x,y,z]
#                counterP+=1
#            if (l[0]=="vn"):
#                a = float(l[1])
#                b = float(l[2])
#                c = float(l[3])
#                normalen[counterN]=[a,b,c]
#                counterN+=1
#            if(l[0]=="vt"):
#                a = float(l[1])
#                b = float(l[2])
#                c = float(l[3])
#                texturen[counterT] = [a, b, c]
#                counterT += 1
#            if(l[0]=="f"):
#                eckP1= l[1].split("//")
#                eckP2= l[2].split("//")
#                eckP3= l[3].split("//")
#                dreiecke.append(eckP1)
#                dreiecke.append(eckP2)
#                dreiecke.append(eckP3)

           # dreiecke.append((punkte[eckP1[0]],normalen[eckP1[1]]),(punkte[eckP2[0]],normalen[eckP2[1]]),(punkte[eckP3[0]],normalen[eckP3[1]]))

#    for k in dreiecke:
#        if (len(k)==2):
#            pInd,nvInd = int(k[0]),int(k[1])
#            data.append(punkte[pInd]+normalen[nvInd])
#        elif(len(k)==3):
#            pInd,tInd,nvInd = k[0],k[1],k[2]
#            data.append(punkte[int(pInd)]+texturen[int(tInd)]+normalen[int(nvInd)])
#        else:
#            pInd = k[0]
#            data.append(punkte[int(pInd)])

#    myvbo = vbo.VBO(np.array(data, 'f'))

def main():
    global WIDTH,HEIGHT,myvbo,punkte
    #readData("cow")
    # rw = RenderWindow(WIDTH,HEIGHT,myvbo,punkte)
    object_data = FileReader("cow.obj")
    rw = RenderWindow(WIDTH,HEIGHT,object_data.vbo_data)
    rw.run()

if __name__=='__main__':
    main()