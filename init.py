# -*- coding: utf-8 -*-
import csv
import re

# if detect F so you shall not pass
def check_pass_credits(row):
    if float(row[3]) > 0:
        return True
    return False

with open('grade.csv', 'rb') as csvfile:
    # variables
    ls_points = []
    ls_credits_submit = []
    ls_credits_pass = []
    semester = 0

    #  reset

    # init
    reader = csv.reader(csvfile)
    # list all row
    for row in reader:
        # no col in row just go to next row
        if len(row) == 0:
            continue

        # ปีการศึกษา and ชื่อวิชา 's is header
        describe_pattern = re.compile(r"ปีการศึกษา|ชื่อวิชา")
        describe_regex = describe_pattern.search(row[0])

        # check header or grade row
        if not describe_regex:
            # get value from table
            credits_submit = float(row[1])
            if check_pass_credits(row):
                credits_pass = float(row[1])
            else:
                credits_pass = 0
            grade = float(row[3])

            # save value to list (for every semester)
            ls_credits_submit[semester-1] += credits_submit
            ls_credits_pass[semester-1] += credits_pass
            ls_points[semester-1] += credits_submit * grade
        else:
            # find row that has ภาคการเรียนที่ for change semester
            semester_pattern = re.compile(r"ภาคการเรียนที่")
            semester_regex = semester_pattern.search(row[0])
            if semester_regex:
                semester += 1

                #  reset
                ls_points.append(0)
                ls_credits_submit.append(0)
                ls_credits_pass.append(0)
                points = 0
                credits_submit = 0
                credits_pass = 0

    print ls_points, ls_credits_submit, ls_credits_pass
    print semester
