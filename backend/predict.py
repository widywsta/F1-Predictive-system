import os
import pandas as pd
from .data_parser import parser


track_lengths = {
    'Abu Dhabi Grand Prix': {'len': 5.281, 'laps': 58, 'country': 'ОАЭ', 'asphalt': 'Низкая абразивность (гладкий)', 'climate': 'Сухой, жаркий пустынный', 'img': '/frontend/track_img/abudhabi.png'},
    'Australian Grand Prix': {'len': 5.278, 'laps': 58, 'country': 'Австралия', 'asphalt': 'Средняя абразивность (полугородской)', 'climate': 'Переменчивый, весенний', 'img': '/frontend/track_img/australia.png'},
    'Austrian Grand Prix': {'len': 4.318, 'laps': 71, 'country': 'Австрия', 'asphalt': 'Средняя абразивность', 'climate': 'Прохладный, горный (Альпы)', 'img': 'https://formula1.com'},
    'Azerbaijan Grand Prix': {'len': 6.003, 'laps': 51, 'country': 'Азербайджан', 'asphalt': 'Ультра-низкая абразивность (городской)', 'climate': 'Ветреный, умеренно жаркий', 'img': 'https://formula1.com'},
    'Bahrain Grand Prix': {'len': 5.412, 'laps': 57, 'country': 'Бахрейн', 'asphalt': 'Экстремально высокая абразивность (высокий износ)', 'climate': 'Жаркий, сухой ночной', 'img': 'https://formula1.com'},
    'Belgian Grand Prix': {'len': 7.004, 'laps': 44, 'country': 'Бельгия', 'asphalt': 'Высокая абразивность (высокие перегрузки)', 'climate': 'Непредсказуемый, частые дожди', 'img': 'https://formula1.com'},
    'British Grand Prix': {'len': 5.891, 'laps': 52, 'country': 'Великобритания', 'asphalt': 'Экстремально высокая абразивность (жесткие повороты)', 'climate': 'Прохладный, ветреный, дождливый', 'img': 'https://formula1.com'},
    'Canadian Grand Prix': {'len': 4.361, 'laps': 70, 'country': 'Канада', 'asphalt': 'Низкая абразивность (городской парк)', 'climate': 'Переменчивый, умеренный', 'img': 'https://formula1.com'},
    'Chinese Grand Prix': {'len': 5.451, 'laps': 56, 'country': 'Китай', 'asphalt': 'Средне-высокая абразивность (износ передней левой)', 'climate': 'Умеренный, влажный', 'img': 'https://formula1.com'},
    'Dutch Grand Prix': {'len': 4.259, 'laps': 72, 'country': 'Нидерланды', 'asphalt': 'Средняя абразивность (профилированные виражи)', 'climate': 'Морской, сильный ветер с песком', 'img': 'https://formula1.com'},
    'Emilia Romagna Grand Prix': {'len': 4.909, 'laps': 63, 'country': 'Италия (Имола)', 'asphalt': 'Средне-высокая абразивность (старый асфальт)', 'climate': 'Теплый, весенне-летний', 'img': 'https://formula1.com'},
    'Hungarian Grand Prix': {'len': 4.381, 'laps': 70, 'country': 'Венгрия', 'asphalt': 'Средняя абразивность (очень пыльный трек)', 'climate': 'Экстремально жаркий, душный', 'img': 'https://formula1.com'},
    'Italian Grand Prix': {'len': 5.793, 'laps': 53, 'country': 'Италия (Монца)', 'asphalt': 'Средняя абразивность (высокие скорости)', 'climate': 'Жаркий, средиземноморский', 'img': 'https://formula1.com'},
    'Japanese Grand Prix': {'len': 5.807, 'laps': 53, 'country': 'Япония', 'asphalt': 'Высокая абразивность (абразивный старый состав)', 'climate': 'Прохладный, высокий риск тайфунов', 'img': 'https://formula1.com'},
    'Las Vegas Grand Prix': {'len': 6.201, 'laps': 50, 'country': 'США (Лас-Вегас)', 'asphalt': 'Ультра-низкая абразивность (новый городской)', 'climate': 'Очень холодный, ночной (проблемы с прогревом)', 'img': 'https://formula1.com'},
    'Mexico City Grand Prix': {'len': 4.304, 'laps': 71, 'country': 'Мексика', 'asphalt': 'Низкая абразивность (пыльный)', 'climate': 'Разреженный воздух (высокогорье), тепло', 'img': 'https://formula1.com'},
    'Miami Grand Prix': {'len': 5.412, 'laps': 57, 'country': 'США (Майами)', 'asphalt': 'Низкая абразивность (гладкий искусственный)', 'climate': 'Тропический, очень жаркий и влажный', 'img': 'https://formula1.com'},
    'Monaco Grand Prix': {'len': 3.337, 'laps': 78, 'country': 'Монако', 'asphalt': 'Минимальная абразивность в календаре (городские улицы)', 'climate': 'Жаркий, морской', 'img': 'https://formula1.com'},
    'Qatar Grand Prix': {'len': 5.419, 'laps': 57, 'country': 'Катар', 'asphalt': 'Высокая абразивность (острые поребрики/кербы)', 'climate': 'Экстремально жаркий, влажный ночной', 'img': 'https://formula1.com'},
    'Saudi Arabian Grand Prix': {'len': 6.174, 'laps': 50, 'country': 'Саудовская Аравия', 'asphalt': 'Низкая абразивность (очень быстрый городской)', 'climate': 'Жаркий ночной', 'img': 'https://formula1.com'},
    'Singapore Grand Prix': {'len': 4.940, 'laps': 62, 'country': 'Сингапур', 'asphalt': 'Низкая абразивность (кочки, люки, разметка)', 'climate': 'Экстремальная влажность, удушающая жара', 'img': 'https://formula1.com'},
    'Spanish Grand Prix': {'len': 4.657, 'laps': 66, 'country': 'Испания', 'asphalt': 'Высокая абразивность (тестовый трек)', 'climate': 'Жаркий, сухой летний', 'img': 'https://formula1.com'},
    'São Paulo Grand Prix': {'len': 4.309, 'laps': 71, 'country': 'Бразилия', 'asphalt': 'Средне-высокая абразивность (изменчивый зацеп)', 'climate': 'Экстремально изменчивый (резкие ливни)', 'img': 'https://formula1.com'},
    'United States Grand Prix': {'len': 5.513, 'laps': 56, 'country': 'США (Остин)', 'asphalt': 'Высокая абразивность (сильные кочки из-за просадки грунта)', 'climate': 'Переменчивый, ветреный осенью', 'img': 'https://formula1.com'}
}


