import random
from PIL import Image

img = Image.open('c:/Users/User/Desktop/Ksenia/Программирование/Реальные сайты, работы/F1 Project/casual tasks/cryptic.png')
pixels = list(img.get_flattened_data())

P = list(range(len(pixels)))

random.seed(42)
random.shuffle(P)

shuffled_pixels = [pixels[i] for i in P]

img.putdata(shuffled_pixels)
img.save('c:/Users/User/Desktop/Ksenia/Программирование/Реальные сайты, работы/F1 Project/casual tasks/cryptic_shuffled.png')
