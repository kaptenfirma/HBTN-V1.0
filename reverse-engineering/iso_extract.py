import struct
import os
import hashlib

BIN_PATH = r"d:\OpenCode\Harvest Moon - Back to Nature (USA)\Harvest Moon - Back to Nature (USA).bin"
OUT_ORIGINAL = r"D:\OpenCode\HBTN V1.0\source\original"
OUT_EXE = r"D:\OpenCode\HBTN V1.0\reverse-engineering\executable"
DOCS_DIR = r"D:\OpenCode\HBTN V1.0\docs"
EVIDENCE_DIR = r"D:\OpenCode\HBTN V1.0\evidence"

SECTOR_SIZE = 2352
DATA_OFFSET = 24
DATA_SIZE = 2048

def read_sector(f, lba):
    f.seek(lba * SECTOR_SIZE + DATA_OFFSET)
    return f.read(DATA_SIZE)

def parse_dir_record(data, offset):
    rec_len = data[offset]
    if rec_len == 0:
        return None, offset + 1
    ext_len = data[offset + 1]
    lba = struct.unpack('<I', data[offset + 2:offset + 6])[0]
    size = struct.unpack('<I', data[offset + 10:offset + 14])[0]
    flags = data[offset + 25]
    name_len = data[offset + 32]
    name = data[offset + 33:offset + 33 + name_len].decode('latin1', errors='replace')
    is_dir = (flags & 2) != 0
    return {
        'len': rec_len,
        'lba': lba,
        'size': size,
        'flags': flags,
        'is_dir': is_dir,
        'name': name
    }, offset + rec_len

files = []

def list_dir(f, lba, total_size, cur_path=''):
    sectors_to_read = (total_size + DATA_SIZE - 1) // DATA_SIZE
    dir_data = bytearray()
    for i in range(sectors_to_read):
        dir_data.extend(read_sector(f, lba + i))
    
    offset = 0
    while offset < total_size:
        if offset >= len(dir_data):
            break
        rec_len = dir_data[offset]
        if rec_len == 0:
            offset = ((offset // DATA_SIZE) + 1) * DATA_SIZE
            continue
        entry, next_offset = parse_dir_record(dir_data, offset)
        offset = next_offset
        if entry['name'] in ('\x00', '\x01'):
            continue
        name = entry['name'].split(';')[0]
        full_path = cur_path + '/' + name if cur_path else name
        entry['clean_name'] = name
        entry['path'] = full_path
        if entry['is_dir']:
            files.append(entry)
            list_dir(f, entry['lba'], entry['size'], full_path)
        else:
            files.append(entry)

def extract_file(f, lba, size, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'wb') as out_f:
        remaining = size
        cur_lba = lba
        while remaining > 0:
            block = read_sector(f, cur_lba)
            to_write = min(remaining, DATA_SIZE)
            out_f.write(block[:to_write])
            remaining -= to_write
            cur_lba += 1

def main():
    with open(BIN_PATH, 'rb') as f:
        pvd = read_sector(f, 16)
        system_id = pvd[8:40].decode('latin1', errors='replace').strip()
        volume_id = pvd[40:72].decode('latin1', errors='replace').strip()
        root_record = pvd[156:156+34]
        root_lba = struct.unpack('<I', root_record[2:6])[0]
        root_size = struct.unpack('<I', root_record[10:14])[0]
        
        print(f"System ID: {system_id}")
        print(f"Volume ID: {volume_id}")
        print(f"Root dir LBA: {root_lba}, size: {root_size}")
        
        list_dir(f, root_lba, root_size)
        
        print(f"\nDiscovered {len(files)} filesystem entries:")
        for item in sorted(files, key=lambda x: x['lba']):
            kind = "DIR " if item['is_dir'] else "FILE"
            print(f"{kind} LBA={item['lba']:<6} Size={item['size']:<10} {item['path']}")
            
            # Extract SYSTEM.CNF and executable files
            if item['clean_name'].upper() == "SYSTEM.CNF" or "SLUS" in item['clean_name'].upper():
                out_p1 = os.path.join(OUT_ORIGINAL, item['clean_name'])
                extract_file(f, item['lba'], item['size'], out_p1)
                print(f"  -> Extracted to: {out_p1}")
                if "SLUS" in item['clean_name'].upper():
                    out_p2 = os.path.join(OUT_EXE, item['clean_name'])
                    extract_file(f, item['lba'], item['size'], out_p2)
                    print(f"  -> Extracted to: {out_p2}")

if __name__ == "__main__":
    main()
