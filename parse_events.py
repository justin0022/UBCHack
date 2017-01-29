import json
import pickle

def parse_event_data(chapters_dict, sequentials_dict, verticals_dict):
    users = pickle.load(open("users.pickled", "r"))

    f = open("data.json", "r").read()
    obj = json.loads(f)
        
    # stores the number of times a vertical gets a "hit" in list of dictionaries,
    # i.e. [{"vertical_id": a7315890a40a4877913564af13fcdf5e", "hits": 5},
    #       {"vertical_id": f17a1fbcc2234c33b74dca3fdc341551", "hits": 5}] 
    vertical_id_hit_list = []
    for user in users:
        events = users[user]
        for event in events:
            event_id = event["vertical_id"]
            #print event_id
            vertical_id = verticals_dict.get(event_id)
            #print vertical_id

            if not vertical_id:
                continue

            hitBool  = 0
            for vertical_id_hit in vertical_id_hit_list:
                if vertical_id_hit["vertical_id"] == vertical_id:
                    vertical_id_hit["hit"] += 1
                    hitBool = 1
            
            if not hitBool:
                vertical_id_hit_list.append({"vertical_id": vertical_id, "hit": 1})
            
    for vertical_id_hit in vertical_id_hit_list:
        vertical_id = vertical_id_hit["vertical_id"]
        sequential_id = sequentials_dict.get(vertical_id)
        print("sequential_id", sequential_id)
        if not sequential_id:
            continue

        chapter_id = chapters_dict.get(sequential_id)
        print("chapter_id", chapter_id)
        if not chapter_id:
            continue

        chapters_list = obj["children"]
        target_chapter = [chapter for chapter in chapters_list if chapter["url_name"] == chapter_id][0]

        sequentials_list = target_chapter["children"]
        target_sequential = [s for s in sequentials_list if s["url_name"] == sequential_id][0]

        verticals_list = target_sequential["children"]
        target_vertical = [v for v in verticals_list if v["url_name"] == vertical_id][0]

        target_vertical["hit"] = vertical_id_hit["hit"]

        #print target_vertical
    json_obj = json.dumps(obj)
    fout = open("data_with_vertical_hits.json", "w")
    fout.write(json_obj)

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

    parse_event_data(chapters_dict, sequentials_dict, verticals_dict)

if __name__ == '__main__':
    main()