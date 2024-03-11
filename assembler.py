import re

def dec_to_twos_comp(imm):
    n=int(imm)
    if n<0:
        abs_decimal=abs(n)
        bin_str ='0'+bin(abs_decimal)[2:]#[2:] because the first 2 letters are 0b denoting binary number,'0' is added to prevent overflow when 1 is added after inversion
        inverted_bin_str = ''.join(['1' if bit=='0' else '0' for bit in bin_str])#bit inversion to generate 1's complement
        twos_complement=bin(int(inverted_bin_str, base=2)+1)[2:]#Adding 1 to the 1's complement to get the 2's complement(adding 1 in binary is same as adding 1 in decimal) because 1*2**0=1
        return str(twos_complement)
    else:
        return '0'+str(bin(n)[2:])

def hex_to_binary(n):
    dict_hex_to_bin = {'0':'0000','1':'0001','2':'0010','3':'0011','4':'0100','5':'0101','6':'0110','7':'0111','8':'1000','9':'1001','A':'1010','B':'1011','C':'1100','D':'1101','E':'1110','F':'1111'}
    n=''.join([dict_hex_to_bin[i] for i in n])
    return n
 
def sext(imm): #Each register is 32 bit wide and thus each constant value(binary form) is extended to 32 bits
    if imm[0:2]=='0x': imm=hex_to_binary(imm[2:])
    else: imm=dec_to_twos_comp(imm)
    if len(imm)>32: return 'Error'
    signed_bit=imm[0]
    k=(32-len(imm))*signed_bit
    imm=k+imm
    return imm

def R_conversion(l_parts,instruction,line_num):#[instruction,rd,rs1,rs2]
    dict_funct7_funct3_opcode={'add':['0000000','000','0110011'],'sub':['0100000','000','0110011'],'sll':['0000000','001','0110011'],'slt':['0000000','010','0110011'],'sltu':['0000000','011','0110011'],'xor':['0000000','100','0110011'],'srl':['0000000','101','0110011'],'or':['0000000','110','0110011'],'and':['0000000','111','0110011'],'mul':['0000001','000','0110011']}
    rd=l_parts[1]
    rs1=l_parts[2]
    rs2=l_parts[3]
    if(rd not in dict_registers or rs1 not in dict_registers or rs2 not in dict_registers): return ['Error','Typo in register name in line: '+str(line_num)]
    line_encoded=dict_funct7_funct3_opcode[instruction][0]+dict_registers[rs2]+dict_registers[rs1]+dict_funct7_funct3_opcode[instruction][1]+dict_registers[rd]+dict_funct7_funct3_opcode[instruction][2] #funct7+rs2+rs1+funct3+rd+opcode
    return line_encoded+'\n'

def I_conversion(l_parts,instruction,line_num):
    dict_funct3_opcode={'lw':['010','0000011'],'addi':['000','0010011'],'sltiu':['011','0010011'],'jalr':['000','1100111']}
    if instruction=='lw': #[lw,rd,imm,rs1]
        rd=l_parts[1]
        imm=sext(l_parts[2])
        if(imm=='Error'): return ['Error','Immediate value exceeds 32 bits at line:'+str(line_num)]
        rs1=l_parts[3]
        if(rd not in dict_registers or rs1 not in dict_registers): return ['Error','Typo in register name in line: '+str(line_num)]
        line_encoded=imm[32-11-1:]+dict_registers[rs1]+dict_funct3_opcode[instruction][0]+dict_registers[rd]+dict_funct3_opcode[instruction][1] #imm+rs+funct3+rd+opcode
    else:#[instruction,rd,rs/x6,imm]
        rd=l_parts[1]
        imm=sext(l_parts[3])
        if(imm=='Error'): return ['Error','Immediate value exceeds 32 bits at line:'+str(line_num)]
        rs=l_parts[2]
        if(rd not in dict_registers or rs1 not in dict_registers): return ['Error','Typo in register name in line: '+str(line_num)]
        line_encoded=imm[32-11-1:]+dict_registers[rs]+dict_funct3_opcode[instruction][0]+dict_registers[rd]+dict_funct3_opcode[instruction][1]
    return line_encoded+'\n'

