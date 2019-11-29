import matplotlib
import json
import sys
import matplotlib.pyplot as plt
from pathlib import Path

cd = Path(__file__).parent
data_dir = cd.parent / 'data' / 'buf-mode'

def read_json_file(filename):
    f = open(filename)
    return json.load(f)

def read_data():

    raw_arrp_data = read_json_file(data_dir / "arrp-report.json")
    raw_arrp_data_extra = read_json_file(data_dir / "arrp-report-extra.json")
    for key, value in raw_arrp_data_extra.items():
        raw_arrp_data[key] = value

    data = {}

    for key, value in raw_arrp_data.items():

        algo = value["algo"]

        if value["hoist"] != True or value["vector"] != True:
            continue

        key_elems = [
            algo,
            "arrp",
            value["buffer"],
        ]

        new_key = ".".join(key_elems)
        data[new_key] = value["storage"]["memory"]

    # Now sort data in a consistent order

    #json.dump(data, sys.stdout, indent=2)


    raw_ref_data = read_json_file(data_dir / "ref-storage-size.json")

    for algo, modes in raw_ref_data.items():
        for mode, storage in modes.items():
            key_elems = [
                algo,
                "ref",
                mode,
            ]
            new_key = ".".join(key_elems)
            data[new_key] = storage

    raw_opt_data = read_json_file(data_dir / "opt-storage-size.json")

    for algo, value in raw_opt_data.items():
        new_key = ".".join([algo, "opt", "_"])
        data[new_key] = value

    return data


def make_graphs(data):

    fig = plt.figure(figsize = (5.2, 4))

    for i, algo in enumerate(["filter-bank", "max-filter", "ac", "wave1d", "wave2d"]):
        make_graph(i, algo, data)

    fig.legend(bbox_to_anchor=(0.8,0.1), loc="lower right")

    plt.tight_layout(0)

    plt.savefig("buf-mode-storage.svg", format="svg")
    plt.savefig("buf-mode-storage.eps", format="eps")


def make_graph(i, algo, data):

    ax = plt.subplot(3,2,i+1)
    ax.set_title(algo)

    min_size = -1
    for key, size in data.items():
        if not key.startswith(algo + "."): continue
        if min_size < 0 or size < min_size:
            min_size = size

    width = 1 / 3
    offset = 0

    for mode in ["mod", "mask", "shift"]:
        height = []
        for kind in ["ref", "arrp"]:
            key = ".".join([algo, kind, mode])
            if key in data:
                size = data[key]
            else:
                size = 0
            height.append(size / min_size)

        plt.bar([i + offset for i in range(len(height))],
                height, width * 0.6, label = mode)

        offset += width


    kindlabels = ["ref", "arrp"]
    plt.xticks(range(len(kindlabels)), kindlabels, rotation=0)

def make_table(data):

    algo_storage = {}
    algo_min_storage = {}
    algo_max_storage = {}

    for algo in ["filter-bank", "max-filter", "ac", "wave1d", "wave2d"]:
        storage = []
        min_storage = -1
        for kind in ["ref", "opt", "arrp"]:
            for mode in ["mod", "mask", "shift", "_"]:
                key = ".".join([algo, kind, mode])
                if key not in data:
                    continue
                storage.append(data[key])
        algo_storage[algo] = storage
        algo_min_storage[algo] = min(storage)
        algo_max_storage[algo] = max(storage)


    f = open("buf-mode-storage.tex", 'w')

    ncols = 7
    nrows = 5

    column_format = "l"
    for i in range(ncols):
        column_format += " c"

    f.write("\\begin{tabular}{" + column_format + "}\n")
    f.write("\\toprule\n")
    f.write("Algorithm & \multicolumn{3}{c}{C++ AO} & C++ HO & \multicolumn{3}{c}{Arrp}\\\\\n")
    f.write(" & mod & mask & shift & best & mod & mask & shift \\\\\n")
    f.write("\\midrule\n")
    for algo in ["filter-bank", "max-filter", "ac", "wave1d", "wave2d"]:
        row = algo
        found_min = False
        found_max = False
        for value in algo_storage[algo]:
            byte_count = value / 1024 / 1024

            if algo == "ac":
                byte_count_s = "{:.2f}".format(byte_count)
            else:
                byte_count_s = "{:.1f}".format(byte_count)

            bold = False
            if not found_min and value == algo_min_storage[algo]:
                found_min = True
                bold = True
            elif not found_max and value == algo_max_storage[algo]:
                found_max = True
                bold = True

            if bold:
                byte_count_s = "\\textbf{" + byte_count_s + "}"

            row += " & " + byte_count_s

        f.write(row + " \\\\\n")
    f.write("\\bottomrule\n")
    f.write("\\end{tabular}")


def main():
    data = read_data()

    #make_graphs(data)

    make_table(data)


main()
