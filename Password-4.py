from time import time
cvf=0
import os
import binascii
self="'"

namez = input("for password for encrypt file p1 or p2 insert password from file ")
#@Author Jurijus pacalovas
class password_class:

    def password1(self):
                def strToBinary(s):
                    bin_conv = []
                 
                    for c in s:
                         
                        # convert each char to
                        # ASCII value
                        ascii_val = ord(c)
                         
                        # Convert ASCII value to binary
                        binary_val = bin(ascii_val)
                        bin_conv.append(binary_val[2:])
                     
                        return (' '.join(bin_conv))    
                
                self.name = "Author: Jurijus Pacalovas"

                print(self.name)

                if namez!="p1" and namez!="p2":
                    print("Your enter incorrect letter")
                
                if namez=="p1":


                    
                   
                    name = input("What is name of file? ")
                    if os.path.exists(name):
                            print('Path is exists!')
                    else:
                            print('Path is not exists!')
                            raise SystemExit
                   
                    long_block=100
                        
                    namea=""
                    namem=""
                    namema="?"
                    Portal=2
                    assxw=0
                    blockw=5
                    blockw1=4
                    nameas=name
                    nac=len(nameas)

                    long=len(name)
                   
                    Times_compression=1
                    
                    name_cut=len(".bin")
                    
                    nameas=name+".bin"
                    name_bofore=len(nameas)
                    F=0
                    
                    
                    	 
                    nac=len(nameas)
                    
                    countraz=0
                    cvf=2
                    cvf1=0
                    s=""
                    
                 
                    size_data3=""
                    size_data2=""

                    sscvf=0
                    
                    qqqqwzl=0

                    block=1

                    x=0
                    x1=0
                    x2=0
                    x = time()

                    with open(nameas, "w") as f4:
                            f4.write(s)
                    with open(nameas, "a") as f3:
                            f3.write(s)
                    with open(name, "rb") as binary_file:

                       # Read the whole file at once
                        data = binary_file.read()
                        
                
                        size_after2=len(data)
                        #print(size_after2)  
                        
                        if len(data)==0 or len(data)>2**40:
                            x4=0.0
                            print(x4)
                            raise SystemExit
                            
                      
                         

                  
                        s=str(data)
                        
                        
                        lenf1=len(data)
                          
                    
                            
  
                            
                        lenf5=len(data)
                        
                        assx=0
                        qqqwz=0
                       
                        while assx<10:
                       
                            aas1=0
                            a1=0

                            cvf=cvf+1
                            
                            countraz=countraz+1

                            with open(nameas, "ab") as f2:
                                if countraz==1:
                                    size_data=bin(int(binascii.hexlify(data),16))[2:]
                                    lenf=len(size_data)
                                    lenf1=len(data)
                                
                                    xc=(lenf1*8)-lenf
                                    z=0
                                    if xc!=0:
                                        while z<xc:
                                            size_data="0"+size_data
                                            z=z+1
                                            
                                   

                                    if countraz==1:
                                        size_data2=size_data
                            
                                    n = int(size_data2, 2)
                                
                                    qqwslenf=len(size_data2)
                                    qqwslenf=(qqwslenf/8)*2
                                    qqwslenf=str(qqwslenf)
                                    qqwslenf="%0"+qqwslenf+"x"
                             
                                    jl=binascii.unhexlify(qqwslenf % n)
                                    sssssw=len(jl)
                                    
                                    data=jl
                                    qqqwz=qqqwz+1
                                   
                                    if countraz==1:

                                        lenf5=len(data)

                                    size_data=bin(int(binascii.hexlify(data),16))[2:]
                                    lenf=len(size_data)

                                    lenf1=len(data)
                                
                                    xc=(lenf1*8)-lenf
                                    z=0
                                    if xc!=0:
                                        while z<xc:
                                            size_data="0"+size_data
                                            z=z+1

                                    size_data2=size_data

                                    lenf3=len(size_data2)
                                lenf2=len(size_data2)

                                
                                    
                                
                                size_data3=size_data2

                                import getpass
                                
                                password=getpass.getpass()
                                

                            # Python3 program for the above approach
                             
                            # Function to convert Decimal to Hex
                                def convertToHex(num):
                                 
                                    temp = ""
                                    while (num != 0):
                                        rem = num % 16
                                        c = 0
                                         
                                        if (rem < 10):
                                            c = rem + 48
                                        else:
                                            c = rem + 87
                                             
                                        temp += chr(c)
                                        num = num // 16
                                 
                                    return temp
                                 
                                # Function to encrypt the string
                                def encryptString(S, N):
                                 
                                    ans = ""
                                    i = 0
                                 
                                    # Iterate the characters
                                    # of the string
                                    while (i<N): #changed from for i in range(N)
                                        ch = S[i]
                                        count = 0
                                 
                                        # Iterate until S[i] is equal to ch
                                        while (i < N and S[i] == ch):
                                 
                                            # Update count and i
                                            count += 1
                                            i += 1
                                 
                                        # Decrement i by 1
                                        #i -= 1 # not required
                                 
                                        # Convert count to hexadecimal
                                        # representation
                                        hex = convertToHex(count)
                                 
                                        # Append the character
                                        ans += ch
                                 
                                        # Append the characters frequency
                                        # in hexadecimal representation
                                        ans += hex
                                 
                                    # Reverse the obtained answer
                                    ans = ans[::-1]
                                     
                                    # Return required answer
                                    return ans
                                 
                                # Driver Code
                                if __name__ == '__main__':
                                     
                                    # Given Input
                                    S = password
                                    N = len(S)
                                 
                                    # Function Call
                                    s=encryptString(S, N)
                                
                                password=strToBinary(s)
 
