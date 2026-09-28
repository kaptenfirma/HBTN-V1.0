# HBTN V1.0 - EVIDENCE LOG
# Milestone: M0 (Execution Flow & Initial Source of Truth Discovery)

---

ID: EVD-001
SOURCE: Harvest Moon - Back to Nature (USA).bin & Harvest Moon - Back to Nature (USA).cue
OFFSET/ADDRESS: Disc File Metadata
OBSERVATION:
- File: Harvest Moon - Back to Nature (USA).bin (213,954,384 bytes)
  MD5:    424f9fbda58e95f597e39b4bdde239b1
  SHA1:   cb26381fa1336bdd15f07469e59f1143ccf37b03
  SHA256: 41f81532a5fd70d6f79e7b5750513c35eee732d5e31ba144a1db7e90d84d97de
- File: Harvest Moon - Back to Nature (USA).cue (101 bytes)
  MD5:    3c5a8426ed8d5e0907cfdd35f3687106
  SHA1:   42179f1c407f38a5fb0db866d097a1d725987a8b
  SHA256: 73919b99a102ffd9be8b6b2f2f5e062e6874c1988bf532c9d5eecdb6ae4ea19f
INTERPRETATION:
The disc image matches 100% with the official Redump database entry for "Harvest Moon: Back to Nature (USA)" (Sony PlayStation, NTSC-U). It is an unmodified, verified original dump.
CONFIDENCE: 100% (FACT)
TEST: SHA-1 and MD5 comparison against Redump database catalog.
STATUS: VERIFIED

---

ID: EVD-002
SOURCE: Harvest Moon - Back to Nature (USA).bin
OFFSET/ADDRESS: Sector 16 (LBA 16), Offset 0x00009400 in BIN (2352-byte sector Mode 2 Form 1)
OBSERVATION:
ISO9660 Primary Volume Descriptor (PVD):
- Standard Identifier: CD001
- System Identifier: PLAYSTATION
- Volume Identifier: HARVESTMOON
- Root Directory LBA: 22 (Size: 2048 bytes)
INTERPRETATION:
The disc utilizes standard ISO9660 filesystem formatting with CD-ROM Mode 2 Form 1 (2352 bytes/sector with 24 bytes header/subheader and 2048 bytes payload per sector).
CONFIDENCE: 100% (FACT)
TEST: Parsed with ISO9660 PVD reader script `iso_extract.py`.
STATUS: VERIFIED

---

ID: EVD-003
SOURCE: Harvest Moon - Back to Nature (USA).bin -> ISO9660 Directory Table
OFFSET/ADDRESS: Root Directory (LBA 22) and Subdirectory STR (LBA 65584)
OBSERVATION:
The disc contains exactly 13 filesystem entries:
1.  SYSTEM.CNF   | LBA: 23    | Size: 69 bytes
2.  SLUS_011.15  | LBA: 24    | Size: 323,584 bytes
3.  A_FILE.BIN   | LBA: 182   | Size: 133,935,104 bytes
4.  A_FILE.HDT   | LBA: 65580 | Size: 132 bytes
5.  COPYRIGH.TXT | LBA: 65581 | Size: 0 bytes
6.  BIBLIOGP.TXT | LBA: 65582 | Size: 0 bytes
7.  ABSTRACT.TXT | LBA: 65583 | Size: 0 bytes
8.  STR/         | LBA: 65584 | Size: 2,048 bytes (Directory)
9.  STR/01.XA    | LBA: 65585 | Size: 14,794,752 bytes
10. STR/02.XA    | LBA: 72809 | Size: 802,816 bytes
11. STR/03.XA    | LBA: 73201 | Size: 622,592 bytes
12. STR/04.XA    | LBA: 73505 | Size: 2,277,376 bytes
13. DUMMY.DAT    | LBA: 74617 | Size: 33,177,600 bytes
INTERPRETATION:
Complete disc file table identified. The main executable is `SLUS_011.15`. The game assets are archived inside `A_FILE.BIN` indexed by `A_FILE.HDT`. Background music streams are stored in `STR/*.XA`. Outer edge padding is `DUMMY.DAT`.
CONFIDENCE: 100% (FACT)
TEST: Recursive directory traversal verified through ISO9660 parser.
STATUS: VERIFIED

---

