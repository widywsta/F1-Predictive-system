flag = b"?F%^4F8\x02[A\x1a9~'9iu#WeY&\x1eQ"
key = [73, 53, 74, 45, 92, 61, 64, 50, 41, 30, 43, 74, 33, 78, 87, 31, 70, 81, 35, 84, 59, 74, 45, 44]

output = []
for flag_char, key_char in zip(flag, key):
    output.append(flag_char ^ key_char) # XOR

print(f'{bytes(output) = }')

#output = b"?F%^4F8\x02[A\x1a9~'9iu#WeY&\x1eQ"


