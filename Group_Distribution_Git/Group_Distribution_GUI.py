"""
(The manual below can also be read in the program UI itself.)

Hello! This is the Python script for group distribution, created by 2022 G12 Vice President Raymond Kim.
Both before and after running the code, the user has to input data. This manual will walk the user through the process.
Please read everything in detail, as it is important.

------------------------------------------------------------------------------------------------------------------------
At the start of the code, there will be sections denoted by the following sign -> ***
These denote the sections the user has to edit before running the code.

*** INPUT DATA *** refers to student data.
The user will define "student_list" as a list of all student names, in string format.
The user will define "gender_dict" as a dictionary (hash table/map) of all students, in the following form: "student_name": "Male" or "student_name": "Female".

*** PARAMETERS *** refer to parameters regarding the actual group generation.
GROUP_CNT refers to the number of groups the user wants to create. The code will automatically distribute the students evenly into GROUP_CNT groups.
GENDER_RATIO refers to the amount of deviation the user wants to allow the code to have for male-female ratio, in percent form.
    The closer this value is to 0, the stricter the requirement for even male-female ratios, but the lower the likelihood of creating a successful group per iteration.
ITERATION_CNT refers to the number of iterations the code will run, after which the code will display the best results.
    Keep in mind that the user will probably have to run the code multiple times anyway, and too high of an iteration count has tendencies to produce unfavorable results.
POS_EXCEPT_CNT refers to the number of student names each student is expected to write.
    This number is not important for group generation, and only used for the average/median happiness calculations, where happiness for a student "A" refers to the number of student names that student “A” got fulfilled in their groups (AKA number of friends in their group).

Please note that all student names should be constant, for both INPUT DATA and PARAMETERS.

------------------------------------------------------------------------------------------------------------------------
When the script is executed, a window labeled "Group Distribution Settings" will pop up. There will be two main sections.

------------------------------------------------------------------------------------------------------------------------
The first section is where the user has to input different types of exceptions.
1. "Positive Exceptions" refer to which student wants to be with which other student(s).
This data should be inputted by copying & pasting two columns from a spreadsheet, with the first column being each student's name, and second column being a list of students separated by commas ", ".
This can be achieved simply with a Google Form, with dropdowns for student names and checkboxes for desired friends.

2. "Absolute Positive Exceptions" refer to pairs of students that must be put together, determined separately by the user.
This should be inputted in the following string format: "student1_name, student2_name", with the two names separated by commas ", ".

3. "Negative Exceptions" refer to pairs of students that must be separated, determined separately by the user.
This should be inputted in the following string format: "student1_name, student2_name", with the two names separated by commas ", ".

Clicking the "Update Exceptions" button will input the exceptions into the program. If any edit is desired, input new exceptions and click "Update Exceptions" again.

------------------------------------------------------------------------------------------------------------------------
Underneath are two buttons, "Transfer Exceptions" and "Generate Groups". Transfer Exceptions is the process of transferring Tier 1 exceptions into Tier 0 (explained below).

Positive Exceptions are categorized into two tiers. If Person A writes Person B but B does not write A, it is considered Tier 0. If two people write each other, it is considered Tier 1.
The code prioritizes satisfying Tier 1 exceptions. However, if happiness is unfair, transferring some Tier 1s into Tier 0s increases the chances of more equal happiness distribution, but lower average happiness.
It is up to the user whether to transfer, or how many exceptions to transfer at once. Transferred exceptions cannot be reversed, unless the exceptions are re-inputted.

------------------------------------------------------------------------------------------------------------------------
When generating groups, please allow some time for the iterations to occur. The time required will depend on the ITERATION_CNT defined above.
At the end, the code will output the best group, determined by the least number of people with none of their written student names satisfied (zero_num).
From personal experience, it is recommended for the user to run the code multiple times to get candidates with the lowest zero_num, and use the displayed values of average/median happiness and qualitative judgement to choose the best group.

------------------------------------------------------------------------------------------------------------------------
Please keep in mind that this code is not perfect, nor was it ever intended to be. It is simply a method to increase the number of people who receive satisfactory groups.
As with most community-based Python scripts, this is open-source, and anyone can feel free to edit and improve it in any way.
I truly hope this script can be of help for both students and teachers alike.

Sincerely,

Raymond Kim :D
"""

from tkinter import *
from tkinter import ttk
import random
import math
from copy import deepcopy

