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

with open("results.json", "r") as results_file:
    results = json.load(results_file)

mat_size = math.ceil(math.sqrt(len(results)))
fig, axes = plt.subplots(
    nrows = mat_size, ncols = mat_size,
    # This determines the size in pixels of the final image
    figsize = [mat_size * 6 * i for i in (1, 1)]
)

for result, index in zip(results.values(), range(mat_size * mat_size)):
    ax = axes[index // mat_size][index % mat_size]
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

plt.savefig("queries.png")
