# Copyright (C) 2019 Loumeau, Masseria, McDonald
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Used for iterating over standard in (sys.stdin).
import sys


# Used only in testing to print dictionaries in a way which is readable.
from pprint import pprint


# Example person (key 1 is a list of parents, key 2 is spouse, key 3 is children):
# family_tree = {
#     person_name_string : {
#         1 : ['parent_1_name_string', 'parent_2_name_string'],
#         2 : 'spouse_name_string',
#         3 : ['child_name_string', ...]
#     }
# }
family_tree = {}


# Create the people (as sub-dictionaries) if they do not exist, set as each
# other's spouse in either case.
def event_marriage(person_1, person_2) :
    if person_1 not in family_tree :
        family_tree.update({person_1: {
            1 : [],
            2 : person_2,
            3 : []
        }})

    else :
        family_tree[person_1][2] = person_1

    if person_2 not in family_tree :
        family_tree.update({person_2: {
            1 : [],
            2 : person_1,
            3 : []
        }})

    else :
        family_tree[person_2][2] = person_2


# Makes sure the parents exist and are married, then creates the child and
# points the people at one another.
def event_child(person_1, person_2, child) :
    event_marriage(person_1, person_2)

    family_tree.update({child: {
        1: [person_1,person_2],
        2: '',
        3: []
    }})

    family_tree[person_1][3].append(child)
    family_tree[person_2][3].append(child)


#
def x_query_child(child, person) :
    print('Is ' + child + ' a child of ' + person + '?')


#
def x_query_sibling(sibling, person) :
    print('Is ' + sibling + ' a sibling of ' + person + '?')


#
def x_query_ancestor(ancestor, person) :
    print('Is ' + ancestor + ' an ancestor of ' + person + '?')


#
def x_query_cousin(cousin, degree, person) :
    print('Is ' + cousin + ' a ' + degree + ' degree cousin of ' + person + '?')


#
def x_query_unrelated(non_relative, person) :
    print('Is ' + non_relative + ' not a relative of ' + person + '?')


#
def w_query_child(person) :
    print('List all children of ' + person + '.')


#
def w_query_sibling(person) :
    print('List all siblings of ' + person + '.')


#
def w_query_ancestor(person) :
    print('List all ancestors of ' + person + '.')


#
def w_query_cousin(person, degree) :
    print('List all ' + degree + ' cousins of ' + person + '.')


#
def w_query_unrelated(person) :
    print('List all people unrelated to ' + person + '.')



# GETTERS, SETTERS, HELPER METHODS, ETC



# Determines the type of query based on contents and length of the split-up string.
def parse_line(split_line) :
    if split_line[0] == 'E' :
        if len(split_line) == 3 :
            event_marriage(split_line[1], split_line[2])

        else :
            event_child(split_line[1], split_line[2], split_line[3])

    if split_line[0] == 'X' :
        if (split_line[2] == 'child') :
            x_query_child(split_line[1], split_line[3])

        elif (split_line[2] == 'sibling') :
            x_query_sibling(split_line[1], split_line[3])

        elif (split_line[2] == 'ancestor') :
            x_query_ancestor(split_line[1], split_line[3])

        elif (split_line[2] == 'cousin'):
            x_query_cousin(split_line[1], split_line[3], split_line[4])

        else :
            x_query_unrelated(split_line[1], split_line[3])

    if split_line[0] == 'W' :
        if (split_line[1] == 'child'):
            w_query_child(split_line[2])

        elif (split_line[1] == 'sibling'):
            w_query_sibling(split_line[2])

        elif (split_line[1] == 'ancestor'):
            w_query_ancestor(split_line[2])

        elif (split_line[1] == 'cousin'):
            w_query_cousin(split_line[3], split_line[2])

        else :
            w_query_unrelated(split_line[2])


# Iterates over standard in, determines the type of event / query for each line,
# echoes the line back to the user, and then calls the appropriate method.
def main():
    for line in sys.stdin:
        current_line = line.rstrip()
        print(current_line)
        parse_line(current_line.split())
        print()

    pprint(family_tree)

if __name__ == '__main__':
    main()
