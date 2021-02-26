import sys
from huffman_tree import *
import os

sys.path.append('/Users/apple/Library/Preferences/PyCharmCE2019.1/scratches/iSR-master/code_payload')
from my_io import *

def extract_key_factors(ed_payload: str) -> int:
    """Extract the length of each new pattern"""
    i = 0
    while ed_payload[i] != '0':
        i += 1
    return i


def extract_tree(ed_payload: str, len_new_val: int, bit: int) -> tuple:
    """Extract my huffman tree"""

    # initialise tree list
    tree_lst = [ed_payload[:bit+len_new_val]]

    # Get first key and initialise first position
    pos, key = 0, int(ed_payload[:bit],2)

    # Extract huffman tree
    while True:
        pos += bit+len_new_val+1
        previous_key, key = key, int(ed_payload[pos:pos+bit],2)
        if key < previous_key+1:
            break
        tree_lst.append(ed_payload[pos:pos + bit + len_new_val])

    pos = pos + 4
    return tree_lst, pos


def decode_payload(ed_payload: str, nodes: list) -> str:
    """Decode the payload from my huffman tree"""
    start, payload = 0, ''

    # Decode payload
    for i in range(len(ed_payload)+1):
        pattern = search_pattern(nodes[0], ed_payload[start:i], 0, '')
        if pattern:
            start = i
            payload += pattern
    return payload


def decode_frm_file(dir_path: str, new_payload_path: str, payload_path: str) ->None:
    """Decode a payload from a file"""
    # Read
    ed_payload = read(dir_path + new_payload_path)

    # Extract key factors
    num_bits = extract_key_factors(ed_payload)
    ed_payload = ed_payload[num_bits+1:]
    len_new_val = extract_key_factors(ed_payload)
    num_add = int(ed_payload[len_new_val+1:len_new_val+3], 2)
    ed_payload = ed_payload[len_new_val+3:]

    # Extract tree
    new = extract_tree(ed_payload, len_new_val, num_bits)
    tree_lst, pos = new[0], new[1]
    ed_payload = ed_payload[pos:]

    # Regenerate tree
    nodes = regenerate_node(tree_lst, num_bits)
    nodes = regenerate_tree(nodes)
    #print_tree(nodes[0])

    # Decode payload
    payload = decode_payload(ed_payload, nodes)
    if num_add != 0:
        payload = payload[:-num_add]

    # Test
    original = read(dir_path[:-12] + payload_path)
    file_id = get_file_id(payload_path)
    if payload == original:
        print('decode payload ' + str(file_id))
        write(dir_path + '/recovered/recovered_' + str(file_id), payload, 'w')

    else:
        print('fail decode payload ' + str(file_id))


def decode_frm_files(dir_path: str, files: list = None) -> None:
    """Decode payloads from files"""
    # Get payload files
    payloads_files = os.listdir(dir_path[:-12] + "/payloads")

    lst = range(len(payloads_files))
    if files:
        lst = files

    # Decode payloads from files
    for i in lst:
        try:
            new_payload_path = '/new_payloads/new_payload_' + str(i) + '.txt'
            original_file_path = '/payloads/payload_' + str(i) +'.txt'
            decode_frm_file(dir_path, new_payload_path, original_file_path)
        except AttributeError:
            print('fail decode payload ' + str(i))
            break
        except FileNotFoundError:
            pass


def perparation(dir_path):
    """Prepare for encoding"""
    make_directory(dir_path + "/recovered")


def main() -> None:
    # Set the working directory
    os.chdir('/Users/apple/Library/Preferences/PyCharmCE2019.1/scratches/iSR-master/code_payload/huffman_tree')
    dir_path = os.getcwd()

    # Prepare encoding
    perparation(dir_path)

    # Decode
    decode_frm_files(dir_path)
    #decode_frm_file(dir_path, '/new_payloads/new_payload_1300.txt', '/payloads/payload_1300.txt')

    files = get_files(dir_path[:-12] + '/huffman_tree/result.txt')
    decode_frm_files(dir_path, files)


if __name__ == "__main__":
    main()
