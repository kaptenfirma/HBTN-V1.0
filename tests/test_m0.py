import unittest
import os
import struct
import hashlib

BIN_PATH = r"d:\OpenCode\Harvest Moon - Back to Nature (USA)\Harvest Moon - Back to Nature (USA).bin"
CUE_PATH = r"d:\OpenCode\Harvest Moon - Back to Nature (USA)\Harvest Moon - Back to Nature (USA).cue"
ORIGINAL_DIR = r"D:\OpenCode\HBTN V1.0\source\original"
EXE_PATH = os.path.join(ORIGINAL_DIR, "SLUS_011.15")
HDT_PATH = os.path.join(ORIGINAL_DIR, "A_FILE.HDT")

class TestM0Milestone(unittest.TestCase):
    def test_01_original_disc_hashes(self):
        """Verify original USA BIN matches Redump MD5 and SHA-1."""
        self.assertTrue(os.path.exists(BIN_PATH), "Original BIN must exist")
        self.assertTrue(os.path.exists(CUE_PATH), "Original CUE must exist")

        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        with open(BIN_PATH, 'rb') as f:
            while chunk := f.read(1024 * 1024 * 4):
                md5.update(chunk)
                sha1.update(chunk)

        # Redump verified hashes for Harvest Moon: Back to Nature (USA)
        self.assertEqual(md5.hexdigest(), "424f9fbda58e95f597e39b4bdde239b1")
        self.assertEqual(sha1.hexdigest(), "cb26381fa1336bdd15f07469e59f1143ccf37b03")

    def test_02_system_cnf(self):
        """Verify SYSTEM.CNF extraction and exact parameters."""
        cnf_path = os.path.join(ORIGINAL_DIR, "SYSTEM.CNF")
        self.assertTrue(os.path.exists(cnf_path), "SYSTEM.CNF must be extracted")
        with open(cnf_path, 'r', encoding='latin1') as f:
            content = f.read()
        self.assertIn(r"BOOT = cdrom:\\SLUS_011.15;1", content)
        self.assertIn("STACK = 801fff00", content)

    def test_03_executable_header(self):
        """Verify PS-X EXE header fields in SLUS_011.15."""
        self.assertTrue(os.path.exists(EXE_PATH), "SLUS_011.15 must be extracted")
        with open(EXE_PATH, 'rb') as f:
            hdr = f.read(2048)

        magic = hdr[:8].decode('latin1')
        self.assertEqual(magic, "PS-X EXE")

        pc = struct.unpack('<I', hdr[0x10:0x14])[0]
        load_addr = struct.unpack('<I', hdr[0x18:0x1C])[0]
        load_size = struct.unpack('<I', hdr[0x1C:0x20])[0]
        sp_base = struct.unpack('<I', hdr[0x30:0x34])[0]

        self.assertEqual(pc, 0x80011278, "Entry point PC must be 0x80011278")
        self.assertEqual(load_addr, 0x80010000, "Text load address must be 0x80010000")
        self.assertEqual(load_size, 0x0004E800, "Text load size must be 0x0004E800")
        self.assertEqual(sp_base, 0x801FFFF0, "Initial SP base must be 0x801FFFF0")

    def test_04_execution_chain_entry_point(self):
        """Verify initial instructions at entry point 0x80011278."""
        with open(EXE_PATH, 'rb') as f:
            f.seek(0x800 + (0x80011278 - 0x80010000))
            words = [struct.unpack('<I', f.read(4))[0] for _ in range(8)]

        # 0x80011278: lui v0, 0x8006
        self.assertEqual(words[0], 0x3C028006)
        # 0x8001127C: addiu v0, v0, -7304 (0x8005E378)
        self.assertEqual(words[1], 0x2442E378)
        # 0x80011280: lui v1, 0x800B
        self.assertEqual(words[2], 0x3C03800B)
        # 0x80011284: addiu v1, v1, 32288 (0x800B7E20)
        self.assertEqual(words[3], 0x24637E20)
        # 0x80011288: sw zero, 0(v0)
        self.assertEqual(words[4], 0xAC400000)

    def test_05_state_machine_jump_table(self):
        """Verify the 21 entries in the main state machine jump table at 0x80010008."""
        with open(EXE_PATH, 'rb') as f:
            f.seek(0x800 + (0x80010008 - 0x80010000))
            table = [struct.unpack('<I', f.read(4))[0] for _ in range(21)]

        self.assertEqual(len(table), 21)
        # State 0
        self.assertEqual(table[0], 0x800116D0)
        # State 13 (Initial Boot State)
        self.assertEqual(table[13], 0x8001199C)
        # State 20
        self.assertEqual(table[20], 0x80011BCC)

    def test_06_a_file_hdt_partitions(self):
        """Verify A_FILE.HDT partitions match A_FILE.BIN size and sector alignment."""
        self.assertTrue(os.path.exists(HDT_PATH), "A_FILE.HDT must exist")
        with open(HDT_PATH, 'rb') as f:
            hdt_data = f.read()

        self.assertEqual(len(hdt_data), 132, "HDT must be exactly 132 bytes (33 32-bit offsets)")
        offsets = [struct.unpack('<I', hdt_data[i:i+4])[0] for i in range(0, len(hdt_data), 4)]

        self.assertEqual(offsets[0], 0, "First partition starts at offset 0")
        self.assertEqual(offsets[-1], 133935104, "Last offset must match A_FILE.BIN size exactly")

        # Every partition boundary must be sector aligned (2048 bytes)
        for i, off in enumerate(offsets):
            self.assertEqual(off % 2048, 0, f"Offset {i} (0x{off:08X}) must be 2048-byte aligned")

if __name__ == "__main__":
    unittest.main()
