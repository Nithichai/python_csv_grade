# -*- coding: utf-8 -*-
import csv
import re
import math

def check_pass_credits(row):
    if grade_val(row[2]) > 0:
        return float(row[1])
    return 0

def is_describe(row):
    describe_pattern = re.compile(r"ปีการศึกษา|ชื่อวิชา")
    return describe_pattern.search(row[0])

def is_change_semester(row):
    semester_pattern = re.compile(r"ภาคการเรียนที่")
    return semester_pattern.search(row[0])

def save_gpa_packet(row):
    credits_submit = float(row[1])
    credits_pass = check_pass_credits(row)
    grade = grade_val(row[2])
    ls_credits_submit[semester-1] += credits_submit
    ls_credits_pass[semester-1] += credits_pass
    ls_points[semester-1] += credits_submit * grade

def show_grade(row):
    print('%s %s %s' % (row[0], row[1], row[2]))

def show_semester(semester):
    print('Semester : %d' % semester)

def get_gpa(semester, ls_points, ls_credits_submit):
    return ls_points[semester-1] / ls_credits_submit[semester-1]

def show_gpa(semester, ls_points, ls_credits_submit):
    print('GPA : %.2f' % get_gpa(semester, ls_points, ls_credits_submit))

def get_gpax(ls_points, ls_credits_submit):
    return sum(ls_points) / sum(ls_credits_submit)

def show_gpax(ls_points, ls_credits_submit):
    print('GPAX : %.2f' % get_gpax(ls_points, ls_credits_submit))

def new_semester(semester):
    ls_points.append(0)
    ls_credits_submit.append(0)
    ls_credits_pass.append(0)
    return semester + 1

def has_grade(ls_points):
    return len(ls_points) > 0

def grade_val(grade):
    if (grade == "A"):
        return 4.0
    elif (grade == "B+"):
        return 3.5
    elif (grade == "B"):
        return 3.0
    elif (grade == "C+"):
        return 2.5
    elif (grade == "C"):
        return 2.0
    elif (grade == "D+"):
        return 1.5
    elif (grade == "D"):
        return 1.0
    return 0

def set_line():
    print "-----------------------------------"

################################################################################

ls_points = []
ls_credits_submit = []
ls_credits_pass = []
semester = 0

with open('grade.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if not is_describe(row):
            save_gpa_packet(row)
            show_grade(row)
        else:
            if is_change_semester(row):
                if has_grade(ls_points):
                    show_semester(semester)
                    show_gpa(semester, ls_points, ls_credits_submit)
                    show_gpax(ls_points, ls_credits_submit)
                    set_line()
                semester = new_semester(semester)

    if has_grade(ls_points) > 0:
        show_gpa(semester, ls_points, ls_credits_submit)
        show_gpax(ls_points, ls_credits_submit)
