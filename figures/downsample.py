import matplotlib
import matplotlib.pyplot

font = {'family' : 'serif',
        'serif'  : ['Times'],
        'size'   : 13}

matplotlib.rc('font', **font)

fig_size = (3.2,3.2)

#schedule_color = (0.7, 0.95, 0.7)
schedule_color = (0.88, 0.88, 0.88)
#schedule_color = (0.95, 0.8, 0.8)
#schedule_color = (0.95, 0.95, 0.7)
schedule_line_width = 6

point_size = 0.18
point_color1 = (0.1, 0.1, 0.9)
point_color2 = (0.9,0.1,0.1)
#point_color1 = 'black'
#point_color2 = 'black'


def draw_points(ax):
    for i in range(0, 4):
        for j in range(0, 4):
            if i % 2 == 0:
                ax.add_patch(matplotlib.patches.Ellipse((i,j), point_size, point_size, facecolor=point_color1))
            else:
                ax.add_patch(matplotlib.patches.Ellipse((i,j), point_size, point_size, facecolor=point_color2))

    for i in range(0, 4, 2):
        for j in range(0, 4):
            #pass
            ax.arrow(i+0.2, j, 0.6, 0, head_width=0.12, length_includes_head=True,
                     facecolor='black', edgecolor='black')



def draw_tiled_schedule():
    fig = matplotlib.pyplot.figure(figsize = fig_size)
    axes = fig.subplots()

    draw_points(axes)

    x = []
    y = []
    xy = []
    for t in range(0,2):
        for j in range(0,4):
            i0 = t*2
            i1 = t*2 + 1
            xy += [(i0, j), (i1, j)]
            if j < 3:
                xy += [(i1, j+0.5), (i0, j+0.5)]
            else:
                xy += [(i1+0.5, 3), (i1+0.5, 0)]

    xy += [(4,0)]

    x = [a[0] for a in xy]
    y = [a[1] for a in xy]
    axes.plot(x,y, linewidth=schedule_line_width, color=schedule_color, zorder=-1)

    output_figure(axes, fig, 'downsample-sched-tiled')


def draw_simple_schedule1():
    fig = matplotlib.pyplot.figure(figsize = fig_size)
    axes = fig.subplots()

    draw_points(axes)

    xy = []
    for j in range(0,4):
        if j < 3:
            xy += [(0,j), (4,j), (4, j+0.5), (0, j+0.5)]
        else:
            xy += [(0,j), (4,j)]

    x = [a[0] for a in xy]
    y = [a[1] for a in xy]
    axes.plot(x,y, linewidth=schedule_line_width, color=schedule_color, zorder=-1)

    output_figure(axes, fig, 'downsample-sched-simple1')

def draw_simple_schedule2():
    fig = matplotlib.pyplot.figure(figsize = fig_size)
    axes = fig.subplots()

    draw_points(axes)

    xy = []
    for i in range(0,4):
        xy += [(i,0), (i,3), (i+0.5, 3), (i+0.5, 0)]
    xy += [(4,0)]

    x = [a[0] for a in xy]
    y = [a[1] for a in xy]
    axes.plot(x,y, linewidth=schedule_line_width, color=schedule_color, zorder=-1)

    output_figure(axes, fig, 'downsample-sched-simple2')


def output_figure(ax, fig, name):
    ax.set_xlabel('(n = 2m + 1)')
    ax.set_xticks(range(0,7))
    ax.set_xticklabels(list(range(0,4)) + ['...\u221E'])

    ax.set_ylabel('(i)')
    ax.set_yticks(range(0,4))
    ax.set_yticklabels(list(range(0,3)) + ['N'])

    ax.set_aspect(1)
    ax.autoscale_view()

    fig.savefig(name + '.svg', bbox_inches="tight")
    fig.savefig(name + '.eps', bbox_inches="tight")

draw_simple_schedule1()
draw_simple_schedule2()
draw_tiled_schedule()
