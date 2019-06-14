from display import *
from matrix import *
from gmath import *

def draw_scanline_phong(x0, z0, x1, z1, y, screen, zbuffer, view, ambient, light, symbols, reflect, lim0, lim1):
    if x0 > x1:
        tx = x0
        tz = z0
        x0 = x1
        z0 = z1
        x1 = tx
        z1 = tz
        temp = lim0
        lim0 = lim1
        lim1 = temp

    x = x0
    z = z0
    dz = (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0

    distance = x1 - x0 + 1
    x_color = lim0[0]
    y_color = lim0[1]
    z_color = lim0[2]
    dx_color = (lim1[0] - lim0[0]) / distance if distance != 0 else 0
    dy_color = (lim1[1] - lim0[1]) / distance if distance != 0 else 0
    dz_color = (lim1[2] - lim0[2]) / distance if distance != 0 else 0

    while x <= x1:
        pcolor = [ x_color, y_color, z_color]
        color = get_lighting(pcolor,view,ambient,light,symbols,reflect)
        plot(screen, zbuffer, color, x, y, z)

        x+= 1
        z+= dz
        x_color += dx_color
        y_color += dy_color
        z_color += dz_color

def scanline_phong(polygons, i, screen, zbuffer, colors, view, ambient, light, symbols, reflect):
    flip = False
    BOT = 0
    TOP = 2
    MID = 1

    points = [ (polygons[i][0], polygons[i][1], polygons[i][2], colors[0]),
               (polygons[i+1][0], polygons[i+1][1], polygons[i+1][2], colors[1]),
               (polygons[i+2][0], polygons[i+2][1], polygons[i+2][2], colors[2]) ]

    points.sort(key = lambda x: x[1])
    x0 = points[BOT][0]
    z0 = points[BOT][2]
    x1 = points[BOT][0]
    z1 = points[BOT][2]
    y = int(points[BOT][1])

    distance0 = int(points[TOP][1]) - y * 1.0 + 1
    distance1 = int(points[MID][1]) - y * 1.0 + 1
    distance2 = int(points[TOP][1]) - int(points[MID][1]) * 1.0 + 1

    dx0 = (points[TOP][0] - points[BOT][0]) / distance0 if distance0 != 0 else 0
    dz0 = (points[TOP][2] - points[BOT][2]) / distance0 if distance0 != 0 else 0
    dx1 = (points[MID][0] - points[BOT][0]) / distance1 if distance1 != 0 else 0
    dz1 = (points[MID][2] - points[BOT][2]) / distance1 if distance1 != 0 else 0


    x0_color = points[BOT][3][0]
    y0_color = points[BOT][3][1]
    z0_color = points[BOT][3][2]
    x1_color = points[BOT][3][0]
    y1_color = points[BOT][3][1]
    z1_color = points[BOT][3][2]
    dx0_color = (points[TOP][3][0] - points[BOT][3][0]) / distance0 if distance0 != 0 else 0
    dy0_color = (points[TOP][3][1] - points[BOT][3][1]) / distance0 if distance0 != 0 else 0
    dz0_color = (points[TOP][3][2] - points[BOT][3][2]) / distance0 if distance0 != 0 else 0
    dx1_color = (points[MID][3][0] - points[BOT][3][0]) / distance1 if distance1 != 0 else 0
    dy1_color = (points[MID][3][1] - points[BOT][3][1]) / distance1 if distance1 != 0 else 0
    dz1_color = (points[MID][3][2] - points[BOT][3][2]) / distance1 if distance1 != 0 else 0

    while y <= int(points[TOP][1]):
        if ( not flip and y >= int(points[MID][1])):
            flip = True

            dx1 = (points[TOP][0] - points[MID][0]) / distance2 if distance2 != 0 else 0
            dz1 = (points[TOP][2] - points[MID][2]) / distance2 if distance2 != 0 else 0
            x1 = points[MID][0]
            z1 = points[MID][2]

            dx1_color = (points[TOP][3][0] - points[MID][3][0]) / distance2 if distance2 != 0 else 0
            dy1_color = (points[TOP][3][1] - points[MID][3][1]) / distance2 if distance2 != 0 else 0
            dz1_color = (points[TOP][3][2] - points[MID][3][2]) / distance2 if distance2 != 0 else 0
            x1_color = points[MID][3][0]
            y1_color = points[MID][3][1]
            z1_color = points[MID][3][2]


        lim0 = [x0_color, y0_color, z0_color]
        lim1 = [x1_color, y1_color, z1_color]
        draw_scanline_phong(int(x0), z0, int(x1), z1, y, screen, zbuffer, view, ambient, light, symbols, reflect,lim0,lim1)
        x0+= dx0
        z0+= dz0
        x1+= dx1
        z1+= dz1
        y+= 1

        x0_color += dx0_color
        y0_color += dy0_color
        z0_color += dz0_color
        x1_color += dx1_color
        y1_color += dy1_color
        z1_color += dz1_color

def draw_scanline_gouraud(x0, z0, x1, z1, y, screen, zbuffer, lim0, lim1):
    if x0 > x1:
        tx = x0
        tz = z0
        x0 = x1
        z0 = z1
        x1 = tx
        z1 = tz
        temp = lim0
        lim0 = lim1
        lim1 = temp

    x = x0
    z = z0
    dz = (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0

    distance = x1 - x0 + 1
    x_color = lim0[0]
    y_color = lim0[1]
    z_color = lim0[2]
    dx_color = (lim1[0] - lim0[0]) / distance if distance != 0 else 0
    dy_color = (lim1[1] - lim0[1]) / distance if distance != 0 else 0
    dz_color = (lim1[2] - lim0[2]) / distance if distance != 0 else 0

    while x <= x1:


        color = [ int(x_color), int(y_color), int(z_color)]
        plot(screen, zbuffer, color, x, y, z)
        x+= 1
        z+= dz
        x_color += dx_color
        y_color += dy_color
        z_color += dz_color

def scanline_gouraud(polygons, i, screen, zbuffer, colors):
    flip = False
    BOT = 0
    TOP = 2
    MID = 1

    points = [ (polygons[i][0], polygons[i][1], polygons[i][2], colors[0]),
               (polygons[i+1][0], polygons[i+1][1], polygons[i+1][2], colors[1]),
               (polygons[i+2][0], polygons[i+2][1], polygons[i+2][2], colors[2]) ]

    points.sort(key = lambda x: x[1])
    x0 = points[BOT][0]
    z0 = points[BOT][2]
    x1 = points[BOT][0]
    z1 = points[BOT][2]
    y = int(points[BOT][1])

    distance0 = int(points[TOP][1]) - y * 1.0 + 1
    distance1 = int(points[MID][1]) - y * 1.0 + 1
    distance2 = int(points[TOP][1]) - int(points[MID][1]) * 1.0 + 1

    dx0 = (points[TOP][0] - points[BOT][0]) / distance0 if distance0 != 0 else 0
    dz0 = (points[TOP][2] - points[BOT][2]) / distance0 if distance0 != 0 else 0
    dx1 = (points[MID][0] - points[BOT][0]) / distance1 if distance1 != 0 else 0
    dz1 = (points[MID][2] - points[BOT][2]) / distance1 if distance1 != 0 else 0


    x0_color = points[BOT][3][0]
    y0_color = points[BOT][3][1]
    z0_color = points[BOT][3][2]
    x1_color = points[BOT][3][0]
    y1_color = points[BOT][3][1]
    z1_color = points[BOT][3][2]
    dx0_color = (points[TOP][3][0] - points[BOT][3][0]) / distance0 if distance0 != 0 else 0
    dy0_color = (points[TOP][3][1] - points[BOT][3][1]) / distance0 if distance0 != 0 else 0
    dz0_color = (points[TOP][3][2] - points[BOT][3][2]) / distance0 if distance0 != 0 else 0
    dx1_color = (points[MID][3][0] - points[BOT][3][0]) / distance1 if distance1 != 0 else 0
    dy1_color = (points[MID][3][1] - points[BOT][3][1]) / distance1 if distance1 != 0 else 0
    dz1_color = (points[MID][3][2] - points[BOT][3][2]) / distance1 if distance1 != 0 else 0

    # inten0 = bot to top
    # inten1 = bot to mid, mid to top
    while y <= int(points[TOP][1]):
        if ( not flip and y >= int(points[MID][1])):
            flip = True

            dx1 = (points[TOP][0] - points[MID][0]) / distance2 if distance2 != 0 else 0
            dz1 = (points[TOP][2] - points[MID][2]) / distance2 if distance2 != 0 else 0
            x1 = points[MID][0]
            z1 = points[MID][2]

            dx1_color = (points[TOP][3][0] - points[MID][3][0]) / distance2 if distance2 != 0 else 0
            dy1_color = (points[TOP][3][1] - points[MID][3][1]) / distance2 if distance2 != 0 else 0
            dz1_color = (points[TOP][3][2] - points[MID][3][2]) / distance2 if distance2 != 0 else 0
            x1_color = points[MID][3][0]
            y1_color = points[MID][3][1]
            z1_color = points[MID][3][2]

        # inten0_part0 = [ (y - points[BOT][1])*color_mid for color_mid in points[MID][3] ]
        # inten0_part1 = [ (points[MID][1] - y)*color_bot for color_bot in points[BOT][3] ]
        # inten0_part2 = [ inten0_part0[i]+inten0_part1[i] for i in range(len(inten0_part0)) ]
        # inten0 = [ inten0_colo/ (points[MID][1] - points[BOT][1]) for inten0_colo in inten0_part2] if (points[MID][1] - points[BOT][1]) != 0 else [0,0,0]

        # inten1_part0 = [ (y - points[BOT][1])*color_top for color_top in points[TOP][3] ]
        # inten1_part1 = [ (points[TOP][1] - y)*color_bot for color_bot in points[BOT][3] ]
        # inten1_part2 = [ inten0_part0[i]+inten0_part1[i] for i in range(len(inten0_part0)) ]
        # inten1 = [ inten1_colo/ (points[MID][1] - points[BOT][1]) for inten1_colo in inten1_part2] if (points[MID][1] - points[BOT][1]) != 0 else [0,0,0]

        lim0 = [x0_color, y0_color, z0_color]
        lim1 = [x1_color, y1_color, z1_color]
        # draw_scanline_gouraud(int(x0), z0, int(x1), z1, y, screen, zbuffer, inten0, inten1)
        draw_scanline_gouraud(int(x0), z0, int(x1), z1, y, screen, zbuffer, lim0, lim1)
        x0+= dx0
        z0+= dz0
        x1+= dx1
        z1+= dz1
        y+= 1

        x0_color += dx0_color
        y0_color += dy0_color
        z0_color += dz0_color
        x1_color += dx1_color
        y1_color += dy1_color
        z1_color += dz1_color

def draw_scanline(x0, z0, x1, z1, y, screen, zbuffer, color):
    if x0 > x1:
        tx = x0
        tz = z0
        x0 = x1
        z0 = z1
        x1 = tx
        z1 = tz

    x = x0
    z = z0
    delta_z = (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0

    while x <= x1:
        plot(screen, zbuffer, color, x, y, z)
        x+= 1
        z+= delta_z

def scanline_convert(polygons, i, screen, zbuffer, color):
    flip = False
    BOT = 0
    TOP = 2
    MID = 1

    points = [ (polygons[i][0], polygons[i][1], polygons[i][2]),
               (polygons[i+1][0], polygons[i+1][1], polygons[i+1][2]),
               (polygons[i+2][0], polygons[i+2][1], polygons[i+2][2]) ]

    # alas random color, we hardly knew ye
    #color = [0,0,0]
    #color[RED] = (23*(i/3)) %256
    #color[GREEN] = (109*(i/3)) %256
    #color[BLUE] = (227*(i/3)) %256

    points.sort(key = lambda x: x[1])
    x0 = points[BOT][0]
    z0 = points[BOT][2]
    x1 = points[BOT][0]
    z1 = points[BOT][2]
    y = int(points[BOT][1])

    distance0 = int(points[TOP][1]) - y * 1.0 + 1
    distance1 = int(points[MID][1]) - y * 1.0 + 1
    distance2 = int(points[TOP][1]) - int(points[MID][1]) * 1.0 + 1

    dx0 = (points[TOP][0] - points[BOT][0]) / distance0 if distance0 != 0 else 0
    dz0 = (points[TOP][2] - points[BOT][2]) / distance0 if distance0 != 0 else 0
    dx1 = (points[MID][0] - points[BOT][0]) / distance1 if distance1 != 0 else 0
    dz1 = (points[MID][2] - points[BOT][2]) / distance1 if distance1 != 0 else 0

    while y <= int(points[TOP][1]):
        if ( not flip and y >= int(points[MID][1])):
            flip = True

            dx1 = (points[TOP][0] - points[MID][0]) / distance2 if distance2 != 0 else 0
            dz1 = (points[TOP][2] - points[MID][2]) / distance2 if distance2 != 0 else 0
            x1 = points[MID][0]
            z1 = points[MID][2]

        #draw_line(int(x0), y, z0, int(x1), y, z1, screen, zbuffer, color)
        draw_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, color)
        x0+= dx0
        z0+= dz0
        x1+= dx1
        z1+= dz1
        y+= 1

def add_mesh(polygons, filename):

    f = open(filename + '.obj', "r")
    lines = f.read().split("\n")

    # vertex index at 1
    vertices = ["placeholder"]


    for line in lines:
        tokens = line.split()
        if len(tokens) == 0:
            continue

        if tokens[0] == "v":
            coords = [SCALING * float(coord) for coord in tokens[1:4]]
            vertices.append(coords)

        if tokens[0] == "f":
            #print tokens
            Nvertices = []
            for token in tokens[1:]:
                face_infos = token.split("/")
                #print token
                #print face_infos
                Nvertices.append(int(face_infos[0]))
            #print Nvertices



            a = vertices[Nvertices[0]]
            b = vertices[Nvertices[1]]
            c = vertices[Nvertices[2]]
            if len(Nvertices) == 4:
                d = vertices[Nvertices[3]]
                add_polygon(polygons, a[0], a[1], a[2], b[0], b[1], b[2], c[0], c[1], c[2])
                add_polygon(polygons, a[0], a[1], a[2], c[0], c[1], c[2], d[0], d[1], d[2])
            if len(Nvertices) == 3:
                add_polygon(polygons, a[0], a[1], a[2], b[0], b[1], b[2], c[0], c[1], c[2])

    # print(tmp)


def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)

def draw_polygons( polygons, screen, zbuffer, view, ambient, lights, symbols, reflect, shading):
    #print lights
    light = [ lights[0][0], lights[0][1] ]
    print light
    if len(polygons) < 2:
        print 'Need at least 3 points to draw'
        return

    average_vector_norms = {}
    if shading == 'gouraud' or shading == 'phong':
        average_vector_norms = calculate_vertex_norms( polygons )
        # print average_vector_norms

    point = 0
    while point < len(polygons) - 2:

        normal = calculate_normal(polygons, point)[:]

        #print normal
        if normal[2] > 0:

            #scanline_convert(polygons, point, screen, zbuffer, color, shading, average_vector_norms)
            if shading == 'flat':
                color = [0,0,0]
                for light in lights:

                    c =  get_lighting(normal, view, ambient, light, symbols, reflect )

                    color[0] += c[0]
                    color[1] += c[1]
                    color[2] += c[2]
                limit_color(color)
                scanline_convert(polygons, point, screen, zbuffer, color)
            elif shading == 'gouraud':
                norm0 = average_vector_norms[ str(estimate(polygons[point])) ]
                light0 = get_lighting( norm0, view, ambient, light, symbols, reflect  )
                norm1 = average_vector_norms[ str(estimate(polygons[point+1])) ]
                light1 = get_lighting( norm1, view, ambient, light, symbols, reflect  )
                norm2 = average_vector_norms[ str(estimate(polygons[point+2])) ]
                light2 = get_lighting( norm2, view, ambient, light, symbols, reflect  )

                colors = [ light0, light1, light2 ]

                scanline_gouraud(polygons, point, screen, zbuffer, colors)
            elif shading == 'phong':
                #print 'phong'
                norm0 = average_vector_norms[ str(estimate(polygons[point])) ]
                norm1 = average_vector_norms[ str(estimate(polygons[point+1])) ]
                norm2 = average_vector_norms[ str(estimate(polygons[point+2])) ]

                colors = [norm0,norm1,norm2]

                scanline_phong(polygons, point, screen, zbuffer, colors, view, ambient, light, symbols, reflect)



            # draw_line( int(polygons[point][0]),
            #            int(polygons[point][1]),
            #            polygons[point][2],
            #            int(polygons[point+1][0]),
            #            int(polygons[point+1][1]),
            #            polygons[point+1][2],
            #            screen, zbuffer, color)
            # draw_line( int(polygons[point+2][0]),
            #            int(polygons[point+2][1]),
            #            polygons[point+2][2],
            #            int(polygons[point+1][0]),
            #            int(polygons[point+1][1]),
            #            polygons[point+1][2],
            #            screen, zbuffer, color)
            # draw_line( int(polygons[point][0]),
            #            int(polygons[point][1]),
            #            polygons[point][2],
            #            int(polygons[point+2][0]),
            #            int(polygons[point+2][1]),
            #            polygons[point+2][2],
            #            screen, zbuffer, color)
        point+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z)
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z)

    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1)
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1)

    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1)
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1)
    #left side
    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z)
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z)

    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1)
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z)
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)

