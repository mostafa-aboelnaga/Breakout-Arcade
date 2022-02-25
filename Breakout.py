import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Some global variables #

# for controlling
mouse_x = 0
go = False
reset = False
lost = False
score300 = 0
y_shift = 0

# for score and lives/tries
current_score = 0
current_tries = 3

# for ball movement
first_x = 2
first_y = 1
first_direction_x = 1
first_direction_y = -1

# for blocks
blocks_container = []

# Main settings


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
    glutInitWindowSize(600, 800)

    glutCreateWindow("Breakout")

    glutDisplayFunc(display)
    glutTimerFunc(0, timer_func, 0)

    glutPassiveMotionFunc(mouse_control)
    glutKeyboardFunc(keyboard_control)

    # setting the view
    set_projection_settings()
    set_camera_settings()


def set_projection_settings():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(-10.5, 10.5, -10.5, 10.5, 1, 20)

    glMatrixMode(GL_MODELVIEW)


def set_camera_settings():
    gluLookAt(0, 0, 2, 0, 0, 0, 0, 1, 0)


def display():
    global go

    if go:
        glClearColor(0.1, 0.1, 0.1, 1)
    else:
        glClearColor(1, 1, 1, 1)

    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)

    if go == False and lost == False:
        draw_ui()
    elif go == True and lost == False:
        draw_rect_ball()
        draw_bat()
        draw_current_score()
        draw_current_tries()
        draw_blocks()
        draw_allsides()
    elif go == True and lost == True:
        draw_lost()

    glutSwapBuffers()


def draw_lost():
    glLineWidth(2)
    glColor(1, 1, 1, 1)

    glPushMatrix()
    glLoadIdentity()

    glTranslate(-4.2, 3, -2)
    glScale(0.01, 0.01, 1)
    glutStrokeString(GLUT_STROKE_ROMAN, b" GAMEOVER")

    glLoadIdentity()
    glTranslate(-4.5, 0, -2)
    glScale(0.005, 0.005, 1)
    glutStrokeString(GLUT_STROKE_ROMAN, b"PLAY AGAIN - PRESS ' p '")

    glPopMatrix()


def draw_ui():
    glLineWidth(2)
    glColor(0, 0, 0, 1)

    glPushMatrix()
    glLoadIdentity()

    glTranslate(-2, 3, -2)
    glScale(0.01, 0.01, 1)
    glutStrokeString(GLUT_STROKE_ROMAN, b"START")

    glLoadIdentity()
    glTranslate(-3.5, 0, -2)
    glScale(0.005, 0.005, 1)
    glutStrokeString(GLUT_STROKE_ROMAN, b"BY  PRESSING  ' s ' ")

    glPopMatrix()


def timer_func(v):
    display()
    glutTimerFunc(0, timer_func, 0)


def draw_current_score():
    global current_score
    glLineWidth(2)
    string_current_score = b"SCORE : " + str(current_score).encode()
    glPushMatrix()
    glLoadIdentity()

    glColor(1, 1, 1, 1)
    glTranslate(-9, -10, -2)
    glScale(0.005, 0.005, 1)
    glutStrokeString(GLUT_STROKE_ROMAN, string_current_score)
    glPopMatrix()


def draw_current_tries():
    global current_score
    glLineWidth(2)
    string_current_score = b"LIVES : " + str(current_tries).encode()
    glPushMatrix()
    glLoadIdentity()

    glColor(1, 1, 1, 1)
    glTranslate(6, -10, -2)
    glScale(0.005, 0.005, 1)
    glutStrokeString(GLUT_STROKE_ROMAN, string_current_score)
    glPopMatrix()


# Control functions (mouse and keyboard)

def mouse_control(x, y):
    global mouse_x
    mouse_x = ((x-300) / 30)
    if mouse_x >= 9:
        mouse_x = 9
    if mouse_x <= -9:
        mouse_x = -9


def keyboard_control(key, x, y):
    global go
    global lost
    global current_tries
    global current_score
    global y_shift
    global score300
    global blocks_container

    if key == b"s":
        go = True
    if key == b"p":
        if lost:
            # resetting everything
            lost = False
            current_score = 0
            current_tries = 3

            y_shift = 0
            score300 = 0
            for list_block in blocks_container:
                for block in list_block.block_list:
                    block.block_position[1] = block.reset_y
                    block.original_position_y = block.reset_y
                    block.hit = False

# Defining some shapes, for the player, ball and blocks

def draw_rect_ball():
    global first_x
    global first_y

    glPushMatrix()
    glLoadIdentity()

    first_x = first_x + 0.15*first_direction_x
    first_y = first_y + 0.15*first_direction_y

    check_bat()
    check_wall()

    glColor(1, 1, 1, 1)
    glTranslate(0, 0, -1)
    glTranslate(first_x, first_y, 0)
    glutSolidCube(0.3)
    glPopMatrix()


def draw_rectangle(v1x, v1y, v2x, v2y, v3x, v3y, v4x, v4y):
    z = -1
    glBegin(GL_POLYGON)
    glVertex(v1x, v1y, z)
    glVertex(v2x, v2y, z)
    glVertex(v3x, v3y, z)
    glVertex(v4x, v4y, z)
    glEnd()


