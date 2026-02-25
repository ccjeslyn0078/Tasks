from abc import ABC, abstractmethod
import uuid

class Crud(ABC):

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def read(self, key):
        pass

    @abstractmethod
    def update(self, key, data):
        pass

    @abstractmethod
    def delete(self, key):
        pass
    

class StudentService(Crud):
    students = {}

    def create(self, name, usn):
        if usn in StudentService.students:
            print("Student already exists.")
            return

        StudentService.students[usn] = {
            "uid": str(uuid.uuid4()),
            "name": name,
            "usn": usn,
            "subjects": []
        }

        print(f"{name} ({usn}) added successfully!")

    def read(self, usn):
        student = StudentService.students.get(usn)
        if student:
            print(student)
        else:
            print("Student not found.")

    def update(self, usn, data):
        if usn in StudentService.students:
            StudentService.students[usn].update(data)
            print("Student updated successfully.")
        else:
            print("Student not found.")

    def delete(self, usn):
        if usn in StudentService.students:
            del StudentService.students[usn]
            print("Student deleted successfully.")
        else:
            print("Student not found.")


class SubjectService(Crud):

    def create(self, usn, subjects):
        student = StudentService.students.get(usn)
        if student:
            student["subjects"].extend(subjects)
            print("Subjects added successfully.")
        else:
            print("Student not found.")

    def read(self, usn):
        student = StudentService.students.get(usn)
        if student:
            print("Subjects:", student["subjects"])
        else:
            print("Student not found.")

    def update(self, usn, subjects):
        student = StudentService.students.get(usn)
        if student:
            student["subjects"] = subjects
            print("Subjects updated successfully.")
        else:
            print("Student not found.")

    def delete(self, usn):
        student = StudentService.students.get(usn)
        if student:
            student["subjects"] = []
            print("All subjects removed.")
        else:
            print("Student not found.")
            

def main():
    student_service = StudentService()
    subject_service = SubjectService()

    while True:
        print("""
        1. Add Student
        2. View Student
        3. Update Student
        4. Delete Student
        5. Add Subjects
        6. View Subjects
        7. Update Subjects
        8. Remove All Subjects
        9. Exit
        """)

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter name: ")
            usn = input("Enter usn: ")
            student_service.create(name, usn)

        elif choice == "2":
            usn = input("Enter usn: ")
            student_service.read(usn)

        elif choice == "3":
            usn = input("Enter usn: ")
            new_name = input("Enter new name: ")
            student_service.update(usn, {"name": new_name})

        elif choice == "4":
            usn = input("Enter usn: ")
            student_service.delete(usn)

        elif choice == "5":
            usn = input("Enter usn: ")
            subjects = input("Enter subjects (comma separated): ").split(",")
            subject_service.create(usn, subjects)

        elif choice == "6":
            usn = input("Enter usn: ")
            subject_service.read(usn)

        elif choice == "7":
            usn = input("Enter usn: ")
            subjects = input("Enter new subjects (comma separated): ").split(",")
            subject_service.update(usn, subjects)

        elif choice == "8":
            usn = input("Enter usn: ")
            subject_service.delete(usn)

        elif choice == "9":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
