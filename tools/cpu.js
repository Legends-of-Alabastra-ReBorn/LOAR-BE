let opTable = {
    0b10000010: 'LDI',
    0b01000111: 'PRN',
  
    0b10100000: 'ADD',
    0b10100001: 'SUB',
    0b10100010: 'MUL',
    0b10100011: 'DIV',
    0b10100100: 'MOD',
    0b01100110: 'DEC',
    0b01100101: 'INC',
  
    0b01000110: 'POP',
    0b01000101: 'PUSH',
  
    0b01010000: 'CALL',
    0b00010001: 'RET',
  
    0b10100111: 'CMP',
    0b01010100: 'JMP',
    0b01010101: 'JEQ',
    0b01010110: 'JNE',
  
    0b10101000: 'AND',
    0b10101010: 'OR',
    0b10101011: 'XOR',
    0b01101001: 'NOT',
    0b10101100: 'SHL',
    0b10101101: 'SHR',
  
    0b01010010: 'INT',
    0b00010011: 'IRET',
  
    0b01011010: 'JGE',
    0b01010111: 'JGT',
    0b01011001: 'JLE',
    0b01011000: 'JLT',
    0b10000011: 'LD',
    0b01001000: 'PRA',
    0b10000100: 'ST',
  };
  
class CPU {
    constructor() {
      this.opTable = {
        LDI: (a, b) => { this.reg_write(a, b)},
        PRN: (a, b) => { this.message += this.reg[a]},
        ADD: (a, b) => { this.alu('ADD', a, b)},
        SUB: (a, b) => { this.alu('SUB, a, b')},
        MUL: (a, b) => { this.alu('MUL', a, b)},
        DIV: (a, b) => { this.alu('DIV', a, b)},
        MOD: (a, b) => { this.alu('MOD', a, b)},
        DEC: (a, b) => { this.alu('DEC', a, b)},
        INC: (a, b) => { this.alu('INC', a, b)},
        POP: (a, _) => { this.pop_stack(a)},
        PUSH: (a, _) => { this.push_stack(a)},
  
        CALL: (a, _) => { this.call(a)},
        RET: (a, _) => { this.ret()},
  
        CMP: (a, b) => { this.alu('CMP', a, b)},
        JMP: (a, _) => { this.set_pc(a)},
        JEQ: (a, b) => { this.comparator('eq', a)},
        JNE: (a, b) => { this.comparator('ne', a)},
  
        AND: (a, b) => { this.alu('AND', a, b)},
        OR: (a, b) => { this.alu('OR', a, b)},
        XOR: (a, b) => { this.alu('XOR', a, b)},
        NOT: (a, b) => { this.alu('NOT', a, b)},
        SHL: (a, b) => { this.alu('SHL', a, b)},
        SHR: (a, b) => { this.alu('SHR', a, b)},
  
        JGE: (a, b) => { this.comparator('ge', a)},
        JGT: (a, b) => { this.comparator('gt', a)},
        JLE: (a, b) => { this.comparator('le', a)},
        JLT: (a, b) => { this.comparator('lt', a)},
  
        LD: (a, b) => { this.ld(a, b)},
        ST: (a, b) => { this.st(a, b)},
  
        PRA: (a, b) => { this.message += String.fromCharCode(this.reg[a])},
      };
  
      this.PC = 0;
      this.FL = 0;
      this.ram = Array(256).fill(0)
      this.reg = Array(8).fill(0)
      this.IM = 5;
      this.IS = 6;
      this.SP = 7;
      this.KEY = 0xf4;
      this.reg[this.SP] = 0xf4;
      this.timer = 0;
      this.interrupts_allowed = true;
      this.message = '';
    }
  
    load(programArr) {
      let address = 0;
      for (let line of programArr) {
        this.ram_write(address, parseInt(line, 2));
        address += 1;
      }
    }
  
