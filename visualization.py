#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy
import json
import math

# https://matplotlib.org/stable/gallery/color/named_colors.html
colors = {
    "MongoDB": "limegreen",
    "MongoDB with index": "green",
    
    "PostgreSQL text json": "skyblue",
    "PostgreSQL binary json": "deepskyblue",
    "PostgreSQL with index jsonb_ops": "lightskyblue",
    "PostgreSQL with index jsonb_path_ops": "steelblue",
}

def normalize(description, names):
    columns = {}
    result = {
        "description": description,
        "columns": columns,
    }
    for name in names:
        maximum = 0
        for column_values in results[name]["columns"].values():
            for value in column_values:
                maximum = max(maximum, value)
        for column_name, column_values in results[name]["columns"].items():
            new_column = columns.setdefault(column_name, [])
            for value in column_values:
                new_column.append(value / maximum)
    return result

def preprocess(results):
    width = math.ceil(math.sqrt(len(results)))
    fig, axes = plt.subplots(
        ncols = width,
        nrows = (len(results) + width - 1) // width,
        # This determines the size in pixels of the final image
        figsize = [width * 6 * i for i in (1, 1)]
    )
    
    return width, fig, axes

def savefigs(output_name, results):
    width, fig, axes = preprocess(results)
    
    for result, index in zip(results.values(), range(len(results))):
        ax = axes[index // width][index % width]
        labels = list(result["columns"].keys())
        data = [column for column in result["columns"].values()]
        
        bar = ax.bar(
            labels,
            [numpy.average(d) * 1000 for d in data],
            yerr = [numpy.std(d) * 1000 for d in data],
            width = 0.35,
            color = [colors[col] for col in labels],
        )
        
        ax.set_title(result["description"])
        
        ax.set_ylim(0)
        
        ## Set axis names
        ax.yaxis.grid(True)
        ax.set_xlabel("Database type")
        ax.set_ylabel("Time [ms]")
        
    plt.savefig(output_name)

def savefigs_grouped(output_name, results):
    width, fig, axes = preprocess(results)
    
    for result, index in zip(results, range(len(results))):
        ax = axes[index // width][index % width]
        
        labels = list(result["columns"].keys())
        data = [column for column in result["columns"].values()]
        
        bar = ax.bar(
            labels,
            [numpy.average(d) for d in data],
            yerr = [numpy.std(d) for d in data],
            width = 0.35,
            color = [colors[col] for col in labels],
        )
        
        ax.set_title(result["description"])
        
        ax.set_ylim(0)
        
        ## Set axis names
        ax.yaxis.grid(True)
        ax.set_xlabel("Database type")
        ax.set_ylabel("Relative time")
        
    plt.savefig(output_name)

################################################################################

with open("results.json", "r") as results_file:
    results = json.load(results_file)

savefigs("queries.png", results)

savefigs_grouped("queries-grouped.png", [normalize("selecty", [
        "6", "7", "21", "24", "26", "28",
    ]),
    normalize("selecty s podmienkami", [
        "1", "2", "3", "4", "5", "29", "31", "32",
    ]),
    normalize("join", [
        "8",
    ]),
    normalize("agregacie", [
        "9", "10", "11", "12", "14", "23", "30",
    ]),
    normalize("select + podmienka + agregace", [
        "13"
    ]),
    normalize("doplnkovy count na prikazoch", [
        "15", "16", "17", "18", "19", "20", "22", "25", "27",
    ]),
    normalize("insert jeden zaznam", [
        "33",
    ]),
    normalize("update", [
        "34", "35", "36", "37", "38", "39", "40",
    ]),
    normalize("delete", [
        "41", "42", "43", "44", "45",
    ]),
])
