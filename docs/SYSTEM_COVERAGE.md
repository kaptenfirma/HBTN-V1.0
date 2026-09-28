# HBTN V1.0 - SYSTEM COVERAGE MATRIX
# Milestone: M0 (Execution Flow & Initial Architecture Discovery)

Status Legend:
- `UNKNOWN`: Not yet encountered or proved in the source code.
- `DISCOVERED`: Address or routine located, but complete behavior not yet analyzed.
- `UNDERSTOOD`: Disassembled, control-flow mapped, and evidence documented.
- `VERIFIED`: Proven through automated test or execution trace against original data.

| System Component | Status | Evidence ID | Details / Proven Addresses |
| :--- | :---: | :---: | :--- |
| **Boot / CRT0** | `VERIFIED` | EVD-005, EVD-006 | Entry point `0x80011278`, BSS clear `0x8005E378`-`0x800B7E20`, GP `0x8005E274`, SP `0x801FFFF0` |
| **Main Loop Engine** | `VERIFIED` | EVD-008 | Loop `0x80011638`-`0x80011C1C`, inner frame loop `0x80011C24` |
| **Game State Machine** | `VERIFIED` | EVD-008 | 21 states (0..20) dispatched via jump table at `0x80010008` |
| **Boot State (State 13)** | `UNDERSTOOD` | EVD-008, EVD-009 | Initial state `13` (0x0D), loads Subfile 27 & 28 overlays, tick at `0x800B7EEC` |
| **Asset Archive Loader (CD)** | `VERIFIED` | EVD-007, EVD-009 | `A_FILE.HDT` parsing at `0x800147BC`, subfile loader at `0x800145F0` |
| **Input Polling** | `UNDERSTOOD` | EVD-007, EVD-008 | Controller init `0x8003727C`, per-frame read `0x80013B04` invoking `0x80045ED4` |
| **Video / Frame Synchronization** | `UNDERSTOOD` | EVD-007, EVD-008 | GPU Reset `0x8003B064`, 320x240 double-buffering `0x8003E0C4`/`0x8003E184`, `VSync(1)` `0x8003B3E0` |
| **Sound / Audio System** | `DISCOVERED` | EVD-007, EVD-009 | SPU init routines at `0x800386F4`+, VAB sound bank in Subfile 09, XA audio in `STR/*.XA` |
| **Font / Text Display** | `DISCOVERED` | EVD-007 | Font init `0x8003EAE4`, `Font_all.tex` string at `0x80048C38` |
| **Save / Load Subsystem** | `DISCOVERED` | EVD-007, EVD-009 | MemoryCard init `0x80045254`, slot identifiers `BASLUS-01115-FARM*` in Subfile 15 |
| **Event Script System** | `DISCOVERED` | EVD-009 | Command queue / executor in Subfile 10 (`command executing`, `command can't reserve`) |
| **Map / Area Engine** | `UNKNOWN` | - | To be mapped in subsequent vertical slice milestones |
| **Player Entity System** | `UNKNOWN` | - | To be mapped in subsequent vertical slice milestones |
| **NPC Entity System** | `UNKNOWN` | - | To be mapped in subsequent vertical slice milestones |
| **Collision System** | `UNKNOWN` | - | To be mapped in subsequent vertical slice milestones |
| **Time / Calendar System** | `UNKNOWN` | - | To be mapped in subsequent vertical slice milestones |
| **Season / Weather System** | `UNKNOWN` | - | To be mapped in subsequent vertical slice milestones |
| **Item / Inventory System** | `UNKNOWN` | - | To be mapped in subsequent vertical slice milestones |
| **Animation System** | `UNKNOWN` | - | To be mapped in subsequent vertical slice milestones |
| **Renderer Implementation** | `UNTOUCHED` | - | Renderer postponed strictly as per M0 rule |
