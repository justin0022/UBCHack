#!/usr/bin/env python

import json
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


def generate_json_object(course_data):
    
    final_dict = {}

    for row in course_data:
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

        elif row["category"] in ["html", "video", "problem"]:

            vertical_id = row["parent"]

            all_chapters = [ch["children"] for ch in final_dict["children"]]

            all_sequentials_flattened = []

            for sequential_list in all_chapters:
                for sequential in sequential_list:
                    all_sequentials_flattened.append(sequential)
            
            all_verticals_flattened = []

            for sequential in all_sequentials_flattened:
                for vertical in sequential["children"]:
                    all_verticals_flattened.append(vertical)

            vertical = [ve for ve in all_verticals_flattened if ve["url_name"] == vertical_id][0]

            vertical["children"].append({"category": row["category"], "name": row["name"], "element_order": row["element_order"], "url_name": row["url_name"], "parent": row["parent"]})
    
    
   



    json_obj = json.dumps(final_dict)

    fout = open("data.json", "w")
    fout.write(json_obj)
    print(json_obj)


def main():

    course_structure = parse_course_structure()
    
    generate_json_object(course_structure)


if __name__ == '__main__':
    main()