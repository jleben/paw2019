import matplotlib
import matplotlib.pyplot
import math

font = {'family': 'sans',
        'serif' : 'DejaVu Sans',
        'style': 'normal',
        'size'   : 7,
        'weight': 400
        }

matplotlib.rc('font', **font)
matplotlib.rcParams['hatch.linewidth'] = 0.5

fig_size = (6.6, 5)

S = 4 # tile size
N = S*6 # max i
T = S*4+S # max n
K = int(N/2/S)*S

input_tile_color = (0.6, 0.6, 0.6)
output_tile_color = input_tile_color
other_tile_color = 'grey'

input_dot_color = 'black'
output_dot_color = input_dot_color
io_dot_size = 0.3

prologue_color = (0.95, 0.8, 0.8)
period_color = (0.8, 0.8, 0.95)

tile_boundary_color = 'grey'
tile_boundary_width = 0.5
tile_boundary_style = '--'

arrow_linewidth = 0.5
arrow_headwidth = 0.4

clip_box = matplotlib.transforms.Bbox([(0,0),(T,N)]);

def parallel_tile_boundary(n_start):
    b = []
    n_end = int(N/2)
    for n in range(0,n_end,S):
        i = N - 2*n*S
        b.append([n_start+n,i])
        b.append([n_start+n+S,i-S])
    b.append([n_start+n_end,0])
    return b

# (n,i) is the bottom-left corner
def parallelepiped_shape(n,i):
    bl = [n,i]
    tl = [n,i+S]
    tr = [n+S,i]
    br = [n+S,i-S]

    # bottom edge
    if i <= 0:
        return [bl,tl,tr]
    # top edge
    elif i >= N:
        return [bl,tr,br]
    else:
        return [bl,tl,tr,br]


def draw_tile(ax, points, **kwds):
    #v = [[p[0],p[1]] for p in xy]
    ax.add_patch(matplotlib.patches.Polygon(points, **kwds))


def draw_tile_separator(ax, points):
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    line = matplotlib.lines.Line2D(x, y,
            color = tile_boundary_color, zorder=1, linewidth=tile_boundary_width, linestyle=tile_boundary_style)
    ax.add_line(line)




def draw_tile_boundaries(ax,N,T):
    boundary_tiles_bottom = [ [(n,0),(n+S,0),(n,S)] for n in range(0,T,S) ]
    boundary_tiles_top = [ [(n,N-S),(n+S,N-S),(n,N)] for n in range(0,T,S) ]
    output_tiles = [ [(n,K), (n+S,K-S), (n+S,K), (n,K+S)] for n in range(0,T,S) ]

    for n in range(S,T+N,S):
        n_left = max(0, n-N)
        n_right = min(T, n)
        i_left = min(N, n);
        i_right = max(0, n-T);

        draw_tile_separator(ax, [[n_left, i_left], [n_right, i_right]])

    #for tile in boundary_tiles_bottom:
        #draw_tile(ax, tile, facecolor=input_tile_color)
        #draw_tile(ax, tile, facecolor=input_tile_color, zorder=2)

    #for tile in output_tiles:
        #draw_tile(ax, tile, facecolor=output_tile_color, zorder=2)

    for n in range(0,T+1,S):
        draw_tile_separator(ax, [[n,0], [n,N]])


def draw_diamond_tile_bounds(ax,N,T):
    for n in range(S,T+N,S):
        n_left = max(0, n-N)
        n_right = min(T, n)
        i_left = min(N, n);
        i_right = max(0, n-T);

        i2_left = N-i_left
        i2_right = N-i_right

        draw_tile_separator(ax, [[n_left, i_left], [n_right, i_right]])
        draw_tile_separator(ax, [[n_left, i2_left], [n_right, i2_right]])


def draw_io_dot(ax, pos, color):
    ax.add_patch(matplotlib.patches.Circle((pos[0] + S/2, pos[1]), io_dot_size,
                                                edgecolor='none', facecolor=color))