# *** INPUT DATA ***
student_list = [
    'Somin (Angelina) An', 'Minxuan (Kevin) Jin', 'Dongwon (Henry) Kang', 'Minkyu (Robin) Kim',
    'Hyeok-kyu (James) Kwon', 'Jesung Lee', 'Hannah Park', 'Eun Bin (Alice) Seo', 'Tae In Shim',
    'Jaegeun (Bill) Song', 'Liyu Gashawbeza Arega', 'Sebastian Ellis', 'Sahar Hany Mohamed Farag',
    'Rosemary Del Valle Gostovich', 'Junyoung (Roy) Kim', 'Raymond Kim', 'Yedam (Allen) Kim',
    'Ki Hyuk (Chris) Lee', 'Gi Pyo (Frank) Park', 'Isaac Tao', 'Yun Seong (Jamie Chung)', 'Min Joon Kang',
    'Junseok (Zane) Kim', 'Sarah Kim', 'Jinsong (Edward) Park', 'Sung Joon Park', 'Eunseo (Chloe) Won',
    'Sae Kyun (Chris) Chung', 'Luis Alberto Garcia Valbuena', 'Taehwi (Charlie) Kim', 'Dayeon (Jane) Lee',
    'Junwoo (Andrew) Park', 'Stephan Park', 'Julian Suh-Jin Rothe', 'Claudia Sersen Valdeiglesias', 'Nguyet Anh Truong',
    'Brent Jiho Yoo', 'Hyojin (Kaylee) Chae', 'Yehin (Victoria) Cho', 'Hyunwoo Kim', 'Seungjae (Isaac) Kim',
    'Jamie Ha-Young Kwon', 'Chae Won (Ariel) Lee', 'Hyejun (Julie) Lee', 'Jiwon (Vanessa) Lee', 'Seokhwan (Terry) Park',
    'Aimee Belle Cho', 'Youn Sung Cho', 'Yoolim (Sally) Choi', 'SeungHan (Sean) Ha', 'Jiwon (Justine) Kim',
    'Yelynn (Kathleen) Kim', 'Seoyeon Kweon', 'Suh Jin (Ann) Park', 'Hyunwoo Ra', 'Charles Chansoo Shin',
    'Maria Jesus Soto', 'Bo Eun (Sally) Kang', 'Doyoung (Dorothy) Kim', 'Jiseong (Jason) Kim', 'Se Hee (Clare) Kim',
    'Kyeonguk (Jake) Min', 'Jeanne F Park', 'Joane Seol', 'Ye Eun (Emily) Shim', 'Yunji (Liz) Bae',
    'Sohyun (Emma) Baik', 'Yerim (Jenny) Kim', 'Bu Kyeong (Katie) Kwak', 'Daniel Seungmin Lee',
    'Wooyong (Aiden) Lee', 'Davis Park', 'Seungbee (Paul) Park', 'Woojean Shon', 'Min Wook (Edward) Song',
    'Oleksii (Alex) Varlamov'
]
gender_dict = {
    'Bu Kyeong (Katie) Kwak': 'Female', 'Bo Eun (Sally) Kang': 'Female', 'Min Wook (Edward) Song': 'Male',
    'Somin (Angelina) An': 'Female', 'Eunseo (Chloe) Won': 'Female', 'Yun Seong (Jamie Chung)': 'Male',
    'Jesung Lee': 'Male', 'Junseok (Zane) Kim': 'Male', 'Ye Eun (Emily) Shim': 'Female', 'Junyoung (Roy) Kim': 'Male',
    'Doyoung (Dorothy) Kim': 'Female', 'Hyejun (Julie) Lee': 'Female', 'Hyunwoo Ra': 'Male',
    'Sahar Hany Mohamed Farag': 'Female', 'Dongwon (Henry) Kang': 'Male', 'Min Joon Kang': 'Male',
    'Jiseong (Jason) Kim': 'Male', 'Seungbee (Paul) Park': 'Male', 'Charles Chansoo Shin': 'Male',
    'Suh Jin (Ann) Park': 'Female', 'Jiwon (Justine) Kim': 'Female', 'Taehwi (Charlie) Kim': 'Male',
    'Jamie Ha-Young Kwon': 'Female', 'Dayeon (Jane) Lee': 'Female', 'Jaegeun (Bill) Song': 'Male',
    'Gi Pyo (Frank) Park': 'Male', 'Aimee Belle Cho': 'Female', 'Isaac Tao': 'Male', 'Yerim (Jenny) Kim': 'Female',
    'Eun Bin (Alice) Seo': 'Female', 'Julian Suh-Jin Rothe': 'Male', 'Kyeonguk (Jake) Min': 'Male',
    'Tae In Shim': 'Male', 'SeungHan (Sean) Ha': 'Male', 'Yunji (Liz) Bae': 'Female', 'Raymond Kim': 'Male',
    'Minxuan (Kevin) Jin': 'Male', 'Hyojin (Kaylee) Chae': 'Female', 'Seokhwan (Terry) Park': 'Male',
    'Davis Park': 'Male', 'Seungjae (Isaac) Kim': 'Male', 'Brent Jiho Yoo': 'Male', 'Sae Kyun (Chris) Chung': 'Male',
    'Stephan Park': 'Male', 'Ki Hyuk (Chris) Lee': 'Male', 'Yehin (Victoria) Cho': 'Female',
    'Chae Won (Ariel) Lee': 'Female', 'Youn Sung Cho': 'Male', 'Junwoo (Andrew) Park': 'Male',
    'Seoyeon Kweon': 'Female', 'Sarah Kim': 'Female', 'Hyeok-kyu (James) Kwon': 'Male', 'Sohyun (Emma) Baik': 'Female',
    'Yelynn (Kathleen) Kim': 'Female', 'Jiwon (Vanessa) Lee': 'Female', 'Sung Joon Park': 'Male',
    'Liyu Gashawbeza Arega': 'Female', 'Joane Seol': 'Female', 'Se Hee (Clare) Kim': 'Female',
    'Yoolim (Sally) Choi': 'Female', 'Yedam (Allen) Kim': 'Male', 'Wooyong (Aiden) Lee': 'Male',
    'Minkyu (Robin) Kim': 'Male', 'Hannah Park': 'Female', 'Sebastian Ellis': 'Male',
    'Rosemary Del Valle Gostovich': 'Female', 'Jinsong (Edward) Park': 'Male', 'Luis Alberto Garcia Valbuena': 'Male',
    'Claudia Sersen Valdeiglesias': 'Female', 'Nguyet Anh Truong': 'Female', 'Hyunwoo Kim': 'Male',
    'Maria Jesus Soto': 'Female', 'Jeanne F Park': 'Female', 'Daniel Seungmin Lee': 'Male', 'Woojean Shon': 'Male',
    'Oleksii (Alex) Varlamov': 'Male'
}

