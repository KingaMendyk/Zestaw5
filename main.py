import smtplib
from email.mime.text import MIMEText


def show(students):
    for student in students.values():
        print(student)


def read_file(filepath):
    with open(filepath) as file_object:
        res = {}
        index = 1
        for line in file_object:
            line_dict = {}
            line_list = line.rstrip().split(",")
            line_dict["email"] = line_list[0]
            line_dict["name"] = line_list[1]
            line_dict["surname"] = line_list[2]
            line_dict["points"] = line_list[3]
            if len(line_list) == 6:
                line_dict["grade"] = line_list[4]
                line_dict["status"] = line_list[5]
            res["student" + str(index)] = line_dict
            index += 1
    return res


def save_to_file(filepath, content):
    with open(filepath, "w") as file_object:
        for c in content.values():
            line = c.get("email")+","+c.get("name")+","+c.get("surname")+","+c.get("points")
            if "grade" in c.keys():
                line = line+","+c.get("grade")
            if "status" in c.keys():
                line = line+","+c.get("status")
            line = line+"\n"
            file_object.write(line)


def mail_students(students):
    for student in students.values():
        if student.get("status") != "MAILED":
            send_mail("Grade", student.get("grade"), "mymail@gmail.com", student.get("email"), "mypassword")
            student["status"] = "MAILED"
    save_to_file("new_file.txt", students)


def send_mail(subject, body, sender, recipients, password):
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ",".join(recipients)
    smtp_server = smtplib.SMTP_SSL("smpt.gmail.com", 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, message.as_string())
    smtp_server.quit()


# 50 i mniej - 2
# 51 -60 pkt - 3
# 61 – 70 pkt – 3.5
# 71 – 80 pkt - 4
# 81 - 90 pkt – 4.5
# 91 - 100 pkt – 5
def grade_students(students):
    for student in students.values():
        if "grade" not in student.keys():
            points = float(student.get("points"))
            if points <= 50:
                student["grade"] = "2"
            elif 50 < points <= 60:
                student["grade"] = "3"
            elif 60 < points <= 70:
                student["grade"] = "3.5"
            elif 70 < points <= 80:
                student["grade"] = "4"
            elif 80 < points <= 90:
                student["grade"] = "4.5"
            else:
                student["grade"] = "5"
            student["status"] = "GRADED"
    save_to_file("new_file.txt", students)


def add_student(students, email, name, surname, points, grade="", status=""):
    for student in students.values():
        if email == student.get("email"):
            print("Student already exists!")
            return
    students["student" + str(len(students) + 1)] = {"email": email,
                                                    "name": name,
                                                    "surname": surname,
                                                    "points": points
                                                    }
    if grade != "":
        students["student" + str(len(students) + 1)]["grade"] = grade
    if status != "":
        students["student" + str(len(students) + 1)]["status"] = status
    save_to_file("new_file.txt", students)


def delete_student(students, email):
    for student in students.keys():
        if email == students[student].get("email"):
            key = student
    del students[key]
    save_to_file("new_file.txt", students)


# 1.
studentDict = read_file("students.txt")
print("Students:")
show(studentDict)

# 2.
grade_students(studentDict)
print("\nStudents after grading:")
show(studentDict)

# 3.
print("\nAdding student:")
add_student(studentDict, "aaa@gmail.com", "AA", "BB", "80")
show(studentDict)
print("\nDeleting student:")
delete_student(studentDict, "aaa@gmail.com")
show(studentDict)

# 4.
print("\nSending emails:")
#mail_students(studentDict)
show(studentDict)

# 5.
# Zrealizowane na końcu w odpowiednich funkcjach - add_student, delete_student,
# grade_students, mail_students
