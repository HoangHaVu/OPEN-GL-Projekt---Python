import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from numpy import array
import sys,math,os
import numpy as np

class Scene: # initialization
    #def __init__(self, width, height,punkte):
    def __init__(self, width, height):
        self.shadow =True
        self.width = width
        self.height = height
        self.angle =0.0
        self.axis= np.array([0.0,1.0,0.0])
        self.actOri = 1.0
        self.light = (-3, -4, -4)
        self.p = [1., 0, 0, 0, 0, 1., 0, -1. / self.light[1], 0, 0, 1., 0, 0, 0, 0, 0] # 4er EinheitsMatrix
        self.color = (0.0,1.0,0.0)
        self.backgroundcolor=(0.2, 0.0, 0.8, 0.5)
        self.scalefactor = None
        self.center = (0, 0, 0)
        self.x_translate = 0
        self.y_translate = 0
        #self.maxX = 0
        #self.maxY = 0
        #self.maxZ = 0
        #self.minX = 0
        #self.minY = 0
        #self.minZ = 0
        #self.punkte = punkte
        #self.getBoundingBox()
        #self.getScaleFactor()
        #self.getCenter()

        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)

    def toggle_shadow(self):
        self.shadow = not self.shadow
    def display(self,vboData):
        glClear(GL_COLOR_BUFFER_BIT)
        self.renderObject(vboData,False)
        if self.shadow:
            glPushMatrix()
            glTranslatef(self.light[0], self.light[1], self.light[2])
            glMultMatrixf(self.p)
            glTranslatef(-self.light[0], -self.light[1], -self.light[2])
            self.renderObject(vboData,True)
            glPopMatrix()

    def renderObject(self,vbo_data,shadow):
        myvbo = vbo.VBO(np.array(vbo_data,'f'))
        myvbo.bind()
        glClearColor(self.backgroundcolor[0],self.backgroundcolor[1],self.backgroundcolor[2],self.backgroundcolor[3])
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        glVertexPointer(3, GL_FLOAT, 24, myvbo)
        glNormalPointer(GL_FLOAT, 24, myvbo + 12)


        #self.scale()
        #glTranslate(self.center[0], self.center[1], self.center[2])
        #glTranslate(self.x_translate, self.y_translate, 0)
        glMultMatrixf(self.actOri* self.rotate())
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        if shadow:
            glColor3fv([0., 0., 0.])
        else:
            glColor3f(self.color[0], self.color[1], self.color[2])

        glDrawArrays(GL_TRIANGLES, 0, len(vbo_data))
        myvbo.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)



    def rotate(self):
        c, mc = math.cos(self.angle), 1 - math.cos(self.angle)
        s = math.sin(self.angle)
        l = math.sqrt(np.dot(np.array(self.axis), np.array(self.axis)))
        #print("l ", l, "  axis", self.axis)
        x, y, z = np.array(self.axis) / l
        r = np.matrix(
            [[x * x * mc + c, x * y * mc - z * s, x * z * mc + y * s, 0],
             [x * y * mc + z * s, y * y * mc + c, y * z * mc - x * s, 0],
             [x * z * mc - y * s, y * z * mc + x * s, z * z * mc + c, 0],
             [0, 0, 0, 1]]
        )

        return r.transpose()


    def zoom(self,scale):
        scale_factor = 1 + scale / 100.
        glScale(scale_factor, scale_factor, scale_factor)

   
    def move(self,x_translate, y_translate):
        glTranslate(x_translate, y_translate, 0)

    #def getBoundingBox(self):
    #    for counter in self.punkte:
    #        point = self.punkte[counter]
    #        if (self.maxX < point[0]):
    #            self.maxX = point[0]
    #        if (self.maxY < point[1]):
    #            self.maxY = point[1]
    #        if (self.maxZ < point[2]):
    #            self.maxZ = point[2]
    #        if (self.minX > point[0]):
    #            self.minX = point[0]
    #        if (self.minY > point[1]):
    #            self.minY = point[1]
    #        if (self.minZ > point[2]):
    #            self.minZ = point[2]
    #    print("MaxX:", self.maxX)
    #    print("MaxY:", self.maxY)
    #    print("MaxZ:", self.maxZ)
    #    print("minX:", self.minX)
    #    print("minY:", self.minY)
    #    print("minZ:", self.minZ)

    #def getScaleFactor(self):
    #    x = self.maxX - self.minX
    #    y = self.maxY - self.minY
    #    z = self.maxZ - self.minZ
    #    print("X Seite", x)
    #    print("Y Seite", y)
    #    print("Z Seite", z)
    #    list = [x, y, z]
    #    self.scalefactor = 2 / max(list)
    #    print("Scalefactor: ", self.scalefactor)


    #def scale(self):
    #    glScalef(self.scalefactor, self.scalefactor, self.scalefactor)

    #def getCenter(self):
    #    self.center = np.array([self.maxX / 2, self.maxY / 2, self.maxZ / 2])
    #    print("Center:", self.center)
