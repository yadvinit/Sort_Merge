import random
import math
import time
from faker import Faker

# GENERATES RANDOM STUDENT DATA LIKE ROLL NO, NAME, LAST NAME, BRANCH, YEAR
def generate_random_student_data(num_students):
    fake = Faker()
    student_data = []

    for i in range(num_students):
        student = [i, fake.first_name(), fake.last_name(), fake.random_element(elements=('Computer Science', 'Electrical Engineering', 'Mechanical Engineering', 'Civil Engineering')), random.randint(1, 4)]
        student_data.append(student)

    return student_data

# GENERATES STUDENTS MARKS DETAILS -> ROLL NO FOLLOWED BY MARKS
def generate_random_student_marks_data(num_students):
    fake = Faker()
    student_data = []

    for i in range(num_students):
        student = [i, random.randint(1,100), random.randint(1,100), random.randint(1, 100)]
        student_data.append(student)

    return student_data

# COMPUTE EXECUTION TIME
def find_execution_time(st, et):
    execution_time = et-st
    return execution_time

# COMPUTE COST ASSUMING THAT BOTH THE RELATIONS ARE ALREADY SORTED
def cost_without_sorting(br, bs):
    cost = br+bs
    return cost

# COMPUTE COST FOR SORTING RELATION R
def cost_of_sorting_R(br, M):
    cost = 2*br + 2*br*math.log(br/M, M-1)
    return cost

# COMPUTE COST FOR SORTING RELATION S
def cost_of_sorting_S(bs, M):
    cost = 2*bs + 2*bs*math.log(bs/M, M-1)
    return cost

# COMPUTE COST FOR MERGE JOIN WITH ALREADY SORTED RELATION R
def cost_with_sorted_R(br, bs, M):
    cost_without_sort = cost_without_sorting(br, bs)
    sort_cost_S = cost_of_sorting_S(bs, M)
    cost = cost_without_sort + sort_cost_S
    return cost

# COMPUTE COST FOR MERGE JOIN WITH ALREADY SORTED RELATION S
def cost_with_sorted_S(br, bs, M):
    cost_without_sort = cost_without_sorting(br, bs)
    sort_cost_R = cost_of_sorting_R(br, M)
    cost = cost_without_sort + sort_cost_R
    return cost

# COMPUTE COST FOR MERGE JOIN FOR NOT SORTED RELATION R & S
def cost_with_complete_sort(br, bs, M):
    return cost_without_sorting(br, bs) + cost_of_sorting_R(br, M) + cost_of_sorting_S(bs, M)





# MAIN FUNCTION
if __name__ == '__main__':

    # TAKE INPUTS
    fr = int(input('Enter Bloking Factor for Relation R: '))
    fs = int(input('Enter Bloking Factor for Relation S: '))
    M = int(input('Enter Memory Size: '))


    num_students = 100000
    random_student_data = generate_random_student_data(num_students)

    print("Generated Random Student Data:")

    # WRITE RANDOMLY GENERATED STUDENTS DATA TO R.txt
    with open('/Users/mach/Desktop/adb/R.txt', 'w') as f:    
        for student in random_student_data:
            # Convert the list to a formatted string before writing to the file
            line = ", ".join(map(str, student))
            f.write(line + "\n")

    random_student_data = generate_random_student_marks_data(num_students)

    # WRITE RANDOMLY GENERATED STUDENTS MARKS TO S.txt
    with open('/Users/mach/Desktop/adb/S.txt', 'w') as f:    
        for student in random_student_data:
            # Convert the list to a formatted string before writing to the file
            line = ", ".join(map(str, student))
            f.write(line + "\n")


    # COMPUTE BR AND BS FOR FURTHER JOIN OPERATION

    with open('/Users/mach/Desktop/adb/R.txt') as f:
        nr = len(f.readlines())

    with open('/Users/mach/Desktop/adb/S.txt') as f:
        ns = len(f.readlines())

    br = math.ceil(nr/fr)

    bs = math.ceil(ns/fs)


    # JOIN OPERATION STARTS HERE
    # HASH MAPS FOR MAPPING STUDENTS {KEY: VALUE} KEY=ROLL-NO
    table1 = {} # VALUE = STUDENTS DETAILS EXCEPT ROLL NO
    table2 = {} # VALUE = STUDENTS MARKS

    st = time.time()
    with open('/Users/mach/Desktop/adb/R.txt') as f:
        lines = f.readlines()
    
    # print(lines[:5])

    # ADD DATA TO HASH MAPS
    for line in lines:
        data = line.strip().split(',')
        rollNo = data[0]
        table1[rollNo] = data[1:]
    # print(table1)

    with open('/Users/mach/Desktop/adb/S.txt') as f:
        lines = f.readlines()
    
    # ADD DATA TO HASH MAPS
    for line in lines:
        data = line.strip().split(',')
        table2[data[0]] = data[1:]
    
    # print('-----------------\n',table2)

    # COMBINE DATA BY SEARCHING ON RELATION S HASH MAP AND ADD DATA TO CORRESPONDING RELATION R IF 
    # IT'S THERE IN MEMORY
    for k,v in table2.items():
        table1[k].extend(v)
    
    # print('----------------\n', table1)

    # WRITE TO OUTPUT FILE
    with open('/Users/mach/Desktop/adb/output.txt', 'w') as f:
        for k,v in table1.items():
            string = "{} {} {} {} {} {} {} {}".format(k, v[0], v[1],v[2],v[3],v[4],v[5],v[6])
            f.write(string)
            f.write('\n')
    
    et = time.time()

    elapsed_time = find_execution_time(st, et)

    print('\n\n-----------------------------------------\n\n')
    print('Execution time:', elapsed_time, 'seconds')

    
    # ---- COST OF COMPUTATIONS ----


    cost_without_sort = cost_without_sorting(br, bs)

    print('\n\n---------------------------------\n\n')

    print('Cost for Sorted Relations R and S -> ', cost_without_sort)

    sort_cost_R = cost_of_sorting_R(br, M)

    sort_cost_S = cost_of_sorting_S(bs, M)

    print('\n\n---------------------------------\n\n')

    cost_for_sorted_R = cost_with_sorted_R(br, bs, M)
    print('Cost for Sorted Relations R -> ', cost_for_sorted_R)

    print('\n\n---------------------------------\n\n')

    cost_for_sorted_S = cost_with_sorted_S(br, bs, M)
    print('Cost for Sorted Relations S -> ', cost_for_sorted_S)

    print('\n\n---------------------------------\n\n')

    cost = cost_with_complete_sort(br, bs, M)
    print('Cost for Not sorted R & Not Sorted S -> ', cost)
