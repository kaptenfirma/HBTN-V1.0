import struct
import sys

# MIPS I instruction decoder
REG_NAMES = [
    "zero", "at", "v0", "v1", "a0", "a1", "a2", "a3",
    "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
    "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",
    "t8", "t9", "k0", "k1", "gp", "sp", "fp", "ra"
]

def disasm_inst(word, pc):
    op = (word >> 26) & 0x3F
    rs = (word >> 21) & 0x1F
    rt = (word >> 16) & 0x1F
    rd = (word >> 11) & 0x1F
    shamt = (word >> 6) & 0x1F
    funct = word & 0x3F
    imm16 = word & 0xFFFF
    simm16 = imm16 if imm16 < 0x8000 else imm16 - 0x10000
    target = (word & 0x03FFFFFF) << 2
    branch_target = pc + 4 + (simm16 << 2)

    r_s = REG_NAMES[rs]
    r_t = REG_NAMES[rt]
    r_d = REG_NAMES[rd]

    if word == 0:
        return "nop", None

    if op == 0x00: # SPECIAL
        if funct == 0x00: return f"sll {r_d}, {r_t}, {shamt}", None
        if funct == 0x02: return f"srl {r_d}, {r_t}, {shamt}", None
        if funct == 0x03: return f"sra {r_d}, {r_t}, {shamt}", None
        if funct == 0x04: return f"sllv {r_d}, {r_t}, {r_s}", None
        if funct == 0x06: return f"srlv {r_d}, {r_t}, {r_s}", None
        if funct == 0x07: return f"srav {r_d}, {r_t}, {r_s}", None
        if funct == 0x08: return f"jr {r_s}", None
        if funct == 0x09: return f"jalr {r_d}, {r_s}", None
        if funct == 0x0C: return f"syscall 0x{((word >> 6) & 0xFFFFF):X}", None
        if funct == 0x0D: return f"break 0x{((word >> 6) & 0xFFFFF):X}", None
        if funct == 0x10: return f"mfhi {r_d}", None
        if funct == 0x11: return f"mthi {r_s}", None
        if funct == 0x12: return f"mflo {r_d}", None
        if funct == 0x13: return f"mtlo {r_s}", None
        if funct == 0x18: return f"mult {r_s}, {r_t}", None
        if funct == 0x19: return f"multu {r_s}, {r_t}", None
        if funct == 0x1A: return f"div {r_s}, {r_t}", None
        if funct == 0x1B: return f"divu {r_s}, {r_t}", None
        if funct == 0x20: return f"add {r_d}, {r_s}, {r_t}", None
        if funct == 0x21: return f"addu {r_d}, {r_s}, {r_t}", None
        if funct == 0x22: return f"sub {r_d}, {r_s}, {r_t}", None
        if funct == 0x23: return f"subu {r_d}, {r_s}, {r_t}", None
        if funct == 0x24: return f"and {r_d}, {r_s}, {r_t}", None
        if funct == 0x25: return f"or {r_d}, {r_s}, {r_t}", None
        if funct == 0x26: return f"xor {r_d}, {r_s}, {r_t}", None
        if funct == 0x27: return f"nor {r_d}, {r_s}, {r_t}", None
        if funct == 0x2A: return f"slt {r_d}, {r_s}, {r_t}", None
        if funct == 0x2B: return f"sltu {r_d}, {r_s}, {r_t}", None
        return f"special_0x{funct:02X} {word:08X}", None

    if op == 0x01: # REGIMM
        if rt == 0x00: return f"bltz {r_s}, 0x{branch_target:08X}", branch_target
        if rt == 0x01: return f"bgez {r_s}, 0x{branch_target:08X}", branch_target
        if rt == 0x10: return f"bltzal {r_s}, 0x{branch_target:08X}", branch_target
        if rt == 0x11: return f"bgezal {r_s}, 0x{branch_target:08X}", branch_target
        return f"regimm_0x{rt:02X}", None

    if op == 0x02:
        jump_addr = (pc & 0xF0000000) | target
        return f"j 0x{jump_addr:08X}", jump_addr
    if op == 0x03:
        jump_addr = (pc & 0xF0000000) | target
        return f"jal 0x{jump_addr:08X}", jump_addr
    if op == 0x04: return f"beq {r_s}, {r_t}, 0x{branch_target:08X}", branch_target
    if op == 0x05: return f"bne {r_s}, {r_t}, 0x{branch_target:08X}", branch_target
    if op == 0x06: return f"blez {r_s}, 0x{branch_target:08X}", branch_target
    if op == 0x07: return f"bgtz {r_s}, 0x{branch_target:08X}", branch_target
    if op == 0x08: return f"addi {r_t}, {r_s}, {simm16}", None
    if op == 0x09: return f"addiu {r_t}, {r_s}, {simm16}", None
    if op == 0x0A: return f"slti {r_t}, {r_s}, {simm16}", None
    if op == 0x0B: return f"sltiu {r_t}, {r_s}, {simm16}", None
    if op == 0x0C: return f"andi {r_t}, {r_s}, 0x{imm16:04X}", None
    if op == 0x0D: return f"ori {r_t}, {r_s}, 0x{imm16:04X}", None
    if op == 0x0E: return f"xori {r_t}, {r_s}, 0x{imm16:04X}", None
    if op == 0x0F: return f"lui {r_t}, 0x{imm16:04X}", None
    if op == 0x20: return f"lb {r_t}, {simm16}({r_s})", None
    if op == 0x21: return f"lh {r_t}, {simm16}({r_s})", None
    if op == 0x22: return f"lwl {r_t}, {simm16}({r_s})", None
    if op == 0x23: return f"lw {r_t}, {simm16}({r_s})", None
    if op == 0x24: return f"lbu {r_t}, {simm16}({r_s})", None
    if op == 0x25: return f"lhu {r_t}, {simm16}({r_s})", None
    if op == 0x26: return f"lwr {r_t}, {simm16}({r_s})", None
    if op == 0x28: return f"sb {r_t}, {simm16}({r_s})", None
    if op == 0x29: return f"sh {r_t}, {simm16}({r_s})", None
    if op == 0x2A: return f"swl {r_t}, {simm16}({r_s})", None
    if op == 0x2B: return f"sw {r_t}, {simm16}({r_s})", None
    if op == 0x2E: return f"swr {r_t}, {simm16}({r_s})", None

    # COP0 / COP2
    if op == 0x10: return f"cop0 0x{word:08X}", None
    if op == 0x12: return f"cop2 (gte) 0x{word:08X}", None
    if op == 0x32: return f"lwc2 0x{word:08X}", None
    if op == 0x3A: return f"swc2 0x{word:08X}", None

    return f"unk_op_0x{op:02X} 0x{word:08X}", None

