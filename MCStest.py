import pandas as pd
import csv
import geopy.distance

# Used to aggregate data point closer than 20 meters
# Data points are aggregated averaging the temperature value
# and keeping the location of the first point in the list as
# reference (just for simplicity)
def aggregate_neighbours(data):

    indexes = list(data.index.values)
    aggregated = list()

    for index_i, i in data.iterrows():
        coords_i = list([i['latitude'], i['longitude']])
        if index_i in indexes:
            indexes.remove(index_i)
            for index_j, j in data.iterrows():
                if index_j in indexes and index_i != index_j:
                    coords_j = list([j['latitude'], j['longitude']])
                    if geopy.distance.vincenty(coords_i, coords_j).m < 20:
                        indexes.remove(index_j)
                        i['PerceivedTemperature'] = (i['PerceivedTemperature'] + j['PerceivedTemperature']) / 2
                        aggregated.append(index_j)
                        print("Aggregated!")

    print(aggregated)

    return data.drop(data.index[aggregated])



#####################
### RECEIVE DATA  ###
#####################
data = pd.read_csv('mcs-input.csv', decimal='.', error_bad_lines=False, delimiter=',', quoting=csv.QUOTE_ALL)

###########################
### DATA PRE-PROCESSING ###
###########################
df = data['Coordinates'].str.split(',', expand=True).rename(columns={1: 'longitude', 0: 'latitude'})
df = df.assign(PerceivedTemperature=data['Perceived temperature'].values)
print(df)


#######################
### AGGREGATE DATA  ###
#######################
df = aggregate_neighbours(df)
print(df)

##########################
### STORE INTO A "DB"  ###
##########################
df.to_csv('mcs-cleaned.csv', encoding='utf-8', index=False)
