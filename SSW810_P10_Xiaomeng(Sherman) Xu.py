"""SSW810 HomeWork 9
    Xiaomeng(Sherman) Xu"""


from prettytable import PrettyTable
import os
from SSW810_P8 import file_reader
from collections import defaultdict
import unittest

class University:
    """This is the Repository class for storing all the information that came from same University"""
    
    def __init__(self, path_dir):
        """Attributes for this class"""
        self._student = dict()
        self._instructor = dict()
        self._grade = list()
        self._major = dict()
        

    
    def read_student(self, path):
        """Read student from file, get their cwid, name and major, and creat a new instence of Student class"""
        try:
            for cwid, name, major in file_reader(path, 3, sep='\t', header = False):
                if cwid in self._student:
                    print(f'Student{cwid} already in file!')  #Catch duplicate instence of student
                else:
                    self._student[cwid] = Student(cwid, name, major)
        except ValueError as err:  
            raise ValueError(err)   #Raise a exception when encountering a bad data


    def read_instructor(self, path):
        """Read instuctor form file, get their cwid, name and department, and creat a new instence"""
        try:
            for cwid, name, department in file_reader(path, 3, sep='\t', header = False):
                if cwid in self._instructor:
                    print(f'Instructor{cwid} already in file!') #Catch duplicated instence of instructor
                else:
                    self._instructor[cwid] = Instructor(cwid, name, department)
        except ValueError as err:
            raise ValueError(err)   #Raise a exception when encountering a bad data


    def read_major(self, path):
        """Read major file, create new instance for every major, add required courses and elective courses into instance"""
        for major, flag, course in file_reader(path, 3, sep='\t', header = False):
            if major in self._major:    #If this major already have an instance
                if flag == 'R':
                    self._major[major].add_required(course) #Add required courses into instance
                elif flag == 'E':
                    self._major[major].add_elective(course) #Add elective courses into instance
            
            else:
                self._major[major] = Major(major)   #If this major does not have an intance yet, create a new instance first
                if flag == 'R':
                    self._major[major].add_required(course) #Add required courses into instance
                elif flag == 'E':
                    self._major[major].add_elective(course) #Add elective courses into instance

    
    def match_major(self):
        """Match up students with their majors"""
        for cwid in self._student.keys():   #Iterate through all instance of Student
            if self._student[cwid]._major in self._major.keys():    #Catch bad vakues if one student's major is not in Major class
                for major in self._major.keys():    #Iterate through all instance of Major
                    if self._student[cwid]._major == major: #Match each student with his/her major
                        self._student[cwid].add_majorlist(self._major[major]._required, self._major[major]._elective)   #Add required course and elective course into instance of student

            else:
                raise ValueError("Major was not matched with Student's record") #Raise exception if one student's major is not in Major class
            



    def read_grade(self, path):
        """Read grade file, get student's cwid, course name, grade, insturctor's cwid, and create a new instence"""
        try:
            for scwid, course, grade, icwid in file_reader(path, 4, sep='\t', header = False):
                if scwid in self._student:
                    self._student[scwid].add_course(course, grade)  #Add courses and grade into instence of student
                else:
                    print(f'This student{scwid} is not in file!')
                
                if icwid in self._instructor:
                    self._instructor[icwid].add_course(course)  #Add course and how many students into instence of instructor
                else:
                    print(f'This instructoe{icwid} is not in file!')
        except ValueError as err:
            raise ValueError(err)  #Raise a exception when encountering a bad data


    def student_pt(self):
        """Add information into PrettyTable for student class"""
        pt = PrettyTable(field_names = Student.pt_labels)   #Get filed names
        for student in self._student.values():  
            pt.add_row(student.pt_row())    #Add stuff into PrettyTable

        print('Student Summary\n')
        print (pt,'\n')


    def instructor_pt(self):
        """Add information into PrettyTable for instructor class"""
        pt = PrettyTable(field_names = Instructor.pt_labels)    #Get filed names
        for instructor in self._instructor.values():
            for i in list(instructor.pt_row()):
                pt.add_row(i)   #Add stuff into PrettyTable

        print("Instructors Summary\n")
        print(pt,'\n')





