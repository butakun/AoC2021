import numpy as np


def decode_literal(bits):
    print("decode_literal: ", bits)
    i0 = 0
    total_len = 0
    value = ""
    while True:
        more = bits[i0] == "1"
        value += bits[i0 + 1:i0 + 5]

        if not more:
            total_len = i0 + 5
            break
        i0 += 5

    return int(value, 2), total_len


def decode(bits, depth=0):
    # return ver, typ, content, the number of bits read

    if depth > 0:
        header = ""
    else:
        header = ">" * depth

    print(header, "decoding ", bits, " ", len(bits), " bits")
    ver = int(bits[:3], 2)
    typ = int(bits[3:6], 2)
    if typ == 4:
        val, val_bits_len = decode_literal(bits[6:])
        return ver, typ, val, 6 + val_bits_len
    else:
        # operator
        len_typ = bits[6]
        if len_typ == "0":
            sub_len_bits = int(bits[7:7+15], 2)
            print(header, " sub packets of ", sub_len_bits, " bits")
            sub_packets = []
            sub_bits_read = 0
            while sub_bits_read < sub_len_bits:
                sub = decode(bits[7+15+sub_bits_read:], depth=depth+1)
                print(header, " subpacket was ", sub[3], "bits long")
                sub_bits_read += sub[3]
                sub_packets.append(sub)
            assert sub_bits_read == sub_len_bits
            return ver, typ, sub_packets, 7 + 15 + sub_len_bits
        elif len_typ == "1":
            sub_len_packets = int(bits[7:7+11], 2)
            print(header, sub_len_packets, "sub packets follows")
            sub_packets = []
            i0 = 7 + 11
            for i in range(sub_len_packets):
                sub = decode(bits[i0:], depth=depth+1)
                print(header, i, "-th subpacket was ", sub[3], "bits long")
                i0 += sub[3]
                sub_packets.append(sub)
            return ver, typ, sub_packets, i0
        else:
            raise ValueError

        return ver, typ, s
        
def hex_to_bin(hex):
    num_bits = len(hex) * 4
    return bin(int(hex, 16))[2:].zfill(num_bits)


def version_sum(packet):
    ver, typ, content, bits_len = packet
    if typ != 4:
        for sub_packet in content:
            ver += version_sum(sub_packet)
    return ver


def main(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f]

    print(lines)

    ver, typ, content, num_bits = decode(hex_to_bin(lines[0]))
    print(ver, typ, content, num_bits)
    
    ver_acc = version_sum((ver, typ, content, num_bits))
    print("version sum = ", ver_acc)


if __name__ == "__main__":
    main("input.txt")