def add_sphere(polygons, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            p1 = p0+1
            p2 = (p1+step) % (step * (step-1))
            p3 = (p0+step) % (step * (step-1))

            if longt != step - 2:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p1][0],
                             points[p1][1],
                             points[p1][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2])
            if longt != 0:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2],
                             points[p3][0],
                             points[p3][1],
                             points[p3][2])


def generate_sphere( cx, cy, cz, r, step ):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt;
            if (longt == (step - 1)):
                p1 = p0 - longt;
            else:
                p1 = p0 + 1;
            p2 = (p1 + step) % (step * step);
            p3 = (p0 + step) % (step * step);

            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2] )


def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, zbuffer, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   matrix[point][2],
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   matrix[point+1][2],
                   screen, zbuffer, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )



def draw_line( x0, y0, z0, x1, y1, z1, screen, zbuffer, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        zt = z0
        x0 = x1
        y0 = y1
        z0 = z1
        x1 = xt
        y1 = yt
        z1 = zt

    x = x0
    y = y0
    z = z0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False

    if ( abs(x1-x0) >= abs(y1 - y0) ): #octants 1/8
        wide = True
        loop_start = x
        loop_end = x1
        dx_east = dx_northeast = 1
        dy_east = 0
        d_east = A
        distance = x1 - x + 1
        if ( A > 0 ): #octant 1
            d = A + B/2
            dy_northeast = 1
            d_northeast = A + B
        else: #octant 8
            d = A - B/2
            dy_northeast = -1
            d_northeast = A - B

    else: #octants 2/7
        tall = True
        dx_east = 0
        dx_northeast = 1
        distance = abs(y1 - y) + 1
        if ( A > 0 ): #octant 2
            d = A/2 + B
            dy_east = dy_northeast = 1
            d_northeast = A + B
            d_east = B
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A/2 - B
            dy_east = dy_northeast = -1
            d_northeast = A - B
            d_east = -1 * B
            loop_start = y1
            loop_end = y

    dz = (z1 - z0) / distance if distance != 0 else 0

    while ( loop_start < loop_end ):
        plot( screen, zbuffer, color, x, y, z )
        if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
             (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):

            x+= dx_northeast
            y+= dy_northeast
            d+= d_northeast
        else:
            x+= dx_east
            y+= dy_east
            d+= d_east
        z+= dz
        loop_start+= 1
    plot( screen, zbuffer, color, x, y, z )
