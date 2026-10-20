import itertools

elements = ['HARD', 'MEDIUM', 'SOFT']
final_combinations = []

for length in [2, 3, 4]:
    for combo in itertools.product(elements, repeat=length):
        if len(set(combo)) >= 2:
            final_combinations.append(combo)

print(f"Всего найдено комбинаций: {len(final_combinations)}")

for combination in final_combinations:
    print(f'{combination},')









                     