class Student:
    """Class of Students from same Unioversity"""
    pt_labels = ['CWID', 'NAME', 'MAJOR', 'COMPLETED COURSES', 'REMAINING REQUIRED', 'REMAINING ELECTIVE']    #Filed names

    def __init__(self, cwid, name, major):
        """Attributes for instences of Student"""
        self._cwid = cwid
        self._name = name
        self._major = major
        self._course_took = dict()
        self._major_list = dict()
        self._major_required = list()
        self._major_elective = list()
        self._course_completed = list()
        self._remaning_required = list()
        self._remaning_elective = list()

    def add_course(self, course, grade):
        """Add course  and grades into this instence of Student"""
        self._course_took[course] = grade
        self._course_completed = [i for i in self._course_took if self._course_took[i] in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']]  #Only courses with a grade better than 'C' will be determined as completed
        self._remaning_required = [i for i in self._major_required if i not in self._course_completed]  #Courses are required but not yet completed
        self._remaning_elective = 'None' if len(set(self._course_completed) & set(self._major_elective)) > 0 else self._major_elective  #Shows 'None' if at least one elective course has been taken, otherwise, shows list of elective courses



    def add_majorlist(self, required, elective):
        """Add major courses list into instance of Student"""
        self._major_required = required     #Add required courses based on major
        self._major_elective = elective     #Add elective courses based on major

        


    def pt_row(self):
        """Provide information to be added into PrettyTable for Student instences"""
        return self._cwid, self._name, self._major, self._course_completed,  self._remaning_required, self._remaning_elective

    def __str__(self):
        """Convert to strings for Autotest"""
        return f"Student: {self._cwid}, Name: {self._name}, Major: {self._major}, Completed Course: {sorted(self._course_completed)}, Remaining Required Courses: {sorted(self._remaning_required)}, Remaining Elective Courses: {sorted(self._remaning_elective)}"
        #Gotta fouced them into a aorted list! Otherwise it will failed in AutoTest, took me an hour to figure this out!



    

class Instructor:
    """Class of Instructors from same University"""

    pt_labels = ['CWID', 'NAME', 'DEPARTMENT', 'COURSE', 'STUDENTS']    #Filed names

    def __init__(self, cwid, name, department):
        """Attributes for instences of Instructor"""
        self._cwid = cwid
        self._name = name
        self._department = department
        self._course = defaultdict(int)

    def add_course(self, course):
        """Add course amd how many students in that course into instence of Instructor"""
        self._course[course] += 1

    def get_course(self):
        """Yield courses and how many students for instence of Instructor"""
        for key in self._course.keys():
            yield key, self._course[key]    #Generator since one instructor might have move than one course

    def pt_row(self):
        """Provide information that to be added into PrettyTable for instence of Instructor"""
        for key in self._course.keys():
            yield self._cwid, self._name, self._department, key, self._course[key]

    def __str__(self):
        """Convert into strings for AutoTest"""
        return f"Instructor: {self._cwid}, Name: {self._name}, Department: {self._department}, {self._course}"
        


class Grade:
    """Class for all students, instructors, grades associated with all courses"""
    def __init__(self, scwid, course, grade, icwid):
        """Attributes for Grade class"""
        self._scwid = scwid
        self._course = course
        self._grade = grade
        self._icwid = icwid


class Major:
    """Calss for all majors and its required courses and elective courses"""
    def __init__(self, major):
        self._major = major
        self._required = set()  #Using set to avoid dulicate course names
        self._elective = set()  #Using set to avoid dulicate course names

    def add_required(self, course):
        """Read from file add course as required when flag == 'R' """
        self._required.add(course)
    
    def add_elective(self, course):
        """Read from file add course as elective when flag == 'E' """
        self._elective.add(course)

    def __str__(self):
        return f"{self._required}, {self._elective}"



def main():
    path_dir = input('Please enter the directory')  #Get path_dir from user
    Stevens = University(path_dir)  #Create a instence of University for Stevens
    try:
        Stevens.read_student(os.path.join(path_dir, 'students.txt'))
    except ValueError as err:
        print(err)  #Catch exception when dealing with bad data
    else:
        try:
            Stevens.read_instructor(os.path.join(path_dir, 'instructors.txt'))
        except ValueError as err:
            print(err)  #Catch exception when dealing with bad data
        else:
            try:
                Stevens.read_major(os.path.join(path_dir, 'majors.txt'))
            except ValueError as err:
                print(err)
            else:
                try:
                    Stevens.match_major()
                except ValueError as err:
                    print(err)
                else:
                    try:
                        Stevens.read_grade(os.path.join(path_dir, 'grades.txt'))
                    except ValueError as err:
                        print(err)  #Catch exception when dealing with bad data
                        
                    else:
                        Stevens.student_pt()
                        Stevens.instructor_pt()
                        #print(Stevens._instructor['98765'])
                        print(Stevens._student['11714'])
                        #print(Stevens._major['SFEN'])
                        #print(Stevens._major['SYEN'])





class AuotoTest(unittest.TestCase):
    
    def test_Stevens(self):
        path_dir = '/Users/sherman/Desktop/Python/810'
        Stevens = University(path_dir)
        Stevens.read_student(os.path.join(path_dir, 'students.txt'))
        Stevens.read_instructor(os.path.join(path_dir, 'instructors.txt'))
        Stevens.read_major(os.path.join(path_dir, 'majors.txt'))
        Stevens.match_major()
        Stevens.read_grade(os.path.join(path_dir, 'grades.txt'))


        except1 = "Student: 11714, Name: Morton, A, Major: SYEN, Completed Course: ['SYS 611', 'SYS 645'], Remaining Required Courses: ['SYS 612', 'SYS 671', 'SYS 800'], Remaining Elective Courses: ['SSW 540', 'SSW 565', 'SSW 810']"
        except2 = "Instructor: 98765, Name: Einstein, A, Department: SFEN, defaultdict(<class 'int'>, {'SSW 567': 4, 'SSW 540': 3})"

        self.assertEqual(str(Stevens._student['11714']), except1)
        self.assertEqual(str(Stevens._instructor['98765']), except2)
        





if __name__ == '__main__':
    main()
    unittest.main(exit = False, verbosity=2)