def draw_allsides():
    glPushMatrix()
    glLoadIdentity()

    # side-white-low
    glColor(1, 1, 1, 1)
    draw_rectangle(12, -12, 10, -12, 10, 3, 12, 3)
    draw_rectangle(-12, -12, -10, -12, -10, 3, -12, 3)

    # side-blue
    glColor(0, 0, 1, 1)
    draw_rectangle(-12, -8, -10, -8, -10, -7.5, -12, -7.5)
    draw_rectangle(12, -8, 10, -8, 10, -7.5, 12, -7.5)

    # side-yellow
    glColor(1, 1, 0, 1)
    draw_rectangle(-12, 3, -10, 3, -10, 5, -12, 5)
    draw_rectangle(12, 3, 10, 3, 10, 5, 12, 5)

    # side-green
    glColor(0, 1, 0, 1)
    draw_rectangle(-12, 5, -10, 5, -10, 7, -12, 7)
    draw_rectangle(12, 5, 10, 5, 10, 7, 12, 7)

    # side-red
    glColor(1, 0, 0, 1)
    draw_rectangle(-12, 7, -10, 7, -10, 9, -12, 9)
    glColor(1, 0, 0, 1)
    draw_rectangle(12, 7, 10, 7, 10, 9, 12, 9)

    # side-blue-up
    glColor(0, 0, 1, 1)
    draw_rectangle(12, 9, 10, 9, 10, 10.5, 12, 10.5)
    draw_rectangle(-12, 9, -10, 9, -10, 10.5, -12, 10.5)
    draw_rectangle(-10, 10, -10, 10.5, 10, 10.5, 10, 10)

    glPopMatrix()


def draw_bat():
    global mouse_x
    bat_position = [mouse_x, -7.75]

    # drawing
    glColor(0, 0, 1, 1)
    glPushMatrix()
    glLoadIdentity()
    bat_shape(bat_position[0], bat_position[1])
    glPopMatrix()


def bat_shape(x, y):
    z = -1
    glBegin(GL_POLYGON)
    glVertex(x+1, y+0.25, z)
    glVertex(x+1, y-0.25, z)
    glVertex(x-1, y-0.25, z)
    glVertex(x-1, y+0.25, z)
    glEnd()


def fill_blocks():
    global blocks_container
    blocks_container = []
    y = 3

    for i in range(4):
        new_list = rect_list(y+0.75*i, [1, 0, 0])
        blocks_container.append(new_list)

    for i in range(4):
        new_list = rect_list(5+y+0.75*i, [0, 0, 1])
        blocks_container.append(new_list)

    for i in range(4):
        new_list = rect_list(10+y+0.75*i, [0, 1, 0])
        blocks_container.append(new_list)


def draw_blocks():
    global blocks_container
    global current_score
    global score300
    global y_shift

    if current_score - score300 >= 300:
        score300 = current_score
        y_shift -= 0.3

    for list_items in blocks_container:
        list_items.draw_list()


class rect_list:
    block_list = []
    list_position = None
    color = []

    def __init__(self, y_position, color):
        self.list_position = y_position
        self.color = color
        for i in range(8):
            new = rect_block([-8.6+(2.45*i), self.list_position], self.color)
            self.block_list.append(new)

    def draw_list(self):
        for item in self.block_list:
            item.draw_block()

    def clear_list(self):
        self.block_list = []


def rect_block_shape(x, y):
    z = -1
    glBegin(GL_POLYGON)
    glVertex(x+1, y+0.3, z)
    glVertex(x+1, y-0.3, z)
    glVertex(x-1, y-0.3, z)
    glVertex(x-1, y+0.3, z)
    glEnd()


class rect_block:
    block_position = [0, 0]
    hit = False
    color = []

    def __init__(self, position, block_color):
        self.block_position = position
        self.original_position_y = self.reset_y = position[1]
        self.color = block_color

    def draw_block(self):
        self.block_position[1] += y_shift

        glPushMatrix()
        glLoadIdentity()
        if self.hit == False:
            self.collision_test()
            glColor(self.color[0], self.color[1], self.color[2], 1)
            rect_block_shape(self.block_position[0], self.block_position[1])
        glPopMatrix()

        self.pass_test()
        self.block_position[1] = self.original_position_y

# Collision detection
    def collision_test(self):
        global first_direction_y
        global first_x
        global first_y
        global current_score
        global go
        global lost

        current_distance = math.sqrt(
            (self.block_position[0]-first_x)**2 + (self.block_position[1]-first_y)**2)
        if current_distance <= 1.0422:
            current_score += 100
            self.hit = True
            first_direction_y *= -1

    def pass_test(self):
        global lost
        if self.hit and self.block_position[1] <= 1:
            self.original_position_y += 15
            self.hit = False
        if self.hit == False and self.block_position[1] <= -7.25:
            lost = True


def check_bat():
    global first_direction_x
    global first_direction_y
    global first_x
    global first_y
    global current_tries
    global lost

    if first_y <= -11:
        if current_tries == 1:
            lost = True
        else:
            current_tries -= 1

        first_x = 2
        first_y = 1
        first_direction_x = 1
        first_direction_y = -1

    if first_x - mouse_x < 1 and first_x - mouse_x >= -1:
        if first_y >= -8 and first_y < -7.5:
            first_direction_y *= -1
            first_y = -7.5


def check_wall():
    global first_direction_x
    global first_direction_y
    global first_x
    global first_y

    if first_x >= 10:
        first_direction_x *= -1
    if first_x <= -10:
        first_direction_x *= -1
    if first_y >= 9.5:
        first_direction_y *= -1
        first_y = 9.3


# Lastly, the main section, where the magic starts

main()
fill_blocks()
glutMainLoop()