"""

TAD_to_TXT reads in TAD files of the packet 4 format and produces a txt file 

that will be used to create a FITS file 

"""

import datetime
from struct import pack
from struct import unpack


"""variables for navigating the stream"""
s1234 = b'\x8c\x8d' #start row literal, 8C8D
                    #beginning of new row data stream
s43 = b'\x31\xb1'

ltc1 = 15           #local time first  literal, F
ltc2 = 14           #local time second literal, E

r1 = 13             #row literal, D

t01 = 12            #temp sensor literal 01, C
t02 = 11            #temp sensor literal 02, B
t11 = 10            #temp sensor literal 11, A
t12 = 9             #temp sensor literal 12, 9

e1234 = b'\x8e\x8f' #end of row literal, 8E8F

FILE_PATH = input("Enter the global filename and location\nin the format 'D:/Path/to/the/thing.tad':\n")
FILE_PATH="C:\dec13_det_warm_tad_test_Card0.tad"
while (True):
    try:
        read_bytes = open(FILE_PATH, 'rb')
        break
    except FileNotFoundError:
        print("\nWATCH the direction of the slashes, Python is finicky...\n\n")
        FILE_PATH = input("Enter the global filename and location\nin the format 'D:/Path/to/the/thing.tad':\n")
    
#do nothing before the first start packet literal
trigger_start = False

now = datetime.datetime.now()

#mv_ascii_data_mm-dd-YYYY-HH-MM-SS.txt
mv_txt = open('D:/WRX-R TEST DATA (PACKET 2)/mv_ascii_data_{:%m-%d-%Y-%H-%M-%S}.txt'.format(now),'w')

## FRC Numbers
num_row    = 1024
num_column = 1024
word_counter = 0
#D:/WRX-R TEST DATA (PACKET 2)/MVE_TestBox_PSU_FakeData_Try3_2017_07_19_193859_Card0.tad

#determine whether it needs to flip its bits or not
reversed = None
while reversed not in ['0','1']:
    reversed = input("Enter 1 if the data is flipped, 0 if not: \n")

while (True):
    if reversed == '0':
        """run until we hit the end of the stream"""
        
        #4 bytes = 32 bits
        word = read_bytes.read(2)
        
        #change from bytes to hex
        word = format(unpack('>H',word)[0],'04x')
        #print(word)
        
        if word == s1234:
            trigger_start = True
        
        #keep track of 16 bit words to remove BS header
        if trigger_start:
            word_counter += 1
            #write to file here
            mv_txt.write(word+'\n')
            

        
        # if word == '6bfe':
        #     print(word_counter)
        #     input()
        #frame sync is b'\xfek(@'
        
        if word_counter == 98:
            #removes the minor frame BS and FS
            garbage = read_bytes.read(12+4)
            #reset the word counter
            word_counter = 0
        
        if word == b'':
            read_bytes.close()
            mv_txt.close()
            break
            
    elif reversed == '1':
        #in order to flip needs to read in 2 at once
        try:
            word = read_bytes.read(4)
            
            #reverse the bits of the whole thing
            word2 = word[-1::-1]
            
            #more confusing variable names
            words = ['','']
            
            #do it twice so we get it all
            for k in range(2):
                #words is now in the correct order
                words[1] = format(int(format(unpack(
                '<2H', word)[0],'016b')[-1::-1],2),'04x')
                
                words[0] = format(int(format(unpack(
                '<2H', word)[1],'016b')[-1::-1],2),'04x')
                
                #to find the start bit
                check = (int(words[k],16))>>12
                
                #start of the garbage header
                if (words==['0040', '2c98']):
                    #removes all the rest of the header
                    garbage = read_bytes.read(12)
                    
                    # jums = unpack('>6H', garbage)
                    # for i in jums:
                    #     print(format(i,'02x'))
                    # input('pause')
                    break
                
                #
                word2 = words[k]
                
                #string version of the unfucked s1234
                if word2 == '8c8d':
                    trigger_start = True
                
                if trigger_start:
                    word_counter += 1
                    #write to file here
                    mv_txt.write(word2+'\n')
        
        except struct.error:
            read_bytes.close()
            mv_txt.close()
            break