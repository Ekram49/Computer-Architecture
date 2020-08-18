"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0b0] * 256
        self.reg[7] = 0xF4

    def load(self, filename=None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        if filename:
            with open(sys.argv[1]) as x:
                address = 0
                for l in x:
                    value = l.split('#')[0].strip()
                    if value == "":
                        continue
                    else:
                        instruction = int(l, 2)
                        self.ram[address] = instruction
                        address +=1

        else:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

        for instruction in program:
            self.ram[address] = instruction
            


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        running = True

        while running:
            ir = self.ram[self.pc]

            operand_a = self.ram[self.pc+1]
            operand_b = self.ram[self.pc+2]

            if ir == HLT:
                running = False
                self.pc+=1
            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc +=3
            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc+=2
            else:
                print(f"Unknown instruction {ir} at address {self.pc}")
                self.pc += 1

