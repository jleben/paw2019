import matplotlib
import json
import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import colorsys
from pathlib import Path
import argparse

#matplotlib.rcParams.update({'figure.autolayout': True})

algo_names = ["filter-bank", "max-filter", "ac", "wave1d", "wave2d"]

def read_data():
    f = open(Path(args.input_dir) / "data/par-scaling-perf-report.json")

    try:
        raw_data = json.load(f)
    except JSONDecodeError as e:
        print("Failed to read data: " + str(e))

    # Place into a map with keys in this format: <algo>-(arrp|ref)-(gcc|icc)-<par>

    data = {}

    min_algo_speed = {}

    for value in raw_data.values():

        algo = value["algo"]
        kind = ""

        for name in algo_names:
            if algo.startswith(name):
                kind = algo[len(name)+1:]
                algo = name
                if len(kind) == 0:
                    kind = "Arrp"
                elif kind == "ref":
                    kind = "C++ AO"
                elif kind == "opt":
                    kind = "C++ HO"
                elif kind == "streamit-uno":
                    kind = "StreamIt"
                break

        if kind == "":
            raise Exception("Unrecognized algorithm name: " + str(algo));

        key = ".".join([algo, kind, value["compiler"], str(value["par"])])
        print(key)

        speed = value["speed"]

        data[key] = speed

        if algo in min_algo_speed:
            min_algo_speed[algo] = min(min_algo_speed[algo], speed)
        else:
            min_algo_speed[algo] = speed

    return data, min_algo_speed

def generate_plots(data, min_speed):

    fig_width = 5.9

    if False:
        fig = plt.figure(figsize = (fig_width, 3))

        axs = fig.subplots(2,5, gridspec_kw = { 'left': 0.02, 'right': 1, 'wspace': 0.25, 'hspace': 0.3 })

        for i, algo in enumerate(algo_names):
            generate_plot(axs[0][i], algo, data, 'icc')
            generate_plot(axs[1][i], algo, data, 'gcc')

    elif args.with_gnu:
        fig = plt.figure(figsize = (fig_width, 8))

        axs = fig.subplots(5, 2,
                        gridspec_kw = { 'left': 0.15, 'right': 0.85, 'top': 0.97, 'bottom': 0.06, 'wspace': 0.25, 'hspace': 0.2 })

        for i, algo in enumerate(algo_names):
            generate_bar_plot(axs[i][0], algo, data, 'icc')
            generate_bar_plot(axs[i][1], algo, data, 'gcc')

            range = axs[i][0].get_ylim()

            #axs[i][0].set_title(algo, loc='left')
            #axs[i][0].set_ylabel(algo)
            axs[i][0].text(-2.2,range[1]/2,algo)
            plot = axs[i][0]
            #fig.add_artist(matplotlib.text.Text(plot.x - 10, plot.y, algo))


            axs[i][1].set_ylim(range[0], range[1])

            #generate_plot(axs[1][i], algo, data, 'gcc')

        axs[0][0].set_title('Intel')
        axs[0][1].set_title('GNU')

        handles, labels = axs[0][0].get_legend_handles_labels()

        fig.legend(handles[:4], ["Arrp", "C++ (restricted manual optimization)", "C++ (auto optimization)", "StreamIt"], loc='lower center', ncol=4, frameon=False)
        #fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    elif args.for_slides:

        matplotlib.rc('font', size = 9)

        fig = plt.figure(figsize = (7, 4))

        axs2d = fig.subplots(2, 3,
                    gridspec_kw = { 'left': 0.04, 'right': 0.99, 'top': 0.95, 'bottom': 0.05, 'wspace': 0.24, 'hspace': 0.28 })

        axs = [item for sublist in axs2d for item in sublist]
        for i, algo in enumerate(algo_names):
            generate_bar_plot(axs[i], algo, data, 'icc')
            axs[i].set_title(algo)

        axs[4].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))

        axs[5].axis('off')

        handles, labels = axs[0].get_legend_handles_labels()

        fig.legend(handles[:4], ["Arrp", "C++\n(expected man. optim.)", "C++\n(auto optimization)", "StreamIt"],
                   bbox_to_anchor=(0.66,0,0.33,0.5),
                   labelspacing=1.0,
                   loc='center', ncol=1, frameon=False)

    else:
        print("Nothing to do.")

    #axs[0][0].legend(frameon=False)

    #fig.legend(bbox_to_anchor=(0.1,0.1), loc="lower left")
    #fig.legend(loc="lower right")

    #fig.set_tight_layout(True)
    #plt.tight_layout(0.2)

    #plt.savefig("parallel-scaling.svg", format="svg")
    #plt.savefig("parallel-scaling.eps", format="eps")
    out_name = "parallel-scaling"
    if args.with_gnu:
        out_name += '-with-gnu'
    elif args.for_slides:
        out_name += '-slide'
    out_name += '.' + args.format

    plt.savefig(out_name, format=args.format, bbox_inches=0)


