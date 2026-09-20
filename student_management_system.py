"""
Student Management System
Python Essentials - Evaluated Course Project
"""

import json
from pathlib import Path

DATA_FILE = Path("students.json")


class Student:
    def __init__(self, roll_no, name, age, course, marks):
        self.roll_no = roll_no
        self.name = name
        self.age = age
        self.course = course
        self.marks = marks

    def average(self):
        return sum(self.marks) / len(self.marks)

    def grade(self):
        avg = self.average()
        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F"

    def to_dict(self):
        return {
            "roll_no": self.roll_no,
            "name": self.name,
            "age": self.age,
            "course": self.course,
            "marks": self.marks
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["roll_no"],
            data["name"],
            data["age"],
            data["course"],
            data["marks"]
        )


class StudentManagementSystem:
    def __init__(self):
        self.students = []
        self.load_data()

    def load_data(self):
        try:
            if DATA_FILE.exists():
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.students = [Student.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, TypeError):
            print("Warning: Data file is corrupted. Starting with empty records.")

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump([student.to_dict() for student in self.students], file, indent=4)

    def find_student(self, roll_no):
        for student in self.students:
            if student.roll_no == roll_no:
                return student
        return None

    def add_student(self):
        try:
            roll_no = input("Enter roll number: ").strip()
            if not roll_no:
                raise ValueError("Roll number cannot be empty.")
            if self.find_student(roll_no):
                print("A student with this roll number already exists.")
                return

            name = input("Enter student name: ").strip()
            age = int(input("Enter age: "))
            course = input("Enter course: ").strip()

            if age <= 0:
                raise ValueError("Age must be positive.")
            if not name or not course:
                raise ValueError("Name and course cannot be empty.")

            marks = []
            for subject in ["Python", "Mathematics", "Computer Fundamentals"]:
                mark = float(input(f"Enter marks in {subject} (0-100): "))
                if not 0 <= mark <= 100:
                    raise ValueError("Marks must be between 0 and 100.")
                marks.append(mark)

            self.students.append(Student(roll_no, name, age, course, marks))
            self.save_data()
            print("Student added successfully.")

        except ValueError as error:
            print(f"Invalid input: {error}")

    def display_student(self, student):
        print("\n" + "-" * 45)
        print(f"Roll Number : {student.roll_no}")
        print(f"Name        : {student.name}")
        print(f"Age         : {student.age}")
        print(f"Course      : {student.course}")
        print(f"Average     : {student.average():.2f}")
        print(f"Grade       : {student.grade()}")
        print("-" * 45)

    def view_students(self):
        if not self.students:
            print("No student records found.")
            return

        for student in self.students:
            self.display_student(student)

    def search_student(self):
        roll_no = input("Enter roll number to search: ").strip()
        student = self.find_student(roll_no)

        if student:
            self.display_student(student)
        else:
            print("Student not found.")

    def update_student(self):
        roll_no = input("Enter roll number to update: ").strip()
        student = self.find_student(roll_no)

        if not student:
            print("Student not found.")
            return

        try:
            new_name = input(f"Enter new name [{student.name}]: ").strip()
            new_course = input(f"Enter new course [{student.course}]: ").strip()
            new_age = input(f"Enter new age [{student.age}]: ").strip()

            if new_name:
                student.name = new_name
            if new_course:
                student.course = new_course
            if new_age:
                age = int(new_age)
                if age <= 0:
                    raise ValueError("Age must be positive.")
                student.age = age

            self.save_data()
            print("Student updated successfully.")

        except ValueError as error:
            print(f"Invalid input: {error}")

    def delete_student(self):
        roll_no = input("Enter roll number to delete: ").strip()
        student = self.find_student(roll_no)

        if not student:
            print("Student not found.")
            return

        self.students.remove(student)
        self.save_data()
        print("Student deleted successfully.")

    def run(self):
        while True:
            print("\n===== STUDENT MANAGEMENT SYSTEM =====")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.update_student()
            elif choice == "5":
                self.delete_student()
            elif choice == "6":
                print("Thank you for using Student Management System.")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = StudentManagementSystem()
    app.run()