# *** PARAMETERS ***
GROUP_CNT = 6
GENDER_RATIO = 0.2
ITERATION_CNT = 50000
POS_EXCEPT_CNT = 3

# variables
group_sizes = []
groups = []
final_group_candidates = []  # [group, average happiness, median happiness, zero_num]
final_group = []

pos_exceptions_raw = dict()  # [person1] = [ [person2, 0], [person3, 1], ... ]
pos_exceptions_tier = dict()  # [subject] = [[ tier0 ], [ tier1 ], [ tier2 ]]
pos_exceptions = dict()  # [subject] = [ list ]  # doesn't include absolute positive exceptions
pos_exceptions_remain = dict()  # [subject] = [ list ]  // as ppl join groups, TAKE OUT names
pos_exceptions_receive = dict()  # [recipients] = [ senders list ]  // opposite direction
pos_exceptions_absolute = dict()  # [recipients] = [ tier2 ]
pos_exceptions_absolute_count = dict()  # [recipients] = count
pos_degree = dict()  # [subject] = [g1, g2, ...., gn]
pos_student_list = deepcopy(student_list)
pos_student_list_temp = []

pos_exceptions_cnt = [dict(), dict(), dict()]  # [subject] = count
pos_exceptions_cnt_reverse = [dict(), dict(), dict()]  # [count] = [ subjects ]

total_pos_except_cnt = []  # [ tier0_cnt, tier1_cnt, tier2_cnt ]
total_neg_except_cnt = 0

pos_level = dict()  # [student] = happiness level
happiness_list = []  # [happiness value, student]
happiness_list_raw = []  # happiness values
zero_num_list = []  # [ zero_num people ]

# three tiers
''' tier 0: Person A writes Person B, Person B doesn't write Person A
    tier 1: Person A & B writes each other
    tier 2: ABSOLUTE exceptions chosen by GL Lead '''

neg_exceptions = dict()  # [subject] = [ list ]
neg_student_set = set()
neg_student_list = []
neg_student_list_temp = []
neg_degree = dict()  # [subject] = [g1, g2, ..., gn]

# constants
STUDENT_CNT = len(student_list)
NEWLINE = "\n"
SPACER_1 = "\t"
SPACER_2 = ", "

# manual text
break_length = 256
break_str = '-' * break_length
manual_file = open("manual.txt", "r", encoding='utf-8')
manual_text = manual_file.read()
manual_file.close()


