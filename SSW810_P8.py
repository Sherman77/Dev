"""SSW810 HomeWork Week 8
    Xiaomeng(Sherman) Xu"""

import datetime
import os
import unittest
from prettytable import PrettyTable

#Part #1-1
def date_arithmetic1(date1, num):
    dt1 = datetime.datetime.strptime(date1, '%b %d, %Y')
    dt2 = dt1 + datetime.timedelta(days = num)
    print('{} days after {} is {}'.format(num, dt1, dt2.strftime('%m/%d/%Y')))


#Part #1-2
def date_arithmetic2(date1, date2):
    dt1 = datetime.datetime.strptime(date1, '%b %d, %Y')
    dt2 = datetime.datetime.strptime(date2, '%b %d, %Y')
    delta = dt2 - dt1
    print('{} days in between {} and {}'.format(delta.days, dt1, dt2))


#Part #2
def file_reader(name, num, sep = '|', header = True):
    try:
            fp = open(name, 'r')  #Open file
    except FileNotFoundError:
        print("Can't open", name)  #Raise Error when dealing with non-existing files
    else:
        with fp:
            lines = fp.readlines()  #Read all the lines from file
            for offset, line in enumerate(lines):
                line = line.strip()  #Strip whrite spaces
                elements = line.split(sep)  #Split up lines(cwid, name, major)
                if len(elements) == num:  #Check if line has same amount of elemetns as excepted
                    if header == True:  #Skip header
                        header = False
                        continue
                    else:
                        yield tuple(elements)  #Yield emelent from line as a tuple
                else:
                    raise ValueError('{}has {} fields on line {} but except {}'.format(name, len(elements), offset, num))  #Rise exception if one has unexcepted dufferent amount of elements



#Part #3
def file_scan(path):
    pt = PrettyTable(field_names = ['file', 'calsses', 'functionns', 'characters', 'lines'])  #Get a pretty table
    result = []  #For unittest i have to retuen something
    try:
        files = os.listdir(path)
    except FileNotFoundError:
        print ("Invalid directory!")  #Error message if directory is unvalid

    else:
        if files == []:
            print ("Not Python file found!")  #End of story if no .py file was found
        
        else:
            for item in files:
                if item.endswith('.py'):  #Look for Python files
                    classes, functions, characters, lines = scan(item)  #Get classes functions characters and liunes from scan(item)

                    pt.add_row([item, classes, functions, characters, lines])  #Add to table
                    result.append([item, classes, functions, characters, lines])  #Append to result

            print (pt)

            return result  #For auto test


def scan(item):
    """Scan the file line by line"""

    classes = 0
    functions = 0 
    characters = 0
    lines = 0

    fp = open(item, 'r')  #Open file one by one
    with fp:
        for line in fp:  #Get the lines and characters BEFORE strip
            lines += 1
            characters += len(line)

            if line.strip().startswith('def '):  #Get functions
                functions += 1
            
            if line.strip().startswith('class '):  #Get classes
                classes += 1

    return classes, functions, characters, lines





#Test
class AutoTest(unittest.TestCase):

    #Test_Part #2
    def test_file_reader(self):
        """Verify that file_reader() works properly"""
        exception = [('LL ', ' 001 ', ' cs'), ('AA ', ' 002 ', ' cs'), ('BB ', ' 003 ', ' se'), ('CCCccc ', ' 004 ', ' mse'), ('asduhuiqwbdi ', ' 000005 ', ' bia')]
        self.assertEqual(list(file_reader('p8_test.txt', 3)), exception)


    #Test_Part #3
    def test_file_scan(self):
        exception = [['try.py', 0, 5, 1257, 80], ['SSW810_HW2_Xiaomeng Xu.py', 1, 13, 4786, 165], ['RPS.py', 0, 2, 662, 29], ['SSW810_HW3_Xiaomeng Xu.py', 2, 26, 11725, 329], ['0_defs_in_this_file.py', 0, 0, 57, 3], ['SSW810_HW1_Xiaomeng(Sherman) Xu_V2.py', 0, 3, 1388, 41], ['SSW540_P4_Xiaomeng Xu.py', 0, 4, 1584, 74], ['SSW810_P5_Xiaomeng Xu.py', 1, 9,4589, 207], ['RPS_2.py', 0, 3, 1254, 46], ['SSW810_P8_Xiaomeng Xu.py', 1, 7, 4481, 123], ['SSW810_HomeWork4_Xiaomeng Xu.py', 2, 23, 7882, 218], ['SSW810_P7_Xiaomeng Xu.py', 1, 10, 4103, 116], ['SSW810_P6_Xiaomeng Xu.py', 2, 10, 4216, 136], ['SSW810_HW1_Xiaomeng(Sherman) Xu.py', 0, 3, 1388, 41]]
        self.assertEqual(file_scan('/Users/sherman/Desktop/Python/810'), exception)
        







if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)


