import csv
import sys, getopt


def main(argv):
      
    #Read argv for csv file locate.
    inputfile = ''
    mapfile = ''
    
    try:
        opts, args = getopt.getopt(argv,"hi:m:",["ifile=","map="]) 
    except getopt.GetoptError:
        print 'SPI_decode.py -i <inputfile> -m <mapfile>'
        sys.exit(2)   
    for opt, arg in opts:
    
        #Help
        if opt == '-h':
            print 'SPI_decode.py -i <inputfile> -m <mapfile>'
            sys.exit()
            
        #Input file
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            
        #Map file
        elif opt in ("-m", "--ifile"):
            mapfile = arg
    
    #Confirm file is already found.
    if inputfile == '':
        print 'SPI_decode.py -i <inputfile> -m <mapfile>'
        sys.exit(2)
    
    #Confirm map is already found.
    if mapfile == '':
        print 'SPI_decode.py -i <inputfile> -m <mapfile>'
        sys.exit(2)
    
    #Read Intel BIOS build map
    path = mapfile
    StartRead = 0
    MEMap = []
    with open(path) as f:
        for line in f.readlines():
        
            #Split data in the map
            s = line.split('     ')
            
            #Remove space in the map
            for i in s:
                if '' in s:
                    s.remove('')
            
            #Start read from Descriptor Region
            if s[0] == "00000000" and s[1] == "  00000FFF":
                StartRead = 1
                s[3] = s[3].lstrip()
                s[3] = s[3].replace("\n","")
                MEMap.append([s[3],s[0]])
            
            #Do not read reiong that it is in the Descriptor Region
            if StartRead == 1 and s[1] > "  00000FFF":
                s[3] = s[3].lstrip()
                s[3] = s[3].replace("\n","")
                MEMap.append([s[3],s[0]])
    
    #Decode SPI date    
    with open(inputfile) as csvfile:
    
        #Start search from last region
        MEMap.reverse()  
        
        #Init variable
        decodeList = []
        PreDisplayRegion = ""

        #Read LA csv data
        rows = csv.reader(csvfile)
      
        for row in rows:

            #SPI Read data command is "0B"
            if row[1] == "=\"SDO\"" and row[2] == "=\"0B\"":
            
                #Remove not use character
                row[3] = row[3].replace("=","")
                row[3] = row[3].replace("\"","")
                row[4] = row[4].replace("=","")
                row[4] = row[4].replace("\"","")
                row[5] = row[5].replace("=","")
                row[5] = row[5].replace("\"","")
                row[6] = row[6].replace("=","")
                row[6] = row[6].replace("\"","")
                
                #Convert region number to decimal
                region = int((row[3] + row[4] + row[5] + row[6]),16)
                
                #Search the region wtih the map
                for i in MEMap:
                
                    #Convert map address to decimal
                    RegionNum = int(i[1],16)  
                    RegionName = i[0]     
                    
                    #Scan region from the map
                    if region >= RegionNum:
                    
                        #Break if region is same as previous region.
                        if RegionName != PreDisplayRegion:
                            PreDisplayRegion = RegionName
                            decodeList.append(RegionName + "\n")
                            print(RegionName)
                            break
                        else:
                            break                   
                        
        
    #Save result to tge file
    path = 'output.txt'
    f = open(path, 'w')
    f.writelines(decodeList)
    f.close
    print("\n\nDecoding complete.\nResult is saved in output.txt")    

if __name__ == "__main__":
   main(sys.argv[1:])           
