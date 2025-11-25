from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

DATA_FILE = "employees.json"

class EmployeeManagementSystem:
    def __init__(self, data_file):
        self.data_file_path = data_file
        if not os.path.exists(self.data_file_path):
            with open(self.data_file_path, 'w') as file:
                json.dump([], file)

    def _load_data(self):
        try:
            with open(self.data_file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self, data):
        try:
            with open(self.data_file_path, 'w') as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            return False

    def add_employee(self, employee_data):
        all_employees = self._load_data()
        
        # Check for duplicate ID
        for employee in all_employees:
            if employee['id'] == employee_data['id']:
                return False, "Employee ID already exists"
                
        all_employees.append(employee_data)
        if self._save_data(all_employees):
            return True, "Employee added successfully"
        return False, "Error saving employee"

    def view_all_employees(self):
        return self._load_data()

    def search_employee(self, emp_id):
        all_employees = self._load_data()
        for employee in all_employees:
            if employee['id'] == emp_id:
                return employee
        return None

# Initialize the system
system = EmployeeManagementSystem(DATA_FILE)

# API Routes
@app.route('/api/employees', methods=['GET'])
def get_employees():
    employees = system.view_all_employees()
    return jsonify(employees)

@app.route('/api/employees', methods=['POST'])
def add_employee():
    employee_data = request.get_json()
    
    # Validate required fields
    required_fields = ['id', 'name', 'department', 'salary']
    for field in required_fields:
        if field not in employee_data or not employee_data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    success, message = system.add_employee(employee_data)
    if success:
        return jsonify({'message': message}), 201
    else:
        return jsonify({'error': message}), 400

@app.route('/api/employees/<emp_id>', methods=['GET'])
def get_employee(emp_id):
    employee = system.search_employee(emp_id)
    if employee:
        return jsonify(employee)
    else:
        return jsonify({'error': 'Employee not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)