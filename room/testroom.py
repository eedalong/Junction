#coding:utf-8


# 材料 http://devernay.free.fr/cours/opengl/materials.html

SCREEN_SIZE = (650, 350)

import multiprocessing
import os


from math import radians 

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pygame
from pygame.locals import *

from gameobjects.matrix44 import *
from gameobjects.vector3 import *

import pandas as pd

def resize(width, height):
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    
    glEnable(GL_DEPTH_TEST)
    
    glShadeModel(GL_FLAT)
    #glClearColor(2./255, 124./255, 219./255, 0.0)
    glClearColor(0, 0, 0, 0)

    glEnable(GL_COLOR_MATERIAL)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)        
    glLight(GL_LIGHT0, GL_POSITION,  (5.0, 5.0, 5.0, 1.0))
    glLight(GL_LIGHT0,  GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    
class Entity(object):
    def __init__(self):
        self._matrix = Matrix44()

    def render(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glColor3f(*self.color)      # color
        #glMultMatrixf(self._matrix.to_opengl()) # attitude and position
        glScalef(*self.scale)            

        self.unit_render()

        glPopMatrix()

class Teapot(Entity):
    def __init__(self, position = (0.0, 0.0, 0.0), color = (1.0, 1.0, 1.0), scale = (1.0, 1.0, 1.0)):
        super(Teapot, self).__init__()
        self.position = position
        self.color = color
        self.scale = scale

    def unit_render(self):
        glTranslate(*self.position)
        print(self.scale)
        print('self.scale')
        glutSolidTeapot(10)

class Cube(Entity):
    
    
    def __init__(self, position = (0.0, 0.0, 0.0), color = (1.0, 1.0, 1.0), scale = (1.0, 1.0, 1.0)):
        super(Cube, self).__init__()
        self.position = position
        self.color = color
        self.scale = scale
    
    num_faces = 6
        
    vertices = [ (0.0, 0.0, 1.0),
                 (1.0, 0.0, 1.0),
                 (1.0, 1.0, 1.0),
                 (0.0, 1.0, 1.0),
                 (0.0, 0.0, 0.0),
                 (1.0, 0.0, 0.0),
                 (1.0, 1.0, 0.0),
                 (0.0, 1.0, 0.0) ]
        
    normals = [ (0.0, 0.0, +1.0),  # front
                (0.0, 0.0, -1.0),  # back
                (+1.0, 0.0, 0.0),  # right
                (-1.0, 0.0, 0.0),  # left 
                (0.0, +1.0, 0.0),  # top
                (0.0, -1.0, 0.0) ] # bottom
    
    vertex_indices = [ (0, 1, 2, 3),  # front
                       (4, 5, 6, 7),  # back
                       (1, 5, 6, 2),  # right
                       (0, 4, 7, 3),  # left
                       (3, 2, 6, 7),  # top
                       (0, 1, 5, 4) ] # bottom    

    def unit_render(self):    

    
        # Adjust all the vertices so that the cube is at self.position
        vertices = [tuple(Vector3(v) + self.position) for v in self.vertices]
            
        # Draw all 6 faces of the cube
        glBegin(GL_QUADS)
    
        for face_no in xrange(self.num_faces):
                        
            glNormal3dv( self.normals[face_no] )
            
            v1, v2, v3, v4 = self.vertex_indices[face_no]
                    
            glVertex( vertices[v1] )
            glVertex( vertices[v2] )
            glVertex( vertices[v3] )
            glVertex( vertices[v4] )            
        
        glEnd()


def setMaterial(df, name):
    mat = [0,0,0,0]
    mat[0] = df.loc[name]["Ambient_r"];
    mat[1] = df.loc[name]["Ambient_g"];
    mat[2] = df.loc[name]["Ambient_b"];
    mat[3] = 1.0;
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat);
    mat[0] = df.loc[name]["Diffuse_r"];
    mat[1] = df.loc[name]["Diffuse_g"];
    mat[2] = df.loc[name]["Diffuse_b"];
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat);
    mat[0] = df.loc[name]["Specular_r"];
    mat[1] = df.loc[name]["Specular_g"];
    mat[2] = df.loc[name]["Specular_b"];
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat);
    shine = df.loc[name]["Shininess"]
    glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0);

