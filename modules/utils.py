import pandas as pd

data = None
cluster_info = None

with open('./modules/util.txt', 'r') as file:
    data = file.read().replace('\n', ' ')


with open('./modules/cluster_info.txt', 'r') as file:
    cluster_info = file.read().replace('\n', ' ')

