import os
import sys
from encoder_2 import get_files, key_to_lst

sys.path.append('/Users/apple/Library/Preferences/PyCharmCE2019.1/scratches/iSR-master/code_payload')
from my_io import read, write, get_file_id

def get_max_bits(key: str):
    """Get the max bits need for storing factors"""
    i = 0
    while key[i] != '0':
        i += 1
    return i


def get_factor(key: str, max_bits: int):
    """Get my factor"""
    end, factors = max_bits*3, []
    for i in range(0, end, max_bits):
        factor = key[i: i+max_bits]
        factor = int(factor, 2)
        factors.append(factor)
    return factors


def get_unrecorded(key: str, unrecorded_end_with: int, len_pad: int):
    """Get my un-recorded bits stored in each row of a key"""
    pad = len_pad * str(unrecorded_end_with^1)
    n = 0
    for i in range(1, len(key)):
        if key[i] == str(unrecorded_end_with):
            if key[i+1: i+len_pad+1] == pad:
                return i+1


def get_keys(key) -> tuple:
    """Get my key"""
    key = key[1:]

    max_bits = get_max_bits(key)
    key = key[max_bits+1:]

    len_pad = get_max_bits(key)
    key = key[len_pad+1:]

    recorded_bit = int(key[0])
    start_bit = int(key[1])
    unrecorded_end_with = int(key[2])
    key = key[3:]

    factors = get_factor(key, max_bits)
    key = key[3*max_bits:]

    unrecorded_pos = get_unrecorded(key, unrecorded_end_with, len_pad)
    unrecorded = key[:unrecorded_pos]
    my_payload = key[unrecorded_pos+len_pad:]

    new_key = [recorded_bit, start_bit, factors[0], factors[1], factors[2], unrecorded]
    return new_key, my_payload


def get_key_payload(dir_path, new_payload_path):
    """Get key and payload"""
    my_payload = read(dir_path + new_payload_path)
    new_key = []
    while my_payload[0] == '0':
        new = get_keys(my_payload)
        new_key.append(new[0])
        my_payload = new[1]
    my_payload = my_payload[1:]
    return new_key, my_payload


def decode_key(key: list) -> list:
    """Decode my key"""
    key_str, recode_bit, max_repeat = key[-1], key[0], key[4]

    if recode_bit == 1:
        len_key = key[2]
    else:
        len_key = key[3]

    my_payload, end_pos = [], len_key

    while end_pos < len(key_str):
        start_pos = end_pos - len_key
        pattern = int(key_str[start_pos:end_pos], 2)
        repeat = key_str[end_pos] == '1'
        my_payload.append([0,0])
        if repeat:
            end_pos += 1
            repeat_times = int(key_str[end_pos:end_pos + max_repeat], 2)
            end_pos += max_repeat - 1
            lst = [0,0]
            lst[recode_bit^1] = pattern
            my_payload[-1] = (repeat_times, lst)
        else:
            my_payload[-1][recode_bit^1] = pattern
        end_pos += len_key + 1
    return my_payload

def decode_payload(payload: str, my_payload: list, key: list) -> list:
    """Decode my payload"""
    recode_bit = key[0]

    if recode_bit == 0:
        len_pattern = key[2]
    else:
        len_pattern = key[3]

    end_pos, pos = len_pattern, 0

    while end_pos < len(payload)+1:
        start_pos = end_pos - len_pattern
        pattern = int(payload[start_pos:end_pos], 2)
        if isinstance(my_payload[pos], list):
            my_payload[pos][recode_bit] = pattern
        else:
            lst = my_payload[pos][1]
            lst[recode_bit] = pattern
            my_payload[pos] = (my_payload[pos][0], lst)
        pos += 1
        end_pos += len_pattern
    return my_payload


def decode_seq(my_payload: list, key: list) -> str:
    """Decode my sequence"""
    start_bit, recovered = key[1], ''
    for i in range(len(my_payload)):
        repeat = 1
        if isinstance(my_payload[i], list):
            leading = my_payload[i][start_bit]
            padding = my_payload[i][start_bit^1]
        if isinstance(my_payload[i], tuple):
            repeat = my_payload[i][0]
            leading = my_payload[i][1][start_bit]
            padding = my_payload[i][1][start_bit^1]
        recovered += ((leading * str(start_bit)) + (padding * str(start_bit^1))) * repeat
    return recovered

def decode_pattern(payload: str, key: list) -> str:
    """Decode my pattern"""
    my_payload = ''
    for i in range(len(key)-1,-1,-1):
        my_payload = decode_key(key[i])
        my_payload = decode_payload(payload, my_payload, key[i])
        my_payload = decode_seq(my_payload, key[i])
        payload = my_payload
    return my_payload

def decode_frm_files(dir_path: str, files: list) -> None:
    """Decode from files"""

    for file in files:
        new_payload_path = '/new_payloads/new_payload_' + str(file) + '.txt'
        key_path = '/keys/key_' + str(file) + '.csv'
        recovered_file_path = '/recovered/recovered_' + str(file) + '.txt'
        original_file_path = '/payloads/payload_' + str(file) +'.txt'

        decode_frm_file(dir_path, new_payload_path, key_path, recovered_file_path,original_file_path)


def decode_frm_file(dir_path: str, new_payload_path: str, key_path: str, recovered_file_path: str, original_file_path: str) -> None:
    """Decode from a single file"""
    key_lst, my_payload = get_key_payload(dir_path, new_payload_path)
    recovered = decode_pattern(my_payload, key_lst)
    write(dir_path + recovered_file_path, recovered, 'w')
    decode = test(dir_path[:-10] + original_file_path, dir_path + recovered_file_path)
    file_id =  get_file_id(original_file_path)
    if decode:
        print('decode payload ' + str(file_id))
    else:
        print('fail decode payload ' + str(file_id))
        print(dir_path, new_payload_path, key_path, recovered_file_path, original_file_path)
        raise ValueError


def test(payload: str, recovered: str) -> bool:
    """Test"""
    payload = read(payload)
    recovered = read(recovered)
    return payload == recovered


def perparation(dir_path):
    """Prepare for encoding"""
    make_directory(dir_path + "/recovered")

def main() -> None:
    os.chdir('/Users/apple/Library/Preferences/PyCharmCE2019.1/scratches/iSR-master/code_payload/run_length')
    dir_path = os.getcwd()
    
    # Preparation for decoding 
    perparation(dir_path)
    
    files = get_files(dir_path[:-10] + '/huffman_tree/result.txt')
    #files = list(range(10001))
    decode_frm_files(dir_path, files)


if __name__ == "__main__":
     main()
