
import logging
from glfw import *
from OpenGL.GL import *

import numpy as np
# create logger for the context of this function
logger = logging.getLogger(__name__)

import time
from pyglui import ui
from pyglui.cygl.utils import init
from pyglui.cygl.utils import RGBA

from pyglui.pyfontstash import fontstash as fs

width, height = (1280,720)


def basic_gl_setup():
    glEnable(GL_POINT_SPRITE )
    glEnable(GL_VERTEX_PROGRAM_POINT_SIZE) # overwrite pointsize
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glClearColor(.8,.8,.8,1.)
    glEnable(GL_LINE_SMOOTH)
    # glEnable(GL_POINT_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)


def adjust_gl_view(w,h,window):
    """
    adjust view onto our scene.
    """

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, w, h, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



def clear_gl_screen():
    glClearColor(.9,.9,0.9,1.)
    glClear(GL_COLOR_BUFFER_BIT)


def demo():
    global quit
    quit = False

    # Callback functions
    def on_resize(window,w, h):
        h = max(h,1)
        w = max(w,1)
        hdpi_factor = glfwGetFramebufferSize(window)[0]/glfwGetWindowSize(window)[0]
        w,h = w*hdpi_factor,h*hdpi_factor
        gui.update_window(w,h)
        active_window = glfwGetCurrentContext()
        glfwMakeContextCurrent(window)
        # norm_size = normalize((w,h),glfwGetWindowSize(window))
        # fb_size = denormalize(norm_size,glfwGetFramebufferSize(window))
        adjust_gl_view(w,h,window)
        glfwMakeContextCurrent(active_window)


    def on_iconify(window,iconfied):
        pass

    def on_key(window, key, scancode, action, mods):
        gui.update_key(key,scancode,action,mods)

        if action == GLFW_PRESS:
            if key == GLFW_KEY_ESCAPE:
                on_close(window)

    def on_char(window,char):
        gui.update_char(char)

    def on_button(window,button, action, mods):
        gui.update_button(button,action,mods)
        # pos = normalize(pos,glfwGetWindowSize(window))
        # pos = denormalize(pos,(frame.img.shape[1],frame.img.shape[0]) ) # Position in img pixels

    def on_pos(window,x, y):
        hdpi_factor = float(glfwGetFramebufferSize(window)[0]/glfwGetWindowSize(window)[0])
        x,y = x*hdpi_factor,y*hdpi_factor
        gui.update_mouse(x,y)

    def on_scroll(window,x,y):
        gui.update_scroll(x,y)

    def on_close(window):
        global quit
        quit = True
        logger.info('Process closing from window')


    # get glfw started
    glfwInit()
    version = 2,1
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, version[0])
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, version[1])
    # glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, 1)
    # glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

    window = glfwCreateWindow(width, height, "pyglui demo", None, None)
    if not window:
        exit()

    glfwSetWindowPos(window,0,0)
    # Register callbacks window
    glfwSetWindowSizeCallback(window,on_resize)
    glfwSetWindowCloseCallback(window,on_close)
    glfwSetWindowIconifyCallback(window,on_iconify)
    glfwSetKeyCallback(window,on_key)
    glfwSetCharCallback(window,on_char)
    glfwSetMouseButtonCallback(window,on_button)
    glfwSetCursorPosCallback(window,on_pos)
    glfwSetScrollCallback(window,on_scroll)


    glfwSwapInterval(1)
    glfwMakeContextCurrent(window)
    init()
    basic_gl_setup()

    print('GL:',glGetString(GL_VERSION))
    print('GLFW3:',glfwGetVersionString())
    class Temp(object):
        """Temp class to make objects"""
        def __init__(self):
            pass

    foo = Temp()
    foo.bar = 34
    foo.bur = 4
    foo.mytext = [203,12]
    foo.myswitch = 10
    foo.select = 'Tiger'
    foo.record = False
    foo.calibrate = False
    foo.stream = True
    foo.test = False


    d = {}

    d['one'] = 1
    def print_hello():
        foo.select = 'Cougar'
        gui.scale += .1
        print 'hello'

        # m.configuration = sidebar.configuration

    def printer(val):
        print 'setting to :',val


    print "pyglui version: %s" %(ui.__version__)
    gui = ui.UI()
    gui.scale = 1.0
    sidebar = ui.Scrolling_Menu("MySideBar",pos=(-300,0),size=(0,0),header_pos='left')

    for x in range(10):
        sidebar.append(ui.Slider("one",d,label="bar %s"%x))
        sidebar.append(ui.Slider("bur",foo,label="bur %s"%x))
        sm = ui.Growing_Menu("SubMenu",pos=(0,0),size=(0,100))
        sm.toggle_iconified()
        sm.append(ui.Slider("bar",foo))
        sm.append(ui.Text_Input('mytext',foo,setter=printer))
        ssm = ui.Growing_Menu("SubSubMenu",pos=(0,0),size=(0,100))
        ssm.append(ui.Slider("bar",foo))
        ssm.append(ui.Text_Input('mytext',foo,setter=printer))
        ssm.toggle_iconified()

        sm.append(ssm)

        sidebar.append(sm)
        sm.append(ui.Selector('select',foo,selection=['Tiger','Lion','Cougar','Hyena']) )

        sm.append(ui.Button("Say Hi!",print_hello))
        sm.append(ui.Button("Say Hi!",print_hello))
        sm.append(ui.Button("Say Hi!",print_hello))
    gui.append(sidebar)


    m = ui.Scrolling_Menu("MyMenu",pos=(250,30),size=(300,500),header_pos='top')
    for x in range(1):
        m.append(ui.Info_Text("This is my multiline info text. I wonder if multilines break as designed... How does it look? Info Text with long label text to test multiline break handling." ))
        m.append(ui.Selector('select',foo,selection=['Tiger','Lion','Cougar','Hyena'],setter=printer) )
        m.append(ui.Slider("bur",foo,step=50,min=1,max=1005, label="Slider label with long label text to test overflow handling"))
        m.append(ui.Button("Say Hi!",print_hello))
        m.append(ui.Button("Say Hi!",print_hello))
        m.append(ui.Switch("myswitch",foo,on_val=1000,off_val=10,label="Switch Me"))

        m.append(ui.Button("Say Hi!",print_hello))
        sm = ui.Growing_Menu("SubMenu",pos=(0,0),size=(0,100))
        sm.append(ui.Slider("bar",foo))

        sm.append(ui.Text_Input('mytext',foo))
        sm.append(ui.Text_Input('mytext',foo))
        m.append(sm)
        m.append(ui.Button("Say Hi!",print_hello))

    # m.elements[0].read_only = True
    # m.elements[1].read_only = True
    # m.elements[2].read_only = True
    # sm.elements[1].read_only = True
    # sm.elements[1].read_only = True

    rightbar = ui.Stretching_Menu('Right Bar',(0,100),(150,-100))
    rightbar.append(ui.Thumb("record",foo,label="Record") )
    rightbar.append(ui.Thumb("calibrate",foo,label="Calibrate") )
    rightbar.append(ui.Thumb("stream",foo,label="Stream") )
    rightbar.append(ui.Thumb("test",foo,label="Test") )
    gui.append(rightbar)
    gui.append(m)

    m.color.a = 0


    import os
    import psutil
    pid = os.getpid()
    ps = psutil.Process(pid)
    ts = time.time()

    from pyglui import graph
    print graph.__version__
    cpu_g = graph.Line_Graph()
    cpu_g.pos = (50,100)
    cpu_g.update_fn = ps.get_cpu_percent
    cpu_g.update_rate = 5
    cpu_g.label = 'CPU %0.1f'

    fps_g = graph.Line_Graph()
    fps_g.pos = (50,100)
    fps_g.update_rate = 5
    fps_g.label = "%0.0f FPS"
    fps_g.color[:] = .1,.1,.8,.9

    st_graph = graph.Averaged_Value()
    st_graph.pos = (200,200)
    st_graph.update_rate = 5
    st_graph.label = "Slider Value: %0.0f"
    st_graph.color[:] = 1.,0.,.6,.9


    on_resize(window,*glfwGetWindowSize(window))
    # gui.update()
    # on_resize(window,*glfwGetWindowSize(window))

    glfont = fs.Context()
    glfont.add_font('opensans','../pyglui/OpenSans-Regular.ttf')
    glfont.set_size(14)
    font_color = .1,.1,.7,.9
    glfont.set_color_float(font_color)


    import numpy as np
    from pyglui.cygl import utils

    a = (np.random.random_sample((200,200,3))*200).astype(dtype=np.uint8)
    tex = utils.create_named_texture(a.shape)
    utils.update_named_texture(tex,a)
    while not quit:
        dt,ts = time.time()-ts,time.time()
        clear_gl_screen()
        # utils.draw_polyline( [(20,20),(500,500)] )

        # gui.scale +=.001
        # print gui.scale
        cpu_g.update()
        cpu_g.draw()
        fps_g.add(1./dt)
        fps_g.draw()
        st_graph.add(foo.bur)
        st_graph.draw()
        # foo.bar += .1
        # if foo.bar >= 100:
            # foo.bar = 0
        utils.update_named_texture(tex,a)
        utils.draw_named_texture(tex,quad=((400.,400.),(600.,400.),(600.,600.),(400.,600.)))
        glfont.draw_text(400,390,"This is pyfontstash text.")
        glfont.draw_text(400,620,"The square (above) is a texture with random colors.")

        gui.update()
        # tex = utils.create_named_texture(a.shape)
        # a = (np.random.random_sample((1280,720,1))*100).astype(dtype=np.uint8)
        # utils.draw_gl_texture(a)
        glfwSwapBuffers(window)
        glfwPollEvents()
        # time.sleep(.03)

    glfwDestroyWindow(window)
    glfwTerminate()
    logger.debug("Process done")

if __name__ == '__main__':
    if 1:
        demo()
    else:
        import cProfile,subprocess,os
        cProfile.runctx("demo()",{},locals(),"example.pstats")
        gprof2dot_loc = 'gprof2dot.py'
        subprocess.call("python "+gprof2dot_loc+" -f pstats example.pstats | dot -Tpng -o example_profile.png", shell=True)
        print "created cpu time graph for example. Please check out the png next to this."
