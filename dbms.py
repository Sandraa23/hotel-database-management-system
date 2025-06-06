from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
from datetime import datetime, date

app = Flask(__name__, template_folder='temp2')

# Connect to MySQL Database
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345',
        database='dbproj'
    )
    return conn

@app.route('/')
def index():
    return render_template('finall.html', login_required=True)

@app.route('/login', methods=['POST'])
def login():
    employee_name = request.form.get('employee_name')
    password = request.form.get('password')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT E_Name FROM Employee WHERE E_Name = %s", (employee_name,))
    employee = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if employee and password == '1234':
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid employee name or password'})

@app.route('/submit', methods=['POST'])
def submit():
    cust_name = request.form.get('cust_name')
    check_in_date = request.form.get('check_in_date')
    check_out_date = request.form.get('check_out_date')
    room_no = request.form.get('room_no')
    no_in_party = request.form.get('no_in_party')
    gender = request.form.get('gender')
    aadhar_no = request.form.get('aadhar_no')
    phone_no = request.form.get('phone_no')
    email_id = request.form.get('email_id')
    meals = request.form.get('meals')
    table_no = request.form.get('table_no')

    E_name = request.form.get('E_name')
    designation = request.form.get('designation')
    department = request.form.get('department')
    date_of_joining = request.form.get('date_of_joining')

    conn = get_db_connection()
    cursor = conn.cursor()

   

    if cust_name and room_no:
        
        cursor.execute("SELECT 1 FROM rooms WHERE Room_no = %s", (room_no,))
        room_exists = cursor.fetchone()
        if not room_exists:
            cursor.close()
            conn.close()
            return f"<script>alert('Room number {room_no} does not exist. Please select a valid room.'); window.history.back();</script>"




        if check_in_date and check_out_date:
            check_in_date_obj = datetime.strptime(check_in_date, '%Y-%m-%d')
            check_out_date_obj = datetime.strptime(check_out_date, '%Y-%m-%d')
            stay_duration = (check_out_date_obj - check_in_date_obj).days

            cursor.execute("SELECT cost_per_night, room_type FROM rooms WHERE Room_no = %s", (room_no,))
            room_data = cursor.fetchone()

            if room_data:
                cost_per_night, room_type = room_data
                total_amt = cost_per_night * stay_duration

                cursor.execute("""
                    INSERT INTO customers (cust_name, check_in_date, check_out_date, room_no, no_in_party, gender, aadhar_no, phone_no, email_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (cust_name, check_in_date, check_out_date, room_no, no_in_party, gender, aadhar_no, phone_no, email_id))
                conn.commit()

                cursor.execute("SELECT LAST_INSERT_ID()")
                cust_id = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO bookings (cust_id, room_no, cust_name, room_type, check_in_date, check_out_date, total_amt)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (cust_id, room_no, cust_name, room_type, check_in_date, check_out_date, total_amt))
                conn.commit()

                if meals and table_no:
                    cursor.execute("""
                        INSERT INTO restaurant (Cust_ID, Cust_Name, room_no, Table_no, No_in_Party, Meals)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (cust_id, cust_name, room_no, table_no, no_in_party, meals))
                    conn.commit()

  
  
    if E_name and designation and department and date_of_joining:
        cursor.execute("""
            INSERT INTO Employee (E_Name, Designation, Department, Date_of_joining)
            VALUES (%s, %s, %s, %s)
        """, (E_name, designation, department, date_of_joining))
        conn.commit()

        cursor.execute("""
            UPDATE departments
            SET no_of_workers = no_of_workers + 1
            WHERE department_name = %s
        """, (department,))
        conn.commit()

    cursor.close()
    conn.close()

    return redirect('/')


@app.route('/update_emp', methods=['POST'])
def update_emp():
    emp_id = request.form['id']
    name = request.form.get('name')
    designation = request.form.get('designation')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Employee SET E_Name=%s, Designation=%s WHERE emp_id=%s", (name, designation, emp_id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')


