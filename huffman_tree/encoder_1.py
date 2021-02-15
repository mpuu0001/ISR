import sys
import os
import collections
from huffman_tree import *

sys.path.append('/Users/apple/Library/Preferences/PyCharmCE2019.1/scratches/iSR-master/code_payload')
from my_io import read, write, get_file_id

def partition(payload: str) -> tuple:
    """Split the given payload into several subgroups, where each
    subgroup contains 4 bits"""
    # Number of bits we will pad into the payload
    num_add = 0
    if (len(payload) % 4) > 0:
        num_add = 4 - (len(payload) % 4)
    payload += num_add * '0'

    # Store each subgroup into a list
    lst = []
    for i in range(0, len(payload), 4):
        lst.append(payload[i:i+4])

    return lst, num_add


def unique(pattern: list) -> tuple:
    """Get unique patterns, and count the number of
    times each pattern appears in the given payload"""
    unique, freq = [], []
    for this in pattern:
        if this not in unique:
            unique.append(this)
            freq.append(pattern.count(this))

    return unique, freq


def get_tree(pattern: list, freq: list) -> dict:
    """Get the Huffman Tree
    pattern: Characters for huffman tree
    freq: frequency of characters
    """
    # Create my Huffman Tree
    nodes = create_tree(freq, pattern)

    # Recode my Huffman Tree
    dictnr = {}
    dictnr = recode_nodes(nodes[0], dictnr)

    return dictnr


def encode_payload(pattern, dict) -> list:
    """Encode the given payload"""
    for i in range(len(pattern)):
        code = search_nodes(dict, pattern[i])
        pattern[i] = code

    return pattern


def get_max_bits(dictnr: dict) -> int:
    """
    Get the max bits need to store each value of the dictionary
    """
    len_new_val = -1
    for x in dictnr.values():
        if len(x) > len_new_val:
            len_new_val = len(x)

    return len_new_val


def dict_to_binary(dictnr: dict) -> str:
    """
    Reform each value of the dictionary by the max bits, and
    store each items of the dictionary in a string
    """
    encoded_dict = ''
    for x, y in dictnr.items():
        encoded_dict += x
        encoded_dict += y

    return encoded_dict


def list_to_binary(pattern: list) -> str:
    """Combines the list that is outputted by encode_payload() into binary"""
    payload = ''
    for p in pattern:
        payload += p

    return payload


def encode_binary(dictnr: dict, debug: bool) -> tuple:
    """Convert the given dictionary to binary string.
     each key of the dictionary: 4-bits substring of the old payload
     each value of the dictionary: substring of the new payload"""

    # Sort the dictionary by its keys
    od = collections.OrderedDict(sorted(dictnr.items()))

    # Get the max bits need to store each value of the dictionary
    len_new_val = get_max_bits(od) + 1

    # Reform each value of the dictionary by the max bits 
    for x, y in od.items():
        if debug:
            print(f"{x} -> {od[x]}")

        # Offset
        num_pad = len_new_val - len(y)
        lead, pad = '0', '1'

        # Partition
        if num_pad > 1:
            lead = '1'
        if y[-1] == '1':
            pad = '0'

        # Reform
        od[x] = lead + od[x] + pad * num_pad

    return dict_to_binary(od), len_new_val


def get_file_id(path: str) -> int:
    """Get the id of a file"""
    lst = list(path.split('_'))
    lst = list(lst[1].split('.'))
    file_id = int(lst[0])

    return file_id


def encode_frm_file(file_path: str, dir_path: str, file_id: int, debug: bool) -> None:
    """ Encode a payload from a single file """
    # Read
    payload = read(file_path)

    # Partition into 4-bits per group
    new = partition(payload)
    pattern = new[0]
    num_add = new[1]
    new = unique(pattern)

    # Get my Huffman Tree
    dictnr = get_tree(new[0], new[1])

    # Encode the given payload using Huffman tree
    new_pattern = encode_payload(pattern, dictnr)
    new_payload = 4*'0' + list_to_binary(new_pattern)

    # Encode my Huffman Tree into binary
    # Combine it with my encoded payload
    new = encode_binary(dictnr, debug)
    encoded_dict = new[0]
    len_new_val = new[1] * '1' + '0'
    num_add = f"{num_add:b}".zfill(2)
    new_payload = len_new_val + num_add + encoded_dict + new_payload

    # Write new payload
    if len(new_payload) <= len(payload):
        write(dir_path + "/new_payloads/new_payload_"+str(file_id)+".txt", new_payload, 'w')
    else:
        write(dir_path + "/result.txt", str(file_id)+',', 'a')

    # Write data
    content = str(file_id) +','+ str(len(payload)) +','+ str(len(new_payload)) + '\n'
    write(dir_path + "/data/data.csv", content, 'a')

    if debug:
        print("num_add: " + str(int(num_add,2)) + '\n' +
              'len_new_val: ' + str(len(len_new_val)-1))


def encode_frm_files(dir_path: str, debug: bool) -> None:
    """ Encode payloads from multiple files """
    # Set the working directory
    # Get files
    os.chdir(dir_path[:-12] + "/payloads")
    files = os.listdir(dir_path[:-12] + "/payloads")

    # Encode files
    for i in range(len(files)):
        if files[i].startswith('.'):
            continue
        file_id = get_file_id(files[i])
        print("encode payload " + str(file_id))
        if files[i][0] == '.':
            continue
        encode_frm_file(files[i], dir_path, file_id, debug)


def main() -> None:
    # Set the working directory
    os.chdir('/Users/apple/Library/Preferences/PyCharmCE2019.1/scratches/iSR-master/code_payload/huffman_tree')
    dir_path = os.getcwd()

    # Write data
    write(dir_path + "/data/data.csv", 'id,original_payload,new_payload\n', 'w')
    write(dir_path + "/result.txt", '', 'w')

    # Encode
    encode_frm_files(dir_path, False)
    #encode_frm_file(dir_path +'/payloads/payload_1.txt', dir_path, 1, True)


if __name__ == "__main__":
    main()