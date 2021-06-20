import pandas as pd
import numpy as np

def clean_ids(x):
    try:
        return int(x)
    except:
        return np.nan

def generate_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #To maintain max size of keywords list to 10 
        if len(names) > 10:
            names = names[:10]
        return names
    return []

def extract_director(x):
    if isinstance(x, list):
        for i in x:
            if (i.get('job') == 'Director'):
                return i['name']

def weighted_rating(data):
    v = data['vote_count'] + 1 # added +1
    R = data['vote_average']
    return (v / (v + m) * R) + (m / (m + v) * C)

def scale_money(num):
    if num < 100:
        return num * 1000000
    elif num >= 100 and num < 1000:
        return num * 10000
    elif num >= 1000 and num < 10000:
        return num *100
    else:
        return num

def list_counter(col, limiter = 9999, log = True):
    result = dict()
    for cell in col:
        if isinstance(cell, float):
            continue
        for element in cell:
            if element in result:
                result[element] += 1
            else:
                result[element] = 1
    if log:
        print("Size of words:", len(result))
    result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}
    if log:
        print("Sorted result is:")
    counter = 1
    sum_selected = 0
    total_selected = 0
    rest = 0
    returned = []
    for i in result: 
        if counter > limiter:
            total_selected += result[i]
        else:
            counter += 1
            sum_selected += result[i]
            total_selected += result[i]
            if log:
                print(result[i], " - ", i) 
            returned.append([i, result[i]])
    if log:
        print("Covered:", sum_selected, "out of", total_selected, "\n")
    return returned

def list_to_col(data, col_name, col_list, limiter = 9999):
    counter = 0
    selected_items = set()
    for item in col_list:
        if counter >= limiter:
            break
        item = item[0]
        data[item] = 0
        selected_items.add(item)
        counter += 1
    
    for index, row in data.iterrows():
        for item in row[col_name]:  
            if item in selected_items:
                data.at[index, item] = 1
    data.drop([col_name], axis=1, inplace=True)
    return data

def binary_mean_dataset_generator(data, col_list, limiter = 9999):
    counter = 0
    items = []
    for item in col_list:
        if counter >= limiter:
            break
        items.append(item[0])
        counter += 1
    rows = []
    for item in items:
        value = data[data[item] == 1].mean()
        rows.append([item, value[0], value[1], value[2], value[3], value[4]])  
    
    df_genres_means = pd.DataFrame(rows, columns=["type", "popularity", "budget", "revenue", 
                                            "vote_count", "rating"])
    return df_genres_means