

import os

try:
    from a import writeMissingEntries

except ImportError:
    pass


def test_missingEntries1():
    try:
        os.remove('logfile.log')
        writeMissingEntries('18P-6089,Muhammad,1,4')
        assert(os.path.isfile('logfile.log')==True)
    except:
        pass

def test_missingEntries2():
    try:
        os.remove('logfile.log')
        writeMissingEntries('18P-6089,Muhammad,1,2,4')
        assert(os.path.isfile('logfile.log')==False)
    except:
        pass

def test_missingEntries3():
    data=[
	'18P-0006,Ahmed Khan,1,8',
	'18P-0130,Ali Hassan,2,2,4',
	'18P-6061,Ikram Durrani,3,2,4',
	'18P-6089,Muhammad,14',
	'18P-6154,Syed Shahid Khaqani,1,2,3',
	'18P-6064,Hamza Arif,6.5,7,2.5',
	'18P-6065,Muhammad Ali,2,3.2,4'  
	]

    for i in range(len(data)):
        writeMissingEntries(data[i]) 
    with open('logfile.log','r') as flog:
        assert(flog.readline()=='[18P-0006,Ahmed Khan,1,8]\n')
        assert(flog.readline()=='[18P-6089,Muhammad,14]\n')

def test_missingEntries4():
    os.remove('logfile.log')
    data=[
	'18P-6089,Muhammad,14',
	'18P-0006,Ahmed Khan,1,8',
	'18P-0130,Ali Hassan,2,2,4',
	'18P-6061,Ikram Durrani,3,2,4',
	'18P-6154,Syed Shahid Khaqani,1,2,3',
	'18P-6064,Hamza Arif,6.5,7,2.5',
	'18P-6065,Muhammad Ali,2,3.2,4'  
	]

    for i in range(len(data)):
        writeMissingEntries(data[i]) 
    with open('logfile.log','r') as flog:
        assert(flog.readline()=='[18P-6089,Muhammad,14]\n')
        assert(flog.readline()=='[18P-0006,Ahmed Khan,1,8]\n')