@app.route('/get_customer/<int:cust_id>', methods=['GET'])
def get_customer(cust_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, r.Meals, r.Table_no
        FROM customers c
        LEFT JOIN restaurant r ON c.cust_id = r.Cust_ID
        WHERE c.cust_id = %s
    """, (cust_id,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    if customer:
        return jsonify(customer)
    return jsonify({'error': 'Customer not found'}), 404


@app.route('/get_employee/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Employee WHERE emp_id = %s", (emp_id,))
    employee = cursor.fetchone()
    cursor.close()
    conn.close()
    if employee:
        return jsonify(employee)
    return jsonify({'error': 'Employee not found'}), 404


@app.route('/update_cust', methods=['POST'])
def update_cust():
    cust_id = request.form['cust_id']
    fields = {
        'cust_name': request.form.get('cust_name'),
        'check_in_date': request.form.get('check_in_date'),
        'check_out_date': request.form.get('check_out_date'),
        'room_no': request.form.get('room_no'),
        'no_in_party': request.form.get('no_in_party'),
        'gender': request.form.get('gender'),
        'aadhar_no': request.form.get('aadhar_no'),
        'phone_no': request.form.get('phone_no'),
        'email_id': request.form.get('email_id'),
        'meals': request.form.get('meals'),
        'table_no': request.form.get('table_no')
    }

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        update_fields = []
        update_values = []
        for field, value in fields.items():
            if field in ['meals', 'table_no']:
                continue  
            if value and value.strip():
                if field in ['check_in_date', 'check_out_date']:
                    try:
                        datetime.strptime(value, '%Y-%m-%d')
                    except ValueError:
                        return jsonify({'error': f'Invalid date format for {field}'}), 400
                update_fields.append(f"{field}=%s")
                update_values.append(value)

        if not update_fields:
            return jsonify({'error': 'No valid fields provided for update'}), 400

        update_values.append(cust_id)
        query = f"UPDATE customers SET {', '.join(update_fields)} WHERE cust_id=%s"
        cursor.execute(query, update_values)

       
        update_bookings = False
        booking_fields = ['room_no', 'check_in_date', 'check_out_date', 'cust_name']
        provided_booking_fields = {k: v for k, v in fields.items() if k in booking_fields and v and v.strip()}
        
        if provided_booking_fields:
            
            cursor.execute("SELECT cust_name, check_in_date, check_out_date, room_no FROM customers WHERE cust_id = %s", (cust_id,))
            current_customer = cursor.fetchone()
            if not current_customer:
                return jsonify({'error': 'Customer not found'}), 404

            current_cust_name, current_check_in_date, current_check_out_date, current_room_no = current_customer
            cust_name = provided_booking_fields.get('cust_name', current_cust_name)
            check_in_date = provided_booking_fields.get('check_in_date', current_check_in_date)
            check_out_date = provided_booking_fields.get('check_out_date', current_check_out_date)
            room_no = provided_booking_fields.get('room_no', current_room_no)

           
            if isinstance(check_in_date, str):
                check_in_date_obj = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            else:
                check_in_date_obj = check_in_date  # Already a datetime.date

            if isinstance(check_out_date, str):
                check_out_date_obj = datetime.strptime(check_out_date, '%Y-%m-%d').date()
            else:
                check_out_date_obj = check_out_date  
                

            cursor.execute("SELECT cost_per_night, room_type FROM rooms WHERE Room_no = %s", (room_no,))
            room_data = cursor.fetchone()
            if not room_data:
                return jsonify({'error': f'Room {room_no} does not exist'}), 400

            cost_per_night, room_type = room_data
            stay_duration = (check_out_date_obj - check_in_date_obj).days
            total_amt = cost_per_night * stay_duration

            cursor.execute("""
                UPDATE bookings
                SET room_no=%s, cust_name=%s, room_type=%s, check_in_date=%s, check_out_date=%s, total_amt=%s
                WHERE cust_id=%s
            """, (room_no, cust_name, room_type, check_in_date, check_out_date, total_amt, cust_id))
            update_bookings = True


        if fields['meals'] and fields['table_no']:
            cursor.execute("SELECT cust_name, room_no, no_in_party FROM customers WHERE cust_id = %s", (cust_id,))
            customer_data = cursor.fetchone()
            if not customer_data:
                return jsonify({'error': 'Customer not found'}), 404

            cust_name = provided_booking_fields.get('cust_name', customer_data[0])
            room_no = provided_booking_fields.get('room_no', customer_data[1])
            no_in_party = fields.get('no_in_party', customer_data[2])

            cursor.execute("SELECT COUNT(*) FROM restaurant WHERE Cust_ID = %s", (cust_id,))
            exists = cursor.fetchone()[0]
            if exists:
                cursor.execute("""
                    UPDATE restaurant
                    SET Cust_Name=%s, room_no=%s, Table_no=%s, No_in_Party=%s, Meals=%s
                    WHERE Cust_ID=%s
                """, (cust_name, room_no, fields['table_no'], no_in_party, fields['meals'], cust_id))
            else:
                cursor.execute("""
                    INSERT INTO restaurant (Cust_ID, Cust_Name, room_no, Table_no, No_in_Party, Meals)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (cust_id, cust_name, room_no, fields['table_no'], no_in_party, fields['meals']))

        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')

    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': f'Database error: {str(err)}'}), 500


