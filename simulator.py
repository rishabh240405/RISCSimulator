#For unsigned case int(,2) will handle for signed case twos_comp_to_dec will handle
def print_all_registers():
    with open('output.txt','a') as f:
        f.write(sext(str(pc))+' ')
        for i in dict_registers_values:
            f.write('0b'+dict_registers_values[i]+' ')
        f.write('\n')

def print_memory_addresses():
    with open('output.txt','a') as f:
        for i in dict_memory_values:
            f.write(i+':0b'+dict_memory_values[i]+'\n')

def twos_comp_to_dec(num):
    if(num[0]=='1'):
        inverted=''.join('1' if bit=='0' else '0' for bit in num)
        return -(int(inverted,2)+1)
    else:
        return (int(num,2))

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

def add(m_code):
    rs2=m_code[7:12]
    rs1=m_code[12:17]
    rd=m_code[20:25]
    value=sext(str(twos_comp_to_dec(dict_registers_values[rs1])+twos_comp_to_dec(dict_registers_values[rs2])))
    dict_registers_values[rd]=value
    print_all_registers()

def sub(m_code):
    rs2=m_code[7:12]
    rs1=m_code[12:17]
    rd=m_code[20:25]
    value=sext(str(twos_comp_to_dec(dict_registers_values[rs1])-twos_comp_to_dec(dict_registers_values[rs2])))
    dict_registers_values[rd]=value
    print_all_registers()

def sll(m_code):
    rs2=m_code[7:12]
    rs1=m_code[12:17]
    rd=m_code[20:25]
    value=sext(str(int(dict_registers_values[rs1],2)*(2**int(dict_registers_values[rs2][32-4-1:],2))))
    dict_registers_values[rd]=value
    print_all_registers()

def slt(m_code):
    rs2=m_code[7:12]
    rs1=m_code[12:17]
    rd=m_code[20:25]
    if(twos_comp_to_dec(dict_registers_values[rs1])<twos_comp_to_dec(dict_registers_values[rs2])): dict_registers_values[rd]='0'*31+'1'
    print_all_registers()

def sltu(m_code):
    rs2=m_code[7:12]
    rs1=m_code[12:17]
    rd=m_code[20:25]
    if(int(dict_registers_values[rs1],2)<int(dict_registers_values[rs2],2)): dict_registers_values[rd]='0'*31+'1'
    print_all_registers()

