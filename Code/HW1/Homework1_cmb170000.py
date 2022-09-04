'''
    To run: python3 Homework1_cmb170000.py data/data.csv
    Make sure data is in same directory subfolder called data
'''

import sys
import os
import re
import pickle


class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("\t", self.first, self.mi, self.last)
        print("\t", self.phone)


# read in the lines of the csv file
def read_lines():
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        current_dir: str = os.getcwd()

        with open(os.path.join(current_dir, fp), 'r') as f:
            # read each line into it's own array, split on comma
            lines = [line.rstrip().split(',') for line in f]

        return lines[1:]


def format_persons(data):
    temp_ids = []
    persons = {}

    # make a list of temporary id's to compare against
    for person in data:
        temp_ids.append(person[3])

    for person in data:
        temp_id = person[3]
        temp_phone = person[4]
        temp_mid = "X" if not person[2] else person[2].capitalize()

        # check if id is correct format
        while not re.search("[a-zA-Z]{2}\d{4}", temp_id):
            print("ID is invalid:", temp_id)
            print("ID is two letters followed by 4 digits")
            temp_id = input("Enter a valid id: ")

            # check if duplicate
            if temp_id in temp_ids:
                temp_id = person[3]
                print("Entered ID is already in use, please enter another.")
            else:
                temp_ids.append(temp_id)

            print("")

        # have user input correctly formatted phone number
        while not re.search("^\d{3}-\d{3}-\d{4}$", temp_phone):
            print("Phone is invalid:", temp_phone)
            print("Enter phone number in form 123-456-7890")
            temp_phone = input("Enter a valid phone number: ")
            print("")

        persons[temp_id] = Person(person[0].capitalize(
        ), person[1].capitalize(), temp_mid, temp_id, temp_phone)

    return persons


if __name__ == '__main__':
    data = read_lines()

    # format the persons into a dict
    data = format_persons(data)
    print("Employee list: \n")

    # write to pickle file
    with open('filename.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    for person in data:
        print("Employee ID:", person)
        data[person].display()
        print()
