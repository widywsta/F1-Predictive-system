from backend.data_parser import parser
import pandas as pd
df = parser()

user_track = 'Monaco Grand Prix'
user_tyre = input('Enter the compound ')

all_df = df[df['compound'] == user_tyre]
track_df = df[(df['compound'] == user_tyre) & (df['name'] == user_track)]


def mileage(current_df):
    cliff = 0
    cliffs = []
    if current_df.empty:
        print('current_df is empty')
        return 120.0
    stints = current_df.groupby(["year", "name", "code", "compound"])

    for (year, name, code, compound), stint in stints:
        print(f'checking {year}, {name}, {code}, {compound}...')
        anomal_time = stint['time'].mean()*1.05
        print(f' for this stint anomal time is {anomal_time}')

        clean_stint = stint[stint['time'] <= anomal_time]
        if clean_stint is None:
            print('clean_stint is empty')
            break
        else:
            print('a little bit of clean_stint df:')
            print(clean_stint[:7])

            if len(clean_stint) < 8:
                print('len of clean stint is < 8')
                continue

            best_stint_time = clean_stint['time'].min()
            print(f'best time of the stint is {best_stint_time}')

            stint_laps = clean_stint.to_dict('records')

            for index, row in clean_stint.iterrows():
                for k, row in enumerate(stint_laps):
                    current_tyre_age = row['lap'] - stint['lap'].min() + 1
                    if current_tyre_age <= 3:
                        continue

                    if k + 1 < len(stint_laps):
                            next_row = stint_laps[k + 1]
                            if next_row['time'] > best_stint_time + 1.0:
                                current_race_name = row['name']
                                hist_lap_len = 3.337
                                cliff = current_tyre_age * hist_lap_len
                                cliffs.append(cliff)
                                break
                            else:
                                continue




                
                # if row['time'] > best_stint_time + 1.5:
                #     print('row["time"] > best_stint_time + 1.5 (we found THE CLIFF)')
                #     current_race_name = row['name']
                #     print(f' current race name is {current_race_name}')
                #     hist_lap_len = 3.337
                #     cliff = current_tyre_age * hist_lap_len
                #     print(f'our cliff is {cliff}')
                #     # cliff = row['lapsOnTire'] * track_lengths[user_track]['len']
                #     cliffs.append(cliff)
                #     break

    if not cliffs:
        print('NO CLIFFS, USING 120.0 KM INSTEAD')
        return 120.0    

    cliff_df = pd.DataFrame(cliffs)

    anomal_cliff = cliff_df[0].mean()*1.05

    clean_cliff = cliff_df[cliff_df[0] <= anomal_cliff]

    return clean_cliff[0].mean()

# all_mileage_lap = round(mileage(all_df)/3.337)
track_mileage_km = round(mileage(track_df))
track_mileage_lap = round(mileage(track_df)/3.337)

# print(f'Average mileage of your stint for all tracks: {round(mileage(all_df))} km = {all_mileage_lap} laps')
print(f'Average mileage of your stint for only your track: {track_mileage_km} km = {track_mileage_lap} laps')

