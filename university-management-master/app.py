from flask import Flask, render_template, g, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuration for MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vruthika@1234'
app.config['MYSQL_DB'] = 'university'

def get_db_connection():
    if 'db_connection' not in g:
        try:
            g.db_connection = mysql.connector.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                database=app.config['MYSQL_DB']
            )
        except Error as e:
            print(f"Error: {e}")
            g.db_connection = None
    return g.db_connection

@app.teardown_appcontext
def close_db_connection(exception):
    db_connection = g.pop('db_connection', None)
    if db_connection is not None:
        db_connection.close()
        
        
@app.route('/<department>')
def department_page(department):
    return render_template(f'{department}.html', department=department)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<department>/students')
def students_page(department):
    depat = department.upper() + ' ENGINEERING'
    app.logger.info(f"Department: {depat}")
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT dept_id FROM dept WHERE dept_name = %s", (depat,))
        dept_result = cursor.fetchone()
        
        if dept_result:
            dept_id = dept_result['dept_id']
            cursor.execute("SELECT * FROM student WHERE dept_id = %s", (dept_id,))
            students = cursor.fetchall()  # Fetch all rows
            cursor.close()  # Close cursor after fetching all rows
            return render_template('students.html', students=students)
        else:
            cursor.close()
            app.logger.error("Department not found")
            return jsonify({"error": "Department not found"}), 404
    else:
        app.logger.error("Error connecting to the database")
        return jsonify({"error": "Error connecting to the database"}), 500
    

@app.route('/<department>/faculty')
def faculty_page(department):
    depat = department.upper() + ' ENGINEERING'
    app.logger.info(f"Department: {depat}")
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT dept_id FROM dept WHERE dept_name = %s", (depat,))
        dept_result = cursor.fetchone()
        
        if dept_result:
            dept_id = dept_result['dept_id']
            cursor.execute("SELECT * FROM faculty WHERE dept_id = %s", (dept_id,))
            faculty = cursor.fetchall()  # Fetch all rows
            cursor.close()  # Close cursor after fetching all rows
            return render_template('faculty.html', facultys=faculty)
        else:
            cursor.close()
            app.logger.error("Department not found")
            return jsonify({"error": "Department not found"}), 404
    else:
        app.logger.error("Error connecting to the database")
        return jsonify({"error": "Error connecting to the database"}), 500

if __name__ == '__main__':
    app.run(debug=True)
