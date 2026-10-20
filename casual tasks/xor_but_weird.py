import itertools
import os

flag = b'_\xc0\xbbZ\xdb\xaf\x1c\x80\xb5[\xd0\xbcv\x86\xa4H\xd0\xe7v\xc7\xe4\x19\xec\xa7D\xf3\xb8E\xce'
# key = os.urandom(3)


for key0 in range(0, 256):
    for key1 in range(0, 256):
        for key2 in range(0, 256):
            key = [key0, key1, key2]
            output = []
            for flag_char, key_char in zip(flag, itertools.cycle(key)):
                output.append(flag_char ^ key_char)

            output = bytes(output)
            if b'vsosh{' in output:

                print(f'{bytes(output) = }')

# output = b'_\xc0\xbbZ\xdb\xaf\x1c\x80\xb5[\xd0\xbcv\x86\xa4H\xd0\xe7v\xc7\xe4\x19\xec\xa7D\xf3\xb8E\xce'
