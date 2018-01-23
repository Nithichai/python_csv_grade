# -*- coding: utf-8 -*-
import csv
import re

# If grade is not "F" then get value. Otherwise get zero
def check_pass_credits(row):
    if grade_val(row[2]) > 0:
        return float(row[1])
    return 0

# Check this is describe row
def is_describe(row):
    describe_pattern = re.compile(r"ปีการศึกษา|ชื่อวิชา")
    return describe_pattern.search(row[0])

# Check this is semester row
def is_change_semester(row):
    semester_pattern = re.compile(r"ภาคการเรียนที่")
    return semester_pattern.search(row[0])

# add points, credits value in list that own semester
def save_gpa_packet(row):
    credits_submit = float(row[1])
    credits_pass = check_pass_credits(row)
    grade = grade_val(row[2])
    ls_credits_submit[semester-1] += credits_submit
    ls_credits_pass[semester-1] += credits_pass
    ls_points[semester-1] += credits_submit * grade

# print grade row
def show_grade(row):
    print('%s %s %s' % (row[0], row[1], row[2]))

# print semester value
def show_semester(semester):
    print('Semester : %d' % semester)

# get GPA value
def get_gpa(semester, ls_points, ls_credits_submit):
    return ls_points[semester-1] / ls_credits_submit[semester-1]

# show GPA value
def show_gpa(semester, ls_points, ls_credits_submit):
    print('GPA : %.2f' % get_gpa(semester, ls_points, ls_credits_submit))

# get GPAX value
def get_gpax(ls_points, ls_credits_submit):
    return sum(ls_points) / sum(ls_credits_submit)

# show GPAX value
def show_gpax(ls_points, ls_credits_submit):
    print('GPAX : %.2f' % get_gpax(ls_points, ls_credits_submit))

# make space for new semester and add semester value
def new_semester(semester):
    ls_points.append(0)
    ls_credits_submit.append(0)
    ls_credits_pass.append(0)
    return semester + 1

# Check there are grade in list
def has_grade(ls_points):
    return len(ls_points) > 0

# Check grade in text and return to value
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

# make line to seperate semester
def set_line():
    print "-----------------------------------"

################################################################################
# ls_points => save sum of points in every semester
# ls_credits_submit => save sum of submitted credit in every semester
# ls_credits_pass => save sum of passed credit in every semester
# semester => index to point in list / show current semester
################################################################################
ls_points = []
ls_credits_submit = []
ls_credits_pass = []
semester = 0

################################################################################
# Read all row and check it.
# If it has grade then add point, credits in list that point to own
# semester and show subject, credit and grade.
# Otherwise. If this is describe then check it that is new semester then show
# semester, gpa, gpax and add semester value.
# If they reach last row, show last packet that has semester, gpa, gpax.
################################################################################
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
