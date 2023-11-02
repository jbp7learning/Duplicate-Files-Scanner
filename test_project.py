# test_project.py

import project
import pytest


# list of keys of the dict to check if the dict is already in the list_of_list_of_dict.
keys_to_check = ["type", "content"]

a1 = {
    "name": "Doc A1", "type": "txt", "size": "2000",
    "path": r"jbp7learning\Projects\Doc A1.docx",
    "content": "Hello, World! This is CS50P",
}

a2 = {
    "name": "Doc A2", "type": "txt", "size": "2000",
    "path": r"jbp7learning\Projects\Doc A2.docx",
    "content": "Hello, World! This is CS50P",
}

a3 = {
    "name": "Doc A3", "type": "txt", "size": "2000",
    "path": r"jbp7learning\Projects\Doc A3.docx",
    "content": "Hello, World! This is CS50P",
}

b = {
    "name": "Doc B", "type": "txt", "size": "2000",
    "path": r"jbp7learning\Projects\Doc B.docx",
    "content": "Final Project in CS50",
}

c = {
    "name": "Doc C", "type": "txt", "size": "2000",
    "path": r"jbp7learning\Projects\Doc C.docx",
    "content": "This is CS50P with a :)",
}

d1 = {
    "name": "Doc E", "type": "txt", "size": "2000",
    "path": r"jbp7learning\Projects\Doc E.docx",
    "content": "Hello, World!",
}

d2 = {
    "name": "Doc F", "type": "txt", "size": "2000",
    "path": r"jbp7learning\Projects\Doc F.docx",
    "content": "Hello, World!",
}


# FUNCTION CHECKS IF PASSED DICT IS ALREADY IN THE LIST OF LIST OF DICT,
# IF IT ALREADY IS, APPEND PASSED DICT TO THE LIST OF SIMILAR DICT.
# ELSE, APPEND PASSED DICT TO A NEW LIST AND ADD IT TO THE LIST OF LISTS OF DICT.
def test_add_to_duplicate_list():

    ls = [[d1, d2], [b,], [a1, a3,], [c,],]
    project.add_to_duplicate_list(a2, a1, ls)
    # The len of the ls should remain 4 as dict a1 is already listed.
    assert len(ls) == 4
    # The list, ls[2], should will be added with a duplicate dict a2, increasing the len by 1.
    assert len(ls[2]) == 3

    ls = [[b,], [a1, a3,],]
    project.add_to_duplicate_list(d2, d1, ls)
    # The len of list of list, ls, will increase by one as dict d2 and d1 is not yet listed.
    assert len(ls) == 3

# SUMMATION OF THE DUPLICATE FILES' SIZES IN BYTES
def test_space_to_free():
    ls = [
        [{"size":33311}, {"size":33311},],
        [{"size":254364}, {"size":254364},],
        [{"size":33092}, {"size":33092}, {"size":33092},],
        [{"size":28}, {"size":28}, {"size":28},],
        [{"size":13363}, {"size":13363}, {"size":13363},],
        [{"size":262394}, {"size":262394},],
    ]
    assert project.space_to_free(ls) == 643035


# CONVERTS SIZE IN BYTES TO THE LARGEST UNIT IT CAN FIT.
def test_convert_size():
    size = 643035
    assert project.convert_size(size) == "627.96 KB"
