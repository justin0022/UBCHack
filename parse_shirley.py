#!/usr/bin/env python

import json
import datetime
from collections import defaultdict
import pickle


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


def parse_user_data(verticals):

    # f = open("person_course_cleaned.tsv", "r")

    # users = {}
    # # users is a dictionary of format
    # # {'4664': datetime.datetime(2015, 11, 13, 2, 37, 7)}
    # # where the key is the user_id and the value is the start_date of that user
    # header_row = f.readline().split()
    # for line in f:
    #     line = line.split("\t")

    #     user_id = ""
    #     for i, element in enumerate(line):
    #         if header_row[i] == "user_id":
    #             user_id = element.strip()
    #         elif header_row[i] == "start_time":
    #             users[user_id] = datetime.datetime.strptime(element.strip(), '%Y-%m-%dT%XZ')



    f = open("tracklog_cleaned_sorted.tsv", "r")

    header_row = f.readline().split()

    users = defaultdict(list)

    for line in f:
        line = line.split("\t")
        row = {}

        for i, element in enumerate(line):
            row[header_row[i]] = element.strip()


        user_id = row["user_id"]
        time = datetime.datetime.strptime(row["time"], '%Y-%m-%dT%XZ')
        event_type = row["event_type"]
        if ("video" in row["event_type"]) or ("speed" in row["event_type"]):

            event = row["event"].replace('""', '"')
            if event.startswith('"'):
                event = event[1:]
            if event.endswith('"'):
                event = event[:-1]
            event = json.loads(event)

            vertical_id = str(event["id"])

            # handle broken IDs in dataset
            if vertical_id == "05590450559045b545844eaaa561fe09391213f":
                vertical_id = "0559045b545844eaaa561fe09391213f"
            elif vertical_id == "97055169705516d01b5406c82d0ef9ec6eacce1":
                continue
            if len(vertical_id) == 39:
                print(vertical_id)

            users[user_id].append({"time": time, "event_type": event_type, "vertical_id": vertical_id})
        elif row["event_type"] == "problem_show":
            event = row["event"].replace('""', '"')
            if event.startswith('"'):
                event = event[1:]
            if event.endswith('"'):
                event = event[:-1]
            event = json.loads(event)
            vertical_id = str(event["problem"].split("@")[-1])
            # print(vertical_id, len(vertical_id), event_type)
            if len(vertical_id) == 39:
                print(row)

            users[user_id].append({"time": time, "event_type": event_type, "vertical_id": vertical_id})
            
        elif "problem" in row["event_type"]:
            if row["event"] == "NA":
                continue
            vertical_id = row["event"].split("input_")[1].split("_")[0]
            
            # print(vertical_id, len(vertical_id), event_type)
            if len(vertical_id) == 39:
                print(row)
            users[user_id].append({"time": time, "event_type": event_type, "vertical_id": vertical_id})
        elif "transcript" in row["event_type"]:
            event = row["event"].replace('""', '"')
            if event.startswith('"'):
                event = event[1:]
            if event.endswith('"'):
                event = event[:-1]
            event = json.loads(event)

            vertical_id = str(event["id"])
            # print(vertical_id, len(vertical_id), event_type)

            if len(vertical_id) == 39:
                print(row)

            users[user_id].append({"time": time, "event_type": event_type, "vertical_id": vertical_id})


        # if event time is greater than the stored event time, replace it
        # if time_offset > engagement_data[vertical_id][user_id]:
        #     engagement_data[vertical_id][user_id] + time_offset


    pickle.dump(users, open("users.pickled", "w"))


def parse_time_data():
    users = pickle.load(open("users.pickled", "r"))
    for user in users:
        print(user)
        print(users[user])
        exit()


def generate_verticals(data):
    """
    generates dictionary to look up vertical ID from element ID
    """

    final_dict = {}

    for row in data:
        if row["category"] in ["html", "video", "problem"]:
            vertical_id = row["parent"]
            final_dict[row["url_name"]] = vertical_id

    return final_dict


def generate_chapters(data):
    final_dict = {}

    for row in data:
        if row["category"] in ["sequential"]:
            chapter_id = row["parent"]
            final_dict[row["url_name"]] = chapter_id

    print(final_dict)
    return final_dict


def generate_json_object(data):
    
    final_dict = {}

    for row in data:
        if row["category"] == "course":
            final_dict["course"] = row["name"]
            final_dict["element_order"] = row["element_order"]
            final_dict["children"] = []
        elif row["category"] == "chapter":
            final_dict["children"].append({"category": row["category"], "name": row["name"], "element_order": row["element_order"], "url_name": row["url_name"], "parent": row["parent"], "children": []})
        elif row["category"] == "sequential":
            chapter = [ch for ch in final_dict["children"] if ch["url_name"] == row["parent"]][0]

            chapter["children"].append({"category": row["category"], "name": row["name"], "element_order": row["element_order"], "url_name": row["url_name"], "parent": chapter["url_name"], "children": []})

        elif row["category"] == "vertical":
            sequential_id = row["parent"]
            all_chapters = [ch["children"] for ch in final_dict["children"]]

            all_sequentials_flattened = []

            for sequential_list in all_chapters:
                for sequential in sequential_list:
                    all_sequentials_flattened.append(sequential)
            
            sequential = [sq for sq in all_sequentials_flattened if sq["url_name"] == sequential_id][0]

            sequential["children"].append({"category": "vertical", "name": row["name"], "element_order": row["element_order"], "url_name": row["url_name"], "parent": row["parent"], "children": []})

    json_obj = json.dumps(final_dict)

    fout = open("data_without_last_level.json", "w")
    fout.write(json_obj)


def main():

    course_structure = parse_course_structure()
    verticals_dict = generate_verticals(course_structure)
    chapters_dict = generate_chapters(course_structure)
    
    # parse_user_data(verticals_dict)
    # time_data = parse_time_data()
    
    # generate_json_object(course_structure)





if __name__ == '__main__':
    main()