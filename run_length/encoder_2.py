import os
import sys

sys.path.append('/Users/apple/Library/Preferences/PyCharmCE2019.1/scratches/iSR-master/code_payload')
from my_io import *

def compress_by_sequences(payload: str) -> list:
    """Compress Payload via repeating bit sequences"""
    payload += '#'
    my_payload, freq, len_zeros, len_ones  = [], 0, 0, 0
    my_payload.append([0, 0])

    # Go through the original payload
    for i in range(1, len(payload)):
        freq += 1
        this_bit = payload[i]
        pre_bit = payload[i-1]

        # Recode length
        if this_bit != pre_bit and my_payload[-1][int(pre_bit)] != 0:
            my_payload.append([0, 0])
            my_payload[-1][int(pre_bit)] = freq
            freq = 0
        elif this_bit != pre_bit:
            my_payload[-1][int(pre_bit)] = freq
            freq = 0
        len_zeros = max(my_payload[-1][0], len_zeros)
        len_ones = max(my_payload[-1][1], len_ones)

    # Record max bits to store zeros or ones
    my_payload.append('#')
    len_zeros, len_ones = len(f"{len_zeros:b}"), len(f"{len_ones:b}")
    my_payload.append([len_zeros, len_ones])
    return my_payload


def compress_by_pattern(payload: list) -> list:
    """Compress Payload by patterns"""
    my_payload, num, max_repeat = [], 1, 0

    # Search patterns
    for i in range(1,len(payload)):
        this_pattern = payload[i-1]
        next_pattern = payload[i]
        # Record num of occurrences
        if this_pattern == next_pattern:
            num += 1
            continue
        # Record patterns
        if this_pattern != next_pattern and num == 1:
            max_repeat = max(max_repeat, num)
            my_payload.append(this_pattern)
        else:
            max_repeat = max(max_repeat, num)
            my_payload.append((num, this_pattern))
            num = 1

    # Recode max bits to store repeating times
    max_repeat = len(f"{max_repeat:b}")
    my_payload.append(payload[-1])
    my_payload[-1].append(max_repeat)
    return my_payload


def list_to_binary(payload: list, ireration: int, start_bit: str, dir_path: str, file_id: int) -> tuple:
    """Encode patterns to binary"""
    keys, len_zeros, len_ones, max_repeat = '', payload[-1][0], payload[-1][1], payload[-1][2]

    # Set pattern of outputs
    new_pattern = [1, len_ones]
    key_pattern = [0, len_zeros]
    if len_zeros < len_ones:
        new_pattern, key_pattern =  key_pattern, new_pattern

    # Encode patterns
    for i in range(len(payload)-1):
        # Single pattern
        if isinstance(payload[i], list):
            my_payload = f"{payload[i][new_pattern[0]]:b}".zfill(new_pattern[1])
            payload[i].append(my_payload)
            keys += (f"{payload[i][key_pattern[0]]:b}"+'0').zfill(key_pattern[1]+1)
        # Continuous patterns
        if isinstance(payload[i], tuple):
            my_payload = f"{payload[i][1][new_pattern[0]]:b}".zfill(new_pattern[1])
            payload[i] += (my_payload,)
            keys += (f"{payload[i][1][key_pattern[0]]:b}"+'1').zfill(key_pattern[1]+1)
            keys += f"{payload[i][0]:b}".zfill(max_repeat)

    # Write key
    content = str(ireration) + "," + str(new_pattern[0]) + "," + str(start_bit) + "," + \
              keys[-1] + "," +  str(len_zeros) + "," + str(len_ones) + "," + str(max_repeat) + ","  + keys + "\n"
    write(dir_path + "/keys/key_" + str(file_id) + ".csv", content, 'a')

    # List to a binary string
    my_payload = ''
    for i in range(len(payload)-2):
        my_payload += payload[i][-1]
    return my_payload, keys, content


def encode_payload(payload: str, dir: str, file_id: int, debug: bool) -> tuple:
    """ Encode a payload by sequence and pattern"""
    # Write attributes for key files
    content = "iteration,recorded_bit,old_payload_start_with,unrecorded_end_with," \
              "len_zeros,len_ones,max_repeat,unrecorded_bits+repeating_times\n"
    write(dir + "/keys/key_" + str(file_id) + ".csv", content, 'w')

    # Read payload
    my_payload, keys = payload, ''

    # Encode payload
    ireration = 0

    for i in range(1):
        show = "\n################ old payload ################" + '\n\tlen(my_payload): ' + str(len(my_payload)) + '\n\t' + my_payload
        seq = compress_by_sequences(my_payload)
        pattern = compress_by_pattern(seq)
        start_bit = my_payload[0]
        new = list_to_binary(pattern, ireration, start_bit, dir, file_id)
        my_payload = new[0]
        keys += new[1]
        ireration += 1
        write(dir + "/new_payloads/new_payload_" + str(file_id)+ ".txt", my_payload, 'w')
    key = encode_key(dir + "/keys/key_" + str(file_id) + ".csv")
    write(dir + "/keys/key_" + str(file_id) + ".txt", key, 'w')
    return my_payload, key