def set_group_sizes() -> None:
    res = STUDENT_CNT % GROUP_CNT
    for i in range(GROUP_CNT):
        group_sizes.append(STUDENT_CNT // GROUP_CNT + (i < res))
        groups.append([])


def initialize() -> None:
    global group_sizes, groups, final_group_candidates
    global pos_exceptions_raw, pos_exceptions_tier, pos_exceptions, pos_exceptions_remain, pos_exceptions_receive, \
        pos_exceptions_absolute, pos_exceptions_absolute_count, pos_degree, pos_student_list, pos_student_list_temp
    global pos_exceptions_cnt, pos_exceptions_cnt_reverse
    global total_pos_except_cnt, total_neg_except_cnt
    global pos_level, happiness_list, happiness_list_raw, zero_num_list

    # i was lazy, so i just copied and pasted everything above
    group_sizes = []
    groups = []
    final_group_candidates = []  # [group, average happiness, median happiness, zero_num]

    pos_exceptions_raw = dict()  # [person1] = [ [person2, 0], [person3, 1], ... ]
    pos_exceptions_tier = dict()  # [subject] = [[ tier0 ], [ tier1 ], [ tier2 ]]
    pos_exceptions = dict()  # [subject] = [ list ]  # doesn't include absolute positive exceptions
    pos_exceptions_remain = dict()  # [subject] = [ list ]  // as ppl join groups, TAKE OUT names
    pos_exceptions_receive = dict()  # [recipients] = [ senders list ]  // opposite direction
    pos_exceptions_absolute = dict()  # [recipients] = [ tier2 ]
    pos_exceptions_absolute_count = dict()  # [recipients] = count
    pos_degree = dict()  # [subject] = [g1, g2, ...., gn]
    pos_student_list = deepcopy(student_list)
    pos_student_list_temp = []

    pos_exceptions_cnt = [dict(), dict(), dict()]  # [subject] = count
    pos_exceptions_cnt_reverse = [dict(), dict(), dict()]  # [count] = [ subjects ]

    total_pos_except_cnt = []  # [ tier0_cnt, tier1_cnt, tier2_cnt ]
    total_neg_except_cnt = 0

    pos_level = dict()  # [student] = happiness level
    happiness_list = []  # [happiness value, student]
    happiness_list_raw = []  # happiness values
    zero_num_list = []  # [ zero_num people ]

    for student in student_list:
        pos_exceptions_raw[student] = []
        pos_exceptions_tier[student] = [[], [], []]
        pos_level[student] = 0
        for i in range(3):
            pos_exceptions_cnt[i][student] = 0


def input_pos_except() -> None:
    # input positive exception raw list
    raw_pos_except = pos_exceptions_text.get("1.0", 'end-1c')
    raw_pos_except_split = raw_pos_except.split(NEWLINE)

    if raw_pos_except == "":
        return

    for item in raw_pos_except_split:
        temp_input = item.split(SPACER_1)  # Name1 () Name2, Name3, ...

        subject = temp_input[0]
        recipients = temp_input[1].split(SPACER_2)

        for j in range(len(recipients)):  # iterate for each recipient
            found_flag = False
            for k in range(len(pos_exceptions_raw[recipients[j]])):  # each name in rec
                if pos_exceptions_raw[recipients[j]][k][0] == subject:
                    found_flag = True
                    pos_exceptions_raw[recipients[j]][k][1] += 1
                    break
            if not found_flag:
                pos_exceptions_raw[subject].append([recipients[j], 0])

    # defining pos_exceptions
    for student_key in pos_exceptions_raw.keys():
        for rec_list in pos_exceptions_raw[student_key]:
            pos_exceptions_tier[student_key][rec_list[1]].append(rec_list[0])
            if rec_list[1] == 1:
                pos_exceptions_tier[rec_list[0]][rec_list[1]].append(student_key)


def input_abs_pos_except() -> None:
    # input absolute positive exceptions
    raw_abs_pos_except = abs_pos_exceptions_text.get("1.0", 'end-1c')
    raw_abs_pos_except_split = raw_abs_pos_except.split(NEWLINE)

    if raw_abs_pos_except == "":
        return

    for item in raw_abs_pos_except_split:
        temp_input = item.split(SPACER_2)

        [person1, person2] = list(temp_input)  # INPUT: Name1, Name2 \end
        pos_exceptions_tier[person1][2].append(person2)
        pos_exceptions_tier[person2][2].append(person1)


def input_neg_except() -> None:
    global total_neg_except_cnt
    # input negative exceptions
    raw_neg_except = neg_exceptions_text.get("1.0", 'end-1c')
    raw_neg_except_split = raw_neg_except.split(NEWLINE)

    if raw_neg_except == "":
        return

    total_neg_except_cnt = len(raw_neg_except_split)

    for item in raw_neg_except_split:
        temp_input = item.split(SPACER_2)

        [person1, person2] = list(temp_input)  # INPUT: Name1, Name2 \end
        if person1 in neg_exceptions.keys():
            neg_exceptions[person1].append(person2)
        else:
            neg_exceptions[person1] = [person2]
        if person2 in neg_exceptions.keys():
            neg_exceptions[person2].append(person1)
        else:
            neg_exceptions[person2] = [person1]
        neg_student_set.add(person1)
        neg_student_set.add(person2)
        if person1 in pos_student_list:
            pos_student_list.remove(person1)
        if person2 in pos_student_list:
            pos_student_list.remove(person2)


def update_before_run() -> None:
    global pos_exceptions_cnt, pos_exceptions_cnt_reverse
    global MIN_ZERO_NUM

    MIN_ZERO_NUM = float('inf')

    for student in student_list:
        for i in range(3):
            pos_exceptions_cnt[i][student] = 0
    pos_exceptions_cnt_reverse = [dict(), dict(), dict()]  # [count] = [ subjects ]

    for student in student_list:
        for i in range(3):
            pos_exceptions_cnt[i][student] += len(pos_exceptions_tier[student][i])

    for i in range(3):
        for student in pos_exceptions_cnt[i].keys():
            if pos_exceptions_cnt[i][student] not in pos_exceptions_cnt_reverse[i].keys():
                pos_exceptions_cnt_reverse[i][pos_exceptions_cnt[i][student]] = [student]
            else:
                pos_exceptions_cnt_reverse[i][pos_exceptions_cnt[i][student]].append(student)

    final_group.clear()


def reset_variables() -> None:
    global pos_student_list_temp, neg_student_list, neg_student_list_temp
    global groups, total_pos_except_cnt
    global generate_ready

    groups = [[] for i in range(GROUP_CNT)]
    total_pos_except_cnt = [0, 0, 0]

    random.shuffle(student_list)

    for student in student_list:
        pos_exceptions_receive[student] = []

    for student in student_list:
        pos_degree[student] = [0 for i in range(GROUP_CNT)]
        pos_level[student] = 0

        pos_exceptions[student] = []
        pos_exceptions_remain[student] = []
        pos_exceptions_absolute_count[student] = 0

        for i in range(3):  # only tier0 and tier1 goes inside pos_exceptions & pos_exceptions_remain
            total_pos_except_cnt[i] += len(pos_exceptions_tier[student][i])

            if i != 2:
                pos_exceptions[student] += pos_exceptions_tier[student][i]
                pos_exceptions_remain[student] += pos_exceptions_tier[student][i]
            if i == 2:
                pos_exceptions_absolute[student] = []
                for student2 in pos_exceptions_tier[student][i]:
                    pos_exceptions_absolute[student].append(student2)
                    pos_exceptions_absolute_count[student] += 1
        for student2 in pos_exceptions[student]:
            pos_exceptions_receive[student2].append(student)

    for student in neg_student_set:
        neg_degree[student] = [0 for i in range(GROUP_CNT)]

    total_pos_except_cnt[1] //= 2  # pairs
    total_pos_except_cnt[2] //= 2  # pairs

    pos_student_list_temp = deepcopy(pos_student_list)
    neg_student_list = list(neg_student_set)
    neg_student_list_temp = deepcopy(neg_student_list)

    # update GUI count labels
    pos_except_cnt_label.configure(
        text="Positive Exceptions: {}".format(total_pos_except_cnt[0] + total_pos_except_cnt[1]))
    abs_pos_except_cnt_label.configure(text="Absolute Positive Exceptions: {}".format(total_pos_except_cnt[2]))
    neg_except_cnt_label.configure(text="Negative Exceptions: {}".format(total_neg_except_cnt))

    if total_pos_except_cnt[0] == 0:
        generate_ready = False
        message_label.configure(text="Not Ready. Please Input Exceptions.", fg='red', font=bold_font)
    else:
        generate_ready = True
        message_label.configure(text="Ready to Generate Groups!", fg='green', font=bold_font)


def choose_optimal_person(my_list: list) -> str:
    """Chooses student first with the highest number of absolute positive exceptions,
    then with the least possible number of positive exceptions that can be satisfied and the least number of pos exceptions overall."""
    abs_temp_list = []
    for student in my_list:
        if pos_exceptions_absolute_count[student] != 0:
            abs_temp_list.append([pos_exceptions_absolute_count[student], student])
    if len(abs_temp_list) != 0:
        abs_temp_list.sort(reverse=True)

        abs_temp_num = 0
        while abs_temp_num < len(abs_temp_list) - 1 and abs_temp_list[abs_temp_num][0] == \
                abs_temp_list[abs_temp_num + 1][0]:
            abs_temp_num += 1
        return abs_temp_list[random.randint(0, abs_temp_num)][1]

    temp_list = []
    for student in my_list:
        temp_list.append([len(pos_exceptions_remain[student]), len(pos_exceptions[student]), student])
    temp_list.sort()

    temp_num = 0
    while temp_num < len(temp_list) - 1 and temp_list[temp_num][0] == temp_list[temp_num + 1][0] and \
            temp_list[temp_num][1] == temp_list[temp_num + 1][1]:
        temp_num += 1
    return temp_list[random.randint(0, temp_num)][2]


def distribute_students() -> bool:
    """Two input variables (given_student, given_group_num)
    These are for absolute positive exceptions where given_student HAS to go to given_group_num.
    Both functions are recursive."""
    if not neg_group_distribution(None, None):
        return False
    return pos_group_distribution(None, None)


def neg_group_distribution(given_student: str | None, given_group_num: int | None) -> bool:
    absolute = False

    if len(neg_student_list_temp) == 0:
        return True

    if given_student is not None:
        absolute = True
        student = given_student
        group_num = given_group_num
        if len(groups[group_num]) + 1 >= group_sizes[group_num]:
            return False
    else:
        student = choose_optimal_person(neg_student_list_temp)

        # choose optimal group
        min_neg_lvl = min(neg_degree[student])
        temp_group_select = []
        for i in range(GROUP_CNT):
            if neg_degree[student][i] == min_neg_lvl:
                temp_group_select.append([pos_degree[student][i], i])  # [pos degree, group_num]
        temp_group_select.sort(reverse=True)
        temp_num = 0
        while temp_num < len(temp_group_select) - 1 and temp_group_select[temp_num][0] == \
                temp_group_select[temp_num + 1][0]:
            temp_num += 1
        group_num = temp_group_select[random.randint(0, temp_num)][1]

    if student in neg_student_list_temp:
        neg_student_list_temp.remove(student)
    elif student in pos_student_list_temp:
        pos_student_list_temp.remove(student)

    # update pos_exceptions_remain
    if not absolute:  # pos_exceptions_remain doesn't have absolute
        for student2 in pos_exceptions_receive[student]:
            pos_exceptions_remain[student2].remove(student)

    # update pos/neg degrees
    if student in neg_student_list:  # since if absolute, student may not be in neg list
        for student2 in neg_exceptions[student]:
            neg_degree[student2][group_num] += 1
    for student2 in pos_exceptions[student]:
        pos_degree[student2][group_num] += 1

    # update happiness value
    for groupmate in groups[group_num]:
        if groupmate in pos_exceptions[student]:
            pos_level[student] += 1
            pos_level[groupmate] += 1

    groups[group_num].append(student)

    if len(groups[group_num]) >= group_sizes[group_num]:
        for student2 in pos_student_list:
            pos_degree[student2][group_num] = 0

    # recursively execute function for each student2 with absolute positive exceptions with student1
    for student2 in pos_exceptions_absolute[student]:
        pos_exceptions_absolute[student].remove(student2)
        pos_exceptions_absolute[student2].remove(student)
        neg_group_distribution(student2, group_num)

    # execute function for next student
    neg_group_distribution(None, None)
    return True


def pos_group_distribution(given_student: str | None, given_group_num: int | None) -> bool:
    if len(pos_student_list_temp) == 0:
        return True

    if given_student is not None:
        student = given_student
        group_num = given_group_num
        if len(groups[group_num]) + 1 >= group_sizes[group_num]:
            return False
    else:
        student = choose_optimal_person(pos_student_list_temp)

        # choose optimal group
        max_pos_lvl = max(pos_degree[student])
        temp_group_select = []
        for i in range(GROUP_CNT):
            if pos_degree[student][i] == max_pos_lvl:
                temp_group_select.append([len(groups[i]), i])
        temp_group_select.sort()
        group_num = temp_group_select[0][1]

    # update pos/neg degrees
    for student2 in pos_exceptions[student]:
        pos_degree[student2][group_num] += 1

    groups[group_num].append(student)
    if len(groups[group_num]) >= group_sizes[group_num]:
        for student2 in pos_student_list:
            pos_degree[student2][group_num] = 0

    # update happiness value
    for groupmate in groups[group_num]:
        if groupmate in pos_exceptions[student]:
            pos_level[student] += 1
        if student in pos_exceptions[groupmate]:
            pos_level[groupmate] += 1

    pos_student_list_temp.remove(student)

    # recursively execute function for each student2 with absolute positive exceptions with student1
    for student2 in pos_exceptions_absolute[student]:
        if student2 in pos_student_list_temp:
            pos_group_distribution(student2, group_num)

    # execute function for next student
    pos_group_distribution(None, None)
    return True


def calculate_happiness() -> None:
    happiness_list.clear()
    happiness_list_raw.clear()
    zero_num_list.clear()

    for student in student_list:
        if len(pos_exceptions[student]) == 0:
            happiness_list.append([POS_EXCEPT_CNT, student])
            happiness_list_raw.append(POS_EXCEPT_CNT)
        else:
            happiness_list.append([pos_level[student], student])
            happiness_list_raw.append(pos_level[student])
    happiness_list.sort()
    happiness_list_raw.sort()

    global temp_zero_num, average_happiness, median_happiness
    temp_zero_num = 0
    while happiness_list_raw[temp_zero_num] == 0:
        temp_zero_num += 1
    for i in range(temp_zero_num):
        zero_num_list.append(happiness_list[i][1])

    average_happiness = sum(happiness_list_raw) / STUDENT_CNT
    median_happiness = happiness_list_raw[STUDENT_CNT // 2]


def calculate_gender() -> float:
    # returns standard deviation for male/female distribution in percent, assuming mean of 0.5
    gender_list = []
    gender_stddev_list = []
    for i in range(GROUP_CNT):
        male_cnt = 0
        for student in groups[i]:
            male_cnt += ('Male' == gender_dict[student])
        gender_list.append(male_cnt / group_sizes[i])
    mean = 0.5
    for value in gender_list:
        gender_stddev_list.append((value - mean) ** 2)
    std_dev = math.sqrt(sum(gender_stddev_list) / GROUP_CNT)
    return std_dev


def update_progress(progress: float) -> None:  # given in decimals
    global prog_bar, perc_label
    progress = float(progress)
    if progress >= 1:
        progress = 1
        prog_bar.stop()
        perc_label.configure(text="Done!")
    prog_bar.configure(value=int(progress * 100))
    perc_label.configure(text="Generating... {}%".format(int(progress * 100)))
    root.update()


def choose_delete_pos_except_1() -> tuple[None, None] | tuple[str, str]:
    """Deleting tier1 as ppl still have a chance to get their 'partners', whereas tier0 ppl have no chance if erased"""

    while True:
        if len(pos_exceptions_cnt_reverse[1].keys()) == 0:
            return None, None
        delete_candidates = pos_exceptions_cnt_reverse[1][max(pos_exceptions_cnt_reverse[1].keys())]
        if len(delete_candidates) > 0:
            print("\nDelete candidates: {}".format(delete_candidates))
            break
        else:
            pos_exceptions_cnt_reverse[1].pop(max(pos_exceptions_cnt_reverse[1].keys()))

    final_candidate = random.sample(delete_candidates, 1)[0]
    try:
        final_recipient = random.sample(pos_exceptions_tier[final_candidate][1], 1)[0]
        print("Final Candidate: {}, Final Recipient: {}".format(final_candidate, final_recipient))
        return final_candidate, final_recipient
    except ValueError:
        print("Failed to find delete candidates")
        return None, None


def delete_pos_except_1() -> bool:
    global delete_cnt_entry

    try:
        it_cnt = int(delete_cnt_entry.get())
        success = False

        for i in range(it_cnt):
            final_candidate, final_recipient = choose_delete_pos_except_1()
            if final_candidate is None:
                print("Cannot delete any more positive exceptions")
                break
            success = True

            # edit data for final_candidate
            pos_exceptions_tier[final_candidate][1].remove(final_recipient)

            prev_tier1_cnt = pos_exceptions_cnt[1][final_candidate]
            pos_exceptions_cnt[1][final_candidate] -= 1
            pos_exceptions_cnt_reverse[1][prev_tier1_cnt].remove(final_candidate)
            pos_exceptions_cnt_reverse[1][prev_tier1_cnt - 1].append(final_candidate)

            # edit data for final_recipient
            pos_exceptions_tier[final_recipient][1].remove(final_candidate)
            pos_exceptions_tier[final_recipient][0].append(final_candidate)

            prev_tier1_cnt = pos_exceptions_cnt[1][final_recipient]
            pos_exceptions_cnt[1][final_recipient] -= 1
            pos_exceptions_cnt_reverse[1][prev_tier1_cnt].remove(final_recipient)
            pos_exceptions_cnt_reverse[1][prev_tier1_cnt - 1].append(final_recipient)
            pos_exceptions_cnt[1][final_candidate] += 1

            update_before_run()
            reset_variables()

        if success:
            update_before_run()
            reset_variables()
            delete_toplevel.destroy()
            return True
        else:
            return False
    except ValueError:
        return False


# tkinter code

def show_manual() -> None:
    global manual_text
    manual_toplevel = Toplevel()
    manual_toplevel.title("Program Manual")
    manual_toplevel.option_add("*font", default_font)
    manual_toplevel.geometry("1100x950+400+150")

    manual_all_frame = Frame(manual_toplevel)
    manual_all_frame.place(relx=.5, rely=.5, anchor=CENTER)
    manual_label = Label(manual_all_frame, text=manual_text, width=150, wraplength=1050)
    manual_label.grid(row=0, column=0)


def update_exceptions_enter(event) -> None:
    update_exceptions()


def update_exceptions() -> None:
    # initialize all variables
    initialize()
    set_group_sizes()

    # input exceptions
    input_pos_except()
    input_abs_pos_except()
    input_neg_except()
    update_before_run()
    reset_variables()
    print("Exceptions Successfully Updated")


def delete_exceptions() -> None:
    global delete_toplevel, delete_cnt_entry

    delete_toplevel = Toplevel()
    delete_toplevel.title("Transfer Menu")
    delete_toplevel.geometry("400x200")
    delete_toplevel.option_add("*font", default_font)

    delete_allframe = Frame(delete_toplevel)
    delete_allframe.place(relx=.5, rely=.5, anchor=CENTER)

    # notice frame
    notice_frame = Frame(delete_allframe)
    notice_frame.grid(row=0, column=0, sticky='ew')

    Label(notice_frame, text="**Some Tier 1 Exceptions will be changed to Tier 0.\n"
                             "Number of overall Positive Exceptions doesn't change.**", font=italic_font).grid(row=0,
                                                                                                              column=0)

    # tier count frame
    tier_cnt_frame = Frame(delete_allframe, bg='light gray')
    tier_cnt_frame.grid(row=1, column=0, pady=10, ipadx=20, sticky='ew')
    tier_cnt_frame.grid_rowconfigure(0, weight=1)
    tier_cnt_frame.grid_columnconfigure(0, weight=1)

    Label(tier_cnt_frame, text="Current Positive Exceptions", bg='light gray', font=bold_font).grid(row=0, column=0)
    tier0_cnt_label = Label(tier_cnt_frame, text="Positive Exceptions (Tier 0): {}".format(total_pos_except_cnt[0]),
                            bg='light gray')
    tier0_cnt_label.grid(row=1, column=0)
    tier1_cnt_label = Label(tier_cnt_frame, text="Positive Exceptions (Tier 1): {}".format(total_pos_except_cnt[1]),
                            bg='light gray')
    tier1_cnt_label.grid(row=2, column=0)

    # delete frame
    delete_input_frame = Frame(delete_allframe)
    delete_input_frame.grid(row=2, column=0, pady=10)

    Label(delete_input_frame, text="Number of Exceptions to Transfer: ").grid(row=0, column=0)
    delete_cnt_entry = Entry(delete_input_frame, width=5)
    delete_cnt_entry.grid(row=0, column=1)

    # ok/cancel frame
    ok_cancel_frame = Frame(delete_allframe)
    ok_cancel_frame.grid(row=3, column=0)

    cancel_bt = Button(ok_cancel_frame, text="Cancel", height=1, width=10, command=delete_toplevel.destroy)
    cancel_bt.grid(row=0, column=0, padx=10)
    ok_bt = Button(ok_cancel_frame, text="Transfer", height=1, width=10, command=delete_pos_except_1)
    ok_bt.grid(row=0, column=1, padx=10)


def generate_progress_level() -> None:
    global generating_toplevel, prog_bar, perc_label
    if generate_ready:
        generating_toplevel = Toplevel()
        generating_toplevel.geometry("300x120+500+300")
        generating_toplevel.option_add("*font", default_font)

        generating_all_frame = Frame(generating_toplevel)
        generating_all_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # progress bar
        prog_bar = ttk.Progressbar(generating_all_frame, orient='horizontal', mode='determinate', length=250)
        prog_bar.grid(row=0, column=0, pady=5)

        # percentage label
        perc_label = Label(generating_all_frame, text="Generating... 0%")
        perc_label.grid(row=1, column=0, pady=5)

        prog_bar.after(100, generate_groups)


def generate_groups() -> None:
    global temp_zero_num, average_happiness, median_happiness, MIN_ZERO_NUM, final_group
    global generating_toplevel, prog_bar, perc_label

    random.seed(random.random())
    update_before_run()

    update_progress_list = [int(ITERATION_CNT * 0.02 * i) for i in range(51)]
    update_progress(0)

    for i in range(ITERATION_CNT):
        reset_variables()
        if not distribute_students():
            continue
        calculate_happiness()

        if calculate_gender() > GENDER_RATIO:
            continue
        if temp_zero_num < MIN_ZERO_NUM:
            MIN_ZERO_NUM = temp_zero_num
            final_group_candidates.clear()
        if temp_zero_num <= MIN_ZERO_NUM:
            final_group_candidates.append(
                [groups, average_happiness, median_happiness, temp_zero_num, deepcopy(zero_num_list)])
        if i in update_progress_list:
            update_progress((i + 1) / ITERATION_CNT)
    update_progress(1)

    max_happiness = 0
    for group in final_group_candidates:
        max_happiness = max(max_happiness, group[1])
    for group in final_group_candidates:
        if group[1] == max_happiness:
            final_group = group
            break

    generating_toplevel.destroy()
    display_results()


def display_results() -> None:
    results_window = Toplevel()
    results_window.title("Group Results")
    results_window.geometry("600x800+400+300")
    results_window.option_add("*font", default_font)
    results_window.grid_rowconfigure(0, weight=1)
    results_window.grid_columnconfigure(0, weight=1)

    # parent frame
    group_all_frame = Frame(results_window)
    group_all_frame.place(relx=.5, rely=.5, anchor=CENTER)

    Label(group_all_frame, text="Group Distribution Results", bg='yellow').grid(row=0, column=0, sticky='ew')

    # stats frame
    stats_frame = Frame(group_all_frame, bg='light gray')
    stats_frame.grid(row=1, column=0, sticky='we')
    stats_frame.grid_rowconfigure(0, weight=1)
    stats_frame.grid_columnconfigure(0, weight=1)

    stats_label = Label(stats_frame, text="Average Happiness: {}\nMedian Happiness: {}\nZero Num: {} --> {}".format(
        final_group[1], final_group[2], final_group[3], final_group[4]), width=80, bg='light gray', wraplength=550)
    stats_label.grid(row=0, column=0)

    # results frame
    group_results_frame = Frame(group_all_frame, width=600, height=710)
    group_results_frame.grid(row=2, column=0)

    global results_canvas, canvas_frame, results_grid_frame
    results_canvas = Canvas(group_results_frame)
    results_canvas.option_add("*font", default_font)

    canvas_frame = Frame(results_canvas)

    scroll_bar = Scrollbar(group_results_frame, orient="vertical", command=results_canvas.yview)
    results_canvas.configure(yscrollcommand=scroll_bar.set)

    scroll_bar.pack(side='right', fill='y')
    results_canvas.pack(side='left')

    results_canvas.create_window((0, 0), window=canvas_frame, anchor='nw')
    canvas_frame.bind("<Configure>", canvas_configure)

    results_grid_frame = Frame(canvas_frame)
    results_grid_frame.grid(row=0, column=0)

    fill_groups()


def fill_groups() -> None:
    global canvas_frame, results_grid_frame, display_text_list
    display_text_list = []
    for i in range(GROUP_CNT):
        Label(results_grid_frame, text="Group {}:".format(i + 1), font=group_bold_font).grid(row=(i // 2) * 2,
                                                                                             column=i % 2, pady=(5, 0))
        display_text_list.append(Text(results_grid_frame, width=40, height=len(final_group[0][i])))
    for i in range(GROUP_CNT):
        # config
        display_text_list[i].config(spacing1=2, spacing2=3, spacing3=2)

        # text insert
        text = ''
        display_text_list[i].grid(row=(i // 2) * 2 + 1, column=i % 2, pady=(0, 5))
        for name in final_group[0][i]:
            text += name + "\n"
        display_text_list[i].tag_configure("tag_name", justify='center')
        display_text_list[i].insert('1.0', text[:-1])
        display_text_list[i].tag_add("tag_name", "1.0", "end")


def canvas_configure(event) -> None:
    global results_canvas
    results_canvas.configure(scrollregion=results_canvas.bbox("all"), width=570, height=710)


# set fonts
default_font = 'Roboto 10'
bold_font = 'Roboto 10 bold'
italic_font = 'Roboto 10 italic'

group_default_font = 'Roboto 12'
group_bold_font = 'Roboto 12 bold'
group_italic_font = "Roboto 12 italic"

# tkinter code
root = Tk()

root.title("Group Distribution Program")
root.option_add("*font", default_font)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.geometry("+300+200")

all_frame = Frame(root)
all_frame.grid(row=0, column=0)

display_title = Label(all_frame, text="Group Distribution Settings", bg='yellow', width=80)
display_title.grid(row=0, column=0)

# manual frame
manual_frame = Frame(all_frame)
manual_frame.grid(row=1, column=0, pady=(15, 0))

manual_button = Button(manual_frame, text="Program Manual", width=25, command=show_manual)
manual_button.grid(row=0, column=0)

# exception input frame
input_frame = Frame(all_frame)
input_frame.grid(row=2, column=0, pady=10)

exception_label = Label(input_frame, text="Input Exceptions", font=bold_font)
exception_label.grid(row=0, column=0, columnspan=2)

# exception labels
Label(input_frame, text="Positive Exceptions: ", width=25).grid(row=1, column=0)
Label(input_frame, text="Absolute Positive Exceptions: ", width=25).grid(row=2, column=0)
Label(input_frame, text="Negative Exceptions: ", width=25).grid(row=3, column=0)

# exception update button
update_exception_button = Button(input_frame, text="Update Exceptions", width=25, command=update_exceptions)
update_exception_button.grid(row=4, column=0, columnspan=2)

# exception texts
pos_exceptions_text = Text(input_frame, height=1, width=55)
pos_exceptions_text.grid(row=1, column=1)
pos_exceptions_text.bind("<Return>", update_exceptions_enter)

abs_pos_exceptions_text = Text(input_frame, height=1, width=55)
abs_pos_exceptions_text.grid(row=2, column=1)
abs_pos_exceptions_text.bind("<Return>", update_exceptions_enter)

neg_exceptions_text = Text(input_frame, height=1, width=55)
neg_exceptions_text.grid(row=3, column=1)
neg_exceptions_text.bind("<Return>", update_exceptions_enter)

# exception count frame
count_frame = Frame(all_frame, bg='light gray')
count_frame.grid(row=3, column=0, pady=10, ipadx=20)
count_frame.grid_rowconfigure(0, weight=1)
count_frame.grid_columnconfigure(0, weight=1)

count_label = Label(count_frame, text="Current Exceptions Count", font=bold_font, bg='light gray')
count_label.grid(row=0, column=0)

# count labels
pos_except_cnt_label = Label(count_frame, text="Positive Exceptions: 0", bg='light gray')
pos_except_cnt_label.grid(row=1, column=0)

abs_pos_except_cnt_label = Label(count_frame, text="Absolute Positive Exceptions: 0", bg='light gray')
abs_pos_except_cnt_label.grid(row=2, column=0)

neg_except_cnt_label = Label(count_frame, text="Negative Exceptions: 0", bg='light gray')
neg_except_cnt_label.grid(row=3, column=0)

# buttons frame
button_frame = Frame(all_frame)
button_frame.grid(row=4, column=0)

# buttons
delete_except_bt = Button(button_frame, text="Transfer Exceptions (Make More Fair)", height=1, width=30,
                          command=delete_exceptions)
delete_except_bt.grid(row=0, column=0, padx=10, pady=5)
generate_groups_bt = Button(button_frame, text="Generate Groups", height=1, width=30, command=generate_progress_level)
generate_groups_bt.grid(row=0, column=1, padx=10, pady=5)

# global variable (determines if code is ready to be run) default: False
generate_ready = False

# message frame
message_frame = Frame(all_frame)
message_frame.grid(row=5, column=0, pady=10)

# message label
message_label = Label(message_frame, bg='light gray', width=80)
message_label.grid(row=0, column=0)

update_exceptions()

root.mainloop()
