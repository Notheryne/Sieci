import random


def xor(a, b):
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)


def mod2div(divident, divisor):
    pick = len(divisor)
    result = divident[0 : pick]

    while pick < len(divident):
        if result[0] == '1':
            result = xor(divisor, result) + divident[pick]
        else:
            result = xor('0'*pick, result) + divident[pick]
        pick += 1

    if result[0] == '1':
        result = xor(divisor, result)
    else:
        result = xor('0'*pick, result)

    return result


def read_binary_data(filepath):
    with open(filepath, "rb") as binary_file:
        binary_data = binary_file.read()
    return binary_data


def write_binary_data(filepath, binary_data, mode="wb"):
    with open(filepath, mode) as binary_file:
        binary_file.write(binary_data)


def parity_bit(binary_data):
    result = sum([bin(byte).count("1") for byte in binary_data])
    return result % 2


def modulo_s100(binary_data):
    return sum(binary_data) % 100

def noise(binary_data, repeat = True, frequency = 0.1):
    noise = random.randrange(1,8)
    noise = pow(2,noise)
    binary_data_mut = bytearray(binary_data)
    number_of_noises = int(len(binary_data_mut)*frequency)
    noises_indexes = []
    if repeat:
        for _ in range(1,number_of_noises+1):
            while True:
                new_append = random.randrange(0,len(binary_data_mut))
                if new_append not in noises_indexes:
                    noises_indexes.append(new_append)
                    break
    else:
        noises_indexes.append(random.randrange(0,len(binary_data_mut)))
    for i in noises_indexes:
        binary_data_mut[i] = binary_data_mut[i]^noise
        #binary_data_mut[i] = binary_data_mut[i]&(~(binary_data_mut[i]&noise))

    return binary_data_mut

def calc_crc(binary_data):
    binary_string = ''.join([(bin(x)[2:]) for x in binary_data])
    crc_divider = '100011010'
    crc_len = len(crc_divider) - 1
    check = mod2div(binary_string, crc_divider)

    return (check, crc_len)


def test():
    input_filepath = "image.jpg"
    output_filepath = "written.txt"

    print("Reading input file and calculate it's parameters.")
    binary_data = read_binary_data(input_filepath)
    parity_bit1 = str(parity_bit(binary_data))
    sum_modulo = str(modulo_s100(binary_data))
    crc_value, crc_len = calc_crc(binary_data)

    print('Save data appending parameters to it.')
    write_binary_data(output_filepath, binary_data)
    write_binary_data(output_filepath, parity_bit1, "a")
    write_binary_data(output_filepath, sum_modulo, "a")
    write_binary_data(output_filepath, crc_value, "a")

    print('Read distorted data.')
    distorted_binary_data = read_binary_data(output_filepath)
    parity_bit2 = str(int(distorted_binary_data[-(crc_len + 3): -(crc_len + 2)]))
    sum_modulo2 = str(int(distorted_binary_data[-(crc_len + 2): -crc_len]))
    crc_value2 = str(int(distorted_binary_data[-crc_len:]))
    distorted_binary_data = distorted_binary_data[:-(crc_len + 3)]

    print('Adding noise to distorted data.')
    noised_data = noise(distorted_binary_data)

    print('Getting noised data as bytes.')
    bytes_binary_data = bytes(noised_data)

    print('Calculating noised data parameters.')
    parity_bit3 = str(parity_bit(bytes_binary_data))
    sum_modulo3 = str(modulo_s100(bytes_binary_data))
    crc_value3, crc_len2 = calc_crc(bytes_binary_data)

    print('\nResult data:\n')
    print("Original parity bit: {}\nNoised parity bit: {}\n".format(parity_bit2, parity_bit3))
    print("Original sum: {}\nNoised sum: {}\n".format(sum_modulo2, sum_modulo3))
    print("Original CRC value: {}\nNoised CRC value: {}".format(crc_value2, crc_value3))

test()
