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

# Example person (key 1 is a list of parents, key 2 is spouse, key 3 is children):
# family_tree = {
#     person_name_string : {
#         1 : ['parent_1_name_string', 'parent_2_name_string'],
#         2 : 'spouse_name_string',
#         3 : ['child_name_string', ...]
#     }
# }
family_tree = {}


# Create the people (as sub-dictionaries) if they do not exist, set as each other's spouse
# in either case.
def event_marriage(person_1, person_2) :
    if person_1 not in family_tree :
        family_tree.update({person_1: {
            1 : [],
            2 : person_2,
            3 : []
        }})

    else :
        family_tree[person_1][2] = person_2

    if person_2 not in family_tree :
        family_tree.update({person_2: {
            1 : [],
            2 : person_1,
            3 : []
        }})

    else :
        family_tree[person_2][2] = person_1


# Makes sure the parents exist and are married, then creates the child and # points the
# people at one another.
def event_child(person_1, person_2, child) :
    event_marriage(person_1, person_2)

    family_tree.update({child: {
        1: [person_1,person_2],
        2: '',
        3: []
    }})

    family_tree[person_1][3].append(child)
    family_tree[person_2][3].append(child)


# Leverages existing 'W' query to check whether an individual is in the list of the
# person's children.
def x_query_child(child, person) :
    if child in w_query_child(person) :
        print('Yes')

    else :
        print('No')


# Leverages existing 'W' query to check whether an individual is in the list of the
# person's siblings.
def x_query_sibling(sibling, person) :
    if sibling in w_query_sibling(person) :
        print('Yes')

    else :
        print('No')


# Leverages existing 'W' query to check whether an individual is in the list of the
# person's ancestors.
def x_query_ancestor(ancestor, person) :
    if ancestor in w_query_ancestor(person) :
        print('Yes')

    else :
        print('No')


# Leverages existing 'W' query to check whether an individual is in the list of the
# person's cousins of a specific degree.
def x_query_cousin(cousin, degree, person) :
    if cousin in w_query_cousin(person, degree) :
        print('Yes')

    else :
        print('No')


# Leverages existing 'W' query to check whether an individual is in the list of those
# unrelated to a person.
def x_query_unrelated(non_relative, person) :
    if non_relative in w_query_unrelated(person) :
        print('Yes')

    else :
        print('No')


# Returns a sorted list of the person's children from which duplicates have been removed.
def w_query_child(person) :
    return sorted(family_tree[person][3])


# Returns a sorted list of the person's siblings from which duplicates have been removed.
def w_query_sibling(person) :
    siblings = []

    for parent in family_tree[person][1] :
        siblings = list(set(siblings + family_tree[parent][3]))

    if person in siblings :
        siblings.remove(person)

    return sorted(siblings)


# Returns all of a person's ancestors (recursively).
#def w_query_ancestor(person, list) :
#    if len(family_tree[person][1]) < 2: #if missing a parent
#        return list
#
#    else :
#        w_query_ancestor(family_tree[person][1][0],list)
#        list.append(family_tree[person][1][0])
#
#        w_query_ancestor(family_tree[person][1][1],list)
#        list.append(family_tree[person][1][1])
#
#    return list


# Returns all of a person's ancestors (recursively).
def w_query_ancestor(person) :
    all_ancestors = []

    def get_ancestors(person) :
        ancestors = []

        if len(family_tree[person][1]) == 2 :
            if family_tree[person][1][0] not in all_ancestors :
                all_ancestors.append(family_tree[person][1][0])
                ancestors.extend(get_ancestors(family_tree[person][1][0]))

            if family_tree[person][1][1] not in all_ancestors :
                all_ancestors.append(family_tree[person][1][1])
                ancestors.extend(get_ancestors(family_tree[person][1][1]))

            ancestors.extend(family_tree[person][1])

            all_ancestors.extend(ancestors)

        return ancestors

    get_ancestors(person)

    return list(set(all_ancestors))


#final cousin method that returns ALL the nth zero_removed_cousins
#this includes:
#the nth cousins of the person's ancestors
#the descendents of the persons zero_removed_cousins
def w_query_cousin(person, degree):
    zero_removed = []
    ancestors = []
    cousins = []

    if (degree == 0) : #exception for when degree is zero
        zero_removed += w_query_sibling(person)
        for x in zero_removed:
            cousins += (get_descendents(x,[])) #add decendents of zero removed

        cousins += zero_removed
        return cousins

    #for any other degree above zero...code below

    #get ancestors of person
    ancestors += w_query_ancestor(person)
    #get zero removed cousins of ancestor
    zero_removed += get_zero_removed_cousins(person, degree)


    #add the zero removed cousins of ALL the ancestors
    for ancestor in ancestors:
        cousins += get_zero_removed_cousins(ancestor, degree)

    for x in zero_removed:
        cousins += get_descendents(x, [])

    cousins += zero_removed
    return cousins;


# Finds all ancestors of a person then all decendants of those ancestors. After removing those from
# the list of all people, only those who are unrelated remain.
def w_query_unrelated(person) :
    unrelated = list(family_tree.keys())
    ancestors = list(set(w_query_ancestor(person)))

    for ancestor in ancestors :
        descendants = get_descendents(ancestor, [])

        try:
            unrelated.remove(ancestor)
        except ValueError:
            pass

        for descendant in descendants :
            try :
                unrelated.remove(descendant)
            except ValueError :
                pass

    return sorted(unrelated)


