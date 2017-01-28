#!/usr/bin/env python

import json


def parse_course_structure():

    course_structure = []

    f = open("course_axis.tsv", "r")

    header_row = f.readline().split()
    for line in f:
        line = line.split("\t")
        row = {}

        for i, element in enumerate(line):
            row[header_row[i]] = element.strip()

        course_structure.append(row)

    return course_structure


def parse_user_data():
    user_data = []

    f = open("tracklog_cleaned.tsv", "r")

    header_row = f.readline().split()
    for line in f:
        print(line)
        exit()



def generate_json_object():
    pass


def main():

    course_structure = parse_course_structure()






if __name__ == '__main__':
    main()