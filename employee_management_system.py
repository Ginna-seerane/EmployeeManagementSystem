# =============================================
# Employee Management System
# Author: Ginna Seerane
# 
# 
# Purpose: This program allows a business to
# manage employee records by adding new employees,
# viewing all employees, and searching for an
# employee by their ID. Data is stored in a
# JSON file to persist between sessions.
#
# Design Specs Followed:
# - UML Class Structure: Employee and EmployeeManagementSystem
# - Data Structure: List of dictionaries in JSON file
# - Access Method: File I/O with JSON serialization
# - Logical Flow: Main menu with workflow functions
# =============================================

import json
import os

class Employee:
    """
    Represents a single employee in the system.
    
    Attributes:
        employee_id (str): Unique identifier for the employee
        employee_name (str): Full name of the employee  
        employee_department (str): Department where employee works
        employee_salary (float): Employee's salary amount
    
    Methods:
        get_details(): Returns employee data as dictionary
    """
    
    def __init__(self, emp_id, name, department, salary):
        # Initialize employee attributes with descriptive names
        self.employee_id = emp_id
        self.employee_name = name
        self.employee_department = department
        self.employee_salary = float(salary)  # Convert to float for consistency

    def get_details(self):
        """
        Converts employee object to dictionary for JSON storage.
        
        Returns:
            dict: Employee details in key-value format
        """
        return {
            "id": self.employee_id,
            "name": self.employee_name,
            "department": self.employee_department,
            "salary": self.employee_salary
        }


class EmployeeManagementSystem:
    """
    Main system class that manages all employee data operations.
    
    Attributes:
        data_file_path (str): Path to the JSON data file
    
    Methods:
        add_employee(): Adds new employee to system
        view_all_employees(): Returns all employees
        search_employee(): Finds employee by ID
        _load_data(): Internal method to load data from file
        _save_data(): Internal method to save data to file
    """
    
    def __init__(self, data_file):
        """
        Initializes the system and ensures data file exists.
        
        Args:
            data_file (str): Path to the data storage file
        """
        self.data_file_path = data_file
        # Create empty data file if it doesn't exist
        if not os.path.exists(self.data_file_path):
            with open(self.data_file_path, 'w') as file:
                json.dump([], file)

    def _load_data(self):
        """
        Private method to load all employee data from JSON file.
        
        Returns:
            list: List of employee dictionaries, empty list if file error
        """
        try:
            with open(self.data_file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return empty list if file doesn't exist or is corrupted
            return []

    def _save_data(self, data):
        """
        Private method to save employee data to JSON file.
        
        Args:
            data (list): List of employee dictionaries to save
            
        Returns:
            bool: True if save successful, False if error
        """
        try:
            with open(self.data_file_path, 'w') as file:
                json.dump(data, file, indent=4)  # indent=4 for readable formatting
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def add_employee(self, employee_data):
        """
        Adds a new employee to the system after checking for duplicates.
        
        Args:
            employee_data (dict): Employee details to add
            
        Returns:
            bool: True if employee added, False if duplicate ID or save error
        """
        all_employees = self._load_data()
        
        # Check for duplicate employee ID
        for employee in all_employees:
            if employee['id'] == employee_data['id']:
                print("Error: An employee with this ID already exists.")
                return False
                
        # Add new employee and save
        all_employees.append(employee_data)
        return self._save_data(all_employees)

    def view_all_employees(self):
        """
        Retrieves all employees from the system.
        
        Returns:
            list: List of all employee dictionaries
        """
        return self._load_data()

    def search_employee(self, emp_id):
        """
        Searches for an employee by their ID.
        
        Args:
            emp_id (str): Employee ID to search for
            
        Returns:
            dict: Employee data if found, None if not found
        """
        all_employees = self._load_data()
        for employee in all_employees:
            if employee['id'] == emp_id:
                return employee
        return None


def add_employee_workflow(system):
    """
    Handles the complete workflow for adding a new employee.
    
    Steps:
    1. Get employee details from user input
    2. Validate salary input
    3. Create Employee object
    4. Add to system via EmployeeManagementSystem
    
    Args:
        system (EmployeeManagementSystem): The system instance to use
    """
    print("\n--- Add New Employee ---")
    emp_id = input("Enter Employee ID: ").strip()
    name = input("Enter Employee Name: ").strip()
    department = input("Enter Department: ").strip()
    
    # Validate that salary is a valid number
    try:
        salary = float(input("Enter Salary: "))
    except ValueError:
        print("Invalid salary amount. Please enter a number.")
        return
        
    # Create and add new employee
    new_emp = Employee(emp_id, name, department, salary)
    
    if system.add_employee(new_emp.get_details()):
        print("Employee added successfully!")
    else:
        print("Failed to add employee.")


def view_all_employees_workflow(system):
    """
    Handles displaying all employees in a formatted way.
    
    Args:
        system (EmployeeManagementSystem): The system instance to use
    """
    print("\n--- All Employees ---")
    employees = system.view_all_employees()
    if not employees:
        print("No employees found.")
    else:
        # Display each employee with formatted output
        for emp in employees:
            print(f"ID: {emp['id']}, Name: {emp['name']}, Dept: {emp['department']}, Salary: ${emp['salary']:.2f}")


def search_employee_workflow(system):
    """
    Handles searching for an employee by ID and displaying results.
    
    Args:
        system (EmployeeManagementSystem): The system instance to use
    """
    print("\n--- Search Employee ---")
    emp_id = input("Enter Employee ID to search: ").strip()
    employee = system.search_employee(emp_id)
    if employee:
        print(f"Employee Found: ID: {employee['id']}, Name: {employee['name']}, Dept: {employee['department']}, Salary: ${employee['salary']:.2f}")
    else:
        print("Employee not found.")


def main():
    """
    Main program loop that displays menu and handles user choices.
    
    The loop continues until user chooses to exit (option 4).
    Creates EmployeeManagementSystem instance and calls appropriate workflows.
    """
    # Initialize system with data file
    system = EmployeeManagementSystem("employees.json")
    
    while True:
        # Display main menu options
        print("\n=== Employee Management System ===")
        print("1. Add New Employee")
        print("2. View All Employees")
        print("3. Search Employee by ID")
        print("4. Exit")
        
        user_choice = input("Please choose an option (1-4): ").strip()
        
        # Handle user menu selection
        if user_choice == '1':
            add_employee_workflow(system)
        elif user_choice == '2':
            view_all_employees_workflow(system)
        elif user_choice == '3':
            search_employee_workflow(system)
        elif user_choice == '4':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 4.")


# Standard Python practice - only run main() if file is executed directly
if __name__ == "__main__":
    main()