def get_max_bits(payload: str) -> tuple:
    """Get the max bits need to store zero or one"""
    max_one = -1
    max_zero = -1
    n = 0
    for i in range(1,len(payload)):
        n += 1
        if payload[i-1] != payload[i]:
            if payload[i] == '1':
                max_one = max(max_one, n)
            if payload[i] == '0':
                max_zero = max(max_zero, n)
            n = 0
    return max_zero, max_one


def key_to_lst(key: str) -> list:
    """convert key to list"""
    lst = list(key[128:-1].split('\n'))
    for i in range(len(lst)):
        key = lst[i].split(',')
        lst[i] = list(map(int, key[0:-1])) + [key[-1]]
    return lst


def encode_key(key_path: str):
    """Encode key into binary"""
    key = read(key_path)
    key_lst = key_to_lst(key)
    max_bit = 0
    pad = ''
    for i in range(len(key_lst)):
        len_bit = max(key_lst[i][4:7])
        max_bit = max(max(key_lst[i][4:7]), max_bit)
        pad = get_max_bits(key_lst[i][-1])
        key_lst[i].append(max(pad)+1)
        key_lst[i].append(len(f"{len_bit:b}"))

    new_key = ''
    for i in range(len(key_lst)):
        new_key += '0'
        new_key += '1' * key_lst[i][-1] + '0'
        new_key += '1' * key_lst[i][-2] + '0'
        new_key += str(key_lst[i][1]) + str(key_lst[i][2]) + str(key_lst[i][3])
        for j in range(4, 7):
            new_key += f"{key_lst[i][j]:b}".zfill(key_lst[i][-1])
        new_key += key_lst[i][-3]
        new_key += str(key_lst[i][3]^1) * key_lst[i][-2]
    return new_key


def get_files(result_path: str):
    """ Get un-encode files """
    file_id = read(result_path)
    lst = list(file_id.split(','))
    lst = list(map(int, lst[:-1]))
    return lst


def encode_frm_files(dir_path: str, files: list, data_path: str) -> None:
    """ Encode payloads from multiple files """
    write(dir_path + data_path, 'id,original_payload,new_payload\n', 'w')

    for file in files:
        print('encode payload ' + str(file))
        encode_frm_file(dir_path[:-10] +'/payloads/payload_' + str(file) + '.txt', dir_path, file, data_path)


def encode_frm_file(file_path: str, dir_path: str, file_id: int, data_path: str) -> None:
    """ Encode payload from a single file """
    this_payload = read(file_path)
    original_len = len(this_payload)
    new = encode_payload(this_payload, dir_path, file_id, False)
    content = str(file_id) + ',' + str(original_len) + ',' + str(len(new[0])+len(new[1])) + '\n'
    write(dir_path + "/new_payloads/new_payload_" + str(file_id) + ".txt", new[1] +'1'+ new[0], 'w')
    write(dir_path + data_path, content, 'a')


def perparation(dir_path):
    """Prepare for encoding"""
    make_directory(dir_path + "/keys")
    make_directory(dir_path + "/new_payloads")
    make_directory(dir_path + "/data")


def main() -> None:
    # Set the working directory
    os.chdir('/Users/apple/Library/Preferences/PyCharmCE2019.1/scratches/iSR-master/code_payload/run_length')
    dir_path = os.getcwd()

    # Prepare for encoding
    perparation(dir_path)

    # Get the files
    files = get_files(dir_path[:-10] + '/huffman_tree/result.txt')
    data_path = "/data/data_partial.csv"
    #files = list(range(10001))
    #data_path = "/data/data.csv"

    # Encode files
    encode_frm_files(dir_path, files, data_path)
    #encode_frm_file(dir_path[:-10] +'/payloads/payload_0.txt', dir_path, 0)

    # Remove temporary files
    remove_dir(dir_path + "/keys")


if __name__ == "__main__":
    main()
