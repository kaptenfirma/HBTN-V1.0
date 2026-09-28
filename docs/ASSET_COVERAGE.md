# HBTN V1.0 - ASSET COVERAGE MATRIX
# Milestone: M0 (Execution Flow & Initial Architecture Discovery)

Status Legend:
- `UNKNOWN`: Nature and format of asset unknown.
- `DISCOVERED`: File location and boundaries identified.
- `PARSED`: Header or table successfully decoded.
- `UNDERSTOOD`: Asset internal data structure and purpose verified from game logic.
- `VERIFIED`: Proven and validated with automated unit test / checksums.
- `UNTOUCHED`: Intentionally untouched during current milestone.

## 1. Disc Primary Filesystem (ISO9660)

| Disc File | LBA | Size (Bytes) | Status | Evidence ID | Purpose / Content |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `SYSTEM.CNF` | 23 | 69 | `VERIFIED` | EVD-004 | PSX boot configuration (`BOOT = cdrom:\SLUS_011.15;1`, Stack: `0x801FFF00`) |
| `SLUS_011.15` | 24 | 323,584 | `VERIFIED` | EVD-005 | Primary PSX MIPS binary executable |
| `A_FILE.BIN` | 182 | 133,935,104 | `PARSED` | EVD-009 | Main game archive containing 32 subfile partitions |
| `A_FILE.HDT` | 65580 | 132 | `VERIFIED` | EVD-009 | Allocation table header defining 33 partition offsets for `A_FILE.BIN` |
| `COPYRIGH.TXT`| 65581 | 0 | `VERIFIED` | EVD-003 | Standard zero-byte ISO copyright descriptor placeholder |
| `BIBLIOGP.TXT`| 65582 | 0 | `VERIFIED` | EVD-003 | Standard zero-byte ISO bibliography descriptor placeholder |
| `ABSTRACT.TXT`| 65583 | 0 | `VERIFIED` | EVD-003 | Standard zero-byte ISO abstract descriptor placeholder |
| `STR/01.XA` | 65585 | 14,794,752 | `DISCOVERED` | EVD-003 | CD-XA ADPCM Streaming Audio Track 1 |
| `STR/02.XA` | 72809 | 802,816 | `DISCOVERED` | EVD-003 | CD-XA ADPCM Streaming Audio Track 2 |
| `STR/03.XA` | 73201 | 622,592 | `DISCOVERED` | EVD-003 | CD-XA ADPCM Streaming Audio Track 3 |
| `STR/04.XA` | 73505 | 2,277,376 | `DISCOVERED` | EVD-003 | CD-XA ADPCM Streaming Audio Track 4 |
| `DUMMY.DAT` | 74617 | 33,177,600 | `VERIFIED` | EVD-003 | Disc outer-rim speed optimization padding |

## 2. A_FILE.BIN Subfile Partitions (Derived from A_FILE.HDT)

| Partition | Start Offset | Size (Bytes) | Status | Evidence ID | Details |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **Subfile 00** | `0x00000000` | 64,475,136 | `DISCOVERED` | EVD-009 | Main world / map / model asset bank |
| **Subfile 01** | `0x03D7D000` | 1,683,456 | `DISCOVERED` | EVD-009 | Character / entity models |
| **Subfile 02** | `0x03F18000` | 15,155,200 | `DISCOVERED` | EVD-009 | Area data partition 1 |
| **Subfile 03** | `0x04D8C000` | 16,883,712 | `DISCOVERED` | EVD-009 | Area data partition 2 |
| **Subfile 04** | `0x05DA6000` | 5,332,992 | `DISCOVERED` | EVD-009 | Area data partition 3 |
| **Subfile 05** | `0x062BC000` | 11,411,456 | `DISCOVERED` | EVD-009 | Area data partition 4 |
| **Subfile 06** | `0x06D9E000` | 458,752 | `DISCOVERED` | EVD-009 | Graphic textures |
| **Subfile 07** | `0x06E0E000` | 63,488 | `DISCOVERED` | EVD-009 | UI texture elements |
| **Subfile 08** | `0x06E1D800` | 2,048 | `UNDERSTOOD` | EVD-009 | Gamepad debug & button configuration |
| **Subfile 09** | `0x06E1E000` | 6,006,784 | `UNDERSTOOD` | EVD-009 | SPU sound bank (`VABp` header detected) |
| **Subfile 10** | `0x073D8800` | 16,384 | `UNDERSTOOD` | EVD-009 | Event command executor script tables |
| **Subfile 11** | `0x073DC800` | 483,328 | `DISCOVERED` | EVD-009 | Shared core assets (loaded across multiple states) |
| **Subfile 12** | `0x07452800` | 10,878,976 | `DISCOVERED` | EVD-009 | Message / dialogue text archives (`messege*.bin`) |
| **Subfile 13** | `0x07EB2800` | 69,632 | `DISCOVERED` | EVD-009 | Font & text layout assets |
| **Subfile 14** | `0x07EC3800` | 36,864 | `DISCOVERED` | EVD-009 | Menu overlays |
| **Subfile 15** | `0x07ECC800` | 98,304 | `UNDERSTOOD` | EVD-009 | Save/load structures & card slot headers |
| **Subfile 16** | `0x07EE4800` | 4,096 | `DISCOVERED` | EVD-009 | Memory card auxiliary data |
| **Subfile 17** | `0x07EE5800` | 26,624 | `DISCOVERED` | EVD-009 | State 3 data overlay |
| **Subfile 18** | `0x07EEC000` | 124,928 | `DISCOVERED` | EVD-009 | State 3 code overlay |
| **Subfile 19** | `0x07F0A800` | 32,768 | `DISCOVERED` | EVD-009 | State 4 data overlay |
| **Subfile 20** | `0x07F12800` | 110,592 | `DISCOVERED` | EVD-009 | State 4 code overlay |
| **Subfile 21** | `0x07F2D800` | 36,864 | `DISCOVERED` | EVD-009 | State 5 data overlay |
| **Subfile 22** | `0x07F36800` | 92,160 | `DISCOVERED` | EVD-009 | State 5 code overlay |
| **Subfile 23** | `0x07F4D000` | 34,816 | `DISCOVERED` | EVD-009 | State 8 data overlay |
| **Subfile 24** | `0x07F55800` | 126,976 | `DISCOVERED` | EVD-009 | State 8 code overlay |
| **Subfile 25** | `0x07F74800` | 34,816 | `DISCOVERED` | EVD-009 | State 10 data overlay |
| **Subfile 26** | `0x07F7D000` | 75,776 | `DISCOVERED` | EVD-009 | State 10 code overlay |
| **Subfile 27** | `0x07F8F800` | 57,344 | `UNDERSTOOD` | EVD-009 | Boot State (13) data overlay |
| **Subfile 28** | `0x07F9D800` | 12,288 | `UNDERSTOOD` | EVD-009 | Boot State (13) MIPS code overlay (`0x800B7EEC`) |
| **Subfile 29** | `0x07FA0800` | 75,776 | `DISCOVERED` | EVD-009 | Secondary title / logo data |
| **Subfile 30** | `0x07FB3000` | 28,672 | `UNDERSTOOD` | EVD-009 | Debug display and benchmark stats strings |
| **Subfile 31** | `0x07FBA000` | 4,096 | `UNDERSTOOD` | EVD-009 | `Ez MemoryCard Util` utility code |