class PSXExe:
    def __init__(self, path):
        with open(path, "rb") as f:
            self.data = f.read()
        self.pc = struct.unpack('<I', self.data[0x10:0x14])[0]
        self.gp = struct.unpack('<I', self.data[0x14:0x18])[0]
        self.load_addr = struct.unpack('<I', self.data[0x18:0x1C])[0]
        self.load_size = struct.unpack('<I', self.data[0x1C:0x20])[0]
        self.code = self.data[0x800:0x800+self.load_size]

    def addr_to_offset(self, addr):
        if addr < self.load_addr or addr >= self.load_addr + len(self.code):
            return None
        return addr - self.load_addr

    def read_word(self, addr):
        off = self.addr_to_offset(addr)
        if off is None or off + 4 > len(self.code):
            return None
        return struct.unpack('<I', self.code[off:off+4])[0]

    def disasm_range(self, start_addr, count):
        res = []
        for i in range(count):
            addr = start_addr + i * 4
            w = self.read_word(addr)
            if w is None:
                res.append(f"{addr:08X}: <unmapped>")
                break
            text, tgt = disasm_inst(w, addr)
            res.append((addr, w, text, tgt))
        return res

if __name__ == "__main__":
    exe = PSXExe(r"D:\OpenCode\HBTN V1.0\reverse-engineering\executable\SLUS_011.15")
    print(f"Entry Point: 0x{exe.pc:08X}")
    print("Disassembly from Entry Point:")
    lines = exe.disasm_range(exe.pc, 60)
    for addr, w, text, tgt in lines:
        print(f"  0x{addr:08X} [{w:08X}]  {text}")