strategy_vars = {
('HARD', 'MEDIUM'),
('HARD', 'SOFT'),
('MEDIUM', 'HARD'),
('MEDIUM', 'SOFT'),
('SOFT', 'HARD'),
('SOFT', 'MEDIUM'),
('HARD', 'HARD', 'MEDIUM'),
('HARD', 'HARD', 'SOFT'),
('HARD', 'MEDIUM', 'HARD'),
('HARD', 'MEDIUM', 'MEDIUM'),
('HARD', 'MEDIUM', 'SOFT'),
('HARD', 'SOFT', 'HARD'),
('HARD', 'SOFT', 'MEDIUM'),
('HARD', 'SOFT', 'SOFT'),
('MEDIUM', 'HARD', 'HARD'),
('MEDIUM', 'HARD', 'MEDIUM'),
('MEDIUM', 'HARD', 'SOFT'),
('MEDIUM', 'MEDIUM', 'HARD'),
('MEDIUM', 'MEDIUM', 'SOFT'),
('MEDIUM', 'SOFT', 'HARD'),
('MEDIUM', 'SOFT', 'MEDIUM'),
('MEDIUM', 'SOFT', 'SOFT'),
('SOFT', 'HARD', 'HARD'),
('SOFT', 'HARD', 'MEDIUM'),
('SOFT', 'HARD', 'SOFT'),
('SOFT', 'MEDIUM', 'HARD'),
('SOFT', 'MEDIUM', 'MEDIUM'),
('SOFT', 'MEDIUM', 'SOFT'),
('SOFT', 'SOFT', 'HARD'),
('SOFT', 'SOFT', 'MEDIUM'),
('HARD', 'HARD', 'HARD', 'MEDIUM'),
('HARD', 'HARD', 'HARD', 'SOFT'),
('HARD', 'HARD', 'MEDIUM', 'HARD'),
('HARD', 'HARD', 'MEDIUM', 'MEDIUM'),
('HARD', 'HARD', 'MEDIUM', 'SOFT'),
('HARD', 'HARD', 'SOFT', 'HARD'),
('HARD', 'HARD', 'SOFT', 'MEDIUM'),
('HARD', 'HARD', 'SOFT', 'SOFT'),
('HARD', 'MEDIUM', 'HARD', 'HARD'),
('HARD', 'MEDIUM', 'HARD', 'MEDIUM'),
('HARD', 'MEDIUM', 'HARD', 'SOFT'),
('HARD', 'MEDIUM', 'MEDIUM', 'HARD'),
('HARD', 'MEDIUM', 'MEDIUM', 'MEDIUM'),
('HARD', 'MEDIUM', 'MEDIUM', 'SOFT'),
('HARD', 'MEDIUM', 'SOFT', 'HARD'),
('HARD', 'MEDIUM', 'SOFT', 'MEDIUM'),
('HARD', 'MEDIUM', 'SOFT', 'SOFT'),
('HARD', 'SOFT', 'HARD', 'HARD'),
('HARD', 'SOFT', 'HARD', 'MEDIUM'),
('HARD', 'SOFT', 'HARD', 'SOFT'),
('HARD', 'SOFT', 'MEDIUM', 'HARD'),
('HARD', 'SOFT', 'MEDIUM', 'MEDIUM'),
('HARD', 'SOFT', 'MEDIUM', 'SOFT'),
('HARD', 'SOFT', 'SOFT', 'HARD'),
('HARD', 'SOFT', 'SOFT', 'MEDIUM'),
('HARD', 'SOFT', 'SOFT', 'SOFT'),
('MEDIUM', 'HARD', 'HARD', 'HARD'),
('MEDIUM', 'HARD', 'HARD', 'MEDIUM'),
('MEDIUM', 'HARD', 'HARD', 'SOFT'),
('MEDIUM', 'HARD', 'MEDIUM', 'HARD'),
('MEDIUM', 'HARD', 'MEDIUM', 'MEDIUM'),
('MEDIUM', 'HARD', 'MEDIUM', 'SOFT'),
('MEDIUM', 'HARD', 'SOFT', 'HARD'),
('MEDIUM', 'HARD', 'SOFT', 'MEDIUM'),
('MEDIUM', 'HARD', 'SOFT', 'SOFT'),
('MEDIUM', 'MEDIUM', 'HARD', 'HARD'),
('MEDIUM', 'MEDIUM', 'HARD', 'MEDIUM'),
('MEDIUM', 'MEDIUM', 'HARD', 'SOFT'),
('MEDIUM', 'MEDIUM', 'MEDIUM', 'HARD'),
('MEDIUM', 'MEDIUM', 'MEDIUM', 'SOFT'),
('MEDIUM', 'MEDIUM', 'SOFT', 'HARD'),
('MEDIUM', 'MEDIUM', 'SOFT', 'MEDIUM'),
('MEDIUM', 'MEDIUM', 'SOFT', 'SOFT'),
('MEDIUM', 'SOFT', 'HARD', 'HARD'),
('MEDIUM', 'SOFT', 'HARD', 'MEDIUM'),
('MEDIUM', 'SOFT', 'HARD', 'SOFT'),
('MEDIUM', 'SOFT', 'MEDIUM', 'HARD'),
('MEDIUM', 'SOFT', 'MEDIUM', 'MEDIUM'),
('MEDIUM', 'SOFT', 'MEDIUM', 'SOFT'),
('MEDIUM', 'SOFT', 'SOFT', 'HARD'),
('MEDIUM', 'SOFT', 'SOFT', 'MEDIUM'),
('MEDIUM', 'SOFT', 'SOFT', 'SOFT'),
('SOFT', 'HARD', 'HARD', 'HARD'),
('SOFT', 'HARD', 'HARD', 'MEDIUM'),
('SOFT', 'HARD', 'HARD', 'SOFT'),
('SOFT', 'HARD', 'MEDIUM', 'HARD'),
('SOFT', 'HARD', 'MEDIUM', 'MEDIUM'),
('SOFT', 'HARD', 'MEDIUM', 'SOFT'),
('SOFT', 'HARD', 'SOFT', 'HARD'),
('SOFT', 'HARD', 'SOFT', 'MEDIUM'),
('SOFT', 'HARD', 'SOFT', 'SOFT'),
('SOFT', 'MEDIUM', 'HARD', 'HARD'),
('SOFT', 'MEDIUM', 'HARD', 'MEDIUM'),
('SOFT', 'MEDIUM', 'HARD', 'SOFT'),
('SOFT', 'MEDIUM', 'MEDIUM', 'HARD'),
('SOFT', 'MEDIUM', 'MEDIUM', 'MEDIUM'),
('SOFT', 'MEDIUM', 'MEDIUM', 'SOFT'),
('SOFT', 'MEDIUM', 'SOFT', 'HARD'),
('SOFT', 'MEDIUM', 'SOFT', 'MEDIUM'),
('SOFT', 'MEDIUM', 'SOFT', 'SOFT'),
('SOFT', 'SOFT', 'HARD', 'HARD'),
('SOFT', 'SOFT', 'HARD', 'MEDIUM'),
('SOFT', 'SOFT', 'HARD', 'SOFT'),
('SOFT', 'SOFT', 'MEDIUM', 'HARD'),
('SOFT', 'SOFT', 'MEDIUM', 'MEDIUM'),
('SOFT', 'SOFT', 'MEDIUM', 'SOFT'),
('SOFT', 'SOFT', 'SOFT', 'HARD'),
('SOFT', 'SOFT', 'SOFT', 'MEDIUM'),
}


