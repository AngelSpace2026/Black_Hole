import os

import binascii
import math
import os.path
import sys
import random
import paq  # Ensure PAQ module is available

import heapq

# @Author Jurijus Pacalovas

# Get the name of the current script
print("Created by Jurijus Pacalovas.")

if os.path.basename(sys.argv[0]) != 'Black_Hole_91.py':

    sys.exit("This is not 'Black_Hole_91.py'.")

print("The script 'Black_Hole_91.py' is currently running.")

class compression:
    def cryptograpy_compression4(self):

        def process_file1(Extract1=0, File_information5_17="Ex", name="", x=0):

            if Extract1 == 1:

                with open(name + ".b", "wb") as f2:

                    f2.write(

                        binascii.unhexlify(

                            ("%0" + str((len(File_information5_17) // 8) * 2) + "x")

                            % int(File_information5_17, 2)

                        )

                    )

                    return str(time() - x)

        def process_file(Extract1=0, File_information5_17="Ex", name="", x=0):
            if Extract1 == 1:
                width_bits = (
                    "%0" + str((len(File_information5_17) // 8) * 2) + "x"
                ) % int(File_information5_17, 2)
                with open(name[:-2], "wb") as f2:
                    f2.write(binascii.unhexlify(width_bits))
                    return str(time() - x)
        def Count_adds(En, Row1, Row):
            Row += 1
            if Row == (2**28) - 1:
                Row = 0
            if En == (2**28) - 1:
                En = 255
            En+=1
            return En, Row1, Row
        import re
        def find_smallest_longl_F_values(input_string):
            # Extract all 'En', 'En2', 'Row', and 'Longl_F' values
            pattern = r'En=(\d+), Longl_F=(\d+)'
            matches = re.findall(pattern, input_string)
            # Convert the extracted strings to tuples of integers
            longl_F_values = [(int(en), int(longl_f)) for en, longl_f in matches]
            if longl_F_values:                
                # Find the smallest 'Longl_F' value and its corresponding variables
                smallest_longl_F_values = min(longl_F_values, key=lambda x: x[1])                
                return smallest_longl_F_values                
            else:
                return None
        self.name = "Written: Jurijus pacalovas"
        N5 = 1
        if N5 == 1:
            
            Clear = ""
            name = input("What is name of file input? ")
            long_21 = len(name)
            name_f = name[long_21 - 2 :]
            if name_f == ".b":
                i = 2
            else:
                i = 1
                En_number=int(input("Point(s) of the intresection(s) 2-28? "))

                if En_number<2:

                    En_number=2

                if En_number>28:

                    En_number=28

            # print(i)
            if os.path.exists(name):
                print('Path is exists!')                
            else:
                print('Path is not exists!')
                raise SystemExit
            x = 0
            C1 = 1
            x1 = 0
            x2 = 0
            x3 = 0
            X2 = 0
            C1 = 0
            C2 = 0
            C3 = 0
            C4 = 0
            ZEROS_ONE_1 = ""
            Circle_times = 0
            Circle_times2 = 1
            Circle_times3 = 0
            CB = -1
            x = time()
            File_information6_Times2_1 = 0
            name_2 = name
            Long_Change = len(name_2)
            compress_or_not_compress = 1
            File_information6_Times3 = 0
            if i == 2:
                C = 1
            Long_Change = len(name_2)
            s = ""
            File_information5 = ""
            File_information5_2 = ""
            Clear = ""
            Translate_info_Decimal = ""
            D = 0
            long_name = len(name)
            with open(name, "rb") as binary_file:
                data = binary_file.read()
                s = str(data)
                long_11 = len(data)
                long_17 = len(data)
                if long_17 == 0:
                    raise SystemExit
                END_working = 0
                File_information6_Times2 = 0
                File_information5_23 = ""
                INFO18 = ""
                File_information5_29 = ""
                SpinS = 0
                while END_working < 10:
                    File_information6_Times3 = File_information6_Times3 + 1                    
                    D = 1
                    if D == 1:
                        if File_information6_Times3 == 1:
                            INFO = bin(int(binascii.hexlify(data), 16))[
                                2:
                            ]  # data to binary
                            long_1 = len(INFO)
                            long_11 = len(data)
                            count_bits = (long_11 * 8) - long_1
                            z = 0
                            if count_bits != 0:
                                while z < count_bits:
                                    INFO = "0" + INFO

                                    z = z + 1

                            if File_information6_Times3 == 1:

                                File_information5_2 = INFO

                            n = int(File_information5_2, 2)

                            width_bits = len(File_information5_2)

                            width_bits = (width_bits / 8) * 2

                            width_bits = str(width_bits)

                            width_bits = "%0" + width_bits + "x"

                            width_bits3 = binascii.unhexlify(width_bits % n)

                            width_bits2 = len(width_bits3)

                            data = width_bits3

                            long_15 = len(data)
                            
                            INFO = bin(int(binascii.hexlify(data), 16))[2:]

                            long_1 = len(INFO)

                            long_11 = len(data)

                            count_bits = (long_11 * 8) - long_1

                            z = 0

                            if count_bits != 0:

                                while z < count_bits:

                                    INFO = "0" + INFO

                                    z = z + 1

                            Check = INFO

                            File_information5_2 = INFO

                            Extact = File_information5_2

                            A = int(Extact, 2)

                        long_13 = len(File_information5_2)

                        long_12 = len(File_information5_2)

                        if i == 1:

                            if long_17 > (2**28) - 1 and i == 1:

                                print("print file is too big!")

                                raise SystemExit

                        if i == 1:

                            Ex = 1

                            if Ex == 1:

                                Extract1 = 0

                                Find = 0

                                En = 3

                                Ci = 1

                                M1 = 0

                                Row1 = 0

                                input_string = ""

                                C1 = ""

                                Row = 0

                                I8 = INFO

                                W3 = ""

                                W4 = ""

                                block = 0

                                IF1 = ""

                                long_F = len(I8)

                                # print(long_F)

                                FC = 0

                                IF2 = ""

                                Z7 = 0

                                CZ = 0

                                if Circle_times == 0:

                                    SINFO = ""

                                    TUPLE = INFO

                                if Circle_times == 0:

                                    SINFO = INFO

                                if I8[long_F-8]!="00000000":

                                    I8+="00000000"

                                else:

                                	I8+="11111111"

                                while block < long_F+8:
                                    IF = I8[block : block + 8]

                                    if FC == 0:

                                        IF1 = I8[block + 8 : block + 16]
                                    W4 += IF

                                    block += 8

                                    if IF1 == IF:

                                        FC += 1

                                        if FC == 1:



                                            W = block - 8



                                    if IF1 != IF:



                                        if FC < 3:



                                            FC = 0



                                        if Z7 == 0:



                                            if FC >= 3:



                                                Z7 = 1



                                                CZ = 1



                                                W1 = block - 16



                                                Sw1 = format(W//8, '01b')



                                                Sw3 = format(len(Sw1), '05b')



                                                # print(FC)



                                                Sw2 = format(FC, '01b')



                                                Sw4 = format(len(Sw2), '05b')



                                                W3 += "0" + IF1 + Sw3 + Sw1 + Sw4 + Sw2



                                                W4 = W4[:W] + W4[W1:]



                                                FC = 0



                                if CZ == 0:



                                    W5 = W3 + "1"



                                elif CZ == 1:



                                    W5 = W3



                                W4 = W5 + W4



                                INFO = W4

                                long_F = len(INFO)

                                INFO=INFO[:long_F-8]



                                # print(len(INFO))



                                while Find != 1:



                                    # print(Find)



                                    TUPLE = ""



                                    N3 = 0



                                    long_F = len(INFO)



                                    block = 0



                                    FC = 0



                                    IF1 = ""



                                    while block < long_F:



                                        INFO_A = INFO[block : block + En]



                                        longl = len(INFO_A)



                                        Counts = int(INFO_A, 2)



                                        C = format(Counts, '01b')



                                        C3 = En - len(C)



                                        # print(C1)



                                        if (C3 >= 6 and En <= (2 ** (C3 - 4) - 1)) or INFO_A[:3] in {"011", "010"}:

    

                                            # print(C3)



                                            Counts = int(INFO_A, 2)



                                            C = format(Counts, '01b')



                                            C4 = En - len(C)



                                            bit_width = math.ceil(math.log2(En + 1))



                                            C1 = format(C4, f'0{bit_width}b')



                                            C2 = format(longl, '06b')



                                            if C3 != 1:



                                                Z5 = "011" + C1 + C



                                                # print(Z5)



                                            if C3 == 1:



                                                Z5 = "010" + INFO_A[2:]



                                                # print(Z5)



                                                # print(INFO_A)



                                            # print(C1)



                                            # print(INFO_A)



                                        else:



                                            Z5 = INFO_A



                                            # not six Zeros_onesros else 7 Zeros_onesros or more left or 2-5 Zeros_onesros



                                        # change back



                                        # same siZeros_ones



                                        TUPLE += Z5



                                        # print(Find)



                                        block += En



                                    if Find == 2 or Row == (2**En_number) - 2:



                                        Find = 1



                                        Extract1 = 1



                                    elif Row == (2**En_number) - 3 and Find == 3:



                                        smallest_longl_F_values = (

                                            find_smallest_longl_F_values(input_string)

                                        )



                                        if smallest_longl_F_values:



                                            en, longl_F = smallest_longl_F_values



                                            En = int(en)



                                            Find = 2



                                    elif (

                                        len(TUPLE) +  len(C1) < long_11 * 8

                                        and len(C1) != 0

                                    ):



                                        input_string += (

                                            "En="

                                            + str(En)

                                            + ", "

                                            + "Longl_F="

                                            + str(len(TUPLE))

                                            + " / "

                                        )



                                        if len(input_string) > 100:



                                            smallest_longl_F_values = (

                                                find_smallest_longl_F_values(

                                                    input_string

                                                )

                                            )



                                            if smallest_longl_F_values:



                                                en, longl_F = smallest_longl_F_values



                                                input_string = (

                                                    "En="

                                                    + str(en)

                                                    + ", "

                                                    + "Longl_F="

                                                    + str(longl_F)

                                                    + " / "

                                                )



                                                # print(input_string)



                                        Find = 3



                                        En, Row1, Row = Count_adds(En, Row1, Row)



                                        # print(En)



                                        # print(len(TUPLE))



                                    else:

                                            En, Row1, Row = Count_adds(En, Row1, Row)



                                if Ci == 1:



                                    N3 = 1



                                    W = "0" + str(len(C1)) + "b"



                                    CL1 = format(longl, W)



                                    CL2 = format(En, '01b')
                                    
                                    CL3=format(len(CL2), '05b')



                                    # print(N3)



                                    if N3 == 1:



                                        # print(Long_PM1)



                                        N3 = 1



                                        Circle_times += 1



                                        # print(Circle_times)



                                        # print(len(TUPLE))



                                        # print(long_11)



                                        INFO = CL3+CL2 + CL1 + TUPLE



                                        if Circle_times == 1:



                                            Circle_times2 = Circle_times



                                            long_11 = long_11 * 8



                                        Extract1 = 0



                                        if len(TUPLE) <= long_11 or Circle_times == (2**24)-1:



                                            long_11 = len(TUPLE)



                                            INFOS = INFO



                                            Circle_times2 = Circle_times



                                        if (

                                            len(TUPLE) > long_11

                                            or Circle_times > Circle_times2 + 1

                                            or Circle_times == (2**24)-1

                                        ):



                                            N3 = 2



                                            Extract1 = 1



                                        if N3 == 2:



                                            SCircle_times = format(Circle_times2, '01b')
                                            SCircle_times_cut = format(len(SCircle_times), '05b')



                                            if Circle_times == 1:



                                                File_information5_17 = (

                                                    "1" + SCircle_times_cut+SCircle_times + INFO

                                                )



                                            if Circle_times != 1:



                                                File_information5_17 = (

                                                    "1" + SCircle_times_cut+SCircle_times + INFOS

                                                )



                                            N4 = 2



                                            if N4 == 2:



                                                long_1 = len(File_information5_17)



                                                add_bits = ""



                                                count_bits = 8 - long_1 % 8



                                                z = 0



                                                if count_bits != 0:



                                                    while z < count_bits:



                                                        add_bits = "0" + add_bits



                                                        z = z + 1



                                                File_information5_17 = (

                                                    add_bits + File_information5_17

                                                )



                                                N4 = 3



                                                if N4 == 3:



                                                    File_information5 = (

                                                        File_information5_17

                                                    )



                                                    Check2 = File_information5_17



                                                    N5 == 1



                                                    if N5 == 1:



                                                        Ex = "00000000" + Check



                                                        File_information5_17 = Ex



                                                        elapsed_time = process_file1(

                                                            Extract1=1,

                                                            File_information5_17=File_information5_17,

                                                            name=name,

                                                            x=x,

                                                        )



                                                    Circle_times3 = 0



                                                    Extract1 = 0



                                                    Circle_times = 0



                                                    if Circle_times3 == 0:



                                                        long_16 = len(File_information5)



                                                        if File_information5[:1] == "0":



                                                            while (

                                                                File_information5[:1]

                                                                != "1"

                                                            ):



                                                                if (

                                                                    File_information5[

                                                                        :1

                                                                    ]

                                                                    == "0"

                                                                ):



                                                                    File_information5 = File_information5[

                                                                        1:

                                                                    ]



                                                        if File_information5[:1] == "1":



                                                            File_information5 = (

                                                                File_information5[1:]

                                                            )



                                                    INFO = File_information5



                                                    if Circle_times3 == 0:



                                                        Circle_times4_1 = int(INFO[:5], 2)



                                                        # print(Circle_times4)



                                                        INFO = INFO[5:]
                                                        Circle_times4 = int(INFO[:Circle_times4_1], 2)



                                                        # print(longl)



                                                        INFO = INFO[Circle_times4_1:]                                                        
                                                        



                                                    while Extract1 != 1:



                                                        En_c = int(INFO[:5], 2)
                                                        INFO = INFO[5:]
                                                        En = int(INFO[:En_c], 2)



                                                        # print(longl)



                                                        INFO = INFO[En_c:]



                                                        En2 = 0



                                                        for i in range(3, 29):



                                                            if En <= (2**i) - 1:



                                                                longl = int(INFO[:i], 2)



                                                                INFO = INFO[i:]



                                                                SEN = i



                                                                break



                                                        Extract1 = 0



                                                        TUPLE = ""



                                                        N3 = 0



                                                        long_F = len(INFO)



                                                        block = 0



                                                        Save = 0



                                                        while block < len(INFO):



                                                            C9 = 0



                                                            C10 = 0



                                                            Block_Check_Add = block



                                                            O = INFO[block : block + 3]



                                                            if O == "010":



                                                                block += 3



                                                                OC = INFO[

                                                                    block : block

                                                                    + En

                                                                    - 2

                                                                ]



                                                                C10 = 1



                                                                C9 = 1



                                                                if len(OC) == 0:



                                                                    File_information5_17 = (

                                                                        "00000000"

                                                                        + Check

                                                                    )



                                                                    Ex = Check



                                                                    elapsed_time = process_file1(

                                                                        Extract1=1,

                                                                        File_information5_17=File_information5_17,

                                                                        name=name,

                                                                        x=x,

                                                                    )



                                                                    return elapsed_time



                                                                E = int(OC, 2)



                                                                Row1 = (

                                                                    "0"

                                                                    + str(En - 2)

                                                                    + "b"

                                                                )



                                                                ZEROS_ONES = format(

                                                                    E, Row1

                                                                )



                                                                if len(ZEROS_ONES) == 0:



                                                                    File_information5_17 = (

                                                                        "00000000"

                                                                        + Check

                                                                    )



                                                                    Ex = Check



                                                                    elapsed_time = process_file1(

                                                                        Extract1=1,

                                                                        File_information5_17=File_information5_17,

                                                                        name=name,

                                                                        x=x,

                                                                    )



                                                                    return elapsed_time



                                                                ZEROS_ONES = (

                                                                    "01" + ZEROS_ONES

                                                                )



                                                                ZEROS_ONE_1 = (

                                                                    "01" + ZEROS_ONE_1

                                                                )



                                                                block += En - 2



                                                            elif O == "011":



                                                                block += 3



                                                                C10 = 1



                                                                if En <= (2**28) - 1:



                                                                    OCl = INFO[

                                                                        block : block

                                                                        + SEN

                                                                    ]



                                                                    SiZeros_ones = int(

                                                                        OCl, 2

                                                                    )



                                                                    block += SEN



                                                                EB = INFO[

                                                                    block : block

                                                                    + (

                                                                        En

                                                                        - SiZeros_ones

                                                                    )

                                                                ]



                                                                S = len(EB)



                                                                block += (

                                                                    En - SiZeros_ones

                                                                )



                                                                Row1 = (

                                                                    "0" + str(En) + "b"

                                                                )



                                                                if S > 0:



                                                                    E = int(EB, 2)



                                                                else:



                                                                    E = 0



                                                                ZEROS_ONES = format(

                                                                    E, Row1

                                                                )



                                                                C = (

                                                                    "0"

                                                                    + str(longl)

                                                                    + "b"

                                                                )



                                                                ZEROS_ONES = format(

                                                                    E, Row1

                                                                )



                                                                ZEROS_ONE_1 = format(

                                                                    E, C

                                                                )
                                                                block+=En



                                                            else:



                                                                EB = INFO[

                                                                    block : block + En

                                                                ]



                                                                C10 = 1



                                                                block += En



                                                                Row1 = (

                                                                    "0" + str(En) + "b"

                                                                )



                                                                E = int(EB, 2)



                                                                ZEROS_ONES = format(

                                                                    E, Row1

                                                                )



                                                                C = (

                                                                    "0"

                                                                    + str(longl)

                                                                    + "b"

                                                                )



                                                                ZEROS_ONES = format(

                                                                    E, Row1

                                                                )



                                                                ZEROS_ONE_1 = format(

                                                                    E, C

                                                                )



                                                            Z2 = ZEROS_ONES



                                                            # print(Z2)



                                                            TUPLE += Z2



                                                            # print(block)



                                                            # print(long_F)



                                                            if block >= long_F:



                                                                Save = 1



                                                                # print(Save)



                                                        # print(TUPLE)



                                                        long_L = len(TUPLE)



                                                        # print(long_L)



                                                        if (

                                                            C9 == 0

                                                            and (long_L - En) >= 0

                                                        ):



                                                            TUPLE = TUPLE[: long_L - En]



                                                            TUPLE += ZEROS_ONE_1



                                                        elif (

                                                            C9 == 1

                                                            and (long_L - (En-2))>= 0

                                                        ):



                                                            TUPLE = TUPLE[

                                                                : long_L - (En-2)

                                                            ]



                                                            TUPLE += ZEROS_ONE_1



                                                        N3 = 1



                                                        # print(N3)



                                                        if N3 == 1:



                                                            N3 = 1



                                                            block = 0



                                                            long_F = len(TUPLE)



                                                            Z = TUPLE



                                                            Z6 = ""



                                                            Z7 = 0



                                                            TUPLE1 = Z



                                                            cut_b = 0



                                                            long_F = len(TUPLE)



                                                            # print(len(TUPLE))



                                                            if N3 == 1:



                                                                E = Z[block : block + 1]



                                                                if E == "0":



                                                                    cut_b = 1



                                                                    CB += 1



                                                                    block += 1



                                                                    E2 = Z[

                                                                        block : block

                                                                        + 8

                                                                    ]



                                                                    block += 8



                                                                    E3 = int(

                                                                        Z[

                                                                            block : block

                                                                            + 5

                                                                        ],

                                                                        2,

                                                                    )



                                                                    block += 5



                                                                    S5 = Z[

                                                                        block : block

                                                                        + E3

                                                                    ]



                                                                    if len(S5) == 0:



                                                                        File_information5_17 = (

                                                                            "00000000"

                                                                            + Check

                                                                        )



                                                                        Ex = Check



                                                                        elapsed_time = process_file1(

                                                                            Extract1=1,

                                                                            File_information5_17=File_information5_17,

                                                                            name=name,

                                                                            x=x,

                                                                        )



                                                                        return (

                                                                            elapsed_time

                                                                        )



                                                                    E1 = int(

                                                                        Z[

                                                                            block : block

                                                                            + E3

                                                                        ],

                                                                        2,

                                                                    )



                                                                    block += E3



                                                                    TUPLE4 = int(

                                                                        Z[

                                                                            block : block

                                                                            + 5

                                                                        ],

                                                                        2,

                                                                    )



                                                                    block += 5



                                                                    E5 = int(

                                                                        Z[

                                                                            block : block

                                                                            + TUPLE4

                                                                        ],

                                                                        2,

                                                                    )



                                                                    block += TUPLE4



                                                                    b = 0



                                                                    E3 = ""



                                                                    while b < E5 - 1:



                                                                        E3 += E2



                                                                        b += 1



                                                                        # print(E2)



                                                                    TUPLE1 = TUPLE1[

                                                                        block:

                                                                    ]

                                                                    E1*=8



                                                                    TUPLE1 = (

                                                                        TUPLE1[:E1]

                                                                        + E3

                                                                        + TUPLE1[E1:]

                                                                    )



                                                                    block += long_F



                                                                elif E == "1":



                                                                    block += 1



                                                                    Z7 = 1



                                                                    if cut_b == 0:



                                                                        TUPLE1 = TUPLE1[

                                                                            block:

                                                                        ]



                                                                        block += long_F



                                                                        cut_b = 1



                                                                        # print(CB)



                                                                        # print(block)



                                                                else:



                                                                    block += 1



                                                            # print(Long_PM1)



                                                            TUPLE = TUPLE1



                                                            # print(len(TUPLE))



                                                            N3 = 1



                                                            Circle_times += 1



                                                            # print(Circle_times)



                                                            INFO = TUPLE



                                                            Extract1 = 0



                                                            N3 = 0



                                                            # print(len(TUPLE))



                                                            # print(Circle_times4)



                                                            if (

                                                                Circle_times

                                                                == Circle_times4

                                                            ):



                                                                Extract1 = 1



                                                                if Check == TUPLE:

                                                                    File_information5_17 = Check2

                                                                    if Check2[:8]=="00000000":

                                                                    	File_information5_17=Check2[8:]

                                                        		



                                                                if Check != TUPLE:



                                                                    Ex = (

                                                                        "00000000"

                                                                        + Check

                                                                    )



                                                                    File_information5_17 = (

                                                                        Ex

                                                                    )



                                                                    elapsed_time = process_file1(

                                                                        Extract1=1,

                                                                        File_information5_17=File_information5_17,

                                                                        name=name,

                                                                        x=x,

                                                                    )



                                                                    return elapsed_time



                                if Extract1 == 1:



                                    L = len(File_information5_17)



                                    # print(L)



                                    n = int(File_information5_17, 2)



                                    width_bits = len(File_information5_17)



                                    width_bits = (width_bits // 8) * 2



                                    width_bits = str(width_bits)



                                    width_bits = "%0" + width_bits + "x"



                                    width_bits3 = binascii.unhexlify(width_bits % n)



                                    width_bits2 = len(width_bits3)



                                    File_information5_2 = Clear



                                    jl = width_bits3



                                    name1 = name + ".b"



                                    with open(name1, "wb") as f2:



                                        f2.write(jl)



                                    x2 = time()



                                    x3 = x2 - x



                                    print(f"Speed bits: {(long_11) / x3:.5f}")



                                    print("checker seccesufully.")           




                        if i == 2:



                            if C == 1:



                                Extract1 = 0



                                if File_information6_Times2 == 0:



                                    File_information5 = INFO



                                    Extract = 0



                                    Ex = INFO



                                    if Ex[:8] == "00000000":



                                        L = len(Ex[8:])



                                        File_information5_17 = Ex[8:]



                                        n = int(File_information5_17, 2)



                                        width_bits = len(File_information5_17)



                                        width_bits = (width_bits // 8) * 2



                                        width_bits = str(width_bits)



                                        width_bits = "%0" + width_bits + "x"



                                        width_bits3 = binascii.unhexlify(width_bits % n)



                                        width_bits2 = len(width_bits3)



                                        File_information5_2 = Clear



                                        jl = width_bits3



                                        long = len(name)



                                        name2 = name[: long - 2]



                                        with open(name2, "wb") as f2:



                                            f2.write(width_bits3)






          



                                       



                                    if Circle_times3 == 0:



                                        long_16 = len(File_information5)



                                        if File_information5[:1] == "0":



                                            while File_information5[:1] != "1":



                                                if File_information5[:1] == "0":



                                                    File_information5 = (

                                                        File_information5[1:]

                                                    )



                                        if File_information5[:1] == "1":



                                            File_information5 = File_information5[1:]



                                    INFO = File_information5



                                    if Circle_times3 == 0:



                                                        Circle_times4_1 = int(INFO[:5], 2)



                                                        # print(Circle_times4)



                                                        INFO = INFO[5:]
                                                        Circle_times4 = int(INFO[:Circle_times4_1], 2)



                                                        # print(longl)



                                                        INFO = INFO[Circle_times4_1:]   



                                    while Extract1 != 1:


                                        En_c = int(INFO[:5], 2)
                                        INFO = INFO[5:]
                                        En = int(INFO[:En_c], 2)



                                                        # print(longl)



                                        INFO = INFO[En_c:]



                                        En2 = 0



                                        for i in range(3, 29):



                                            if En <= (2**i) - 1:



                                                longl = int(INFO[:i], 2)



                                                INFO = INFO[i:]



                                                SEN = i



                                                break



                                        Extract1 = 0



                                        TUPLE = ""



                                        N3 = 0



                                        long_F = len(INFO)



                                        block = 0



                                        Save = 0



                                        while block < len(INFO):



                                            C9 = 0



                                            O = INFO[block : block + 3]



                                            if O == "010":



                                                block += 3



                                                OC = INFO[block : block + En - 2]



                                                if len(OC) == 0:



                                                    File_information5_17 = Ex



                                                    elapsed_time = process_file(

                                                        Extract1=1,

                                                        File_information5_17=File_information5_17,

                                                        name=name,

                                                        x=x,

                                                    )



                                                    return elapsed_time



                                                E = int(OC, 2)



                                                Row1 = "0" + str(En - 2) + "b"



                                                C9 = 1



                                                ZEROS_ONES = format(E, Row1)



                                                if len(ZEROS_ONES) == 0:



                                                    File_information5_17 = Ex



                                                    elapsed_time = process_file(

                                                        Extract1=1,

                                                        File_information5_17=File_information5_17,

                                                        name=name,

                                                        x=x,

                                                    )



                                                    return elapsed_time



                                                C = "0" + str(longl - 2) + "b"



                                                ZEROS_ONES = format(E, Row1)



                                                if len(ZEROS_ONES) == 0:



                                                    Extract1 = 0



                                                    File_information5_17 = Ex



                                                    elapsed_time = process_file(

                                                        Extract1=1,

                                                        File_information5_17=File_information5_17,

                                                        name=name,

                                                        x=x,

                                                    )



                                                    return elapsed_time



                                                ZEROS_ONES = "01" + ZEROS_ONES



                                                ZEROS_ONE_1 = "01" + ZEROS_ONE_1



                                                block += En - 2



                                            elif O == "011":



                                                block += 3



                                                if En <= (2**28) - 1:



                                                    OCl = INFO[block : block + SEN]



                                                    SiZeros_ones = int(OCl, 2)



                                                    block += SEN



                                                EB = INFO[

                                                    block : block + (En - SiZeros_ones)

                                                ]

                                                S = len(EB)

                                                block += En - SiZeros_ones

                                                Row1 = "0" + str(En) + "b"
                                                if S > 0:

                                                    E = int(EB, 2)
                                                    
                                                else:

                                                    E = 0

                                                ZEROS_ONES = format(E, Row1)

                                                C = "0" + str(longl) + "b"

                                                ZEROS_ONES = format(E, Row1)

                                                ZEROS_ONE_1 = format(E, C)
                                                block+=En

                                            else:

                                                EB = INFO[block : block + En]

                                                block += En

                                                Row1 = "0" + str(En) + "b"

                                                E = int(EB, 2)


                                                ZEROS_ONES = format(E, Row1)

                                                C = "0" + str(longl) + "b"

                                                ZEROS_ONES = format(E, Row1)

                                                ZEROS_ONE_1 = format(E, C)

                                            Z2 = ZEROS_ONES

                                            # print(Z2)

                                            TUPLE += Z2

                                            # print(block)

                                            # print(long_F)

                                            if block >= long_F:
                                                
                                                Save = 1

                                                # print(Save)

                                        # print(TUPLE)

                                        long_L = len(TUPLE)

                                        # print(long_L)

                                        if C9 == 0 and (long_L - En) >= 0:

                                            TUPLE = TUPLE[: long_L - En]

                                            TUPLE += ZEROS_ONE_1

                                        elif C9 == 1 and (long_L - (En-2)) >= 0:

                                            TUPLE = TUPLE[: long_L-(En-2)]

                                            TUPLE += ZEROS_ONE_1

                                        N3 = 1

                                        # print(N3)

                                        if N3 == 1:

                                            N3 = 1

                                            block = 0

                                            long_F = len(TUPLE)

                                            Z = TUPLE

                                            Z6 = ""

                                            Z7 = 0

                                            TUPLE1 = Z

                                            cut_b = 0

                                            long_F = len(TUPLE)
                                            
                                            while block < long_F:

                                                E = Z[block : block + 1]

                                                if E == "0" and Z7 == 0:

                                                    cut_b = 1

                                                    block += 1

                                                    E2 = Z[block : block + 8]

                                                    block += 8

                                                    E3 = int(Z[block : block + 5], 2)

                                                    block += 5

                                                    S5 = Z[block : block + E3]

                                                    if len(S5) == 0:

                                                        Extract1 = 0
                                                        File_information5_17 = Ex



                                                        elapsed_time = process_file(

                                                            Extract1=1,

                                                            File_information5_17=File_information5_17,

                                                            name=name,

                                                            x=x,

                                                        )



                                                        return elapsed_time

                                                    E1 = int(Z[block : block + E3], 2)

                                                    block += E3

                                                    TUPLE4 = int(

                                                        Z[block : block + 5], 2

                                                    )

                                                    block += 5

                                                    E5 = int(

                                                        Z[block : block + TUPLE4], 2

                                                    )

                                                    block += TUPLE4
                                                    
                                                    b = 0

                                                    E3 = ""

                                                    while b < E5 - 1:

                                                        E3 += E2

                                                        b += 1

                                                        # print(E2)

                                                    TUPLE1 = TUPLE1[block:]

                                                    E1*=8

                                                    TUPLE1 = (

                                                        TUPLE1[:E1] + E3 + TUPLE1[E1:]
                                                    )
                                                    
                                                    block += long_F
                                                    
                                                elif E == "1" or Z7 == 1:

                                                    block += 1

                                                    Z7 = 1

                                                    if cut_b == 0:

                                                        TUPLE1 = TUPLE1[block:]

                                                        cut_b = 1

                                                        block += long_F

                                                        # print(block)
                                                # print(block)

                                            # print(Long_PM1)

                                            TUPLE = TUPLE1
                                            # print(len(TUPLE))

                                            N3 = 1

                                            Circle_times += 1

                                            # print(Circle_times)

                                            INFO = TUPLE
                                            Extract1 = 0
                                            N3 = 0
                                            # print(len(TUPLE))
                                            # print(Circle_times4)
                                            if Circle_times == Circle_times4:
                                                Extract1 = 1
                                                N3 = 2
                                            if N3 == 2:
                                                File_information5_17 = TUPLE

                                                long_1 = len(File_information5_17)
                                                add_bits = ""
                                                count_bits = 8 - long_1 % 8
                                                z = 0
                                                if count_bits != 0:
                                                    while z < count_bits:
                                                        add_bits = "0" + add_bits

                                                        z = z + 1

                                                File_information5_17 = (
                                                    File_information5_17

                                                )

                                                if Extract1 == 1:

                                                    L = len(File_information5_17)

                                                    n = int(File_information5_17, 2)

                                                    width_bits = len(

                                                        File_information5_17

                                                    )

                                                    width_bits = (width_bits // 8) * 2

                                                    width_bits = str(width_bits)
                                                    width_bits = "%0" + width_bits + "x"
                                                    width_bits3 = binascii.unhexlify(
                                                        width_bits % n

                                                    )
                                                    width_bits2 = len(width_bits3)

                                                    File_information5_2 = Clear
                                                    jl = width_bits3

                                                    long = len(name)

                                                    name2 = name[: long - 2]
                                                    with open(name2, "wb") as f2:
                                                        f2.write(width_bits3)
                                                    
                                                    


                                                    
                                                    print("checker secefully."
                                                    )
  
                                                    


                                    

                                    # [Rest of the decompression logic would follow here]

    # Strategy 9 compression methods
    def reverse_chunks(self, data, chunk_size, positions):
        """Reverses specified chunks of byte data."""
        reversed_data = bytearray(data)
        for pos in positions:
            start = pos * chunk_size
            end = min((pos + 1) * chunk_size, len(data))
            reversed_data[start:end] = reversed_data[start:end][::-1]
        return bytes(reversed_data)

    def apply_random_bytes(self, data, num_bytes):
        """Adds random bytes to the data."""
        return data + bytearray(random.getrandbits(8) for _ in range(num_bytes))

    def compress_strategy_3(self, data):
        """Subtracts 1 from each byte in the data."""
        return bytearray([x - 1 if x > 0 else 0 for x in data])

    def function_move(self, data, direction, num_bits):
        """Moves bits left or right in the data."""
        bit_string = ''.join(f'{byte:08b}' for byte in data)
        if direction == 'left':
            bit_string = bit_string[num_bits:] + bit_string[:num_bits]
        else:
            bit_string = bit_string[-num_bits:] + bit_string[:-num_bits]
        return bytearray(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))

    def apply_run_length_encoding(self, data):
        """Simple run-length encoding (RLE) for repeated sequences."""
        compressed_data = bytearray()
        i = 0
        while i < len(data):
            count = 1
            while i + 1 < len(data) and data[i] == data[i + 1]:
                i += 1
                count += 1
            compressed_data.append(data[i])
            compressed_data.append(count)
            i += 1
        return bytes(compressed_data)

    def compress_data(self, data):
        """Compresses data using PAQ with byte modifications."""
        compressed_data = paq.compress(data)
        last_byte = compressed_data[-1]
        extra_byte = bytes([random.randint(0, 255)])
        compressed_data += extra_byte
        modified_last_byte = bytes([last_byte ^ 0xFF])
        compressed_data = compressed_data[:-1] + modified_last_byte
        return compressed_data, last_byte

    def decompress_data(self, compressed_data, last_byte):
        """Decompresses PAQ data with byte restoration."""
        compressed_data = compressed_data[:-1]
        modified_last_byte = compressed_data[-1]
        compressed_data = compressed_data[:-1] + bytes([modified_last_byte ^ 0xFF])
        return paq.decompress(compressed_data)

    def strategy_7(self, data, last_byte_from_file):
        """Compresses zero sequences and adds original last byte."""
        bit_string = ''.join(f'{byte:08b}' for byte in data)
        compressed_data = bit_string.replace('0', '')
        compressed_data = bytearray(int(compressed_data[i:i + 8], 2) for i in range(0, len(compressed_data), 8))
        compressed_data.append(last_byte_from_file)
        return bytes(compressed_data)

    def strategy_8(self, data):
        """Compress repeated 4-byte sequences."""
        i = 0
        compressed_data = bytearray()
        while i < len(data):
            count = 1
            while i + 1 < len(data) and data[i:i+4] == data[i+1:i+5]:
                i += 4
                count += 1
            if count > 1:
                compressed_data.append(count)
                compressed_data.extend(data[i:i+4])
            else:
                compressed_data.append(data[i])
            i += 1
        return bytes(compressed_data)

    def find_best_strategy(self, data):
        """Tests all strategies to find the best compression."""
        strategies = [
            lambda d: self.reverse_chunks(d, random.randint(1, 256), 
                           sorted(random.sample(range(len(d) // random.randint(1, 256)), 
                                 random.randint(0, len(d) // random.randint(1, 256))))),
            lambda d: self.apply_random_bytes(d, random.randint(1, 100)),
            self.compress_strategy_3,
            lambda d: self.function_move(d, 'left' if random.random() > 0.5 else 'right', random.randint(1, 7)),
            self.apply_run_length_encoding,
            lambda d: self.strategy_7(d, d[-1]),
            self.strategy_8
        ]
        
        best_compressed_data = None
        best_compression_ratio = float('inf')
        
        for strategy in strategies:
            try:
                transformed_data = strategy(data)
                compressed_data = paq.compress(transformed_data)
                compression_ratio = len(compressed_data) / len(data)
                if compression_ratio < best_compression_ratio:
                    best_compression_ratio = compression_ratio
                    best_compressed_data = compressed_data
            except Exception as e:
                print(f"Strategy failed: {e}")
                continue
                
        return best_compressed_data, best_compression_ratio

    def process_large_file(self, input_filename, output_filename, mode, attempts=1, iterations=100):
        """Handles large files in chunks for compression/decompression."""
        if not os.path.exists(input_filename):
            raise FileNotFoundError(f"Input file '{input_filename}' not found.")
        
        with open(input_filename, 'rb') as infile:
            file_data = infile.read()

        if mode == "compress":
            best_data = None
            best_ratio = float('inf')
            
            for _ in range(attempts):
                compressed_data, ratio = self.find_best_strategy(file_data)
                if ratio < best_ratio:
                    best_ratio = ratio
                    best_data = compressed_data
            
            with open(output_filename, 'wb') as outfile:
                outfile.write(best_data)
            print(f"Compression complete. Output saved to: {output_filename}")
            
        elif mode == "decompress":
            with open(input_filename, 'rb') as infile:
                compressed_data = infile.read()
            
            try:
                restored_data = paq.decompress(compressed_data)
                with open(output_filename, 'wb') as outfile:
                    outfile.write(restored_data)
                print(f"Decompression complete. Restored file: {output_filename}")
            except Exception as e:
                print(f"Error during decompression: {e}")

import os
import binascii
import math
import random
import heapq
import paq

class Node:
    def __init__(self, left=None, right=None, symbol=None):
        self.left = left
        self.right = right
        self.symbol = symbol

    def is_leaf(self):
        return self.left is None and self.right is None

class SmartCompressor:
    def __init__(self):
        self.max_intersections = 28

    def binary_to_file(self, binary_data, filename):
        try:
            n = int(binary_data, 2)
            num_bytes = (len(binary_data) + 7) // 8
            hex_str = "%0*x" % (num_bytes * 2, n)
            if len(hex_str) % 2 != 0:
                hex_str = '0' + hex_str
            byte_data = binascii.unhexlify(hex_str)
            with open(filename, 'wb') as f:
                f.write(byte_data)
            return True
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            return False

    def file_to_binary(self, filename):
        try:
            with open(filename, 'rb') as f:
                data = f.read()
                if not data:
                    print("Error: Empty file")
                    return None
                binary_str = bin(int(binascii.hexlify(data), 16))[2:]
                return binary_str.zfill(len(data) * 8)
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return None

    def calculate_frequencies(self, binary_str):
        frequencies = {}
        for bit in binary_str:
            if bit in frequencies:
                frequencies[bit] += 1
            else:
                frequencies[bit] = 1
        return frequencies

    def build_huffman_tree(self, frequencies):
        heap = [(freq, symbol) for symbol, freq in frequencies.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            freq1, symbol1 = heapq.heappop(heap)
            freq2, symbol2 = heapq.heappop(heap)
            heapq.heappush(heap, (freq1 + freq2, Node(symbol1, symbol2)))
        return heap[0][1]

    def generate_huffman_codes(self, root, current_code="", codes={}):
        if isinstance(root, Node) and root.left is None and root.right is None:
            codes[root.symbol] = current_code
            return codes
        if isinstance(root, Node):
            self.generate_huffman_codes(root.left, current_code + "0", codes)
            self.generate_huffman_codes(root.right, current_code + "1", codes)
        return codes

    def compress_data_huffman(self, binary_str):
        frequencies = self.calculate_frequencies(binary_str)
        huffman_tree = self.build_huffman_tree(frequencies)
        huffman_codes = self.generate_huffman_codes(huffman_tree)
        if '0' not in huffman_codes:
            huffman_codes['0'] = '0'
        if '1' not in huffman_codes:
            huffman_codes['1'] = '1'
        compressed_str = ''.join(huffman_codes[bit] for bit in binary_str)
        return compressed_str

    def decompress_data_huffman(self, compressed_str):
        frequencies = self.calculate_frequencies(compressed_str)
        huffman_tree = self.build_huffman_tree(frequencies)
        huffman_codes = self.generate_huffman_codes(huffman_tree)
        reversed_codes = {code: symbol for symbol, code in huffman_codes.items()}
        decompressed_str = ""
        current_code = ""
        for bit in compressed_str:
            current_code += bit
            if current_code in reversed_codes:
                symbol = reversed_codes[current_code]
                decompressed_str += symbol
                current_code = ""
        return decompressed_str

    def compress_data_zlib(self, data_bytes):
        compressed_data = paq.compress(data_bytes)
        return compressed_data

    def decompress_data_zlib(self, compressed_data):
        try:
            decompressed_data = paq.decompress(compressed_data)
            return decompressed_data
        except zlib.error:
            return None

    def compress(self, filename):
        if not os.path.exists(filename):
            print("Error: File not found")
            return
        print(f"Compressing {filename}...")
        with open(filename, 'rb') as f:
            data_bytes = f.read()
        if len(data_bytes) < 1024:  # Simple heuristic: Use Huffman for small files
            compressed_data = self.compress_data_huffman(self.file_to_binary(filename))
            output_file = filename + '.bin'  # Changed extension
            self.binary_to_file(compressed_data, output_file)
        else:
            compressed_data = self.compress_data_zlib(data_bytes)
            output_file = filename + '.bin'  # Changed extension
            with open(output_file, 'wb') as f:
                f.write(compressed_data)
        orig_size = os.path.getsize(filename)
        comp_size = os.path.getsize(output_file)
        ratio = (comp_size / orig_size) * 100
        print(f"\nCompression complete!")
        print(f"Original: {orig_size} bytes")
        print(f"Compressed: {comp_size} bytes")
        print(f"Ratio: {ratio:.2f}%")
        print(f"Saved as: {output_file}")

    def decompress(self, filename):
        if not os.path.exists(filename):
            print("Error: File not found")
            return
        print(f"Decompressing {filename}...")
        try:
            with open(filename, 'rb') as f:
                compressed_data = f.read()
            #Try zlib first (more likely for larger files)
            decompressed_data = self.decompress_data_zlib(compressed_data)
            if decompressed_data:
                output_file = filename[:-4] #Remove .bin
                with open(output_file, 'wb') as f:
                    f.write(decompressed_data)
                print("Decompressed using Black_Hole_91.")
            else:
                #Try huffman if zlib fails
                compressed_binary = self.file_to_binary(filename)
                if compressed_binary:
                    decompressed_data = self.decompress_data_huffman(compressed_binary)
                    if decompressed_data:
                        output_file = filename[:-4] #Remove .bin
                        self.binary_to_file(decompressed_data, output_file)
                        print("Decompressed using Huffman.")
                    else:
                        print("Error: Decompression failed (both zlib and Huffman).")
                else:
                    print("Error: Decompression failed (both zlib and Huffman).")
        except Exception as e:
            print(f"An error occurred during decompression: {e}")

        comp_size = os.path.getsize(filename)
        try:
            decomp_size = os.path.getsize(output_file)
            print(f"\nDecompression complete!")
            print(f"Compressed: {comp_size} bytes")
            print(f"Decompressed: {decomp_size} bytes")
            print(f"Saved as: {output_file}")
        except NameError:
            print("Decompression failed. No file created.")



def main():
    compressor = SmartCompressor()
    while True:
        print("\nSmart Compression System")
        print("1. Compress File")
        print("2. Decompress File")
        print("3. Exit")
        choice = input("Select option (1-3): ").strip()
        if choice == '1':
            filename = input("Enter file to compress: ").strip()
            if filename: #Check if filename is not empty
                compressor.compress(filename)
        elif choice == '2':
            filename = input("Enter file to decompress: ").strip()
            if filename: #Check if filename is not empty
                compressor.decompress(filename)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again")

if __name__ == "__main__":
    main()