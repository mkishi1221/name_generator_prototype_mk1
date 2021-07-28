#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from numpy import percentile
import orjson as json
import matplotlib.pyplot as plt

filepath = 'dict/wikipedia_word_count/wikipedia-en-words-cumulative.json'

def plot_wikipedia_data(filepath):

    with open(filepath, "rb") as json_file:
        wiki_data = json.loads(json_file.read())

    percentile_10th = 0
    percentile_20th = 0
    percentile_30th = 0
    percentile_40th = 0
    percentile_50th = 0
    percentile_60th = 0
    percentile_70th = 0
    percentile_80th = 0
    percentile_90th = 0
    percentile_99th = 0

    x = []
    y = []

    for data in wiki_data:

        # Generate line graph data
        x.append(data['id'])
        y.append(float(data['cumulative_percentage']))

        # Generate percentile data
        if float(data['cumulative_percentage']) < 0.1:
            percentile_10th += 1
        elif float(data['cumulative_percentage']) < 0.2:
            percentile_20th += 1
        elif float(data['cumulative_percentage']) < 0.3:
            percentile_30th += 1
        elif float(data['cumulative_percentage']) < 0.4:
            percentile_40th += 1
        elif float(data['cumulative_percentage']) < 0.5:
            percentile_50th += 1
        elif float(data['cumulative_percentage']) < 0.6:
            percentile_60th += 1
        elif float(data['cumulative_percentage']) < 0.7:
            percentile_70th += 1
        elif float(data['cumulative_percentage']) < 0.8:
            percentile_80th += 1
        elif float(data['cumulative_percentage']) < 0.9:
            percentile_90th += 1
        else:
            percentile_99th += 1

    print(f"10th percentile: {percentile_10th}")
    print(f"20th percentile: {percentile_20th}")
    print(f"30th percentile: {percentile_30th}")
    print(f"40th percentile: {percentile_40th}")
    print(f"50th percentile: {percentile_50th}")
    print(f"60th percentile: {percentile_60th}")
    print(f"70th percentile: {percentile_70th}")
    print(f"80th percentile: {percentile_80th}")
    print(f"90th percentile: {percentile_90th}")
    print(f"99th percentile: {percentile_99th}")

    # plot line graph with cumulative percentages
    plt.plot(x, y)
    plt.xlabel('words')
    plt.ylabel('cumulative occurrence percentage')
    plt.title('Cumulative word occurrence plot')
    plt.show()

plot_wikipedia_data(filepath)
