#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import json

# https://matplotlib.org/stable/gallery/color/named_colors.html
colors = {
    "MongoDB": "limegreen",
    "PostgreSQL": "skyblue",
    
    "MongoDB with index": "limegreen",
    "PostgreSQL with index": "skyblue",
}

with open("results.json", "r") as results_file:
    results = json.load(results_file)

#for result in results.values():
for result in results["1"],:
    labels = list(result["columns"].keys())
    data = [[i * 1000 for i in column] for column in result["columns"].values()]
    
    fig, ax = plt.subplots()
    
    boxplot = ax.boxplot(
        data,
        vert = True,  # vertical box alignment
        patch_artist = True,  # fill with color
        labels = labels,
        showfliers = False,
    )  # will be used to label x-ticks
    
    ax.set_title(result["description"])
    
    ## Set colors
    for patch, label in zip(boxplot["boxes"], labels):
        patch.set_facecolor(colors[label])
    
    ax.set_ylim(0)
    
    ## Set axis names
    ax.yaxis.grid(True)
    ax.set_xlabel("Database type")
    ax.set_ylabel("Time [ms]")
    
    plt.show()
    
    print(labels)
    print(result)