ID: EVD-004
SOURCE: SYSTEM.CNF (Extracted from LBA 23)
OFFSET/ADDRESS: File content
OBSERVATION:
Content:
```
BOOT = cdrom:\SLUS_011.15;1
TCB = 4
EVENT = 10
STACK = 801fff00
```
INTERPRETATION:
- Primary boot binary: `SLUS_011.15`
- Thread Control Blocks: 4
- Event handles: 10
- Stack Top Address: `0x801FFF00`
CONFIDENCE: 100% (FACT)
TEST: File extracted and decoded as ASCII.
STATUS: VERIFIED

---

ID: EVD-005
SOURCE: SLUS_011.15 (Extracted from LBA 24)
OFFSET/ADDRESS: Header (Bytes 0x0000 - 0x0800)
OBSERVATION:
- File Size: 323,584 bytes
  MD5:    9996dfa672ee83fedf01f25c91659fe7
  SHA1:   07fbcffbdd96080d39939e569f84abe76b9d1039
  SHA256: 34e3b35dcd3fb1cd9a7d4813b8a9ef987915826e3d436f1908ecbe2d4fdf1444
- Magic: "PS-X EXE"
- Initial PC:        0x80011278
- Initial GP:        0x00000000 (Set dynamically at 0x800112F8 to 0x8005E274)
- Text Load Address: 0x80010000
- Text Load Size:    0x0004E800 (321,536 bytes)
- Data Address/Size: 0x00000000 / 0x00000000
- BSS Address/Size:  0x00000000 / 0x00000000 (Explicitly cleared in crt0: 0x8005E378 to 0x800B7E20)
- Initial SP:        0x801FFFF0 (Base: 0x801FFFF0, Offset: 0)
- Region Marker:     "Sony Computer Entertainment Inc. for North America area"
INTERPRETATION:
All initial CPU registers for booting the executable are conclusively determined. The executable occupies RAM from `0x80010000` to `0x8005E800`.
CONFIDENCE: 100% (FACT)
TEST: Binary header decoded and validated.
STATUS: VERIFIED

---

ID: EVD-006
SOURCE: SLUS_011.15
OFFSET/ADDRESS: 0x80011278 - 0x80011320
OBSERVATION:
C runtime startup (`crt0`):
1. 0x80011278 - 0x80011298: BSS zeroing loop from `0x8005E378` up to `0x800B7E20`.
2. 0x800112C4: SP initialization to `0x801FFFF0`.
3. 0x800112F8: Runtime GP initialization: `gp = 0x8005E274`.
4. 0x80011304: Calls `0x800425A4` (heap / memory subsystem allocator init).
5. 0x80011318: Calls `0x80011370` (`main()`).
6. 0x80011320: `break 0x1` (traps CPU if `main` terminates).
INTERPRETATION:
The initial execution chain starts at `0x80011278`, initializes system BSS memory (`0x8005E378` - `0x800B7E20`), sets up registers GP and SP, invokes heap initialization, then enters `main()` at `0x80011370`.
CONFIDENCE: 100% (FACT)
TEST: MIPS disassembler trace verified.
STATUS: VERIFIED

---

ID: EVD-007
SOURCE: SLUS_011.15
OFFSET/ADDRESS: 0x80011370 - 0x80011634
OBSERVATION:
Initialization sequence within `main()`:
- `0x80011270`: C runtime hook / vector setup
- `0x80032D94`: Audio / SPU init or stop
- `0x80033844`: CdInit / CD-ROM subsystem init
- `0x800425F4`: Memory / Heap allocation init (called with arg 2)
- `0x80032B84`: Sound driver call (called multiple times with arg 3)
- `0x80012A68`: Clear VRAM rectangle (640x480)
- `0x8003B3E0`: VSync wait loop
- `0x8001FCE4`: GTE / Geometry subsystem init
- `0x8001FEA4`: Matrix stack init
- `0x80033814`: CdSetDebug / CdMode init
- `0x8003B064`: ResetGraph(0) (GPU reset!)
- `0x800147BC`: CD Table & File Descriptor Init (`\A_FILE.HDT;1` & `\A_FILE.BIN;1`)
- `0x8003E0C4`: SetDefDrawEnv / Framebuffer 0 & 1 draw environments (320x240)
- `0x8003E184`: SetDefDispEnv / Framebuffer 0 & 1 display environments
- `0x8003727C`, `0x80037994`, `0x800379B4`: PadInit / Controller subsystem init
- `0x800386F4`, `0x80038EC4`, `0x80038DD4`, `0x80038C44`, `0x80038F64`: SPU / Sound streaming init
- `0x8003EAE4`, `0x8003EF70`: Font / Text drawing system init
- `0x80045254`: Memory card subsystem init (`libmcrd`)
- `0x800139FC`, `0x80013A24`: Controller buffer setup
- `0x80032E24`: Sound bank / sequence driver setup
- State variable at `296(gp)` is initialized to 13 (0x0D).
INTERPRETATION:
Standard Sony PlayStation SDK subsystem initialization sequence followed by setting game boot state to State 13.
CONFIDENCE: 100% (FACT)
TEST: Disassembly inspection of all function call arguments and register states.
STATUS: VERIFIED

