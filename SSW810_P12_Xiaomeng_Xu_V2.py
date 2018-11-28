"""SSW810 HomeWork Week 12
    Version 2
    Xiaomeng(Sherman) Xu"""


from flask import Flask, render_template, request
import sqlite3
DB_FILE = '/Users/sherman/Desktop/Python/810/810HW11'


app = Flask(__name__)

@app.route('/')
def hello():
    return "Welcome to SSW810 Homework Week 12!"

@app.route('/choose_instructor')
def choose_instructor():
    query = ("select cwid, name from instructors group by cwid, name")
    
    db = sqlite3.connect(DB_FILE)
    results = db.execute(query)

    instructors = [{'cwid' : cwid, 'name' : name} for cwid, name in results]
    db.close()

    return render_template('instructors.html', instructors = instructors)


@app.route('/show_instructor', methods = ['POST'])
def show_instructors():
    if request.method == 'POST':
        cwid = request.form['cwid']

        query = f"select grades.Course, count(*) as 'Students' from grades join instructors on grades.Instructor_CWID = instructors.CWID where instructors.cwid = {cwid} group by Course order by count(*) DESC"
        table_title = f"Courses/Students for CWID {cwid}"

        db = sqlite3.connect(DB_FILE)
        results = db.execute(query)

        rows = [{'course': course, 'students': students} for course, students in results]
        db.close()

        return render_template('show_instructor_course.html',
                                title = f"{cwid}",
                                table_title = table_title,
                                rows = rows)





    
app.run(debug = True)