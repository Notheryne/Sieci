from struct import pack, unpack
from numpy import uint32
import random
from copy import deepcopy


def read_binary(filename):
    with open(filename, "rb") as binary_file:
        binary_data = binary_file.read()
    return binary_data


class PacketManager:
    def __init__(self, number, name='Slim Shady', filepath=None, packed=None):
        self.name = name
        if filepath and packed:
            raise AttributeError('Decide!')
        self.number = number
        self.packed = []
        if filepath:
            self.data = [uint32(byte) for byte in read_binary(filepath)]
            self.__pack()
        if packed:
            self.receive_data(packed)
            self.data = []

    def save_to_file(self, filepath, mode="wb"):
        if len(self.packed) != 0:
            self.__unpack()
        else:
            raise ValueError('No packed data.')

        with open(filepath, mode) as binary_file:
            binary_file.write(bytes(self.data))

    def __eq__(self, other):
        if self.packed == other.packed_data and self.data == other.unpacked_data:
            return True
        else:
            return False

    def show(self):
        print('Hi, my name is %s' % self.name)
        print('Packed Data:')
        print(self.packed)
        print('Unpacked Data:')
        print(self.data)
        print('Length of data:')
        print(len(self.data))
        print('\n')

    def __unpack(self):
        self.packed.sort(key=lambda x: x[0])
        self.data = [unpack('B' * self.number, packet[1]) for packet in self.packed]
        self.data = [part[i] for part in self.data for i in range(len(part))]

    def __pack(self):
        self.packed = [(int(i / self.number), pack('B' * self.number, *self.data[i: i + self.number])) if
                       (i + self.number) < len(self.data) else
                       (int(i / self.number), pack('B' * self.number, *self.data[i: i + self.number],
                                                   *([0] * ((i + self.number) - len(self.data)))))
                       for i in range(0, len(self.data), self.number)]

    def send_data(self):
        random.shuffle(self.packed)
        return deepcopy(self.packed)

    def receive_data(self, packed_data):
        self.packed = packed_data


def test(number, filepath, output_filenames):
    sender = PacketManager(number, filepath=filepath, name='Sender')
    sender_before = deepcopy(sender)
    print('Before sending:')
    sender.show()
    receivers_data = sender.send_data()
    print('After sending:')
    sender.show()

    receiver = PacketManager(number, packed=receivers_data, name='Receiver')
    receiver_before = deepcopy(receiver)
    print('Before saving:')
    receiver.show()
    for output_filename in output_filenames:
        receiver.save_to_file(output_filename)
    print('After saving:')
    receiver.show()

    print('Comparisons:')
    print('Sender before == Sender after:', sender_before == sender)
    print('Sender before == Receiver before:', sender_before == receiver_before)
    print('Receiver before == Receiver after:', receiver_before == receiver)
    print('Receiver after == Sender after:', receiver == sender)
    print('Receiver after == Sender before', receiver == sender_before)


test(4, 'image.jpg', ['output.jpg', 'output.txt'])