    alu(op, a, b) {
      const add = (reg_a, reg_b) => {
        this.reg[reg_a] += this.reg[reg_b];
      };
      const sub = (reg_a, reg_b) => {
        this.reg[reg_a] -= this.reg[reg_b];
      };
      const mul = (reg_a, reg_b) => {
        this.reg[reg_a] *= this.reg[reg_b];
      };
      const div = (reg_a, reg_b) => {
        this.reg[reg_a] /= this.reg[reg_b];
      };
      const mod = (reg_a, reg_b) => {
        this.reg[reg_a] %= this.reg[reg_b];
      };
      const inc = (reg_a, _) => {
        this.reg[reg_a] += 1;
      };
      const dec = (reg_a, _) => {
        this.reg[reg_a] -= 1;
      };
  
      const and_op = (reg_a, reg_b) => {
        this.reg[reg_a] = this.reg[reg_a] & this.reg[reg_b];
      };
      const or_op = (reg_a, reg_b) => {
        this.reg[reg_a] = this.reg[reg_a] | this.reg[reg_b];
      };
      const xor_op = (reg_a, reg_b) => {
        this.reg[reg_a] = this.reg[reg_a] ^ this.reg[reg_b];
      };
      const not_op = (reg_a, _) => {
        this.reg[reg_a] = ~this.reg[reg_a];
      };
      const shl_op = (reg_a, reg_b) => {
        this.reg[reg_a] = this.reg[reg_a] << this.reg[reg_b];
      };
      const shr_op = (reg_a, reg_b) => {
        this.reg[reg_a] = this.reg[reg_a] >> this.reg[reg_b];
      };
      let alu_math_ops = {
        ADD: add,
        SUB: sub,
        MUL: mul,
        DIV: div,
        MOD: mod,
        DEC: dec,
        INC: inc,
      };
  
      let alu_bit_ops = {
        AND: and_op,
        OR: or_op,
        XOR: xor_op,
        NOT: not_op,
        SHL: shl_op,
        SHR: shr_op,
      };
  
      try {
        if (op in alu_math_ops) alu_math_ops[op](a, b);
        else if (op in alu_bit_ops) alu_bit_ops[op](a, b);
        else if (op === 'CMP') this.FL = 0b00000000;
        if (this.reg[a] === this.reg[b]) this.FL = 0b00000001;
        else if (this.reg[a] < this.reg[b]) this.FL = 0b00000100;
        else this.FL = 0b00000010;
      } catch (error) {
        console.log('Unsupported ALU operation');
      }
    }
  
    ram_read(mar) {
      return this.ram[mar];
    }
    ram_write(mar, mdr) {
      this.ram[mar] = mdr;
    }
    reg_write(register, value) {
      this.reg[register] = value;
    }
    pop_stack(reg_address) {
      this.reg[reg_address] = this.ram_read(this.reg[this.SP]);
      this.reg[this.SP] += 1;
    }
  
    push_stack(reg_address) {
      this.reg[this.SP] -= 1;
      this.ram_write(this.reg[this.SP], this.reg[reg_address]);
    }
  
    call(reg_address) {
      this.reg[this.SP] -= 1;
      this.ram_write(this.reg[this.SP], this.PC + 2);
      this.PC = this.reg[reg_address];
    }
  
    ret() {
      this.PC = this.ram_read(this.reg[this.SP]);
      this.reg[this.SP] += 1;
    }
    set_pc(reg_a) {
      this.PC = this.reg[reg_a];
    }
    comparator(test, reg_a) {
      let masks = {
        eq: 0b1,
        ne: 0b1,
        ge: 0b11,
        gt: 0b10,
        le: 0b101,
        lt: 0b100,
      };
      let flag = this.FL & masks[test];
      if (flag && test !== 'ne') this.PC = this.reg[reg_a];
      else if (test === 'ne' && flag === 0) this.PC = this.reg[reg_a];
      else this.PC += 2;
    }
  
    ld(reg_a, reg_b) {
      this.reg[reg_a] = this.ram_read(this.reg[reg_b]);
    }
  