def srl(m_code):
    rs2=m_code[7:12]
    rs1=m_code[12:17]
    rd=m_code[20:25]
    value=sext(str(int(dict_registers_values[rs1],2)//(2**int(dict_registers_values[rs2][32-4-1:],2))))
    dict_registers_values[rd]=value
    print_all_registers()

def xor(m_code):
    rs2=m_code[7:12]
    rs1=m_code[12:17]
    rd=m_code[20:25]
    value=sext(str(twos_comp_to_dec(dict_registers_values[rs1])^twos_comp_to_dec(dict_registers_values[rs2])))
    dict_registers_values[rd]=value
    print_all_registers()

def Or(m_code):
    rs2=m_code[7:12]
    rs1=m_code[12:17]
    rd=m_code[20:25]
    value=sext(str(twos_comp_to_dec(dict_registers_values[rs1])|twos_comp_to_dec(dict_registers_values[rs2])))
    dict_registers_values[rd]=value
    print_all_registers()

def And(m_code):
    rs2=m_code[7:12]
    rs1=m_code[12:17]
    rd=m_code[20:25]
    value=sext(str(twos_comp_to_dec(dict_registers_values[rs1])&twos_comp_to_dec(dict_registers_values[rs2])))
    dict_registers_values[rd]=value
    print_all_registers()

def lw(m_code):
    imm=m_code[0:12]
    rs=m_code[32-19-1:32-15]
    rd=m_code[32-11-1:32-7]
    value=twos_comp_to_dec(dict_registers_values[rs])+twos_comp_to_dec(sext(imm))
    value=hex(value)
    value='0x'+(10-len(value))*'0'+value[2:]
    dict_registers_values[rd]=dict_memory_values[value]
    print_all_registers()

def addi(m_code):
    imm=m_code[0:12]
    rs=m_code[32-19-1:32-15]
    rd=m_code[32-11-1:32-7]
    dict_registers_values[rd]=sext(str(twos_comp_to_dec(dict_registers_values[rs])+twos_comp_to_dec(imm)))
    print_all_registers()

def sltiu(m_code):
    imm=m_code[0:12]
    rs=m_code[32-19-1:32-15]
    rd=m_code[32-11-1:32-7]
    dict_registers_values[rd]='0'*31+'1' if(int(dict_registers_values[rs],2)<int(imm,2)) else dict_registers_values[rd]
    print_all_registers()

def jalr(m_code):
    global pc
    imm=m_code[0:12]
    rs=m_code[32-19-1:32-15]
    rd=m_code[32-11-1:32-7]
    dict_registers_values[rd]=sext(str(pc+4))
    pc=(twos_comp_to_dec(dict_registers_values[rs])+twos_comp_to_dec(sext(imm)))
    print_all_registers()

def sw(m_code):
    imm=m_code[0:7]+m_code[32-11-1:32-7]
    rs2=m_code[32-24-1:32-20]
    rs1=m_code[32-19-1:32-15]
    value=hex(twos_comp_to_dec(dict_registers_values[rs1])+twos_comp_to_dec(imm))
    value='0x'+(10-len(value))*'0'+value[2:]
    dict_memory_values[value]=dict_registers_values[rs2]
    print_all_registers()

def beq(m_code):
    global pc
    imm=m_code[0]+m_code[32-7-1]+m_code[1:32-25]+m_code[32-11-1:32-7-1]
    rs2=m_code[32-24-1:32-20]
    rs1=m_code[32-19-1:32-15]
    if(twos_comp_to_dec(dict_registers_values[rs1])==twos_comp_to_dec(dict_registers_values[rs2])): pc=pc+twos_comp_to_dec(imm+'0')
    print_all_registers()

def bne(m_code):
    global pc
    imm=m_code[0]+m_code[32-7-1]+m_code[1:32-25]+m_code[32-11-1:32-7-1]
    rs2=m_code[32-24-1:32-20]
    rs1=m_code[32-19-1:32-15]
    if(twos_comp_to_dec(dict_registers_values[rs1])!=twos_comp_to_dec(dict_registers_values[rs2])):         pc=pc+twos_comp_to_dec(imm+'0')
    print_all_registers()

def bge(m_code):
    global pc
    imm=m_code[0]+m_code[32-7-1]+m_code[1:32-25]+m_code[32-11-1:32-7-1]
    rs2=m_code[32-24-1:32-20]
    rs1=m_code[32-19-1:32-15]
    if(twos_comp_to_dec(dict_registers_values[rs1])>=twos_comp_to_dec(dict_registers_values[rs2])): pc=pc+twos_comp_to_dec(imm+'0')
    print_all_registers()

def bgeu(m_code):
    global pc
    imm=m_code[0]+m_code[32-7-1]+m_code[1:32-25]+m_code[32-11-1:32-7-1]
    rs2=m_code[32-24-1:32-20]
    rs1=m_code[32-19-1:32-15]
    if(int(dict_registers_values[rs1],2)>=int(dict_registers_values[rs2],2)): pc=pc+twos_comp_to_dec(imm+'0')
    print_all_registers()

def blt(m_code):
    global pc
    imm=m_code[0]+m_code[32-7-1]+m_code[1:32-25]+m_code[32-11-1:32-7-1]
    rs2=m_code[32-24-1:32-20]
    rs1=m_code[32-19-1:32-15]
    if(twos_comp_to_dec(dict_registers_values[rs1])<twos_comp_to_dec(dict_registers_values[rs2])): pc=pc+twos_comp_to_dec(imm+'0')
    print_all_registers()

def bltu(m_code):
    global pc
    imm=m_code[0]+m_code[32-7-1]+m_code[1:32-25]+m_code[32-11-1:32-7-1]
    rs2=m_code[32-24-1:32-20]
    rs1=m_code[32-19-1:32-15]
    if(int(dict_registers_values[rs1],2)<int(dict_registers_values[rs2],2)): pc=pc+twos_comp_to_dec(imm+'0')
    print_all_registers()

def lui(m_code):
    imm=m_code[0:20]+12*'0'
    rd=m_code[20:32-7]
    dict_registers_values[rd]=imm
    print_all_registers()

def auipc(m_code):
    imm=m_code[0:20]+12*'0'
    rd=m_code[20:32-7]
    dict_registers_values[rd]=sext(str(pc+twos_comp_to_dec(imm)))
    print_all_registers()

def jal(m_code):
    global pc
    imm=m_code[0]+m_code[32-19-1:32-12]+m_code[32-20-1]+m_code[32-30-1:21]
    rd=m_code[32-11-1:32-7]
    dict_registers_values[rd]=sext(str(pc+4))
    pc=pc+twos_comp_to_dec(sext(imm+'0'))

dict_registers= {"00000": "zero", "00001": "ra", "00010": "sp", "00011": "gp", "00100": "tp", "00101": "t0", "00110": "t1", "00111": "t2", "01000": "s0/fp", "01001": "s1", "01010": "a0", "01011": "a1", "01100": "a2", "01101": "a3", "01110": "a4", "01111": "a5", "10000": "a6", "10001": "a7", "10010": "s2", "10011": "s3", "10100": "s4", "10101": "s5", "10110": "s6", "10111": "s7", "11000": "s8", "11001": "s9", "11010": "s10", "11011": "s11", "11100": "t3", "11101": "t4", "11110": "t5", "11111": "t6"}
dict_registers_values={key:'0'*32 for key in dict_registers}
dict_registers_values["00010"]='00000000000000000000000100000000'
list_memory_addresses=['0x00010000','0x00010004','0x00010008','0x0001000c','0x00010010','0x00010014','0x00010018','0x0001001c','0x00010020','0x00010024','0x00010028','0x0001002c','0x00010030','0x00010034','0x00010038','0x0001003c','0x00010040','0x00010044','0x00010048','0x0001004c','0x00010050','0x00010054','0x00010058','0x0001005c','0x00010060','0x00010064','0x00010068','0x0001006c','0x00010070','0x00010074','0x00010078','0x0001007c']
dict_memory_values={key:'0'*32 for key in list_memory_addresses}
dict_lines_addresses={} #Integer(not binary/hexa) to machine code mapping
with open('test_case.txt','r') as f:
    l_machine_code=[i.rstrip('\n') for i in f.readlines()]

pc=4
j=4
for i in l_machine_code:
    dict_lines_addresses[j]=i
    if(i=='0'*25+'1100011'): break #in case halt is in between the code
    j+=4
#now j stores the value of halt in the case the code is normal

for i in l_machine_code:
    #R type
    if(i[0:7]=='0000000' and i[17:20]=='000' and i[25:]=='0110011') : add(i)
    elif(i[0:7]=='0100000' and i[17:20]=='000' and i[25:]=='0110011'): sub(i)
    elif(i[0:7]=='0000000' and i[17:20]=='001' and i[25:]=='0110011'): sll(i)
    elif(i[0:7]=='0000000' and i[17:20]=='010' and i[25:]=='0110011'): slt(i)
    elif(i[0:7]=='0000000' and i[17:20]=='011' and i[25:]=='0110011'): sltu(i)
    elif(i[0:7]=='0000000' and i[17:20]=='100' and i[25:]=='0110011'): xor(i)
    elif(i[0:7]=='0000000' and i[17:20]=='101' and i[25:]=='0110011'): srl(i)
    elif(i[0:7]=='0000000' and i[17:20]=='110' and i[25:]=='0110011'): Or(i)
    elif(i[0:7]=='0000000' and i[17:20]=='111' and i[25:]=='0110011'): And(i)

    #I type
    elif(i[17:20]=='010' and i[25:]=='0000011'): lw(i)
    elif(i[17:20]=='000' and i[25:]=='0010011'): addi(i)
    elif(i[17:20]=='011' and i[25:]=='0000011'): sltiu(i)
    elif(i[17:20]=='000' and i[25:]=='1100111'):
      jalr(i)
      continue

    #S type
    elif(i[17:20]=='010' and i[25:]=='0100011'): sw(i)

    #B type
    elif(i[17:20]=='000' and i[25:]=='1100011'):
      beq(i)
      if(i[0:25]=='0'*25): break
      continue
    elif(i[17:20]=='001' and i[25:]=='1100011'):
      bne(i)
      continue
    elif(i[17:20]=='100' and i[25:]=='1100011'):
      blt(i)
      continue
    elif(i[17:20]=='101' and i[25:]=='1100011'):
      bge(i)
      continue
    elif(i[17:20]=='110' and i[25:]=='1100011'):
      bltu(i)
      continue
    elif(i[17:20]=='111' and i[25:]=='1100011'):
      bgeu(i)
      continue

    #U Type
    elif(i[25:]=='0110111'): lui(i)
    elif(i[25:]=='0010111'): auipc(i)

    #J Type
    elif(i[25:]=='1101111'):
      jal(i)
      continue
    pc+=4

print_memory_addresses() 
