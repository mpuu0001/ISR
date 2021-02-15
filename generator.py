from encoder import write
from random import seed, randint
import os
def payload_generator(random_range: int) -> str:
    """Generate payload according to random range"""
    random_length = randint(4*random_range, 100000)
    payload = ''
    while len(payload) < random_length:
        len_ones = randint(-random_range, random_range)
        payload += '1' * len_ones
        len_zeros = randint(-random_range, random_range)
        payload += '0' * len_zeros
    return payload

def increase_range(flag: int, random_range: int, index: int) -> int:
    """Increase random range to generate new payload"""
    if index == flag:
        return random_range * 2
    elif index == 2 * flag:
        return random_range * 10
    elif index == 3 * flag:
        return random_range * 10
    return random_range

def write_files(num_file: int, start_range: int, dir: str) -> None:
    """Write payload"""
    random_range = start_range
    flag = int(num_file/start_range)
    for i in range(num_file):
        random_range = increase_range(flag, random_range, i)
        my_payload = payload_generator(random_range)
        write(dir + '/payload_'+ str(i+1) + ".txt", my_payload, 'w')

def main() -> None:
    seed(9999)
    os.chdir('/Users/apple/Library/Preferences/PyCharmCE2019.1/scratches/iSR-master/payload-processing/payloads')
    dir = os.getcwd()
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    write_files(10000, 5, dir)

if __name__ == "__main__":
    main()