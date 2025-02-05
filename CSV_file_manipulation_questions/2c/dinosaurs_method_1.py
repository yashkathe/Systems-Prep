"""
 Write a program to read in the data files from disk, then print the names of only the bipedal dinosaurs from fastest to slowest.

speed = ((STRIDE_LENGTH / LEG_LENGTH) - 1) * SQRT(LEG_LENGTH * g)
Where g = 9.8 m/s^2 (gravitational constant)
"""

# Join Files + Read Data

import pandas as pd
import csv
from collections import defaultdict

# merge files using pandas

df1 = pd.read_csv('./dinosaurs.csv')
df2 = pd.read_csv('./dinosaurs_strides.csv')

merged_csv = pd.merge(df1, df2, on='NAME', how='inner')

merged_csv.to_csv('./pandas_merged.csv')

# read csv

from collections import defaultdict

speed_dino = defaultdict(int)
g = 9.8

with open('./pandas_merged.csv', 'r') as rf:

    reader = csv.DictReader(rf)

    for line in reader:

        stride = float(line['STRIDE_LENGTH'])
        leg = float(line['LEG_LENGTH'])
        dino = line['NAME']

        speed = ((stride / leg) - 1) * (leg ** g)

        # speed_dino[dino] = float(f'{speed:.2f}')
        speed_dino[dino] = round(speed, 2)

speed_dino = sorted(speed_dino.items(), key = lambda x: x[1], reverse=True)

for k, v in speed_dino:
    print(k, v)
    

"""
Tyrannosaurus 61347.77
Allosaurus 19517.22
Velociraptor 8609.75
Stegosaurus 952.78
Struthiomimus 616.27
Triceratops 222.86
Euoplocephalus 31.99
"""