def generate_separate_plots(data, min_speed):

    for algo in algo_names:
        fig = plt.figure(figsize = (3.5, 1.6))

        axs = fig.subplots(1,2, gridspec_kw = { 'left': 0.05, 'right': 1, 'wspace': 0.2, 'hspace': 0.003 })

        generate_bar_plot(axs[0], algo, data, 'icc')
        generate_bar_plot(axs[1], algo, data, 'gcc')

        # Set equal y range
        lim = axs[0].get_ylim()
        axs[1].set_ylim(lim[0], lim[1])

        out_name = "parallel-scaling-" + algo
        out_name += '.' + args.format

        plt.savefig(out_name, format=args.format, bbox_inches=0)


def generate_max_filter_plot(data):
    print("laksjdlakdjlaksda")
    fig = plt.figure(figsize = (3.5, 2.5))
    axs = fig.subplots(1,1, gridspec_kw = { 'left': 0.1, 'right': 1, 'top': 1,  'bottom': 0.3 })
    generate_bar_plot(axs, 'max-filter', data, 'icc')

    axs.set_ylabel('speed')
    axs.set_xlabel('threads')

    handles, labels = axs.get_legend_handles_labels()
    fig.legend(handles[:3], ["Tile n,i,j", "Iterate n,i,j", "Iterate n,j,i"], loc='lower center', ncol=3, frameon=False)

    plt.savefig('parallel-scaling-max-filter-slide.pdf', format='pdf', bbox_inches=0)


def generate_plot(ax, algo, speed, focused_compiler):

    ax.set_title(algo)

    #plt.axes().get_yaxis().set_ticklabels([])

    colors = [
        (0.6, 0.95, 0.7),
        (0.8, 0.95, 0.8),
        (0.0, 0.95, 0.9),
        (0.2, 0.95, 1),
    ]

    styles = [
        ("StreamIt Intel", "StreamIt", "-|", colors[3]),
        #("StreamIt GNU", "StreamIt", "gcc", "-o", (0.9,0.1,0.7)),
        ("C++ AO Intel", "C++ AO", "-x", colors[2]),
        #("C++ AO GNU","C++ AO", "gcc", "-+", (1,0.5,0.1)),
        ("Arrp Intel", "Arrp","-o", colors[0]),
        #("Arrp GNU", "Arrp", "gcc", "-o", (0.1,0.1,0.9)),
        ("C++ HO Intel","C++ HO", "-s", colors[1]),
        #("C++ HO GNU","C++ HO", "gcc", "-+", (0.1,0.9,0.1)),
    ]

    speed_factor = 1000 if (algo == "wave1d" or algo == "wave2d") else 1

    x0 = 0;
    w = 1/len(styles)
    other_compiler = 'gcc' if focused_compiler == 'icc' else 'icc'

    for name, kind, style, color in styles:
        for compiler in [other_compiler, focused_compiler]:
            x0 += w
            if algo == "max-filter" and kind == "StreamIt":
                continue

            y = []
            for cpus in range(1,7):
                key = ".".join([algo, kind, compiler, str(cpus) if kind != "StreamIt" else "1"])
                s = speed[key] * speed_factor
                y.append(s)

            plot_name = name
            xs = [x for x in range(1,7)]
            #plt.bar(xs, y, width=w, align='edge', color=color, label=plot_name)
            if compiler == focused_compiler:
                ax.plot(xs, y, style, color=colorsys.hsv_to_rgb(*color), label=plot_name,
                        linewidth=0.8, markersize=2, markeredgewidth=0.5)
            else:
                ax.plot(xs, y, color=(0.9,0.9,0.9),
                        linewidth=0)

    ax.autoscale_view()


