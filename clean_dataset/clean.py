
import csv
import numpy as np
import pandas as pd

#%%
def deal_with_initial(instring):
    res = instring[:2]
    return "".join(res.upper())

def deal_with_date(datestring):
    res = datestring.split(" ")
    return res[0]

def deal_with_windspeed(speedstring):
    res = speedstring.split("_")
    if res[-1] == "calm" or len(res)==1:
        return res[-1].title()
    else:
        return res[-2].title()+" "+res[-1].title()

# open the original data csv file
file = open('DragPts_eDNA28May21_OriginalExport.csv')
csvreader = csv.reader(file)

# create an output file
writer = csv.writer(open('output.csv','w',newline=''))
head = ["ObjectID",	"GlobalID",	"Initials",	"CollDate",	"FieldCrew", "SiteName", "County", "Comment_OpenText", "WindSpeed",	"CloudCover",
        "HabitatType",	"eDNA_Smpl", "RandomNum_ID", "Number of ticks found",	"SampleID",	"eDNA_SmplID",	"Coord_X",	"Coord_Y",	"RecCheck"]
writer.writerow(head)

# 1	6622b5e3-7f68-4c8e-9f87-a0cee224fd26	JT	6/1/2021	Lee, Tinoco, Kopsco, UruchimaLamczykProperty	Jefferson
# Its on & on drizzling 	Calm	OVC	Gr			0			-88.9756348	38.3032935
rows = []
i = 0
for idx, row in enumerate(csvreader):
    if idx == 0 or idx == 1: continue
    currow = []
    currow.append(row[0])
    currow.append(row[1])
    currow.append(deal_with_initial(row[3]))
    currow.append(deal_with_date(row[2]))
    currow.append(row[7])
    currow.append(" ")
    currow.append(row[11])
    currow.append(row[20])
    currow.append(deal_with_windspeed(row[21]))
    writer.writerow(currow)
#%%
df = pd.read_csv('./clean_dataset/DragPts_eDNA28May21_OriginalExport.csv', skiprows=1)
print(df)
# adjust Wind speed column.
"""
dictionary for the mapping of description: 
When there is a new values for survey 123
1. add comma to the last row of the dictionary ex: 'House_dropping _on_ruby_slippers': 'Strong Breeze', <= comma
2. add 'original':'new description' to a new row
"""
wind_map = {'Smoke_rises_vertically_calm': 'Calm',
            'Smoke_drifts_slightly_light_air': 'Light Air',
            'Leaves_rustle_light_breeze': 'Light Breeze',
            'Leaves_constant_motion_gentle_breeze': 'Gentle Breeze',
            'Raises_dust_sm_branches_mod_breeze': 'Moderate Breeze',
            'Sm_trees_sway_fresh_breeze': 'Fresh Breeze',
            'House_dropping _on_ruby_slippers': 'Strong Breeze'
            }
# claim a structure to save cleaned data
df_clean = pd.DataFrame()
# do the remapping
df_clean['WindSpeed'] = df['WindSpeed'].replace(wind_map)

#%%
# adjust Cloud Color column.
# prepare dictionary for mapping
cloud_map = {'Sky_clear': 'SKC',
             'Few_clouds': 'FEW',
             'Scattered_clouds': 'SCT',
             'Broken_>1_2_cloud_cover':	'BKN',
             'Overcast': 'OVC'
             }
# do the remapping
df_clean['CloudCover'] = df['CloudCover'].replace(cloud_map)

#%%
# adjust Habitat Type column.
# prepare dictionary for mapping
HabitatType_map = {'Maintained forest': 'For',
                   'TransitionalEcotone': 'ecotone',
                   'Grassland': 'Gr',
                   'unmaintained forest': 'UF'
                   }
# do the remapping
df_clean['Habitat'] = df['HabitatType'].replace(HabitatType_map)

#%%
# rename and copy column
df_clean[['eDNA_Smpl', 'RandomNum_ID', 'NumTicks', 'SampleID', 'eDNA_SmplID', 'Coord_X', 'Coord_Y', 'RecCheck']] =\
    df[['Select one or both', 'RandomNum_ID', 'Number of ticks found', 'SampleID', 'eDNA_SmplID', 'x', 'y', 'RecCheck']]
# change data type of NumTicks from float to int
df_clean['NumTicks'].fillna(0, inplace=True)
df_clean = df_clean.astype({'NumTicks': 'int32'})

