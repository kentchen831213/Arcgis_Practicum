
import csv
import numpy as np
import pandas as pd
import os
import glob


#join current file path
path=os.getcwd()

#read all the csv files
csv_files = glob.glob(os.path.join(path,"*.csv"))

for f in csv_files:
    df = pd.read_csv(f,dtype=object, skiprows=1)
    print(df)
    # adjust Wind speed column.
    """
    dictionary for the mapping of description:
    When there is a new values for survey 123
    1. add comma to the last row of the dictionary ex: 'House_dropping _on_ruby_slippers': 'Strong Breeze', <= comma
    2. add 'original':'new description' to a new row
    """

    # claim a structure to save cleaned data
    df_clean = pd.DataFrame()

    # rename and copy column
    df_clean[['ObjectID', 'GlobalID']] = df[['ObjectID', 'GlobalID']]

    # adjust Creator column.
    df['Creator_substring'] = df['Creator'].str.upper()
    # do the remapping
    df_clean['Initials'] = df['Creator_substring'].str.slice(0, 2)

    # adjust CreationDate column.
    new = df["CreationDate"].str.split(" ", n = 1, expand = True)
    # do the remappingew[0]
    df_clean['CollDate'] = new[0]

    # adjust FieldCrew column
    df_clean['FieldCrew'] = df['FieldCrew'].fillna('') + ','+df['Other - FieldCrew'].fillna('')

    #%%
    # combine multiple sites columns into one
    df_clean['SiteName'] = df['SitesChampaignCo'].fillna('') + df['SiteFordCo'].fillna('') + df['SitesHamiltonCo'].fillna('')\
    + df['SitesJacksonCo'].fillna('') + df['SitesJeffersonCo'].fillna('') + df['SitesPerryCo'].fillna('')\
    + df['SitesPopeCo'].fillna('') + df['SitesWilliamsonCo'].fillna('') + df['Other - SiteName'].fillna('')

    # rename and copy column
    df_clean[['County', 'Comment_OpenText']] = df[['County', 'Comment_OpenText']]

    # do the remapping
    wind_map = {'Smoke_rises_vertically_calm': 'Calm',
                'Smoke_drifts_slightly_light_air': 'Light Air',
                'Leaves_rustle_light_breeze': 'Light Breeze',
                'Leaves_constant_motion_gentle_breeze': 'Gentle Breeze',
                'Raises_dust_sm_branches_mod_breeze': 'Moderate Breeze',
                'Sm_trees_sway_fresh_breeze': 'Fresh Breeze',
                'House_dropping _on_ruby_slippers': 'Strong Breeze'
                }

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

    #%%
    # write to cav file
    df_clean.to_csv('./Field_eDNA_cleaned.csv', index=False)