df = parser()

# user_track = input('Enter the grand-prix ')
# user_tyre = input('Enter the compound ')

# all_df = df[df['compound'] == user_tyre]
# track_df = df[(df['compound'] == user_tyre) & (df['name'] == user_track)]

def mileage(current_df):
    if current_df.empty:
        return 120.0

    cliff = 0
    cliffs = []
    stints = current_df.groupby(["year", "name", "code", "compound"])

    for (year, name, code, compound), stint in stints:
        anomal_time = stint['time'].mean()*1.05
        clean_stint = stint[stint['time'] <= anomal_time]
        
        if len(clean_stint) < 8:
            continue

        best_stint_time = clean_stint['time'].min()
        stint_laps = clean_stint.to_dict('records')

  
        for k, row in enumerate(stint_laps):
            current_tyre_age = row['lap'] - stint['lap'].min() + 1

            if current_tyre_age <= 3:
                continue

            threshold = 2000.0 if best_stint_time > 5000 else 2.0
            next_threshold = 1500.0 if best_stint_time > 5000 else 1.5
    
            if row["time"] > best_stint_time + threshold:
                if k + 2 < len(stint_laps):
                    next_row_1 = stint_laps[k + 1]
                    next_row_2 = stint_laps[k + 2]
                    
                    if (next_row_1['time'] > best_stint_time + next_threshold) and (next_row_2['time'] > best_stint_time + next_threshold):
                        current_race_name = row['name']
                        hist_lap_len = track_lengths.get(current_race_name, {'len': 5.2})['len']
                        cliff = row['lapsOnTire'] * hist_lap_len
                        cliffs.append(cliff)
                        break

    if not cliffs:
        return 120.0    

    cliff_df = pd.DataFrame(cliffs)
    first_column = cliff_df.iloc[:, 0]
    clean_cliff = cliff_df[first_column <= first_column.mean() * 1.05]
    
    if clean_cliff.empty:
        return 120.0
    
    return float(clean_cliff.iloc[:, 0].mean())