# This code is contributed by mohit kumar  
                                #print(password)
                                N=int(password,2)
                                
                                long=len(password)
                                long_N=str(long)
                                
                                long_count="0"+long_N+"b"
                               
                                
                                N=format(N,long_count)
                          
                                    

                                password=N
                                
                                size_data12=password

                                size_data12="1"+size_data12
                            
                                lenf=len(size_data12)
                                        
                                add_bits118=""
                                count_bits=8-lenf%8
                                z=0
                                    
                                if count_bits!=8:
                                    while z<count_bits:
                                                    add_bits118="0"+add_bits118
                                                    z=z+1
                                                                    
                                                                    
                                size_data12=add_bits118+size_data12
                                
                                
                                    
                                size_data11=size_data12 
                                  
                                size_data11=size_data11+size_data3
             
                                                                                
                                n = int(size_data11, 2)
                                
                                qqwslenf=len(size_data11)
                                qqwslenf=(qqwslenf/8)*2
                                qqwslenf=str(qqwslenf)
                                qqwslenf="%0"+qqwslenf+"x"
                             
                                jl=binascii.unhexlify(qqwslenf % n)
                                
                                import paq
                                jl= paq.compress(jl)
                                
                                
                                    
                                size_after=len(jl)

                                size_after=len(jl)
                                
                                   
                                qqqwz=qqqwz+1
                                szxzzza=""
                                szxzs=""
                            
                                assxw=assxw+1
                                if assxw==1:
                                    assx=10
                                    if assx==10:

                                        f2.write(jl)
                                        x2 = time()
                                        x3=x2-x
                                        return print(x3)

    def password2(self):

                 def strToBinary(s):
                    bin_conv = []
                 
                    for c in s:
                         
                        # convert each char to
                        # ASCII value
                        ascii_val = ord(c)
                         
                        # Convert ASCII value to binary
                        binary_val = bin(ascii_val)
                        bin_conv.append(binary_val[2:])
                     
                        return (' '.join(bin_conv))   
                                         
                 if namez=="p2":
                    
                    name = input("What is name of file? ")
                    if os.path.exists(name):
                            print('Path is exists!')
                    else:
                            print('Path is not exists!')
                            raise SystemExit
                    Portal=2
                    namea=""
                    namem=""
                    namema="?"
                    Deep=0
                 
                    assxw=0
                    blockw=5
                    blockw1=4
                    nameas=name
                    nac=len(nameas)
                    name_cut=""
                    name_cut=len(".bin")
                    nameas=name
                    
                    name_long=len(nameas)
                    nameSS=name[name_long-name_cut:]
                    if nameSS!=".bin":
                        x3=0.0
                        return print(x3)
                        
                    nameas=name[:name_long-name_cut]
                    nac=len(nameas)
                    
                  
                    
                    long=len(nameas)

                    nac=len(nameas)
                   
                    countraz=0
                    cvf=2
                    cvf1=0
                    s=""
                    
                 
                    size_data3=""
                    size_data2=""

                    sscvf=0
                    
                    qqqqwzl=0

                    block=1

                    x=0
                    x1=0
                    x2=0
                    x = time()

                    with open(nameas, "w") as f4:
                            f4.write(s)
                    with open(nameas, "a") as f3:
                            f3.write(s)
                    with open(name, "rb") as binary_file:

                       # Read the whole file at once
                        
                        data = binary_file.read()
                        import paq
                        data= paq.decompress(data)

                        

                    
                        if len(data)==0:
                            x4=0.0
                            print(x4)
                            raise SystemExit
                     	

                        s=str(data)
                       
                        lenf1=len(data)
                        lenf5=len(data)
                        
                        assx=0
                        qqqwz=0
                       
                        while assx<10:
                       
                            aas1=0
                            a1=0

                            cvf=cvf+1
                            
                            countraz=countraz+1

                            with open(nameas, "ab") as f2:
                                if countraz==1:
                                    size_data=bin(int(binascii.hexlify(data),16))[2:]
                                    lenf=len(size_data)
                                    lenf1=len(data)
                                
                                    xc=(lenf1*8)-lenf
                                    z=0
                                    if xc!=0:
                                        while z<xc:
                                            size_data="0"+size_data
                                            z=z+1
                                            
                                   

                                    if countraz==1:
                                        size_data2=size_data
                            
                                    n = int(size_data2, 2)
                                
                                    qqwslenf=len(size_data2)
                                    qqwslenf=(qqwslenf/8)*2
                                    qqwslenf=str(qqwslenf)
                                    qqwslenf="%0"+qqwslenf+"x"
                             
                                    jl=binascii.unhexlify(qqwslenf % n)
                                    sssssw=len(jl)
                                    
                                    data=jl
                                    qqqwz=qqqwz+1
                                   
                                    if countraz==1:

                                        lenf5=len(data)

                                    size_data=bin(int(binascii.hexlify(data),16))[2:]
                                    lenf=len(size_data)

                                    lenf1=len(data)
                                
                                    xc=(lenf1*8)-lenf
                                    z=0
                                    if xc!=0:
                                        while z<xc:
                                            size_data="0"+size_data
                                            z=z+1

                                    size_data2=size_data

                                    lenf3=len(size_data2)
                                lenf2=len(size_data2)  
                                x4=1
                                if x4==1:

                                    

                                    size_data3=size_data2
                                    
                                    if size_data3[0:9]=="000000001":
                                        size_data3=size_data3[9:]
                                    elif size_data3[0:8]=="00000001":
                                        size_data3=size_data3[8:]
                                    elif size_data3[0:7]=="0000001":
                                        size_data3=size_data3[7:]
                                    elif size_data3[0:6]=="000001":
                                        size_data3=size_data3[6:]
                                    elif size_data3[0:5]=="00001":
                                        size_data3=size_data3[5:]
                                    elif size_data3[0:4]=="0001":
                                        size_data3=size_data3[4:]
                                    elif size_data3[0:3]=="001":
                                        size_data3=size_data3[3:]
                                    elif size_data3[0:2]=="01":
                                        size_data3=size_data3[2:]
                                    elif size_data3[0:1]=="1":
                                        size_data3=size_data3[1:]                                    
                                    
                                    import getpass

                                    password=getpass.getpass()
                                    
                                                
                                                                    

                                    
                                         
                                 
                                # This code is contributed by mohit kumar 
                                    
                                    # Python3 program for the above approach
                                     
                                    # Function to convert Decimal to Hex
                                    def convertToHex(num):
                                     
                                        temp = ""
                                        while (num != 0):
                                            rem = num % 16
                                            c = 0
                                             
                                            if (rem < 10):
                                                c = rem + 48
                                            else:
                                                c = rem + 87
                                                 
                                            temp += chr(c)
                                            num = num // 16
                                     
                                        return temp
                                     
                                    # Function to encrypt the string
                                    def encryptString(S, N):
                                     
                                        ans = ""
                                        i = 0
                                     
                                        # Iterate the characters
                                        # of the string
                                        while (i<N): #changed from for i in range(N)
                                            ch = S[i]
                                            count = 0
                                     
                                            # Iterate until S[i] is equal to ch
                                            while (i < N and S[i] == ch):
                                     
                                                # Update count and i
                                                count += 1
                                                i += 1
                                     
                                            # Decrement i by 1
                                            #i -= 1 # not required
                                     
                                            # Convert count to hexadecimal
                                            # representation
                                            hex = convertToHex(count)
                                     
                                            # Append the character
                                            ans += ch
                                     
                                            # Append the characters frequency
                                            # in hexadecimal representation
                                            ans += hex
                                     
                                        # Reverse the obtained answer
                                        ans = ans[::-1]
                                         
                                        # Return required answer
                                        return ans
                                     
                                    # Driver Code
                                    if __name__ == '__main__':
                                         
                                        # Given Input
                                        S = password
                                        N = len(S)
                                     
                                        # Function Call
                                        s=encryptString(S, N)                                       
                                    password=strToBinary(s)
                                    long=len(password)
                                    long_eight=long
                                    long_N=str(long)
                                    long_count="0"+long_N+"b"
                                
                                    N=int(password,2)
                                    N=format(N,long_count)

                                    password=N
                                    password1=size_data3[:long_eight] 
                                    
                                    if  password==password1:
                                        size_data3=size_data3[long_eight:]
                                        
                                        long_file=len(size_data3)
                                        divide=long_file%8
                                        if divide==0:
                                            print("Password it's right!")
                                        else:
                                            print("Password it's incorrect!")
                                            raise SystemExit
                                            
                                    else:
                                        print("Password it's incorrect!")
                                        raise SystemExit
                                        
                                    n = int(size_data3, 2)
                                    
                                    
                                    qqwslenf=len(size_data3)
                                    qqwslenf=(qqwslenf/8)*2
                                    qqwslenf=str(qqwslenf)
                                    qqwslenf="%0"+qqwslenf+"x"
                             
                                    jl=binascii.unhexlify(qqwslenf % n)
                                  
                                    sssssw=len(jl) 
                                  
                                   

                                    qqqwz=qqqwz+1
                                    szxzzza=""
                                    szxzs=""
                                    
                            
                                    assxw=assxw+1
                                    if assxw==1:
                                        assx=10
                                        if assx==10:
                                        	
                                            f2.write(jl)
                                            x2 = time()
                                            x3=x2-x
                                            return print(x3)  
                  
self=""                                
d=password_class()
    
xw=d.password1()
print(xw)

xw1=d.password2()
print(xw1)
