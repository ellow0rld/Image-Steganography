def sec_steg(secret_mssg):
    ascii_secret=[]
    binary=[]
    global ciphertxt
    ciphertxt=""
    cipher=[]
    for i in secret_mssg:
        ascii_secret.append(ord(str(i)))
    for i in ascii_secret:
        binary.append(list(bin(i).replace("0b","")))
    for i in range (0,len(binary)):
        if (binary[i][-1] =='0'):
            binary[i][-1] ='1'
        else:
            binary[i][-1] ='0'
    for i in range (0,len(binary)):
        b=""
        for j in binary[i]:
            b=b+j
        cipher.append(chr(int(b,2)))
    for i in cipher:
        if i == "`":
          ciphertxt = ciphertxt+ 'z'
        elif i == "{":
            ciphertxt = ciphertxt + 'a'
        elif i == '@':
            ciphertxt = ciphertxt + 'Z'
        elif i == '[':
            ciphertxt = ciphertxt + 'A'
        else:
            ciphertxt = ciphertxt + i
    return ciphertxt