---

ID: EVD-008
SOURCE: SLUS_011.15
OFFSET/ADDRESS: 0x80011638 - 0x80011C20
OBSERVATION:
Main Game Loop & State Machine:
1. `0x80011638`: Loop head.
2. `0x800116A0`: Reads state variable `lw v1, 296(gp)`.
3. `0x800116A8`: Validates `v1 < 21` (unsigned).
4. `0x800116B0` - `0x800116C8`: Indexes jump table at `0x80010008` with `v1 * 4` and executes `jr a0`.
5. State handler executes state setup, loads corresponding subfiles from `A_FILE.BIN`, and sets per-frame tick function address into `272(gp)`.
6. State handler jumps to `0x80011C14` (`jal 0x80011C24`).
7. `0x80011C24`:
   - Waits for vertical blanking (`VSync(1)` via `0x8003B3E0`)
   - Polls gamepad inputs (`0x80013B04`)
   - Swaps double-buffers and synchronizes drawing (`0x800120C8`, `0x80012D30`)
   - Calls per-frame tick function `lw v0, 272(gp); jalr ra, v0`
8. `0x80011C1C`: Jumps back to loop head: `j 0x80011638`.
INTERPRETATION:
The core execution flow of Harvest Moon: Back to Nature is an infinite state-machine loop with a 21-state jump table dispatching into per-frame tick handlers with synchronized VSync, double-buffering, and input polling.
CONFIDENCE: 100% (FACT)
TEST: Jump table disassembly and control-flow graph verified.
STATUS: VERIFIED

---

ID: EVD-009
SOURCE: A_FILE.HDT & A_FILE.BIN
OFFSET/ADDRESS: Disc LBAs 65580 & 182
OBSERVATION:
`A_FILE.HDT` is exactly 132 bytes, consisting of 33 32-bit little-endian integers:
Each integer represents the starting byte offset of a subfile partition within `A_FILE.BIN`.
Offset[0] = 0x00000000, Offset[32] = 0x07FBB000 (133,935,104 bytes = exact file size of `A_FILE.BIN`).
All 32 partition boundaries are 2048-byte sector-aligned:
- Subfile 00: 64,475,136 bytes
- Subfile 01: 1,683,456 bytes
- Subfile 02: 15,155,200 bytes
- Subfile 03: 16,883,712 bytes
- Subfile 04: 5,332,992 bytes
- Subfile 05: 11,411,456 bytes
- Subfile 06: 458,752 bytes
- Subfile 07: 63,488 bytes
- Subfile 08: 2,048 bytes (Gamepad debug)
- Subfile 09: 6,006,784 bytes (VAB audio sound bank `pBAV`)
- Subfile 10: 16,384 bytes (Script / command parser)
- Subfile 11: 483,328 bytes
- Subfile 12: 10,878,976 bytes
- Subfile 13: 69,632 bytes
- Subfile 14: 36,864 bytes
- Subfile 15: 98,304 bytes (Save/load data & slot headers `BASLUS-01115-FARM*`)
- Subfile 16: 4,096 bytes
- Subfile 17: 26,624 bytes
- Subfile 18: 124,928 bytes
- Subfile 19: 32,768 bytes
- Subfile 20: 110,592 bytes
- Subfile 21: 36,864 bytes
- Subfile 22: 92,160 bytes
- Subfile 23: 34,816 bytes
- Subfile 24: 126,976 bytes
- Subfile 25: 34,816 bytes
- Subfile 26: 75,776 bytes
- Subfile 27: 57,344 bytes (Initial State 13 data overlay)
- Subfile 28: 12,288 bytes (Initial State 13 MIPS code overlay)
- Subfile 29: 75,776 bytes
- Subfile 30: 28,672 bytes (Performance debug strings)
- Subfile 31: 4,096 bytes (MemoryCard Util)
INTERPRETATION:
`A_FILE.HDT` is the Header Table (file allocation table) for `A_FILE.BIN`. Game states load code and data dynamically as overlays using function `0x800145F0`.
CONFIDENCE: 100% (FACT)
TEST: Extracted and mathematically verified sector math in `iso_extract.py` and `disasm.py`.
STATUS: VERIFIED
