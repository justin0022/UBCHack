import json
import pickle


def parse_event_data():
    users = pickle.load(open("users.pickled", "r"))

    for row in users["1"]:
        print row

def main():
    parse_event_data()

if __name__ == '__main__':
    main()