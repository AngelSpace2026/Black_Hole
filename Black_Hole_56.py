import os
pm = input("encrypt/decrypt")
if pm=="encrypt":
    method = input("Method compress 1,2,3,4: ")
    if method=="1":
         os.system("python Black_Hole_m1.py")
    elif method=="2":
        os.system("python Black_Hole_m2.py")
        
    elif method=="3":
        os.system("python Black_Hole_m3.py")
        
    elif method=="4":
        os.system("python Black_Hole_m4.py")
  
if pm=="decrypt":
     
    os.system("password-7.py")

