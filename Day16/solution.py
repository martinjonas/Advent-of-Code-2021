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



def parse_packets(bits) -> Tuple[Literal | Operation, int]:
    version = int(bits[0:3], 2)
    typeid = int(bits[3:6], 2)
    packetdata = bits[6:]

    if typeid == 4:
        if len(packetdata) % 4 != 0:
            packetdata += "0" * (4 - len(packetdata) % 4)
        
        inner = []
        while True:
            inner.append(packetdata[1:5])
            if packetdata[0] == "0":
                break
            packetdata = packetdata[5:]
        literal = int("".join(inner), 2)
        return (Literal(version, typeid, literal), 6 + len(inner) * 5)
    else:
        length = None
        if packetdata[0] == "0":
            length = int(packetdata[1:16], 2)
            packetdata = packetdata[16:]

            parsed = 0
            inner = []
            while parsed < length:
                (packet, plen) = parse_packets(packetdata)
                packetdata = packetdata[plen:]
                inner.append(packet)
                parsed += plen
            assert(parsed == length)
            return (Operation(version, typeid, inner), 6 + 1 + 15 + length)
        else:
            length = int(packetdata[1:12], 2)
            packetdata = packetdata[12:]

            parsed = 0
            inner = []
            for _ in range(length):
                (packet, plen) = parse_packets(packetdata)
                packetdata = packetdata[plen:]
                inner.append(packet)
                parsed += plen
            return (Operation(version, typeid, inner), 6 + 1 + 11 + parsed)


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
            return functools.reduce(min, (eval_packets(packet) for packet in packets))
        case Operation(_, 3, packets):
            return functools.reduce(max, (eval_packets(packet) for packet in packets))
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
    packet, _ = parse_packets(bits)
    return sum_versions(packet)


def part2(data):
    bits = hex_to_bin(data)
    packet, _ = parse_packets(bits)
    return eval_packets(packet)


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    data = aocutils.input.read_lines(input_file)

    print(part1(data[0]))
    print(part2(data[0]))

main()