def S_conversion(l_parts,instruction,line_num):#[sw,rs2,imm,rs1]
    dict_funct3_opcode={'sw':['010','0100011']}
    imm=sext(l_parts[2])
    if(imm=='Error'): return ['Error','Immediate value exceeds 32 bits at line:'+str(line_num)]
    rs2=l_parts[1]
    rs1=l_parts[3]
    if(rs2 not in dict_registers or rs1 not in dict_registers): return ['Error','Typo in register name in line: '+str(line_num)]
    line_encoded=imm[32-11-1:32-5]+dict_registers[rs2]+dict_registers[rs1]+dict_funct3_opcode[instruction][0]+imm[32-4-1:]+dict_funct3_opcode[instruction][1] 
    return line_encoded+'\n'

def B_conversion(l_parts,instruction,line_num):#[instruction,rs1,rs2,imm/label]
    dict_funct3_opcode={'beq':['000','1100011'],'bne':['001','1100011'],'blt':['100','1100011'],'bge':['101','1100011'],'bltu':['110','1100011'],'bgeu':['111','1100011']}
    if(l_parts==['beq','zero','zero','0'] and line_num!=len(l_code_lines)-1): return ['Error','Virtual halt at line '+str(line_num)+'and not at lasts line'] 
    if(l_parts[3].isdigit() or (l_parts[3][0]=='-' and l_parts[3][1:].isdigit())):
        rs1=l_parts[1]
        rs2=l_parts[2]
        if(rs2 not in dict_registers or rs1 not in dict_registers): return ['Error','Typo in register name in line: '+str(line_num)]
        imm=sext(l_parts[3])
        if(imm=='Error'): return ['Error','Immediate value exceeds 32 bits at line:'+str(line_num)]
        line_encoded=(imm[32-12-1]+imm[32-10-1:32-5])+dict_registers[rs2]+dict_registers[rs1]+dict_funct3_opcode[instruction][0]+(imm[32-4-1:32-1]+imm[32-11-1])+dict_funct3_opcode[instruction][1] #imm[12|10:5]+rs2+rs1+funct3+imm[4:1|11]+opcode
        return line_encoded+'\n'
    else:
        rs1=l_parts[1]
        rs2=l_parts[2]
        if(rs2 not in dict_registers or rs1 not in dict_registers): return ['Error','Typo in register name in line: '+str(line_num)]
        imm=sext(str((line_num-dict_label[l_parts[3]])*4))
        if(imm=='Error'): return ['Error','Immediate value exceeds 32 bits at line:'+str(line_num)]
        line_encoded=(imm[32-12-1]+imm[32-10-1:32-5])+dict_registers[rs2]+dict_registers[rs1]+dict_funct3_opcode[instruction][0]+(imm[32-4-1:32-1]+imm[32-11-1])+dict_funct3_opcode[instruction][1] #imm[12|10:5]+rs2+rs1+funct3+imm[4:1|11]+opcode
        return line_encoded+'\n'

def U_conversion(l_parts,instruction,line_num):#[instruction,rd,imm]
    dict_opcode={'lui':'0110111','auipc':'0010111'}
    rd=l_parts[1]
    if(rd not in dict_registers): return ['Error','Typo in register name in line: '+str(line_num)]
    imm=sext(l_parts[2])
    if(imm=='Error'): return ['Error',['Error','Immediate value exceeds 32 bits at line:'+str(line_num)]]
    l_encoded=imm[32-31-1:32-12]+dict_registers[rd]+dict_opcode[instruction]
    return l_encoded+'\n'

def J_conversion(l_parts,instruction,line_num):#[instruction,rd,imm]
    dict_opcode={'jal':'1101111'}
    if(l_parts[2].isdigit() or (l_parts[2][0]=='-' and l_parts[2][1:].isdigit())): #[1:] because there can be a - sign in start
        rd=l_parts[1]
        if(rd not in dict_registers): return ['Error','Typo in register name in line: '+str(line_num)]
        imm=sext(l_parts[2])
        if(imm=='Error'): return ['Error',['Error','Immediate value exceeds 32 bits at line:'+str(line_num)]]
        l_encoded=(imm[32-20-1]+imm[32-10-1:32-1]+imm[32-11-1]+imm[32-19-1:32-12])+dict_registers[rd]+dict_opcode[instruction]
        return l_encoded+'\n'
    else:
        rd=l_parts[1]
        if(rd not in dict_registers): return ['Error','Typo in register name in line: '+str(line_num)]
        imm=sext(str((line_num-dict_label[l_parts[2]])*4))
        if(imm=='Error'): return ['Error',['Error','Immediate value exceeds 32 bits at line:'+str(line_num)]]
        l_encoded=(imm[32-20-1]+imm[32-10-1:32-1]+imm[32-11-1]+imm[32-19-1:32-12])+dict_registers[rd]+dict_opcode[instruction]
        return l_encoded+'\n'