    st(reg_a, reg_b) {
      this.ram_write(this.reg[reg_a], this.reg[reg_b]);
    }
  
    run(){
      let halted = false;
      while (!halted) {
        let IR = this.ram_read(this.PC);
        let operand_a = this.ram_read(this.PC + 1);
        let operand_b = this.ram_read(this.PC + 2);
  
        if (IR in opTable) {
          this.opTable[opTable[IR]](operand_a, operand_b);
          let operands = IR >> 6;
          let set_directly = (IR & 0b10000) >> 4;
          if (!set_directly) this.PC += operands + 1;
        } else if (IR === 'HLT') halted = true;
        else if (IR === 'NOP') continue;
        else {
          halted = true;
        }
      }
    }
  }

// code = ['10000010','00000001','01001101','01001000','00000001','10000010','00000001','01101001','01001000','00000001','10000010','00000001','01101110','01001000','00000001','10000010','00000001','01100101','01001000','00000001','10000010','00000001','00100000','01001000','00000001','10000010','00000001','01111001','01001000','00000001','10000010','00000001','01101111','01001000','00000001','10000010','00000001','01110101','01001000','00000001','10000010','00000001','01110010','01001000','00000001','10000010','00000001','00100000','01001000','00000001','10000010','00000001','01100011','01001000','00000001','10000010','00000001','01101111','01001000','00000001','10000010','00000001','01101001','01001000','00000001','10000010','00000001','01101110','01001000','00000001','10000010','00000001','00100000','01001000','00000001','10000010','00000001','01101001','01001000','00000001','10000010','00000001','01101110','01001000','00000001','10000010','00000001','00100000','01001000','00000001','10000010','00000001','01110010','01001000','00000001','10000010','00000001','01101111','01001000','00000001','10000010','00000001','01101111','01001000','00000001','10000010','00000001','01101101','01001000','00000001','10000010','00000001','00100000','01001000','00000001','10000010','00000001','00110001','01001000','00000001','10000010','00000001','00110010','01001000','00000001','10000010','00000001','00110100','01001000','00000001','00000001']
code = ['10000010','00000001','01001101','01001000','00000001','10000010','00000001','01101001','01001000','00000001','10000010','00000001','01101110','01001000','00000001','10000010','00000001','01100101','01001000','00000001','10000010','00000001','00100000','01001000','00000001','10000010','00000001','01111001','01001000','00000001','10000010','00000001','01101111','01001000','00000001','10000010','00000001','01110101','01001000','00000001','10000010','00000001','01110010','01001000','00000001','10000010','00000001','00100000','01001000','00000001','10000010','00000001','01100011','01001000','00000001','10000010','00000001','01101111','01001000','00000001','10000010','00000001','01101001','01001000','00000001','10000010','00000001','01101110','01001000','00000001','10000010','00000001','00100000','01001000','00000001','10000010','00000001','01101001','01001000','00000001','10000010','00000001','01101110','01001000','00000001','10000010','00000001','00100000','01001000','00000001','10000010','00000001','01110010','01001000','00000001','10000010','00000001','01101111','01001000','00000001','10000010','00000001','01101111','01001000','00000001','10000010','00000001','01101101','01001000','00000001','10000010','00000001','00100000','01001000','00000001','10000010','00000001','11101101','10000010','00000010','10101101','10101000','00000001','00000010','10000010','00000010','10011100','10101011','00000001','00000010','01001000','00000001','10000010','00000001','00010110','10000010','00000010','11001111','10101000','00000001','00000010','10000010','00000010','00110011','10101011','00000001','00000010','01001000','00000001','10000010','00000001','00010111','10000010','00000010','01111110','10101000','00000001','00000010','10000010','00000010','00100001','10101011','00000001','00000010','01001000','00000001','00000001']
const cpu = new CPU()
cpu.load(code)
cpu.run()
console.log(cpu.message)