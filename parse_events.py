import json
import pickle


def parse_event_data(verticals_dict):
    users = pickle.load(open("users.pickled", "r"))

    with open("data.json") as json_file:
        json_data = json.load(json_file)
        
    # stores the number of times a vertical gets a "hit" in list of dictionaries,
    # i.e. [{"vertical_id": a7315890a40a4877913564af13fcdf5e", "hits": 5},
    #       {"vertical_id": f17a1fbcc2234c33b74dca3fdc341551", "hits": 5}] 
    hit_count = {}
    for user in users:
        events = users[user]
        for event in events:
            event_id = event["vertical_id"]
            print event_id
            vertical_id = verticals_dict.get(event_id)
            print vertical_id

            exit()
        # # print events
        # exit()

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

    return final_dict

def main():
    course_structure = parse_course_structure()
    verticals_dict = generate_verticals(course_structure)
    sequentials_dict = generate_sequentials(course_structure)
    chapters_dict = generate_chapters(course_structure)

    parse_event_data(verticals_dict)

if __name__ == '__main__':
    main()