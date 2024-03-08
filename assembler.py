def hex_to_binary(n):
    dict_hex_to_bin = {'0': '0000', '1': '0001', '2': '0010', '3': '0011','4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}
    n=''.join([dict_hex_to_bin[i] for i in n])
    return n

def sext(imm): #Each register is 32 bit wide and thus each constant value is extended to 32 bits
    if imm[0:2]=='0x': imm=hex_to_binary(imm[2:])
    #else: imm=dec_to_binary(imm)
    signed_bit=imm[0]
    k=(32-len(imm))*signed_bit
    imm=k+imm
    return imm

def R_conversion(line,instruction):
    dict_funct7_funct3_opcode={'add':['0000000','000','0110011'],'sub':['0100000','000','0110011'],'sll':['0000000','001','0110011'],'slt':['0000000','010','0110011'],'sltu':['0000000','011','0110011'],'xor':['0000000','100','0110011'],'srl':['0000000','101','0110011'],'or':['0000000','110','0110011'],'and':['0000000','111','0110011']}
    l_parts=line.replace(',','').split(' ') #[instruction,rd,rs1,rs2]
    line_encoded=dict_funct7_funct3_opcode[instruction][0]+dict_registers[l_parts[3]]+dict_registers[l_parts[2]]+dict_funct7_funct3_opcode[instruction][1]+dict_registers[l_parts[1]]+dict_funct7_funct3_opcode[instruction][2] #funct7+rs2+rs1+funct3+rd+opcode
    return line_encoded+'\n'

def I_conversion(line,instruction):
    dict_funct3_opcode={'lw':['010','0000011'],'addi':['000','0010011'],'sltiu':['011','0010011'],'jalr':['000','1100111']}
    if instruction=='lw':
        l_parts=line.replace(',','').replace('(',' ').replace(')','').split(' ') #[lw,rd,imm,rs1]
        imm=sext(l_parts[2])
        line_encoded=imm[32-11-1:]+dict_registers[l_parts[3]]+dict_funct3_opcode[instruction][0]+dict_registers[l_parts[1]]+dict_funct3_opcode[instruction][1] #imm+rs+funct3+rd+opcode
    else:
        l_parts=line.replace(',','').split(' ') #[instruction,rd,rs/x6,imm]
        imm=sext(l_parts[3])
        line_encoded=imm[32-11-1:]+dict_registers[l_parts[2]]+dict_funct3_opcode[instruction][0]+dict_registers[l_parts[1]]+dict_funct3_opcode[instruction][1]
    return line_encoded+'\n'

def S_conversion(line,instruction):
    dict_funct3_opcode={'sw':['010','0100011']}
    l_parts=line.replace(',','').replace('(',' ').replace(')','').split(' ') #[sw,rs2,imm,rs1]
    imm=sext(l_parts[2])
    line_encoded=imm[32-11-1:32-5]+dict_registers[l_parts[1]]+dict_registers[l_parts[3]]+dict_funct3_opcode[instruction][0]+imm[32-4-1:]+dict_funct3_opcode[instruction][1] 
    return line_encoded+'\n'

def B_conversion(line,instruction):
    dict_funct3_opcode={'beq':['000','1100011'],'bne':['001','1100011'],'blt':['100','1100011'],'bge':['101','1100011'],'bltu':['110','1100011'],'bgeu':['111','1100011']}
    l_parts=line.replace(',','').split(' ') #[instruction,rs1,rs2,imm/label]
    if(l_parts[3].isalnum()):
        imm=sext(l_parts[3])
        line_encoded=(imm[32-12-1]+imm[32-10-1:32-4])+dict_registers(l_parts[2])+dict_registers(l_parts[1])+dict_funct3_opcode[instruction][0]+(imm[32-4-1]+imm[32-1-1:32-12])+dict_funct3_opcode[instruction][1] #imm[12|10:5]+rs2+rs1+funct3+imm[4|1:11]+opcode
        return line_encoded+'\n'
    # else:
    #     return

def U_conversion(line,instruction):
    dict_opcode={'lui':'0110111','auipc':'0010111'}
    l_parts=line.replace(',','').split(' ') #[instruction,rd,imm]
    imm=sext(l_parts[2])
    l_encoded=imm[32-31-1:32-11]+dict_registers[l_parts[1]]+dict_opcode[instruction]
    return l_encoded

def J_conversion(line,instruction):
    dict_opcode={'jal':'1101111'}
    l_parts=line.replace(',','').split(' ') #[instruction,rd,imm]
    if(l_parts[2].isalnum()):
        imm=sext(l_parts[2])
        l_encoded=(imm[32-20-1]+imm[32-10-1:]+imm[32-11-1]+imm[32-19-1:32-11])+dict_registers[l_parts[1]]+dict_opcode[instruction]
        return l_encoded
    # else:
    #     return

# def bonus_conversion(line,instruction):
#     return

with open('assembly.txt','r') as f:
    l_code_lines=[i.rstrip('\n') for i in f.readlines()]

l_base_instructions_R=['add','sub','slt','sltu','xor','sll','srl','or','and']
l_base_instructions_I=['lw','addi','sltiu','jalr']
l_base_instructions_S=['sw']
l_base_instructions_B=['beq','bne','bge','bgeu','blt','bltu']
l_base_instructions_U=['auipc','lui']
l_base_instructions_J=['jal']
l_base_instructions_bonus=['mul','rst','halt','rvrs']
dict_registers = {"x0": "00000","x1": "00001","x2": "00010","x3": "00011","x4": "00100","x5": "00101","x6": "00110","x7": "00111","x8": "01000","x9": "01001","x10": "01010","x11": "01011","x12": "01100","x13": "01101","x14": "01110","x15": "01111","x16": "10000","x17": "10001","x18": "10010","x19": "10011","x20": "10100","x21": "10101","x22": "10110","x23": "10111","x24": "11000","x25": "11001","x26": "11010","x27": "11011","x28": "11100","x29": "11101","x30": "11110","x31": "11111"}
str_machine_code=""

for i in l_code_lines:
    l_temp=i.split(" ")
    if l_temp[0] in l_base_instructions_R: str_machine_code+=R_conversion(i,l_temp[0])
    elif l_temp[0] in l_base_instructions_I: str_machine_code+=I_conversion(i,l_temp[0])
    elif l_temp[0] in l_base_instructions_S: str_machine_code+=S_conversion(i,l_temp[0])
    elif l_temp[0] in l_base_instructions_B: str_machine_code+=B_conversion(i,l_temp[0])
    elif l_temp[0] in l_base_instructions_U: str_machine_code+=U_conversion(i,l_temp[0])
    elif l_temp[0] in l_base_instructions_J: str_machine_code+=J_conversion(i,l_temp[0])
    # elif l_temp[0] in l_base_instructions_bonus: str_machine_code+=bonus_conversion(i,l_temp[0])
    else: continue

print(str_machine_code.rstrip('\n'))
