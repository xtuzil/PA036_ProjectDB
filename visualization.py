#!/usr/bin/env python3
import os

import matplotlib.pyplot as plt
import numpy
import json
import math

# https://matplotlib.org/stable/gallery/color/named_colors.html
colors = {
    "MongoDB": "limegreen",
    "MongoDB with index": "green",
    
    "PostgreSQL binary json": "deepskyblue",
    "PostgreSQL with index jsonb_ops": "lightskyblue",
    "PostgreSQL with index jsonb_path_ops": "steelblue",
}

label_names = {
    "MongoDB": "MDB",
    "MongoDB with index": "MDB indexed",
    
    "PostgreSQL binary json": "PSQL",
    "PostgreSQL with index jsonb_ops": "PSQL indexed\n(jsonb_ops)",
    "PostgreSQL with index jsonb_path_ops": "PSQL indexed\n(jsonb_path_ops)",
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
                new_column.append(value / maximum if maximum != 0 else value)
    return result

def preprocess(results):
    width = math.ceil(math.sqrt(len(results)))
    fig, axes = plt.subplots(
        ncols = width,
        nrows = (len(results) + width - 1) // width,
        # This determines the size in pixels of the final image
        figsize = [width * 8 * i for i in (1, 1)]
    )
    
    return width, fig, axes

def make_bar(ax, labels, data):
    for label, d in zip(labels, data):
        ax.bar(
            label_names[label],
            numpy.average(d) * 1000,
            yerr = numpy.std(d) * 1000,
            width = 0.35,
            color = colors[label],
        )

def title_of(result):
    description = result[1]["description"]
    return result[0] + (": " + description if description else "")

def savefigs(output_name, results):
    width, fig, axes = preprocess(results)
    
    for result, index in zip(results.items(), range(len(results))):
        ax = axes[index // width][index % width]
        
        labels = list(result[1]["columns"].keys())
        data = [column for column in result[1]["columns"].values()]
        
        make_bar(ax, labels, data)
        
        ax.set_title(title_of(result))
        
        ax.set_ylim(0)
        
        ## Set axis names
        ax.yaxis.grid(True)
        ax.set_xlabel("Database type")
        ax.set_ylabel("Time [ms]")
        
    plt.savefig(output_name)

def savefigs_each(output_prefix, results):
    for result, index in zip(results.items(), range(len(results))):
        fig, ax = plt.subplots(figsize = (8, 8))
        
        labels = list(result[1]["columns"].keys())
        data = [column for column in result[1]["columns"].values()]
        
        make_bar(ax, labels, data)
        
        ax.set_title(title_of(result))
        
        ax.set_ylim(0)
        
        ## Set axis names
        ax.yaxis.grid(True)
        ax.set_xlabel("Database type")
        ax.set_ylabel("Time [ms]")
        
        plt.savefig(output_prefix + result[0] + ".png")
        plt.close(fig)

def savefigs_grouped(output_name, results):
    width, fig, axes = preprocess(results)
    
    for result, index in zip(results, range(len(results))):
        ax = axes[index // width][index % width]
        
        labels = list(result["columns"].keys())
        data = [column for column in result["columns"].values()]
        
        bar = ax.bar(
            [label_names[label] for label in labels],
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

if not os.path.exists("visualization_output/"):
    os.mkdir("visualization_output/")


savefigs_each("visualization_output/query-", results)

savefigs("visualization_output/queries.png", results)

savefigs_grouped("visualization_output/queries-grouped.png", [
    normalize("selecty", [
        "1", "2", "3", "4", "5", "6",
    ]),
    normalize("selecty s podmienkami", [
        "7", "8", "9", "10", "11", "12", "13", "14", "15",
    ]),
    normalize("join", [
        "16",
    ]),
    normalize("agregacie", [
        "17", "18", "19", "20", "21", "22", "23",
    ]),
    normalize("select + podmienka + agregace", [
        "24", "25",
    ]),
    normalize("doplnkovy count na prikazoch", [
        "26", "27", "28", "29", "30", "31", "32", "33",
    ]),
    normalize("insert jeden zaznam", [
        "34",
    ]),
    normalize("update", [
        "35", "36", "37", "38", "39", "40", "41",
    ]),
    normalize("delete", [
        "42", "43", "44", "45", "46",
    ]),
    normalize("sort + limit", [
        "47", "48",
    ]),
    normalize("lookup/join + aggregate", [
        "49", "50",
    ]),
    normalize("distinct", [
        "51",
    ]),
])