# def bonus_conversion(line,instruction):
#     return

with open('assembly.txt','r') as f:
    l_code_lines=[i.rstrip('\n') for i in f.readlines()]

l_instructions=['add','sub','slt','sltu','xor','sll','srl','or','and','lw','addi','sltiu','jalr','sw','beq','bne','bge','bgeu','blt','bltu','auipc','lui','jal','mul','rst','halt','rvrs']
l_base_instructions_R=['add','sub','slt','sltu','xor','sll','srl','or','and']
l_base_instructions_I=['lw','addi','sltiu','jalr']
l_base_instructions_S=['sw']
l_base_instructions_B=['beq','bne','bge','bgeu','blt','bltu']
l_base_instructions_U=['auipc','lui']
l_base_instructions_J=['jal']
l_base_instructions_bonus=['mul','rst','halt','rvrs']
dict_registers = {"zero": "00000","ra": "00001","sp": "00010","gp": "00011","tp": "00100","t0": "00101","t1": "00110","t2": "00111","s0": "01000","fp": "01000","s1": "01001","a0": "01010","a1": "01011","a2": "01100","a3": "01101","a4": "01110","a5": "01111","a6": "10000","a7": "10001","s2": "10010","s3": "10011","s4": "10100","s5": "10101","s6": "10110","s7": "10111","s8": "11000","s9": "11001","s10": "11010","s11": "11011","t3": "11100","t4": "11101","t5": "11110","t6": "11111"}

l_machine_code=[]
dict_label={}

for i in range(len(l_code_lines)):
    l_first=l_code_lines[i].lstrip(' ').split(' ')[0]
    if l_first[len(l_first)-1]==':': dict_label[l_first.replace(':','')]=i+1

for i in range(len(l_code_lines)):
    l_parts=re.split(r'[,()\s]+',l_code_lines[i])
    if(l_parts[0] not in l_instructions):
        l_machine_code.append(["Error","Instruction typo Error at line:"+str(i+1)])
        break
    while(l_parts[0] not in l_instructions or len(l_parts)==0): l_parts.pop(0)
    if len(l_parts)==0: continue
    if(l_parts==['addi','zero','zero','0'] or l_parts==['addi','x0','x0','0']): continue
    if(i==len(l_code_lines)-1 and l_parts!=['beq','zero','zero','0']): l_machine_code.append(['Error','Virtual halt not present in the code'])
    if l_parts[0] in l_base_instructions_R: 
        returning_value=R_conversion(l_parts,l_parts[0],i+1)
        l_machine_code.append(returning_value)
        if returning_value[0]=='Error': break
    elif l_parts[0] in l_base_instructions_I: 
        returning_value=I_conversion(l_parts,l_parts[0],i+1)
        l_machine_code.append(returning_value)
        if returning_value[0]=='Error': break
    elif l_parts[0] in l_base_instructions_S: 
        returning_value=S_conversion(l_parts,l_parts[0],i+1)
        l_machine_code.append(returning_value)
        if returning_value[0]=='Error': break
    elif l_parts[0] in l_base_instructions_B: 
        returning_value=B_conversion(l_parts,l_parts[0],i+1)
        l_machine_code.append(returning_value)
        if returning_value[0]=='Error': break
    elif l_parts[0] in l_base_instructions_U: 
        returning_value=U_conversion(l_parts,l_parts[0],i+1)
        l_machine_code.append(returning_value)
        if returning_value[0]=='Error': break
    elif l_parts[0] in l_base_instructions_J: 
        returning_value=J_conversion(l_parts,l_parts[0],i+1)
        l_machine_code.append(returning_value)
        if returning_value[0]=='Error': break
    # elif l_parts[0] in l_base_instructions_bonus: str_machine_code+=bonus_conversion(i,l_parts[0])
    else: continue

with open('output.txt','w') as f:
    if(l_machine_code[len(l_machine_code)-1][0]=="Error"): f.write(l_machine_code[len(l_machine_code)-1][1])
    else:
        l_machine_code[len(l_machine_code)-1]=l_machine_code[len(l_machine_code)-1].replace('\n','') #removing escape sequence from last line
        for i in l_machine_code:
            f.write(i) #ek hi run mei multiple writes append ka kaam krte hai aur override nhi krte