def generate_bar_plot(ax, algo, speed, focused_compiler):

    #plt.axes().get_yaxis().set_ticklabels([])

    colors = [
        (0.60, 1, 0.6),
        (0.13, 1, 0.95),
        (0.87, 1, 0.8),
        (0.50, 0.5, 0.92),
    ]

    if False:
        colors = [
            '#003f5c',
            '#ffa600',
            '#7a5195',
            '#ef5675',
        ]

    datasets = [
        ("Arrp Intel", "Arrp", "icc", colors[0]),
        ("Arrp GNU", "Arrp", "gcc", colors[0]),
        ("C++ HO Intel","C++ HO", "icc", colors[1]),
        ("C++ HO GNU","C++ HO", "gcc", colors[1]),
        ("C++ AO Intel", "C++ AO", "icc", colors[2]),
        ("C++ AO GNU","C++ AO", "gcc", colors[2]),
        ("StreamIt Intel", "StreamIt", "icc", colors[3]),
        ("StreamIt GNU", "StreamIt", "gcc", colors[3]),
    ]

    speed_factor = 1000 if (algo == "wave1d" or algo == "wave2d") else 1

    x0 = 0;
    i = 0;
    w = 1/4
    other_compiler = 'gcc' if focused_compiler == 'icc' else 'icc'

    for name, kind, compiler, color in datasets:
            if compiler != focused_compiler:
                continue

            i += 1

            if algo == "max-filter" and kind == "StreamIt":
                continue

            max_cpu = 6 if kind != "StreamIt" else 1

            y = []
            for cpus in range(1, max_cpu+1):
                key = ".".join([algo, kind, compiler, str(cpus) if kind != "StreamIt" else "1"])
                s = speed[key] * speed_factor
                y.append(s)

            plot_name = name
            xs = [x + (i-1)*w for x in range(1, max_cpu+1)]

            #color=colorsys.hsv_to_rgb(*color)
            ax.bar(xs, y, width=w, color=colorsys.hsv_to_rgb(*color), edgecolor=None, linewidth=0, label=plot_name)
            #ax.plot(xs, y, 'o', label=plot_name, color=(0.9,0.9,0.9), markeredgewidth=0, markerfacecolor=colorsys.hsv_to_rgb(*color), markersize=3)

    ax.get_xaxis().set_ticks(range(1,7))
    ax.get_xaxis().set_tick_params(length=3, pad=2)

    ax.get_yaxis().set_tick_params(length=2, pad=1)
    #ax.set_aspect('equal')
    ax.autoscale_view()


def main():
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', default='.')
    parser.add_argument('--with-gnu', action='store_true')
    parser.add_argument('--for-slides', action='store_true')
    parser.add_argument('--separate', action='store_true')
    parser.add_argument('--format', default='pdf')
    args = parser.parse_args()

    data, min_speed = read_data()

    #json.dump(data, sys.stdout, indent=2)

    matplotlib.rc('font', size = 8)

    if args.separate:
        generate_separate_plots(data, min_speed)
    else:
        generate_plots(data, min_speed)

    if args.for_slides:
        generate_max_filter_plot(data)

    #generate_plot("filter-bank", data, min_speed["filter-bank"])

main()
