#coding:utf-8


# 材料 http://devernay.free.fr/cours/opengl/materials.html

SCREEN_SIZE = (800, 600)

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


def run():

    frame = 1
    temp = 2000
    intensity = 0.0
    df_material = pd.read_csv("materials.csv", index_col = "Name")    
    
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
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
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
    
        frame += 1
        
        from color_temp import color_temp

        temp = 3000
        c = color_temp(temp)

        if temp > 9000:
            temp = 2000        
        if frame % 100 == 0:
            temp = int(temp * 1.08)

        #intensity = ( 9000 - bl ) / 2000.0
        intensity += 0.01
        if intensity > 1.0:
            intensity = 0.0

        #print("color_temp = %d, intensity = %d" %(bl, intensity * 100))
        print("color_temp = %d, intensity = %d" %(temp, intensity * 100))

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


        table_leg_height = 3.
        table_leg_width = 1.
        table_plane_height = 1.
        table_plane_width = 5.
        table_px = 1.
        table_pz = 1.

        wall_width = 10.0
        wall_thick = 0.5

        glMatrixMode(GL_MODELVIEW)

        #wall_x
        glPushMatrix()
        setMaterial(df_material, "ruby")
        glTranslate(-wall_thick / 2.0, wall_width / 2.0, wall_width / 2.0)
        glScale(wall_thick, wall_width, wall_width)
        glutSolidCube(1)        
        glPopMatrix()


        #wall_y
        glPushMatrix()
        setMaterial(df_material, "ruby")
        glTranslate(wall_width / 2.0, -wall_thick / 2.0, wall_width / 2.0)
        glScale(wall_width, wall_thick, wall_width)
        glutSolidCube(1)        
        glPopMatrix()

        #wall_z
        glPushMatrix()
        setMaterial(df_material, "ruby")
        glTranslate(wall_width / 2.0, wall_width / 2.0, -wall_thick / 2.0)
        glScale(wall_width, wall_width, wall_thick)
        glutSolidCube(1)        
        glPopMatrix()



        #teapot
        glPushMatrix()
        setMaterial(df_material, "ruby")
        glutSolidTeapot(0.2)
        glPopMatrix()



        # Show the screen
        pygame.display.flip()

run()