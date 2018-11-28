"""SSW810 HomeWork Week 12
    Version 1
    Xiaomeng(Sherman) Xu"""


from flask import Flask, render_template, request
import sqlite3
DB_FILE = '/Users/sherman/Desktop/Python/810/810HW11'   #Global constant


app = Flask(__name__)

@app.route('/')
def hello():
    """Create a welcoming page"""
    return "Welcome to SSW810 Homework Week 12!\n Please type in '/instructor_courses' to view more information"    #Welcoming page

@app.route('/instructor_courses')
def show_instructorZ_courses():
    """Create a page that provides the summary of students by course and instructor"""

    query = """select instructors.CWID, instructors.Name, instructors.Dept, grades.Course, count(*) as 'Students'
            from grades join instructors on grades.Instructor_CWID = instructors.CWID group by Course order by count(*) DESC""" #Sqlite commend

    db = sqlite3.connect(DB_FILE)   #Connecting to database file
    results = db.execute(query) #Get results

    rows = [{'cwid' : cwid, 'name' : name, 'department' : department, 'course': course, 'students': students} for cwid, name, department, course, students in results]  #convert information we need into JSON format
    db.close()  #Close database file

    return render_template('show_instructor_course2.html',
                                title = "Stevens Institute of Technology",
                                table_title = "Number of students by course and instructor",
                                rows = rows)    #Pass information to Jinja format


app.run(debug = False)