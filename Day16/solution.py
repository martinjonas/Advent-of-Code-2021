from __future__ import annotations

import aocutils.input
import aocutils.parsing
import sys
import functools
import _operator
from dataclasses import dataclass
from typing import List, Tuple



def hex_to_bin(s):
    m = {'0' : '0000',
         '1' : '0001',
         '2' : '0010',
         '3' : '0011',
         '4' : '0100',
         '5' : '0101',
         '6' : '0110',
         '7' : '0111',
         '8' : '1000',
         '9' : '1001',
         'A' : '1010',
         'B' : '1011',
         'C' : '1100',
         'D' : '1101',
         'E' : '1110',
         'F' : '1111'}

    return "".join(m[ch] for ch in s)


@dataclass
class Literal:
    version: int
    typeid: int
    value: int

    
@dataclass
class Operation:
    version: int
    typeid: int
    packets: List[Literal | Operation]


class BitReader:
    def __init__(self, bits: str):
        self.bits = bits
        self.offset = 0
    
    def read(self, n: int):
        res = self.bits[self.offset:self.offset+n]
        self.offset += n
        return res

    
def parse_packets(bits: BitReader) -> Literal | Operation:
    version = int(bits.read(3), 2)
    typeid = int(bits.read(3), 2)

    if typeid == 4:
        inner = []
        while True:
            header = bits.read(1)
            data = bits.read(4)
            inner.append(data)
            if header == "0":
                break
        literal = int("".join(inner), 2)
        return Literal(version, typeid, literal)
    else:
        header = bits.read(1)
        
        if header == "0":
            length = int(bits.read(15), 2)
            start_offset = bits.offset
            
            inner = []
            while bits.offset < start_offset + length:
                packet = parse_packets(bits)
                inner.append(packet)
            assert(bits.offset == start_offset + length)
            return Operation(version, typeid, inner)
        else:
            length = int(bits.read(11), 2)            

            inner = []
            for _ in range(length):
                packet = parse_packets(bits)
                inner.append(packet)
                
            return Operation(version, typeid, inner)


def sum_versions(packet: Literal | Operation) -> int:
    match packet:
        case Literal(version, _, _):
            return version
        case Operation(version, _, packets):
            return version + sum(sum_versions(packet) for packet in packets)
    assert False


def eval_packets(packet: Literal | Operation) -> int:
    match packet:
        case Literal(_, _, value):
            return value
        case Operation(_, 0, packets):
            return sum(eval_packets(packet) for packet in packets)
        case Operation(_, 1, packets):
            return functools.reduce(_operator.mul, (eval_packets(packet) for packet in packets))
        case Operation(_, 2, packets):
            return min(eval_packets(packet) for packet in packets)
        case Operation(_, 3, packets):
            return max(eval_packets(packet) for packet in packets)
        case Operation(_, 5, [l, r]):
            return 1 if eval_packets(l) > eval_packets(r) else 0
        case Operation(_, 5, [l, r]):
            return 1 if eval_packets(l) > eval_packets(r) else 0
        case Operation(_, 6, [l, r]):
            return 1 if eval_packets(l) < eval_packets(r) else 0
        case Operation(_, 7, [l, r]):
            return 1 if eval_packets(l) == eval_packets(r) else 0
    assert False
    

def part1(data):
    bits = hex_to_bin(data)
    packet = parse_packets(BitReader(bits))
    return sum_versions(packet)


def part2(data):
    bits = hex_to_bin(data)
    packet = parse_packets(BitReader(bits))
    return eval_packets(packet)


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    data = aocutils.input.read_lines(input_file)

    print(part1(data[0]))
    print(part2(data[0]))

main()
