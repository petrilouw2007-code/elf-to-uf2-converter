#!/usr/bin/env python3
import os, struct, sys

PAGE_SIZE = 256
BASE_ADDR = 0x10000000  # RP2040 flash start

def elf_to_bin(elf_path):
    with open(elf_path, "rb") as f:
        return f.read()

def create_uf2(elf_bytes, uf2_path):
    UF2_MAGIC_START0 = 0x0A324655
    UF2_MAGIC_START1 = 0x9E5D5157
    UF2_MAGIC_END = 0x0AB16F30

    num_blocks = (len(elf_bytes) + PAGE_SIZE - 1) // PAGE_SIZE

    with open(uf2_path, "wb") as uf2:
        for i in range(num_blocks):
            chunk = elf_bytes[i*PAGE_SIZE:(i+1)*PAGE_SIZE]
            chunk += b'\x00' * (PAGE_SIZE - len(chunk))
            header = struct.pack(
                "<IIIIIIIIIIIIIIII",
                UF2_MAGIC_START0,
                UF2_MAGIC_START1,
                0x00002000,
                BASE_ADDR + i*PAGE_SIZE,
                PAGE_SIZE,
                i,
                num_blocks,
                0,0,0,0,0,0,0,0,0
            )
            uf2.write(header)
            uf2.write(chunk)
            uf2.write(struct.pack("<I", UF2_MAGIC_END))

def main():
    if len(sys.argv) < 2:
        print("Usage: python converter.py <file.elf>")
        sys.exit(1)

    elf_file = sys.argv[1]
    uf2_file = elf_file.replace(".elf", ".uf2")
    elf_bytes = elf_to_bin(elf_file)
    create_uf2(elf_bytes, uf2_file)
    print(f"Created {uf2_file}!")

if __name__ == "__main__":
    main()
