#!/usr/bin/env python3
"""Conservative MIPS word inspection; decoding alone does not establish code."""
import argparse
import json
from pathlib import Path
from n64_header import inspect_rom


def decode(word, pc=None):
    op, rs, rt, rd = word >> 26, (word >> 21) & 31, (word >> 16) & 31, (word >> 11) & 31
    imm = word & 0xffff
    signed = imm if imm < 0x8000 else imm - 0x10000
    r = lambda n: f'$r{n}'
    if word == 0:
        return 'nop'
    if op == 0:
        fn = word & 63
        if fn == 8 and rt == rd == ((word >> 6) & 31) == 0:
            return f'jr {r(rs)}'
        if fn in (0x21, 0x23, 0x24, 0x25, 0x26, 0x2a) and ((word >> 6) & 31) == 0:
            return f"{ {0x21:'addu',0x23:'subu',0x24:'and',0x25:'or',0x26:'xor',0x2a:'slt'}[fn]} {r(rd)}, {r(rs)}, {r(rt)}"
    if op in (2, 3):
        target = (word & 0x3ffffff) << 2
        if pc is None:
            return f"{'j' if op == 2 else 'jal'} index=0x{target:07X} (virtual address unknown)"
        target |= (pc + 4) & 0xf0000000
        return f"{'j' if op == 2 else 'jal'} 0x{target:08X}"
    if op in (4, 5):
        target = f'0x{(pc + 4 + signed * 4) & 0xffffffff:08X}' if pc is not None else f'PC+4{signed * 4:+d}'
        return f"{'beq' if op == 4 else 'bne'} {r(rs)}, {r(rt)}, {target}"
    if op == 15 and rs == 0:
        return f'lui {r(rt)}, 0x{imm:04X}'
    if op in (9, 12, 13, 14):
        name = {9:'addiu',12:'andi',13:'ori',14:'xori'}[op]
        return f'{name} {r(rt)}, {r(rs)}, {signed if op == 9 else hex(imm)}'
    if op in (32, 33, 35, 36, 37, 40, 41, 43, 55, 63):
        name = {32:'lb',33:'lh',35:'lw',36:'lbu',37:'lhu',40:'sb',41:'sh',43:'sw',55:'ld',63:'sd'}[op]
        return f'{name} {r(rt)}, {signed}({r(rs)})'
    return f'.word 0x{word:08X} # unsupported instruction or data'


def inspect(path, offset, count, vaddr=None):
    info = inspect_rom(path)
    if offset < 0 or offset % 4 or not 1 <= count <= 4096:
        raise ValueError('Use an aligned nonnegative offset and 1–4096 words')
    if vaddr is not None and (vaddr < 0 or vaddr > 0xffffffff or vaddr % 4 or vaddr + count * 4 > 0x100000000):
        raise ValueError('Virtual address range must be aligned and fit in 32 bits')
    with path.open('rb') as source:
        source.seek(offset)
        raw = source.read(count * 4)
    if len(raw) != count * 4:
        raise ValueError('Requested range extends beyond ROM')
    width = 2 if info['byte_order'].startswith('v64') else 4 if info['byte_order'].startswith('n64') else 1
    raw = b''.join(raw[i:i+width][::-1] for i in range(0, len(raw), width))
    rows = []
    for i in range(count):
        word = int.from_bytes(raw[i*4:i*4+4], 'big')
        pc = None if vaddr is None else vaddr + i*4
        rows.append({'file_offset': offset + i*4, 'virtual_address': pc,
                     'word': f'0x{word:08X}', 'assembly': decode(word, pc)})
    return {'rom': info, 'instructions': rows,
            'limitations': 'Partial scalar MIPS decoder. No code/data classification, decompilation, language identification, RSP decoding or decompression. Branch delay slots apply. Virtual addresses require a verified mapping.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom', type=Path)
    parser.add_argument('--offset', type=lambda s: int(s, 0), required=True)
    parser.add_argument('--words', type=int, default=64)
    parser.add_argument('--vaddr', type=lambda s: int(s, 0))
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.rom, args.offset, args.words, args.vaddr), indent=2))
    except (OSError, ValueError) as error:
        parser.exit(2, f'Error: {error}\n')


if __name__ == '__main__':
    main()