#this method is used in get_zero_removed_cousins
#level is the degree of cousin
#this method will return the proper great (*) gradnparents according to the degree of cousins
#1st cousins retrieves grandparents, 2nd cousins retrieves great grandparents, etc.
def get_grandparents(person, level, list) :
    if len(family_tree[person][1]) < 2: # if missing a parent
        return list

    if (level == 0):
        list.append(family_tree[person][1][0])
        list.append(family_tree[person][1][1])

    else:
        get_grandparents(family_tree[person][1][0], level -1, list)
        get_grandparents(family_tree[person][1][1], level -1, list)

    return list


#this method is used in get_zero_removed_cousins
#returns all people on level zero, starting from the selected grandparent
#level = degreee of cousins
#example - people on the zero level of a grandparent are zero removed first cousins
#        - people on the zero level of a greatgranparent are zero removed second cousins
def get_descendents_at_zero_level(grandparent, level, list) :
    if (len(w_query_child(grandparent)) ==  0):
        return list

    if (level == 0):
        list += w_query_child(grandparent)
        return list

    for descendent in w_query_child(grandparent) :
        get_descendents_at_zero_level(descendent, level - 1, list);

    return list


#returns ALL descendents of person
def get_descendents(person, list):
    if (len(w_query_child(person)) ==  0):
        return list

    else:
        for child in w_query_child(person):
            get_descendents(child, list)
            list.append(child)

    return list


#get zero removed cousins
def get_zero_removed_cousins (starterPerson, degree) :
    grandparents = [] #selected (great)* grandparents depending on degree
    descendents_at_zero_level = []
    flagged = [] #ancestors of starterPerson that must be removed

    #obtain the needed (great)* grandparents according to the degree
    grandparents += get_grandparents(starterPerson, degree, [])

    #Flag people who have starterPerson as a descendent
    for i in grandparents:
        for j in w_query_child(i):
            if (starterPerson in get_descendents(j, [])) :
                flagged.append(j)

    #add to descendents_at_zero_level
    for x in grandparents:
        descendents_at_zero_level += (get_descendents_at_zero_level(x, degree, []))

    #only add people who DO NOT have a flagged person as an ancestor
    zero_removed_cousins = []
    for x in descendents_at_zero_level:
        if not (any( elem in w_query_ancestor(x) for elem in flagged)):
            zero_removed_cousins.append(x)

    return zero_removed_cousins


# Determines the type of query based on contents and length of the split-up string.
def parse_line(split_line) :
    if split_line[0] == 'E' :
        if len(split_line) == 3 :
            event_marriage(split_line[1], split_line[2])

        else :
            event_child(split_line[1], split_line[2], split_line[3])

    if split_line[0] == 'X' :
        if (split_line[2] == 'child') :
            if split_line[3] in family_tree :
                x_query_child(split_line[1], split_line[3])
                print()

            else:
                print(split_line[3] + ' does not exist in the family tree.\n')

        elif (split_line[2] == 'sibling') :
            if split_line[3] in family_tree :
                x_query_sibling(split_line[1], split_line[3])
                print()

            else:
                print(split_line[3] + ' does not exist in the family tree.\n')

        elif (split_line[2] == 'ancestor') :
            if split_line[3] in family_tree :
                x_query_ancestor(split_line[1], split_line[3])
                print()

            else:
                print(split_line[3] + ' does not exist in the family tree.\n')

        elif (split_line[2] == 'cousin') :
            if split_line[4] in family_tree :
                x_query_cousin(split_line[1], int(split_line[3]), split_line[4])
                print()

            else:
                print(split_line[4] + ' does not exist in the family tree.\n')

        else :
            if split_line[3] in family_tree :
                x_query_unrelated(split_line[1], split_line[3])
                print()

            else:
                print(split_line[3] + ' does not exist in the family tree.\n')

    if split_line[0] == 'W' :
        if (split_line[1] == 'child') :
            if split_line[2] in family_tree :
                print(*w_query_child(split_line[2]), sep='\n')
                print()

            else :
                print(split_line[2] + ' does not exist in the family tree.\n')

        elif (split_line[1] == 'sibling') :
            if split_line[2] in family_tree :
                print(*w_query_sibling(split_line[2]), sep='\n')
                print()

            else :
                print(split_line[2] + ' does not exist in the family tree.\n')

        elif (split_line[1] == 'ancestor') :
            if split_line[2] in family_tree :
                ancestors = w_query_ancestor(split_line[2])
                #REMOVE DUPLICATES
                ancestors = sorted(list(dict.fromkeys(ancestors)))
                print(*ancestors, sep='\n')
                print()

            else :
                print(split_line[2] + ' does not exist in the family tree.\n')

        elif (split_line[1] == 'cousin') :
            if split_line[3] in family_tree :
                cousins = (w_query_cousin(split_line[3], int(split_line[2])))
                #REMOVE DUPLICATES
                cousins = sorted(list(dict.fromkeys(cousins)))
                print(*cousins, sep='\n')
                print()

            else :
                print(split_line[3] + ' does not exist in the family tree.\n')

        else :
            if split_line[2] in family_tree :
                print(*w_query_unrelated(split_line[2]), sep='\n')
                print()

            else :
                print(split_line[2] + ' does not exist in the family tree.\n')

# Iterates over standard in, determines the type of event / query for each line,
# echoes the line back to the user, and then calls the appropriate method.
def main():
    for line in sys.stdin:
        current_line = line.rstrip()
        split_line = current_line.split()

        if split_line[0] != 'E' :
            print(current_line)

        parse_line(split_line)


if __name__ == '__main__':
    main()
