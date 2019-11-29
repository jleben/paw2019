import matplotlib
import matplotlib.pyplot

font = {'family': 'sans',
        'serif' : 'DejaVu Sans',
        'style': 'normal',
        'size'   : 7,
        'weight': 400
        }

matplotlib.rc('font', **font)

fig_size = (7.4, 4)
dot_size = 0.08
dot_color = (0.4, 0.4, 0.4)
domain_dot_size = 0.15
domain_dot_color = (0, 0, 0)

N = 7
T = 6
K = 3

x = [(n,0) for n in range(0,T)]
z0 = [(n,0) for n in range(0,T-1)]
z1 = [(n,N-1) for n in range(0,T-1)]
w = [(0,i) for i in range(1,N-1)]
u = [(n,i) for n in range(1,T) for i in range(1,N-1)]
y = [(n,K) for n in range(0,int(T/2))]

def x_s(z): (n,i) = z; return (n,n+1)
def z0_s(z): (n,i) = z; return (n+1,n+2+i)
def z1_s(z): (n,i) = z; return (n+1,n+N-1)
def w_s(z): (n,i) = z; return (0,i)
def u_s(z): (n,i) = z; return (n, n+i)
def y_s(z): (m,i) = z; return (2*m, 2*m + K)

prologue = [(0,1), (1,2), (1,(N-2)+1), (0,(N-2))]
periods = [(1,2), (T-1,T-1+1), (T-1, T-1 + N-2), (1, (N-2)+1)]
bounds = [0, 1, T-1, N-2+T-1] # Two corners: x0, y1, x1, y1

prologue_color = (0.95, 0.8, 0.8)
period_color = (0.8, 0.8, 0.95)
tile_boundary_line_style = '--'
tile_boundary_color = (0.7,0.7,0.7)

arrow_linewidth = 0.8
arrow_headwidth = 0.18

def draw_dots(ax, x0, y0, x1, y1, size=0.1):
    for x in range(x0, x1+1):
        for y in range(y0, y1+1):
            ax.add_patch(matplotlib.patches.Circle((x, y), size,
                                                edgecolor='none', facecolor=dot_color))

def draw_domain(ax, D):
    for n,i in D:
        ax.add_patch(matplotlib.patches.Circle((n, i), domain_dot_size,
                                               edgecolor='none', facecolor=domain_dot_color))


def draw_area(ax, xy, **kwds):
    v = [[p[0],p[1]] for p in xy]
    ax.add_patch(matplotlib.patches.Polygon(v, **kwds))


def draw_periodic_tiling_direction(ax):

    ax.arrow(3, 2, 1, 0, head_width=arrow_headwidth, linewidth=arrow_linewidth, length_includes_head=True,
                        facecolor='black', edgecolor='black')
    ax.text(3.4, 1.4, r'$\vec{d}$', ha='center', va='center')


def draw_ray(ax, size=1):
    ax.arrow(3, 2, 1*size, 1*size, head_width=arrow_headwidth, linewidth=arrow_linewidth, length_includes_head=True,
                    facecolor='black', edgecolor='black')
    ax.text(3.4, 2.8, r'$\vec{r}$', ha='center', va='center')


def draw_domain_plot(ax, dom, ray_size=1):

    draw_area(ax, prologue, edgecolor='none', facecolor=prologue_color, zorder=-2)
    draw_area(ax, periods, edgecolor='none', facecolor=period_color, zorder=-2)

    draw_dots(ax, bounds[0], bounds[1], bounds[2], bounds[3], dot_size)

    for n in range(bounds[0]+1, bounds[2]+1 , 2):
        ax.add_line(matplotlib.lines.Line2D([n, n], [bounds[1], bounds[3]],
                color = tile_boundary_color, zorder=-1, linestyle=tile_boundary_line_style, linewidth=0.9))

    #prologue = [[0,0], [2,2], [8,2], [6,0]]
    #ax.add_patch(matplotlib.patches.Polygon(prologue))

    draw_domain(ax, dom)
    #draw_domain(ax, [w0_s(i) for i in w0])
    #draw_domain(ax, [w1_s(i) for i in w1])
    #draw_domain(ax, [y_s(i) for i in y], offset = 0.4)

    draw_periodic_tiling_direction(ax)
    if ray_size > 0:
        draw_ray(ax, ray_size)

    #ax.get_xaxis().set_ticks([])
    #ax.get_yaxis().set_ticks([])
    ax.set_aspect(1)
    ax.autoscale_view()
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(0.5)

def output_basic_schedule_figure():
    fig = matplotlib.pyplot.figure(figsize = fig_size)

    ax = fig.subplots(1,5, gridspec_kw = { 'wspace': 0.35, 'hspace': 0 })

    draw_domain_plot(ax[0], [x_s(i) for i in x], ray_size=1)
    draw_domain_plot(ax[1], [z0_s(i) for i in z0] + [z1_s(i) for i in z1], ray_size=1)
    draw_domain_plot(ax[2], [w_s(i) for i in w], ray_size=0)
    draw_domain_plot(ax[3], [u_s(i) for i in u], ray_size=1)
    draw_domain_plot(ax[4], [y_s(i) for i in y], ray_size=2)

    fig.savefig('stencil-basic.pdf', bbox_inches="tight", pad_inches=0)


output_basic_schedule_figure()
