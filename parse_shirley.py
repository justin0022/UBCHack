#!/usr/bin/env python

import json
import datetime
from collections import defaultdict
import pickle
import matplotlib.pyplot as plt


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


def parse_time_data(chapters_dict, sequentials_dict, verticals_dict):
    users = pickle.load(open("users.pickled", "r"))
    
    # for row in users["1"]:
    #     print row

    # differences = [(t["time"] - s["time"]).total_seconds() for s, t in zip(users["1"], users["1"][1:])]
    # for i, d in enumerate(differences):
    #     print users["1"][1:][i]["event_type"], d

    # # plt.hist(differences, bins=30)
    # # plt.show()

    threshold = 1800  # 30 minutes

    # differences_threshold = [d for d in zip(differences) if (d <= threshold and d > 0)]



    # plt.hist(differences_threshold, bins=30)
    # plt.show()

    f = open("data.json", "r").read()
    obj = json.loads(f)

    for user in users:
        events = users[user]
        durations = [(t["vertical_id"], (t["time"] - s["time"]).total_seconds()) for s, t in zip(events, events[1:])]

        durations_thresholded = [d for d in durations if (d[1] <= threshold and d[1] > 0)]

        for duration in durations_thresholded:
            elem_id = duration[0]
            duration_s = duration[1]

            vertical_id = verticals_dict.get(elem_id)
            if not vertical_id:
                print("vertical_id", vertical_id, "elem_id", elem_id)
                continue

            sequential_id = sequentials_dict.get(vertical_id)
            if not sequential_id:
                print("sequential_id", sequential_id, "vertical_id", vertical_id, "elem_id", elem_id)
                continue

            chapter_id = chapters_dict.get(sequential_id)
            if not chapter_id:
                print("chapter_id", chapter_id, "sequential_id", sequential_id, "vertical_id", vertical_id, "element id", elem_id)
                continue

            chapters_list = obj["children"]
            target_chapter = [chapter for chapter in chapters_list if chapter["url_name"] == chapter_id][0]

            sequentials_list = target_chapter["children"]
            target_sequential = [s for s in sequentials_list if s["url_name"] == sequential_id][0]

            verticals_list = target_sequential["children"]
            target_vertical = [v for v in verticals_list if v["url_name"] == vertical_id][0]


            if "duration" in target_vertical:
                target_vertical["duration"] += duration_s
            else:
                target_vertical["duration"] = duration_s

    json_obj = json.dumps(obj)

    fout = open("data_with_durations.json", "w")
    fout.write(json_obj)


def sum_levels_engagement():

    f = open("data_with_durations.json", "r").read()
    obj = json.loads(f)

    chapters = obj["children"]
    for chapter in chapters:
        sequentials = chapter["children"]
        for sequential in sequentials:
            verticals = sequential["children"]
            s_durations = [v.get("duration", 0) for v in verticals]
            s_durations_sum = sum(s_durations)
            if s_durations_sum > 0:
                sequential["duration"] = s_durations_sum

        c_durations = [s.get("duration", 0) for s in sequentials]
        c_durations_sum = sum(c_durations)
        if c_durations_sum > 0:
            chapter["duration"] = c_durations_sum

    json_obj = json.dumps(obj)

    fout = open("data_with_durations_multilevel.json", "w")
    fout.write(json_obj)


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


def generate_sequentials(data):
    """
    generates dictionary to look up chapter ID from vertical ID
    """
    final_dict = {}

    for row in data:
        if row["category"] == "vertical":
            vertical_id = row["parent"]
            final_dict[row["url_name"]] = vertical_id

    print(final_dict)
    return final_dict


def generate_chapters(data):
    """
    generates dictionary to look up chapter ID from vertical ID
    """
    final_dict = {}

    for row in data:
        if row["category"] == "sequential":
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

    # course_structure = parse_course_structure()
    # verticals_dict = generate_verticals(course_structure)
    # sequentials_dict = generate_sequentials(course_structure)
    # chapters_dict = generate_chapters(course_structure)
    
    # parse_user_data(verticals_dict)
    # parse_time_data(chapters_dict, sequentials_dict, verticals_dict)
    
    # generate_json_object(course_structure)

    sum_levels_engagement()



if __name__ == '__main__':
    main()