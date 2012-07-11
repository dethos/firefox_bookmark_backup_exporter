# -*- coding: utf-8 -*-

import sys
import simplejson
import codecs

#
# GET the data from the source file
#


def getsource(string):
    f = codecs.open(string, 'r', 'utf-8')
    source = '[' + f.readline() + ']'  # make the string look like a list
    f.close()
    return source


#
# Filter with the wanted fields
#

def filtersource(source):
    try:
        raw_data = simplejson.loads(source)  # Parse the data like a json list
    except:
        print "-  Invalid input (backup) file"
        exit(0)
    final = []
    for item in raw_data:
        final.append(getElements(item))  # build temporary data representation
    return final


def getElements(item):  # with recursion gets children and base info
    childs = []
    if 'children' in item:
        for child in item['children']:
            childs.append(getElements(child))

    if 'uri' in item:
        return {'title': item['title'], 'uri': item['uri']}
    else:
        return {'title': item['title'], 'children': childs}


#
#   PRINT THE OUTPUT
#
def outputdata(data, location):
    toprint = []
    for element in data:
        printElement(element, toprint)

    f = codecs.open(location, 'w', 'utf-8')
    f.write("Opera Hotlist version 2.0\nOptions: encoding = utf8, version=3\n")
    for line in toprint:
        f.write(line)
    f.close()


def printElement(element, toprint):  # with recursion add to print list the items
    if 'uri' in element:
        item = '#URL\n\tNAME=' + element['title'] + '\n\tURL=' + element['uri'] + '\n'
        toprint.append(item)
    else:
        item = '#FOLDER\n\tNAME=' + element['title'] + '\n'
        toprint.append(item)
        for child in element['children']:
            printElement(child, toprint)
        toprint.append('-\n')


#
#   Main function
#
def extract(argv):
    if len(argv) >= 3:
        try:
            s = getsource(argv[1])
        except:
            print "-  The source file doesn't exist"
            exit(0)
        info = filtersource(s)
        outputdata(info, argv[2])
    else:
        print "Not enough arguments"
        print "Usage:"
        print "\t python ffbbe BACKUP.json DESTINY.adr"


if __name__ == '__main__':
    extract(sys.argv)
