import glfw
from Scene import Scene
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from numpy import array
import sys,math,os
import numpy as np





class RenderWindow:
    """GLFW Rendering window class"""

    #def __init__(self,width,height,vbo_Data,vertex_Data):
    def __init__(self, width, height, vbo_Data):
        # save current working directory
        cwd = os.getcwd()

        # Initialize the library
        if not glfw.init():
            return

        # restore cwd
        os.chdir(cwd)

        # buffer hints
        glfw.window_hint(glfw.DEPTH_BITS, 32)

        # define desired frame rate
        self.frame_rate = 100

        # make a window
        self.width, self.height = width,height
        self.aspect = self.width / float(self.height)
        self.window = glfw.create_window(self.width, self.height, "3D Graphics - Abgabe 2", None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)


        self.myvbo = vbo_Data
        #self.punkte = vertex_Data

        self.doRotation= False
        self.doTranslate = False
        self.pressedShift = False


        self.startP = (0,0,0)
        self.actX = None
        self.actY = None
        self.zoomfactor = 0

        # initialize GL - window
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.2, 0.0, 0.8, 0.5)#background color
        glMatrixMode(GL_PROJECTION)
        self.isOrthogonal = True
        self.set_orthogonal()

        # set window callbacks
        glfw.set_mouse_button_callback(self.window, self.onMouseButton)
        glfw.set_key_callback(self.window, self.onKeyboard)
        glfw.set_scroll_callback(self.window,self.onMouseScroll)
        glfw.set_cursor_pos_callback(self.window,self.onMouseMove)
        glfw.set_window_size_callback(self.window,self.WindowSizeChange)

        # create 3D
        #self.scene = Scene(self.width, self.height,self.punkte)
        self.scene = Scene(self.width, self.height)
        self.scene.move(0,-1)
        # exit flag
        self.exitNow = False

    def projectOnSphere(self,x, y, r):
        x, y = x - self.width / 2.0, self.height / 2.0 - y
        a = min(r * r, x ** 2 + y ** 2)
        z = math.sqrt(r * r - a)
        l = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        return x / l, y / l, z / l



    def onMouseScroll(self,win,x_offset,y_offset):
        if y_offset < 0 and self.zoomfactor > 0 or y_offset > 0 and self.zoomfactor < 0:
            self.zoomfactor = y_offset
        else:
            self.zoomfactor = self.zoomfactor + y_offset
        self.scene.zoom(self.zoomfactor)

    def onMouseMove(self,win,x_pos,y_pos):
        r = min(self.width, self.height) / 2.0
        if self.doRotation:
            moveP = self.projectOnSphere(x_pos, y_pos, r)
            if moveP == self.startP:
                return
            self.scene.angle = np.arccos(np.dot(self.startP, moveP))
            self.scene.axis = np.cross(self.startP, moveP)
        if self.doTranslate:
            print("PosX and PosY:  ", x_pos, " ", y_pos)
            print("startX and startY: ", self.actX, " ", self.actY)
            x_dir, y_dir = x_pos - self.actX, self.actY - y_pos
            self.scene.move(x_dir / self.width, y_dir / self.height)
            #self.scene.x_translate=x_dir/self.width
            #self.scene.y_translate=y_dir/self.height
        self.startP = self.projectOnSphere(x_pos,y_pos,r)
        self.actX = x_pos
        self.actY = y_pos

    def WindowSizeChange(self,win,width,height):
        self.width = width
        self.height = height
        if self.isOrthogonal:
            self.set_orthogonal()
        else:
            self.set_projective()

    def onMouseButton(self,win, button, action, mods):
        """Linke Maustaste : Arcball Rotierung"""
        """Rechte Maustaste: verschiebung"""
        if button == glfw.MOUSE_BUTTON_LEFT:
            if (action == glfw.PRESS):
                self.doRotation = True
            if (action == glfw.RELEASE):
                self.doRotation = False
                self.scene.angle = 0
                self.scene.actOri= self.scene.actOri*self.scene.rotate()



        if button == glfw.MOUSE_BUTTON_RIGHT :
            if action == glfw.PRESS:
                self.doTranslate = True
            if action == glfw.RELEASE:
                self.doTranslate = False




    def onKeyboard(self,win, key, scancode, action, mods):
        """
        O und P wechsel zwischen Zentral u. Orthogonal Projektion
        S,W,R,B,G wechsel der Hintergrundfarben
        H an- und ausschalten von Schatten  """

        print("keyboard: ", win, key, scancode, action, mods)

        if key == glfw.KEY_ESCAPE:
            self.exitNow = True

        if key == glfw.KEY_LEFT_SHIFT:
            if action == glfw.PRESS:
                self.pressedShift = True
                return

            if action == glfw.RELEASE:
                self.pressedShift = False
                return

            return

        if key == glfw.KEY_S:
            if self.pressedShift:
                self.scene.backgroundcolor = (0.0, 0.0, 0.0, 0.0)
                return
            else:
                self.scene.color = (0.0,0.0,0.0)
                return



        if key == glfw.KEY_W:
            if self.pressedShift:
                self.scene.backgroundcolor = (1.0, 1.0, 1.0, 1.0)
                return
            else:
                self.scene.color=(1.0,1.0,1.0)
                return



        if key == glfw.KEY_R:
            if self.pressedShift:
                self.scene.backgroundcolor=(1.0, 0.0, 0.0, 0.0)
            else:
                self.scene.color = (1.0, 0.0, 0.0)


        if key == glfw.KEY_B:
            if self.pressedShift:
                self.scene.backgroundcolor = (0.0, 0.0, 1.0, 0.0)
            else:
                self.scene.color = (0.0, 0.0, 1.0)


        if key == glfw.KEY_G:
            if self.pressedShift:
                self.scene.backgroundcolor = (0.0, 1.0, 0.0, 0.0)
            else:
                self.scene.color = (0.0, 1.0, 0.0)

        if key == glfw.KEY_H:
            if action == glfw.RELEASE:
                self.scene.toggle_shadow()

        if key == glfw.KEY_O:
            self.isOrthogonal = True
            self.set_orthogonal()

        if key == glfw.KEY_P:
            self.isOrthogonal = False
            self.set_projective()


    def run(self):

        # initializer timer
        glfw.set_time(0.0)
        t = 0.0
        while not glfw.window_should_close(self.window) and not self.exitNow:
            # update every x seconds
            currT = glfw.get_time()
            if currT - t > 1.0 / self.frame_rate:
                # update time
                t = currT
                # clear
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                self.scene.display(self.myvbo)

                glfw.swap_buffers(self.window)
                # Poll for and process events
                glfw.poll_events()
        # end
        glfw.terminate()


    def set_orthogonal(self):
        self.aspect = self.width / float(self.height)

        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if self.width <= self.height:
            glOrtho(
                -1.5, 1.5,
                -1.5 * self.height / self.width, 1.5 * self.height / self.width,
                -4.0, 10.0
            )
        else:
            glOrtho(
                -1.5 * self.width / self.height, 1.5 * self.width / self.height,
                -1.5, 1.5,
                -4.0, 10.0
            )

        glMatrixMode(GL_MODELVIEW)
        glShadeModel(GL_SMOOTH)

    def set_projective(self):
        self.aspect = self.width / float(self.height)

        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if self.width <= self.height:
            glFrustum(
                -1.0, 1.0,
                -1.0 * self.height / self.width, 1.0 * self.height / self.width,
                1.5, 20.0
            )
        else:
            glFrustum(
                -1.0 * self.width / self.height, 1.0 * self.width / self.height,
                -1.0, 1.0,
                1.5, 20.0
            )

        gluLookAt(
            0, 0, 4,
            0, 0, 0,
            0, 1, 0
        )

        glMatrixMode(GL_MODELVIEW)
        glShadeModel(GL_SMOOTH)