def draw_input_output(ax,N,T):
    input_tile_pos = [[n,0] for n in range(0,T,S)]
    output_tile_pos = [[n,int(N/2)] for n in range(0,T,S)]

    for pos in input_tile_pos:
        draw_io_dot(ax, pos, input_dot_color)
    for pos in output_tile_pos:
        draw_io_dot(ax, pos, output_dot_color)


def draw_parallel_tiles(ax):

    for n in range(0,T,S):
        for i in range(0,N+1,S):
            if i > 0 and i < N:
                shape = [[n,i],[n+S,i-S],[n+S,i],[n,i+S]]
            elif i == 0:
                shape = [[n,0],[n+S,0],[n,S]]
            elif i == N:
                shape = [[n,N],[n+S,N-S],[n+S,N]]

            decorate = False
            if int(2*n+i) % 2 == 0:
                decorate = True

            #hatch = '////' if decorate else None
            #ax.add_patch(matplotlib.patches.Polygon(shape, edgecolor=tile_boundary_color, linewidth=0, fill=False, hatch=hatch))

            if decorate:
                color = (0,0,0,0.2)
                ax.add_patch(matplotlib.patches.Polygon(shape, linewidth=0, facecolor=color))

def draw_dependency(ax, start, length):
    ax.arrow(start[0], start[1], length[0], length[1],
             head_width=arrow_headwidth, linewidth=arrow_linewidth, length_includes_head=True,
             facecolor='black', edgecolor='black')

def draw_dependencies(ax,n,i):

    x = n*S
    y = i*S
    L = S*0.85

    #S = sqrt(x^2 + x^2)/2
    #2S = sqrt(2x^2)
    #(2S)^2 = 2x^2
    #((2S)^2/2) = x^2
    #sqrt((2S)^2/2) = x
    #sqrt(4S^2/2) = x
    #sqrt(2S^2) = x
    Sd = math.sqrt(2*S)

    draw_dependency(ax, (x-S, y), (L, 0))
    draw_dependency(ax, (x-Sd, y+Sd), (Sd*0.85, -Sd*0.85))
    draw_dependency(ax, (x, y-S), (0, L))

def draw_schedule1(ax):

    T = 4*S
    p = S

    prologue = [[0,0], [S,0], [S,N], [0,N]]
    period = [[p,0], [p+S,0], [p+S,N], [p,N]]

    draw_tile(ax, prologue, facecolor=prologue_color)
    draw_tile(ax, period, facecolor=period_color)

    draw_tile_boundaries(ax,N,T);
    draw_input_output(ax,N,T);

    draw_dependencies(ax,3.5,5);

    ax.set_aspect(1)
    ax.autoscale_view()
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(0.5)


def draw_schedule2(ax):

    #prologue = [[0,0], [N,0], [0,N]]
    #period = [[N,0], [N,S], [S,N], [0,N]]

    #prologue = [[0,0], [S,0], [S,N], [0,N]]
    #prologue = [[0,0]] + parallel_tile_boundary(0)
    #print(prologue)
    period = parallel_tile_boundary(0) + list(reversed(parallel_tile_boundary(S)))
    print(period)

    prologue = []
    for i in range(0,N,S):
        for n in range(0, int((N-i)/2), S):
            prologue.append(parallelepiped_shape(n,i))

    period = []
    for i in range(0,N+1,S):
        n = math.ceil((N-i)/S/2)*S
        period.append(parallelepiped_shape(n,i))

    for tile in prologue:
        draw_tile(ax, tile, facecolor=prologue_color)
    for tile in period:
        draw_tile(ax, tile, facecolor=period_color)

    #draw_tile(ax, period, facecolor=period_color)

    draw_tile_boundaries(ax,N,T);
    #draw_parallel_tiles(ax)
    draw_input_output(ax,N,T);

    draw_dependencies(ax,4.5,5);

    ax.add_line(matplotlib.lines.Line2D([S/2,S/2+int(N/2)], [N,0],
                color = 'black', zorder=1, linewidth=2*tile_boundary_width))

    ax.set_aspect(1)
    ax.autoscale_view()
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(0.5)