@app.route('/get_bill/<int:cust_id>', methods=['GET'])
def get_bill(cust_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT b.cust_name, b.room_no, b.room_type, b.check_in_date, b.check_out_date, b.total_amt
        FROM bookings b
        WHERE b.cust_id = %s
    """, (cust_id,))
    booking = cursor.fetchone()
    
    if not booking:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Booking not found for customer'}), 404
    
    
    cursor.execute("""
        SELECT r.Meals, r.Table_no, r.No_in_Party
        FROM restaurant r
        WHERE r.Cust_ID = %s
    """, (cust_id,))
    restaurant = cursor.fetchone()
    
    
    no_in_party = None
    if restaurant and restaurant['No_in_Party']:
        no_in_party = int(restaurant['No_in_Party'])
    else:
        cursor.execute("SELECT no_in_party FROM customers WHERE cust_id = %s", (cust_id,))
        customer = cursor.fetchone()
        if customer and customer['no_in_party']:
            no_in_party = int(customer['no_in_party'])
    
    
    no_in_party = no_in_party if no_in_party is not None else 1
    
    
    check_in_date = booking['check_in_date']
    check_out_date = booking['check_out_date']
    stay_duration = (check_out_date - check_in_date).days
    
 
 
    meal_cost_per_person = 0
    meals = restaurant['Meals'] if restaurant and restaurant['Meals'] else ''
    if meals:
        
        meal_list = meals.split(',')
        num_meals = len([m for m in meal_list if m.strip()]) 
        meal_cost_per_person = num_meals * 1000 
    meal_costs = meal_cost_per_person * no_in_party * stay_duration
    
    
    bill_data = {
        'cust_name': booking['cust_name'],
        'room_no': booking['room_no'],
        'room_type': booking['room_type'],
        'check_in_date': booking['check_in_date'].strftime('%Y-%m-%d'),
        'check_out_date': booking['check_out_date'].strftime('%Y-%m-%d'),
        'stay_duration': stay_duration,
        'room_costs': float(booking['total_amt']), 
        'meals': meals or 'None',
        'no_in_party': no_in_party,
        'meal_costs': float(meal_costs),
        'total_bill': float(booking['total_amt'] + meal_costs)
    }
    
    cursor.close()
    conn.close()
    return jsonify(bill_data)


@app.route('/delete_customer/<int:cust_id>', methods=['POST'])
def delete_customer(cust_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE cust_id = %s", (cust_id,))
    cursor.execute("DELETE FROM restaurant WHERE cust_id = %s", (cust_id,))
    cursor.execute("DELETE FROM customers WHERE cust_id = %s", (cust_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'Customer deleted'})

@app.route('/delete_employee/<int:emp_id>', methods=['POST'])
def delete_employee(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT department FROM employee WHERE emp_id = %s", (emp_id,))
    department = cursor.fetchone()
    if department:
        cursor.execute("UPDATE departments SET no_of_workers = no_of_workers - 1 WHERE department_name = %s", (department[0],))
    cursor.execute("DELETE FROM employee WHERE emp_id = %s", (emp_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'Employee deleted'})


@app.route('/view_customers')
def view_customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(customers)

@app.route('/view_available_rooms')
def view_available_rooms():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM rooms
        WHERE Room_no NOT IN (SELECT room_no FROM customers)
    """)
    rooms = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rooms)

@app.route('/view_employees')
def view_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(employees)

if __name__ == '__main__':
    app.run(debug=True)