def updateLevel(fname = 'level.txt'):
    return int(open(fname, 'r').read().strip())

def updateColor(fname = 'color.txt'):
    return int(open(fname, 'r').read().strip())

def run(conn):


    bl = 1
    temp = 2000
    intensity = 0.0
    df_material = pd.read_csv("materials.csv", index_col = "Name")


    global angle, angle2,moving,startx,starty;
    angle = 0;
    angle2 = 0;
    moving = 0;
    startx = 0
    starty = 0
    
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
    
    resize(*SCREEN_SIZE)
    init()
    
    clock = pygame.time.Clock()    
    
    glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))    
    glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))


    

    # Camera transform matrix
    camera_matrix = Matrix44()
    camera_matrix.translate = (20., 20., 20.)

    # Initialize speeds and directions
    rotation_direction = Vector3()
    rotation_speed = radians(90.0)
    movement_direction = Vector3()
    movement_direction.set(0.0, 0.0, -1.0)
    movement_speed = 2.0    

    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                conn.close()
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                conn.close()
                return                
            
        # Clear the screen, and z-buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                        
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.
        
        pressed = pygame.key.get_pressed()
        
        # Reset rotation and movement directions
        rotation_direction.set(0.0, 0.0, 0.0)
        movement_direction.set(0.0, 0.0, 0.0)
        
        # Modify direction vectors for key presses
        if pressed[K_LEFT]:
            #rotation_direction.y = +1.0
            rotation_direction.y = +1.0
        elif pressed[K_RIGHT]:
            #rotation_direction.y = -1.0
            rotation_direction.y = -1.0
        if pressed[K_UP]:
            rotation_direction.x = +1.0
        elif pressed[K_DOWN]:
            rotation_direction.x = -1.0
        if pressed[K_e]:
            rotation_direction.z = -1.0
        elif pressed[K_q]:
            rotation_direction.z = +1.0            
        if pressed[K_w]:            
            movement_direction.z = -1.0
        elif pressed[K_s]:
            movement_direction.z = +1.0
        if pressed[K_a]:            
            movement_direction.x = -1.0
        elif pressed[K_d]:
            movement_direction.x = +1.0
        if pressed[K_r]:            
            movement_direction.y = +1.0
        elif pressed[K_f]:
            movement_direction.y = -1.0
        if pressed[K_SPACE]:
            movement_direction.x = 0.0
            movement_direction.y = 0.0
            movement_direction.z = 0.0
            print('rotation_direction.z=%f, rotation.z=%f, camera_matrix=' %(rotation_direction.z,rotation.z))
            print(camera_matrix)            
            print('movement_direction',movement_direction)
            
            if rotation.z >= 1.0:
                rotation_direction.z = 1.0
            elif rotation.z <= -1.0:
                rotation_direction.z = 1.0
        
        # Calculate rotation matrix and multiply by camera matrix    
        rotation = rotation_direction * rotation_speed * time_passed_seconds

        rotation_matrix = Matrix44.xyz_rotation(*rotation)      

        camera_matrix *= rotation_matrix
        
        # Calcluate movement and add it to camera matrix translate
        heading_z = Vector3(camera_matrix.forward)        
        heading_x = Vector3(camera_matrix.right)        
        heading_y = Vector3(camera_matrix.up)        
        movement = (heading_x * movement_direction.x + heading_y * movement_direction.y + heading_z * movement_direction.z) * movement_speed
        camera_matrix.translate += movement * time_passed_seconds
        
        # Upload the inverse camera matrix to OpenGL
        glLoadMatrixd(camera_matrix.get_inverse().to_opengl())
                
        # Light must be transformed as well
        #glLight(GL_LIGHT0, GL_POSITION,  (0, 1.5, 1, 0)) 
        #glLight(GL_LIGHT0, GL_POSITION,  (5.0, 5.0, 5.0, 1.0)) 
    
        bl += 1
        
        from color_temp import color_temp

        #temp = 3000
        temp = updateColor()
        c = color_temp(temp)

        if temp > 9000:
            temp = 2000        
        if bl % 100 == 0:
            temp = int(temp * 1.08)

        #intensity = ( 9000 - bl ) / 2000.0

        #intensity += 0.01
        #if intensity > 1.0:
        #   intensity = 0.0

        intensity = updateLevel() / 100.
        

