import os
from time import time
import binascii
import math
import os.path
import sys

# @Author Jurijus Pacalovas
# Get the name of the current script

if os.path.basename(sys.argv[0]) != "Black_Hole_Original_44.py":
    sys.exit("This is not 'Black_Hole_Original_44.py'.")

print("The script 'Black_Hole_Original_44.py' is currently running.")
print("Quantum Computer 16 millions Qubits")


class compression:
    def cryptograpy_compression4(self):

        self.name = "Created Quantum Software: Jurijus pacalovas"
        print(self.name)

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
            

            # print(i)
            if os.path.exists(name):

                print("Path is exists!")

            else:

                print("Path is not exists!")

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
            Times1 = 0
            Tc = 0
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

                            Check = INFO

                            File_information5_2 = INFO

                            Extact = File_information5_2

                        long_13 = len(File_information5_2)

                        long_12 = len(File_information5_2)

                        if i == 1:
                        	Compress_Times_1=int(input("How many times compress? "))
                        	if Compress_Times_1>=(2**256)-2:
                        		Compress_Times_1=(2**256)-2
                        	if Compress_Times_1<1:
                        		Compress_Times_1=1
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

                                long_bits_after = 0
                                long_bits_after_b = 0
                                long_bits_before = 0
                                times_compress = 0
                                long_after_bits = 0
                                long_bits_after_b_1 = 0
                                J = 1
                                long_F1 = long_F
                                long_one_time = long_F1
                                stop_compress = 0
                                while stop_compress != 1:
                                    block = 0
                                    long_after_bits = len(INFO)
                                    Transform = INFO
                                    long_F = len(I8)
                                    T10 = ""
                                    c_c = 0
                                    while block < long_F:
                                        times_c_c = 0
                                        T8 = Transform[block : block + 24]
                                        c_c = 0
                                        c_c1 = 0
                                        block += 24

                                        if len(T8) != 24:

                                            T10 += "1" + T8  # left bits

                                        elif len(T8) == 24:

                                            # Convert the binary string T8 to a decimal integer
                                            num = int(
                                                T8, 2
                                            )  # Convert binary to decimal
                                            num = num - 1
                                            if num == -1:
                                                num = (2**24) - 1
                                            num_c = num
                                            # num check
                                            # print(f"Converted binary {T8} to decimal: {num}")
                                            # Initial calculation
                                            finish = 0
                                            times = 0
                                            binary_representation_before = len(
                                                format(num, "01b")
                                            )
                                            # print("binary_representation_before_long")
                                            # print(binary_representation_before)
                                            # Main loop to calculate binary representations
                                            while finish != 1:
                                                if num > 1000000000:
                                                    print(
                                                        "This number is too big!"
                                                    )
                                                elif num < 0:
                                                    print(
                                                        "Please enter a non-negative integer."
                                                    )
                                                else:
                                                    max_length = len(
                                                        format(num, "b")
                                                    )
                                                    binary_numbers = []
                                                    # Generate binary numbers of lengths 1 to max_length
                                                    for length in range(
                                                        1, max_length + 1
                                                    ):
                                                        for i in range(
                                                            2**length
                                                        ):
                                                            binary_numbers.append(
                                                                format(
                                                                    i,
                                                                    "0"
                                                                    + str(
                                                                        length
                                                                    )
                                                                    + "b",
                                                                )
                                                            )
                                                    # Find the largest binary number less than or equal to the given number
                                                    last_binary = None
                                                    for (
                                                        index,
                                                        binary,
                                                    ) in enumerate(
                                                        binary_numbers
                                                    ):
                                                        if index > num:
                                                            break
                                                        last_binary = (
                                                            binary,
                                                            index,
                                                        )
                                                    if last_binary:
                                                        (
                                                            binary_representation,
                                                            index,
                                                        ) = last_binary
                                                        long_br1 = len(
                                                            binary_representation
                                                        )
                                                        Bi = int(
                                                            binary_representation,
                                                            2,
                                                        )
                                                        Bif = format(Bi, '01b')
                                                        Bif1 = len(Bif)
                                                        # print(len(binary_representation))
                                                        # print(f"{binary_representation}: {index}")
                                                        binary_to_number = int(
                                                            binary_representation,
                                                            2,
                                                        )
                                                        binary_representation = format(
                                                            binary_to_number,
                                                            "01b",
                                                        )
                                                        num = binary_to_number
                                                        binary_to_number_number_after = (
                                                            binary_to_number
                                                        )
                                                        # print("binary_to_number")
                                                        # print(binary_to_number)
                                                        length_tree = len(
                                                            binary_representation
                                                        )
                                                        times += 1
                                                        # print("times")
                                                        # print(times)
                                                        # print("length_tree")
                                                        # print(str(length_tree))
                                                        if length_tree < 8:
                                                            finish = 1
                                                            length_tree_after = (
                                                                length_tree
                                                            )
                                                            times_after = times
                                                            binary_representation_before_long = binary_representation_before
                                                            # Continuation: another loop to perform further calculations
                                            finish = 0
                                            finish1 = 0
                                            times = 0
                                            count_number = 0
                                            while finish1 != 1:
                                                num = count_number
                                                binary_representation_before = (
                                                    len(format(num, "01b"))
                                                )
                                                finish = 0
                                                times = 0
                                                while finish != 2:
                                                    if num < 0:
                                                        print(
                                                            "Please enter a non-negative integer."
                                                        )
                                                    else:
                                                        max_length = len(
                                                            format(num, "b")
                                                        )
                                                        binary_numbers = []
                                                        for length in range(
                                                            1, max_length + 1
                                                        ):
                                                            for i in range(
                                                                2**length
                                                            ):
                                                                binary_numbers.append(
                                                                    format(
                                                                        i,
                                                                        "0"
                                                                        + str(
                                                                            length
                                                                        )
                                                                        + "b",
                                                                    )
                                                                )
                                                        last_binary = None
                                                        for (
                                                            index,
                                                            binary,
                                                        ) in enumerate(
                                                            binary_numbers
                                                        ):
                                                            if index > num:
                                                                break
                                                            last_binary = (
                                                                binary,
                                                                index,
                                                            )
                                                        if last_binary:
                                                            (
                                                                binary_representation,
                                                                index,
                                                            ) = last_binary
                                                            long_br = len(
                                                                binary_representation
                                                            )
                                                            # print(binary_representation)
                                                            Bi3 = int(
                                                                binary_representation,
                                                                2,
                                                            )
                                                            Bif = format(
                                                                Bi3, '01b'
                                                            )
                                                            Bif2 = len(Bif)

                                                            binary_to_number = int(
                                                                binary_representation,
                                                                2,
                                                            )
                                                            binary_representation = format(
                                                                binary_to_number,
                                                                "01b",
                                                            )
                                                            num = (
                                                                binary_to_number
                                                            )
                                                            # print(num)
                                                            # print(index)
                                                            length_tree = len(
                                                                binary_representation
                                                            )
                                                            times += 1
                                                            if length_tree < 8:
                                                                count_number += (
                                                                    1
                                                                )
                                                                finish = 2
                                                            if (
                                                                length_tree < 8
                                                                and binary_representation_before
                                                                == binary_representation_before_long
                                                                and times_after
                                                                == times
                                                                and Bif1 == Bif2
                                                                and Bi == Bi3
                                                                or num>2**24
                                                            ):
                                                                finish1 = 1
                                                                
                                                                # print("binary_representation_before_long")
                                                                # print(binary_representation_before_long)
                                                                # print("times_after")
                                                                # print(binary_representation_before_long)
                                                                # print(times_after)
                                                                # print("length_tree_after")
                                                                # print(length_tree_after)
                                                                # print("binary_to_number_number_after")
                                                                # print(binary_to_number_number_after)
                                                                # print("count_number")
                                                                count_number = (
                                                                    count_number
                                                                    - 1
                                                                )
                                                                if count_number>2**24:
                                                                	IFC="1"+T8
                                                                # print(length_tree)
                                                                # print(count_number)

                                                                # print(times_after)#long after

                                                                # print(binary_representation_before_long)#long after

                                                                # print(binary_to_number_number_after)#binary represation

                                                                # print(binary_to_number_number_after),#binary represation
                                                                # print(length_tree_after)# after
                                                                #
                                                                else:
	                                                                binary_representation = format(
	                                                                    Bi3,
	                                                                    "01b",
	                                                                )
	                                                                times_after = (
	                                                                    times_after
	                                                                    - 1
	                                                                )
	                                                                # print(binary_to_number)
	                                                                binary_representation_before_long1 = format(
	                                                                    times_after,
	                                                                    "06b",
	                                                                )
	                                                                # print(binary_representation_before)
	                                                                length_tree_after = format(
	                                                                    binary_representation_before_long,
	                                                                    "05b",
	                                                                )
	
	                                                                length_tree_after1 = (
	                                                                    Bif2
	                                                                )
	                                                                length_tree_after1 = (
	                                                                    length_tree_after1
	                                                                    - 1
	                                                                )
	                                                                length_tree_after2 = format(
	                                                                    length_tree_after1,
	                                                                    "03b",
	                                                                )
	
	                                                                # print(binary_representation_before)
	
	                                                                IFC = (
	                                                                    "0"
	                                                                    + length_tree_after2
	                                                                    + binary_representation
	                                                                    + binary_representation_before_long1
	                                                                    + length_tree_after
	
	                                                                )
	
	                                                                # print(length_tree_after2)
	                                                                # print(length_tree_after)
	                                                                # print(binary_representation_before_long1)
	                                                                # print(binary_representation)
	                                                                # print(len(IFC))
	                                                                # print(count_number)
                                                                if (
                                                                    len(IFC)
                                                                    <= 23
                                                                    and num_c
                                                                    == count_number
                                                                    and len(
                                                                        length_tree_after
                                                                    )
                                                                    == 5
                                                                    and len(
                                                                        binary_representation
                                                                    )
                                                                    <= 8
                                                                    and len(
                                                                        binary_representation_before_long1
                                                                    )
                                                                    == 6
                                                                    and len(
                                                                        length_tree_after2
                                                                    )
                                                                    == 3
                                                                ):
                                                                    T10 += IFC
                                                                    # print(IFC)
                                                                else:
                                                                    
                                                                    num2 = int(
                                                                    T8, 2)
                                                                    IFC = format(
                                                                        num2,
                                                                        "024b",)
                                                                    T10 += (
                                                                        
                                                                        	"1"+IFC)         
                                              
                                                                    

                                    INFO = T10
                                    T8 = T10

                                    long_one_time = len(T10)

                                    if (
                                        long_one_time <= 256
                                        and times_compress >= 0
                                        or times_compress == Compress_Times_1
                                    ):
                                        stop_compress = 1
                                        Compress_file = 1
                                    long_bits_after_b_1 = 1
                                    times_compress += 1
                                    

                                # print(Compress_file)
                                if Compress_file == 1:
                                    Extract1 = 1
                                    if Extract1 == 1:
                                        times_compression_format = format(
                                            times_compress, "01b"
                                        )
                                        # print(times_compression_format)
                                        times_255 = format(
                                            len(times_compression_format),
                                            "08b",
                                        )
                                        times_255p = format(
                                            len(times_255),
                                            "016b",
                                        )

                                        # print(times_255_p_255)
                                        #  long of file  start number file before

                                        I_F_B = format(long_F1, "01b")
                                        # long of long before of file
                                        I_F_B_L = format(len(I_F_B), "08b")

                                        # long of file
                                        l_F_N = len(INFO)
                                        # long of  last number file after
                                        I_F_A = format(l_F_N, "01b")
                                        #  After long of long of file
                                        I_F_A_L = format(len(I_F_A), "08b")
                                        File_information5_17 = (
                                            "1"
                                            + times_255p
                                            + times_255
                                            + times_compression_format
                                            + I_F_B_L
                                            + I_F_B
                                            + I_F_A_L
                                            + I_F_A
                                            + INFO
                                        )

                                        long_1 = len(File_information5_17)
                                        add_bits = ""
                                        count_bits = (8 - long_1 % 8) % 8

                                        if count_bits > 0 and count_bits < 8:
                                            for _ in range(count_bits):
                                                add_bits = "0" + add_bits

                                    if Extract1 == 1:

                                        File_information5_17 = (
                                            add_bits + File_information5_17
                                        )
                                        L = len(File_information5_17)

                                        # print(L)

                                        n = int(File_information5_17, 2)

                                        width_bits = len(File_information5_17)

                                        width_bits = (width_bits // 8) * 2

                                        width_bits = str(width_bits)

                                        width_bits = "%0" + width_bits + "x"

                                        width_bits3 = binascii.unhexlify(
                                            width_bits % n
                                        )

                                        width_bits2 = len(width_bits3)

                                        File_information5_2 = Clear

                                        jl = width_bits3

                                        name1 = name + ".b"

                                        with open(name1, "wb") as f2:

                                            f2.write(jl)

                                        x2 = time()

                                        x3 = x2 - x

                                        print(
                                            f"Speed bits: {(long_11) / x3:.5f}"
                                        )

                                        xs = float(x3)

                                        xs = str(xs)

                                        return xs

                        if i == 2:

                            if C == 1:

                                Extract1 = 0
                                File_information5 = INFO

                                # extract

                                if Circle_times3 == 0:

                                    long_16 = len(File_information5)

                                    if File_information5[:1] == "0":

                                        while File_information5[:1] != "1":

                                            if File_information5[:1] == "0":

                                                File_information5 = (
                                                    File_information5[1:]
                                                )

                                    if File_information5[:1] == "1":

                                        File_information5 = File_information5[
                                            1:
                                        ]

                                INFO = File_information5
                                # print(INFO)

                                if Circle_times3 == 0:
                                    # times count extract

                                    CEI = int(INFO[:16], 2)

                                    # print(CE)

                                    INFO = INFO[16:]

                                    CE = int(INFO[:CEI], 2)

                                    # print(CE)

                                    INFO = INFO[CEI:]

                                    tce = int(INFO[:CE], 2)

                                    # print(tce)

                                    INFO = INFO[CE:]
                                    #############

                                    # INFO before file before size of file
                                    CE1 = int(INFO[:8], 2)

                                    # print(CE)

                                    INFO = INFO[8:]
                                    bfnz = int(INFO[:CE1], 2)

                                    # print(bfnz)

                                    INFO = INFO[CE1:]
                                    #############

                                    # INFO before file after size of file
                                    CE2 = int(INFO[:8], 2)

                                    # print(CE)

                                    INFO = INFO[8:]
                                    efnz = int(INFO[:CE2], 2)

                                    # print(efnz)

                                    INFO = INFO[CE2:]
                                    # e.g.: 12 8-10
                                    #############

                                while Extract1 != 1:
                                    # 1 bits 21
                                    # 0 19
                                    long_F = len(INFO)
                                    # print(long_F)

                                    block = 0
                                    TUPLE = ""
                                    while block < long_F:
                                        take_c_or_l = INFO[block : block + 23]
                                        long_l = len(take_c_or_l)
                                        # print(long_l)
                                        if INFO[block : block + 1] == "1":
                                            block += 1
                                            T8 = INFO[block : block + 24]
                                            TUPLE += T8
                                            block += 24

                                        elif INFO[block : block + 1] == "0":

                                            block += 1
                                            # print(take_c_or_l)

                                            # print("4")
                                            # print(len(num3))
                                            # print(num3)
                                            # binary_representation+length_tree_after+binary_representation_before_long1#

                                            # print(length_tree_after) #long after
                                            # print(times_after)#binary repreatation
                                            # print(binary_representation_before_long)#long before file
                                            # print(times_after)#long after

                                            # print(binary_representation_before_long)#long after

                                            # print(binary_to_number_number_after)#binary represation
                                            Bif1 = int(
                                                (INFO[block : block + 3]), 2
                                            )
                                            Bif1 += 1
                                            block += 3
                                            if Bif1==0:
                                            	read_b==1
                                            else:
                                                read_b=Bif1                                                                                                                             
                                                                                                                                                                               
                                            Bi3 = int(
                                                (INFO[block : block + read_b]), 2
                                            )
                                            # print(times_after)

                                            block += read_b
                                            times_after = int(
                                                (INFO[block : block + 6]), 2
                                            )
                                            times_after = times_after + 1
                                            # print(binary_representation_before_long)

                                            block += 6

                                            binary_representation_before_long = int(
                                                (INFO[block : block + 5]), 2
                                            )
                                            # print(binary_to_number_number_after)

                                            block += 5


                                            # open 3 key
                                            # binary length tree start and finish and binanary represation

                                            # print(len(num3))

                                            # Continuation: another loop to perform further calculations
                                            finish = 0
                                            finish1 = 0
                                            times = 0
                                            count_number = 0
                                            while finish1 != 1:
                                                num = count_number
                                                binary_representation_before = (
                                                    len(format(num, "01b"))
                                                )
                                                finish = 0
                                                times = 0
                                                while finish != 2:
                                                    if num < 0:
                                                        print(
                                                            "Please enter a non-negative integer."
                                                        )
                                                    else:
                                                        max_length = len(
                                                            format(num, "b")
                                                        )
                                                        binary_numbers = []
                                                        for length in range(
                                                            1, max_length + 1
                                                        ):
                                                            for i in range(
                                                                2**length
                                                            ):
                                                                binary_numbers.append(
                                                                    format(
                                                                        i,
                                                                        "0"
                                                                        + str(
                                                                            length
                                                                        )
                                                                        + "b",
                                                                    )
                                                                )
                                                        last_binary = None
                                                        for (
                                                            index,
                                                            binary,
                                                        ) in enumerate(
                                                            binary_numbers
                                                        ):
                                                            if index > num:
                                                                break
                                                            last_binary = (
                                                                binary,
                                                                index,
                                                            )
                                                        if last_binary:
                                                            (
                                                                binary_representation,
                                                                index,
                                                            ) = last_binary
                                                            long_br = len(
                                                                binary_representation
                                                            )
                                                            Bi = int(
                                                                binary_representation,
                                                                2,
                                                            )
                                                            Bif = format(
                                                                Bi, '01b'
                                                            )
                                                            Bif2 = len(Bif)
                                                            # print(long_br)
                                                            binary_to_number = int(
                                                                binary_representation,
                                                                2,
                                                            )

                                                            binary_representation = format(
                                                                binary_to_number,
                                                                "01b",
                                                            )
                                                            num = (
                                                                binary_to_number
                                                            )
                                                            length_tree = len(
                                                                binary_representation
                                                            )
                                                            times += 1
                                                            if length_tree < 8:
                                                                count_number += (
                                                                    1
                                                                )
                                                                finish = 2
                                                            if (
                                                                length_tree < 8
                                                                and binary_representation_before
                                                                == binary_representation_before_long
                                                                and times_after
                                                                == times
                                                                and Bif1 == Bif2
                                                                and Bi == Bi3
                                                            ):
                                                                finish1 = 1

                                                                # print("binary_representation_before_long")
                                                                # print(binary_representation_before_long)
                                                                # print("times_after")
                                                                # print(times_after)
                                                                # print("length_tree_after")
                                                                # print(length_tree)
                                                                # print("binary_to_number_number_after")
                                                                # print(binary_to_number_number_after)
                                                                # print(count_number)
                                                                count_number = (
                                                                    count_number
                                                                    - 1
                                                                )
                                                                count_number += (
                                                                    1
                                                                )
                                                                if (
                                                                    count_number
                                                                    == 2**24
                                                                ):
                                                                    count_number = (
                                                                        0
                                                                    )

                                                                IFC = format(
                                                                    count_number,
                                                                    "024b",
                                                                )
                                                                TUPLE += IFC

                                                                # print(block)
                                                                # print(IFC)

                                    TUPLE1 = TUPLE
                                    INFO = TUPLE
                                    # print(INFO)

                                    long_L = len(TUPLE)
                                    Tc += 1
                                    # print(Tc)

                                    if tce == Tc:
                                        Extract1 = 1

                                if Extract1 == 1:
                                    num4 = int(TUPLE1, 2)
                                    # print(num4)
                                    C19 = "0" + str(bfnz) + "b"
                                    TUPLE1 = format(num4, C19)
                                    File_information5_17 = TUPLE1

                                if Extract1 == 1:
                                    L = len(File_information5_17)
                                    n = int(File_information5_17, 2)
                                    width_bits = "%0" + str((L // 8) * 2) + "x"
                                    width_bits3 = binascii.unhexlify(
                                        width_bits % n
                                    )
                                    width_bits2 = len(width_bits3)
                                    name2 = name[:-2]
                                    start_time = time()
                                    with open(name2, "wb") as f2:
                                        f2.write(width_bits3)
                                    elapsed_time = time() - start_time
                                    speed_bits = (long_11 * 8) // float(
                                        elapsed_time
                                    )
                                    print(f"Speed bits: {speed_bits:.5f}")
                                    return str(elapsed_time)


d = compression()
xw1 = d.cryptograpy_compression4()
print(xw1)
