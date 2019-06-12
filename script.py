import mdl
import sys
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands ) ==========
  Checks the commands array for any animation commands
  (frames, basename, vary)
  Should set num_frames and basename if the frames
  or basename commands are present
  If vary is found, but frames is not, the entire
  program should exit.
  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):

    name = 'base'
    num_frames = 1

    frames_exist = 0
    vary_exist = 0
    base_exist = 0

    for command in commands:
        print command
        c = command['op']
        args = command['args']
        if c == 'frames':
            num_frames = int(args[0])
            frames_exist = 1
        elif c == 'basename':
            name = args[0]
            base_exist = 1
        elif c == 'vary':
            vary_exist = 1

    if frames_exist == 0 and vary_exist == 1:
        print 'vary found but not frame, exiting'
        sys.exit()
    if frames_exist == 1 and base_exist == 0:
        print 'use default basename "base"'

    return (name, num_frames)

"""======== second_pass( commands ) ==========
  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).
  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.
  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
def second_pass( commands, num_frames ):
    frames = [ {} for i in range(num_frames) ]
    # print frames
    for command in commands:
        if command['op'] == 'vary':
            start_frame = int( command['args'][0] )
            end_frame = int( command['args'][1] )

            start_value = command['args'][2]
            end_value = command['args'][3]
            delta = (end_value - start_value) / ( end_frame - start_frame )

            for i in range( end_frame - start_frame + 1):
                frames[start_frame + i][command['knob']] = start_value + delta * i
    # for i in range(len(frames)):
    #     print i
    #     print frames[i]
    return frames



def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
            0.75,
              1],
             [255,
              255,
            255]]

    color = [0, 0, 0]
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                        'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    [name, num_frames] = first_pass(commands)
    knobs = second_pass(commands, num_frames)


    for i in range(int(num_frames)):
        tmp = new_matrix()
        ident( tmp )

        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 20
        consts = ''
        coords = []
        coords1 = []

        if num_frames > 1:
            for knob in knobs[i]:
                symbols[knob][1] = knobs[i][knob]

        for command in commands:
            print command
            c = command['op']
            args = command['args']
            knob_value = 1

            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                           args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp,
                         args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                if command["knob"]:
                    knob_value = symbols[command["knob"]][1]
                tmp = make_translate(args[0] * knob_value, args[1] * knob_value, args[2] * knob_value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                if command["knob"]:
                    knob_value = symbols[command["knob"]][1]
                tmp = make_scale(args[0] * knob_value, args[1]* knob_value, args[2]* knob_value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                if command["knob"]:
                    knob_value = symbols[command["knob"]][1]
                theta = args[1] * (math.pi/180) * knob_value
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])
        if num_frames > 1:
            filename = 'anim/' + name + ('%03d' %int(i))
            print "file name: " + filename
            save_extension(screen,filename)

    if num_frames > 1:
        make_animation(name)
