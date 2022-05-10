import csv
import sys, getopt

def main(argv):

    #Read argv for csv file locate.
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print 'SPI_decode.py -i <inputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    
    #Confirm file is name is already found.
    if inputfile == '':
        print 'SPI_decode.py -i <inputfile>'
        sys.exit(2)
        
    #Decode SPI date    
    with open(inputfile) as csvfile:
        decodeList = []
        rows = csv.reader(csvfile)
        pre = ""
        for row in rows:
            if row[1] == "=\"SDO\"" and row[2] == "=\"0B\"":
                row[4] = row[4].replace("=","")
                row[4] = row[4].replace("\"","")
                row[5] = row[5].replace("=","")
                row[5] = row[5].replace("\"","")
                region = int((row[4] + row[5]),16)
                if region >= 0 and region < 1040 and pre != "Descriptor Region":
                    pre = "Descriptor Region"
                    decodeList.append("Descriptor Region\n")
                    #print("Descriptor Region")
                elif region >= 1040 and region < 1056 and pre != "ME Region":
                    pre = "ME Region"
                    decodeList.append("ME Region\n")
                    #print("ME Region")
                elif region >= 1056 and region < 1072 and pre != "FPT":
                    pre = "FPT"
                    decodeList.append("FPT\n")
                    #print("FPT")
                elif region >= 1072 and region < 1088 and pre != "FPTB":
                    pre = "FPTB"
                    decodeList.append("FPTB\n")
                    #print("FPTB")
                elif region >= 1088 and region < 1600 and pre != "MFSB":
                    pre = "MFSB"
                    decodeList.append("MFSB\n")
                    #print("MFSB")
                elif region >= 1600 and region < 3200 and pre != "MFS":
                    pre = "MFS"
                    decodeList.append("MFS\n")
                    #print("MFS")
                elif region >= 3200 and region < 3376 and pre != "Reserved":
                    pre = "Reserved"
                    decodeList.append("Reserved\n")
                    #print("Reserved")
                elif region >= 3376 and region < 3408 and pre != "UTOK":
                    pre = "UTOK"
                    decodeList.append("UTOK\n")
                    #print("UTOK")
                elif region >= 3408 and region < 3440 and pre != "UEP":
                    pre = "UEP"
                    decodeList.append("UEP\n")
                    #print("UEP")
                elif region >= 3440 and region < 6224 and pre != "SPS Recovery":
                    pre = "SPS Recovery"
                    decodeList.append("SPS Recovery\n")
                    #print("SPS Recovery")
                elif region >= 6224 and pre != "SPS Operational":
                    pre = "SPS Operational"
                    decodeList.append("SPS Operational\n")
                    #print("SPS Operational")
        
        path = 'output.txt'
        f = open(path, 'w')
        f.writelines(decodeList)
        f.close
        print("Decoding complete.\nResult is saved in output.txt")


if __name__ == "__main__":
   main(sys.argv[1:])           
