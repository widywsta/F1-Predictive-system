import pandas as pd
import os

def parser():
    
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    
    current_dir = os.path.dirname(backend_dir)
    
    races_path = os.path.join(current_dir, 'data_kaggle', 'races.csv')
    laps_path = os.path.join(current_dir, 'data_kaggle', 'lap_times.csv')
    tyres_path = os.path.join(current_dir, 'data_kaggle', 'tire_stints.csv')
    drivers_path = os.path.join(current_dir, 'data_kaggle', 'drivers.csv')

    allraces = pd.read_csv(races_path)
    alllaps = pd.read_csv(laps_path)
    alltyres = pd.read_csv(tyres_path)
    alldrivers = pd.read_csv(drivers_path)

    races = allraces[
        (allraces['year'] >= 2021) & (allraces['year'] <= 2025)
    ].copy()

    laps = alllaps[
        alllaps['raceId'].isin(races['raceId'])
    ].copy()



    splitted_time = laps['time'].str.split(':', expand = True)
    laps['time'] = (splitted_time[0].astype(float) * 60) + splitted_time[1].astype(float)



    firsttemporaldf = pd.merge(
        laps,
        races[['raceId', 'year', 'name']],
        how = 'inner',
        on = 'raceId'
    )



    alldrivers["driverId"] = alldrivers["driverId"].astype('int64')



    secondtemporaldf = pd.merge(
        firsttemporaldf,
        alldrivers[['driverId', 'code']],
        how = 'inner',
        on = 'driverId'
    )



    thirdtemporaldf = pd.merge(
        secondtemporaldf,
        alltyres,
        how = 'inner',
        on=["raceId", "driverId"],
    )

    thirdtemporaldf = thirdtemporaldf[
        (thirdtemporaldf['lap'] >= thirdtemporaldf['startLap']) & 
        (thirdtemporaldf['lap'] <= thirdtemporaldf['endLap'])
    ].copy()



    columns = [
        'year',
        'name',
        'code',
        'lap',
        'time',
        'compound',
        'lapsOnTire'
    ]


    main_df = thirdtemporaldf[columns].copy()

    return main_df



# main_df.to_csv("C:/Users/User/Desktop/Ksenia/Программирование/Реальные сайты, работы/F1 Project/main_dataframe.csv", index=False)









