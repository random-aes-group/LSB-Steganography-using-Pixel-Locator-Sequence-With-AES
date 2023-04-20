import hashlib
import random
import os
import numpy as np
from PIL import Image

import PLShandler as plsh


def pixel_locator_sequence_generator(row, col, len_encoded_message):
    """
    Serializes pixel locator sequence for an encoded message given row and col of
    the input image.
    """
    PLS = []
    new = []
    for i in range(row * col):
        new.append(i)
    for i in range(len(new) - 1, 0, -1):
        j = random.randint(0, i + 1)
        new[i], new[j] = new[j], new[i]
    for i in range(len_encoded_message * 3):
        PLS.append(new[i])
    pixel_locator_sequence = np.array(PLS)
    np.savetxt("pls.txt", pixel_locator_sequence, delimiter="\t")
    return pixel_locator_sequence

def lsb_encode(
        input_image_path, 
        output_image_path, 
        encoded_message, 
        pls_password):
    pls_password = str(pls_password)
    img = Image.open(input_image_path)
    [row, col] = img.size
    pixel_locator_sequence = pixel_locator_sequence_generator(row, col, len(encoded_message))
    # print(pixel_locator_sequence)
    def _data_list_in_bit(data):
        dataBits = list(format(c, '08b') for c in bytearray(data.encode('latin-1')))
        return dataBits
    dataBits = _data_list_in_bit(encoded_message)

    dr = 0
    for i in range(0, len(encoded_message) * 3, 3):
        dc = 0
        for j in range(0, 3):
            rr = pixel_locator_sequence[i + j] // col
            rc = pixel_locator_sequence[i + j] % col
            rgb = img.getpixel((rr, rc))
            value = []
            idx = 0
            for k in rgb:
                # if (dc >= 8):
                #     break
                if (k % 2 == 0 and dataBits[dr][dc] == '1'):
                    if (k == 0):
                        k += 1
                    else:
                        k -= 1
                if (k % 2 == 1 and dataBits[dr][dc] == '0'):
                    k -= 1
                value.append(k)
                idx += 1
                dc += 1
                if (dc >= 8):
                    break
            if (dc >= 8):
                value.append(rgb[2])
            newrgb = (value[0], value[1], value[2])
            img.putpixel((rr, rc), newrgb)
        dr += 1
    
    img.save(output_image_path)
    key = hashlib.sha256(pls_password.encode()).digest()
    plsh.encrypt_file(key, 'pls.txt')


def lsb_decode(
        output_image_path,
        pls_password
    ):
    key = hashlib.sha256(pls_password.encode()).digest()
    plsh.decrypt_file(key, 'pls.txt.enc', 'out.txt')
    pixel_locator_sequence = np.genfromtxt('out.txt', delimiter='\t')
    if os.path.exists("out.txt"):
        os.remove("out.txt")
    if os.path.exists("pls.txt.enc"):
        os.remove("pls.txt.enc")
    pixel_locator_sequence = pixel_locator_sequence.astype(int)
    # print(pixel_locator_sequence)

    img = Image.open(output_image_path)
    [_, col] = img.size

    decodedTextInBits = []

    stegoImage = Image.open(output_image_path)
    for i in range(0, len(pixel_locator_sequence), 3):
        ithChar = ""
        for j in range(0, 3):
            rr = pixel_locator_sequence[i + j] // col
            rc = pixel_locator_sequence[i + j] % col
            rgb = stegoImage.getpixel((rr, rc))
            for k in rgb:
                if (k & 1):
                    ithChar += '1'
                else:
                    ithChar += '0'

        ithChar = ithChar[:-1]
        decodedTextInBits.append((ithChar))
    decodedText = ''
    for i in decodedTextInBits:
        decodedText += chr(int(i, 2))
    return decodedText