#        print("color_temp = %d, intensity = %d" %(temp, intensity * 100))


        #lightIntensity =[ 0.0, (255) / 255., 0, 1.0];
        lightIntensity = [c[0]*intensity, c[1]*intensity, c[2]*intensity, 1.0];

        #light_position =[ 2.0,6.0,3.0,0.0];
        light_position =[ 10.0,10.0, 10, 1.0];
        glLightfv(GL_LIGHT0 ,GL_POSITION,light_position);
        glLightfv(GL_LIGHT0 ,GL_DIFFUSE,lightIntensity);
        # if bl % 100 > 50:
        #     print("glEnable(GL_LIGHTING)")
        #     #glEnable(GL_LIGHTING)
        #     glLightfv(GL_LIGHT0, GL_SPECULAR, (0.0, 1.0, 0.0, 1.0))
        # else:
        #     print("glDisable(GL_LIGHTING)")
        #     #glDisable(GL_LIGHTING)
        #     glLightfv(GL_LIGHT0, GL_SPECULAR, (0.0, 0.0, 1.0, 1.0))
        

    
        #glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))    
        #glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))


        table_leg_height = 3;
        table_leg_width = 1
        table_plane_height = 1
        table_plane_width = 5
        table_px = 1
        table_pz = 1


        #teapot = Teapot(position = (table_plane_width, table_leg_height + table_plane_height, table_plane_width), scale = (0.1, 0.1, 0.1))
        #teapot.render()


        setMaterial(df_material, "pearl") #珍珠 http://devernay.free.fr/cours/opengl/materials.html
        wall_x = Cube(position = (0, 0, 0), scale = (1, 15, 15), color = (0.8, 0.8, 0.8))
        wall_x.render()


        wall_y = Cube(position = (0, 0, 0), scale = (15, 1, 15), color = (0.8, 0.8, 0.8))
        #setMaterial(df_material, "chrome") #铬
        setMaterial(df_material, "pearl") #珍珠
        wall_y.render()

        wall_z = Cube(position = (0, 0, 0), scale = (15, 15, 1), color = (0.8, 0.8, 0.8))
        #setMaterial(df_material, "white rubber") #白色橡胶
        setMaterial(df_material, "pearl") #珍珠
        wall_z.render()
        
                
        #table_leg_00 = Cube(position = (table_px, 0, table_pz), scale = (table_leg_width, table_leg_height, table_leg_width))
        #table_leg_01 = Cube(position = (table_px, 0, table_pz + table_plane_width - table_leg_width), scale = (table_leg_width, table_leg_height, table_leg_width))
        #table_leg_10 = Cube(position = (table_px + table_plane_width - table_leg_width, 0, table_pz), scale = (table_leg_width, table_leg_height, table_leg_width))
        #table_leg_11 = Cube(position = (table_px + table_plane_width - table_leg_width, 0, table_pz + table_plane_width - table_leg_width), scale = (table_leg_width, table_leg_height, table_leg_width))
        table_plane = Cube(position = (table_px, table_leg_height, table_pz), scale = (table_plane_width, table_plane_height, table_plane_width), color = (0.8, 0.3, 0.3))
        setMaterial(df_material, "ruby") #红宝石
        table_plane.render()

     

        #for e in [wall_x, wall_y, wall_z, table_plane]:
        #    e.render()
                
        # Show the screen
        pygame.display.flip()


if __name__ == '__main__':
    conn_a,conn_b=multiprocessing.Pipe() #创建一个管道，两个口
    print(id(conn_a),id(conn_b))
    print(type(conn_a), type(conn_b)) #multiprocessing.connection.PipeConnection类型
    p=multiprocessing.Process(target=run,args=(conn_a,))
    #p.start()
    #conn_b.send([1,2,3])
    #print("Main Proc:",os.getpid(),conn_b.recv())
    #p.join()

    run(None)