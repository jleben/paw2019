import matplotlib
import matplotlib.pyplot
import numpy as np

font = {'family' : 'serif',
        'serif'  : ['Times'],
        'size'   : 13}

matplotlib.rc('font', **font)
#matplotlib.rc('text', usetex=True)

vertices = [[10,10], [2,6], [2,4], [4,4], [10,7]]

tile_boundary_line_style = '--'
tile_boundary_color = (0.6,0.6,0.6)

def draw_polyhedron(axes):
    # Edges

    axes.add_line(matplotlib.lines.Line2D(np.transpose(vertices)[0], np.transpose(vertices)[1],
                                      color = (0.4,0.4,0.4), linewidth=3, zorder=1))

    # Points

    for x in range(2,11):
        for y in range(4, 12):
            axes.add_patch(matplotlib.patches.Ellipse((x, y), 0.1, 0.1, zorder = 2,
                                                    edgecolor='none', facecolor='black'))


def draw_periodic_tiling():

    fig = matplotlib.pyplot.figure(figsize = (4.2, 4))
    axes = fig.subplots()

    prologue = [[4,7], [2,6], [2,4], [4,4]]
    periods = [[10,10], [4,7], [4,4], [10,7]]

    draw_polyhedron(axes)

    # Tiles
    axes.add_patch(matplotlib.patches.Polygon(prologue, edgecolor='none', facecolor=(0.95, 0.8, 0.8)))
    axes.add_patch(matplotlib.patches.Polygon(periods, edgecolor='none', facecolor=(0.8, 0.8, 0.95)))

    # Ray
    axes.arrow(2, 8, 2, 1, head_width=0.2, length_includes_head=True,
                    facecolor='black', edgecolor='black')
    axes.text(2.5, 8.6, r'$\vec{r}$', ha='center', va='center')

    # Direction
    axes.arrow(2, 8, 1, 0, head_width=0.2, length_includes_head=True,
                        facecolor='black', edgecolor='black')
    axes.text(2.5, 7.4, r'$\vec{d}$', ha='center', va='center')

    # Tile division
    for x in range(2,11,2):
        axes.add_line(matplotlib.lines.Line2D([x, x], [4, 11],
                                        color = tile_boundary_color, zorder=1, linestyle=tile_boundary_line_style))
        if x < 10:
            axes.text(x + 1, 10.5, r'$\tau = {}$'.format(int((x - 4) / 2)), ha='center', va='center')


    axes.set_aspect(1)
    axes.autoscale_view()

    fig.savefig('periodic-tiling.svg', bbox_inches="tight")
    fig.savefig('periodic-tiling.eps', bbox_inches="tight")


def draw_wrong_tiling_size():

    fig = matplotlib.pyplot.figure(figsize = (4.2, 4))
    axes = fig.subplots()

    draw_polyhedron(axes)

    # Ray
    axes.arrow(3, 8, 2, 1, head_width=0.2, length_includes_head=True,
                    facecolor='black', edgecolor='black')
    axes.text(3.5, 8.6, r'$\vec{r}$', ha='center', va='center')

    # Direction
    axes.arrow(3, 8, 1, 0, head_width=0.2, length_includes_head=True,
                        facecolor='black', edgecolor='black')
    axes.text(3.5, 7.4, r'$\vec{d}$', ha='center', va='center')

    # Tile division
    for x in range(3,11,3):
        axes.add_line(matplotlib.lines.Line2D([x, x], [4, 11],
                        color = tile_boundary_color, zorder=1, linestyle=tile_boundary_line_style))
        if x < 9:
            axes.text(max(2.75, x + 1.5), 10.5, r'$\tau = {}$'.format(int((x - 3) / 3)), ha='center', va='center')


    axes.set_aspect(1)
    axes.autoscale_view()

    fig.savefig('tiling-wrong-size.svg', bbox_inches="tight")
    fig.savefig('tiling-wrong-size.eps', bbox_inches="tight")

def draw_wrong_tiling_direction():

    fig = matplotlib.pyplot.figure(figsize = (4.2, 4))
    axes = fig.subplots()

    draw_polyhedron(axes)


    # Ray
    axes.arrow(4, 8, 2, 1, head_width=0.2, length_includes_head=True,
                    facecolor='black', edgecolor='black')
    axes.text(4.5, 8.6, r'$\vec{r}$', ha='center', va='center')

    # Direction
    axes.arrow(4, 8, -1, 2, head_width=0.2, length_includes_head=True,
                        facecolor='black', edgecolor='black')
    axes.text(3.7, 9.5, r'$\vec{d}$', ha='center', va='center')


    # Tile boundaries

    axes.add_line(matplotlib.lines.Line2D([2, 10], [4, 8],
                                        color = tile_boundary_color, zorder=1, linestyle=tile_boundary_line_style))
    axes.add_line(matplotlib.lines.Line2D([2, 10], [5, 9],
                                        color = tile_boundary_color, zorder=1, linestyle=tile_boundary_line_style))

    # Tile indices

    for y in range(0,3):
        axes.text(8, 6.5 + y, r'$\tau = {}$'.format(y), ha='center', rotation=26.565)


    axes.set_aspect(1)
    axes.autoscale_view()

    fig.savefig('tiling-wrong-direction.svg', bbox_inches="tight")
    fig.savefig('tiling-wrong-direction.eps', bbox_inches="tight")


draw_periodic_tiling()
draw_wrong_tiling_size()
draw_wrong_tiling_direction()

