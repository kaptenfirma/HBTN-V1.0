# HBTN V1.0 - TESTING STRATEGY
# Milestone: M0 to M-Final

## Testing Principles

1. **Incremental / Vertical Testing**: Every system component reconstructed must be accompanied by evidence, logic tests, and ADB runtime validation where applicable.
2. **Two Levels of Testing**:
   - **Level 1: Logic Test** (Internal logic test without UI: checksum validation, header parsing, state dispatch, math models, asset decompression, archive extraction).
   - **Level 2: Runtime / ADB Test** (On-device deployment, lifecycle, frame loop, memory management, native Android integration).
3. **No Guessing**: A test passes only when the output matches the behavior observed from the original USA binary and data.

## M0 Automated Test Suite

For M0, an automated regression test script (`tests/test_m0.py`) is established to verify:
1. Original BIN and CUE fingerprints against verified Redump checksums.
2. Extraction and byte integrity of `SYSTEM.CNF` and `SLUS_011.15`.
3. Correct decoding of the PS-X EXE header fields (Magic, Initial PC, GP, SP, Load Address, Load Size).
4. Entry point and runtime BSS zeroing boundaries (`0x8005E378` - `0x800B7E20`).
5. Identification of the main game loop at `0x80011638` and the state machine jump table at `0x80010008` (21 states).
6. Extraction and mathematical sector-alignment of all 32 partitions in `A_FILE.HDT` matching the exact byte size of `A_FILE.BIN`.