def draw_schedule3(ax):

    P = 2*S # period size
    p = S # period position
    prologue = [[0,0], [S,0], [S,N], [0,N]]
    period = [[p,0], [p+P,0], [p+P,N], [p,N]]

    draw_tile(ax, prologue, facecolor=prologue_color)
    draw_tile(ax, period, facecolor=period_color)

    draw_tile_boundaries(ax,N,T);
    #draw_parallel_tiles(ax)
    draw_input_output(ax,N,T);

    draw_dependencies(ax,4.5,5);

    ax.add_line(matplotlib.lines.Line2D([S,3*S], [int(N/2)+2*S,int(N/2)-2*S],
            color = 'black', zorder=1, linewidth=2*tile_boundary_width))

    ax.set_aspect(1)
    ax.autoscale_view()
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(0.5)

def draw_schedule4(ax):
    N = 6*S
    T = 4*S
    draw_diamond_tile_bounds(ax, N, T)
    draw_input_output(ax, N, T)

    # (n,i) is the bottom corner of the diamond
    def diamond_shape(n, i):
        b = [n,i]
        l = [n-S/2,i+S/2]
        t =  [n,i+S]
        r = [n+S/2,i+S/2]

        if n <= 0: # left edge
            points = [b,t,r]

        elif i < 0: # bottom edge
            points = [l,t,r]

        elif i > N-S: # top edge
            points = [b,l,r]

        else:
            points = [b,l,t,r]

        return points


    prologue_tiles = []

    for n in range(0,1*S,S):
        for i in range(0,N,S):
            prologue_tiles.append(diamond_shape(n,i))
            prologue_tiles.append(diamond_shape(n+S/2,i-S/2))
        prologue_tiles.append(diamond_shape(n+S/2,N-S/2))

    for tile in prologue_tiles:
        ax.add_patch(matplotlib.patches.Polygon(tile, facecolor = prologue_color, zorder=-1))


    period_tiles = []

    for n in range(1*S,2*S,S):
        for i in range(0,N,S):
            period_tiles.append(diamond_shape(n,i))
            period_tiles.append(diamond_shape(n+S/2,i-S/2))
        period_tiles.append(diamond_shape(n+S/2,N-S/2))

    for tile in period_tiles:
        ax.add_patch(matplotlib.patches.Polygon(tile, facecolor = period_color, zorder=-1))

    ax.add_line(matplotlib.lines.Line2D([S,S], [0+S*0.2,N-S*0.2],
        color = 'black', zorder=1, linewidth=2*tile_boundary_width))

    Ld = math.sqrt(2*S)/2
    draw_dependency(ax, (2.5*S, 5*S),(S*0.8,0))
    draw_dependency(ax, (3*S, 4.5*S),(Ld,Ld))
    draw_dependency(ax, (3*S, 5.5*S),(Ld,-Ld))

    ax.set_aspect(1)
    ax.autoscale_view()
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(0.5)


def output_figure():

    fig_funcs = [
        draw_schedule1,
        draw_schedule2,
        draw_schedule3,
        draw_schedule4
    ]

    for index, func in enumerate(fig_funcs):

        fig = matplotlib.pyplot.figure(figsize = (3,1.8))
        ax = fig.subplots(1,1)
        func(ax)

        fig.savefig('stencil-tiled{}.pdf'.format(index), bbox_inches='tight', pad_inches=0)
        #fig.savefig('stencil-tiled{}.pdf'.format(index), bbox_inches=0)
        #fig.savefig('stencil-tiled{}.pdf'.format(index))


    #ax = fig.subplots(1,4, gridspec_kw = { 'wspace': 0.2, 'hspace': 0 })

    #draw_schedule1(ax[0])
    #draw_schedule2(ax[1])
    #draw_schedule3(ax[2])
    #draw_schedule4(ax[3])

    #fig.savefig('stencil-tiled.pdf', bbox_inches="tight")


output_figure()