# all_mileage_km = round(mileage(all_df))
# all_mileage_lap = round(mileage(all_df)/track_lengths[user_track]['len'])
# track_mileage_km = round(mileage(track_df))
# track_mileage_lap = round(mileage(track_df)/track_lengths[user_track]['len'])

# print(f'Average mileage of your stint for all tracks: {all_mileage_km} km = {all_mileage_lap} laps')
# print(f'Average mileage of your stint for only your track: {track_mileage_km} km = {track_mileage_lap} laps')





def race_strategy(track_name, safety_reserve):
    lap_len = track_lengths[track_name]['len']
    lap_num = track_lengths[track_name]['laps']
    
    # safety_reserve = int(input("Enter the number if safe (reserve) laps for a stint from 0 (very risky) to 3 (very safe)"))

    soft_df = df[(df["compound"] == "SOFT") & (df["name"] == track_name)]
    medium_df = df[(df["compound"] == "MEDIUM") & (df["name"] == track_name)]
    hard_df = df[(df["compound"] == "HARD") & (df["name"] == track_name)]


    if soft_df.empty: soft_df = df[df["compound"] == "SOFT"]
    if medium_df.empty: medium_df = df[df["compound"] == "MEDIUM"]
    if hard_df.empty: hard_df = df[df["compound"] == "HARD"]

    base_soft_km = mileage(soft_df)
    base_medium_km = mileage(medium_df)
    base_hard_km = mileage(hard_df)

    if track_name == "Monaco Grand Prix":
        soft_km = 25.0 * 3.337
        medium_km = 38.0 * 3.337
        hard_km = 50.0 * 3.337
    else:
        soft_km = max(55.0, base_soft_km)
        medium_km = max(90.0, base_medium_km)
        hard_km = max(130.0, base_hard_km)

    tyre_average_laps = {
        'SOFT': int(round(soft_km / lap_len)),
        'MEDIUM': int(round(medium_km / lap_len)),
        'HARD': int(round(hard_km / lap_len))
    }


    strategies = []
     

    for var_strategy in strategy_vars:
        current_lap = 1
        failed = False
        pit_laps = []
        current_chain = list(var_strategy)
        stints_safety = []

        for idx, tyre in enumerate(current_chain):
            average_mileage = tyre_average_laps.get(tyre, 15)

            if idx < (len(current_chain) - 1):
                pit_lap = current_lap + max(1, (average_mileage - safety_reserve))


                if (pit_lap > (lap_num - 6) and pit_lap <= lap_num) or pit_lap < 4:
                    failed = True
                    break
                else:
                    pit_laps.append(pit_lap)
                stints_safety.append(safety_reserve)
                current_lap = pit_lap
            else:
                laps_till_end = lap_num - current_lap
                if average_mileage < laps_till_end:
                    failed = True
                    break
                stints_safety.append(average_mileage - laps_till_end)


        if not failed:
            max_allowed_pits = 3 if lap_num > 75 else 2
            if len(pit_laps) <= max_allowed_pits:
                strategies.append({
                    'chain': current_chain,
                    'pits': pit_laps,
                    'safety': min(stints_safety) if stints_safety else 0
                })
            
    top_strategies = sorted(strategies, key=lambda x: (len(x['pits']), -x['safety']))

    # print(f"\n --- ТОП ОПТИМАЛЬНЫХ СТРАТЕГИЙ ДЛЯ {track_name.upper()} ---")
    # if not top_strategies:
    #     print('Found no strategies for these conditions and settings')
    #     return
    
    # for idx, strategy in enumerate(top_strategies, 1):
    #     chain_text = " -> ".join(strategy["chain"])
    #     pit_strings = [f"Lap {p} (pit-window: {p-3} - {p+2})" for p in strategy["pits"]]
    #     pit_info = " , ".join(pit_strings) if pit_strings else "No pitstops till the checked flag"

    #     print(f"\n{idx}. {chain_text}")
    #     print(f"   Pitstop windows: {pit_info}")

    #     if "safety" in strategy:
    #         print(f"   Safety index: +{strategy['safety']} laps in reserve")

    return top_strategies, tyre_average_laps

# race_strategy(user_track)                
