# -*- coding: utf-8 -*-
import re


def deleteComments(code):
    list_objects = re.finditer(r'\'[^\']*\'', code)
    removeInCode(list_objects, code)

    list_objects = re.finditer(r'\"[^\"]*\"', code)
    removeInCode(list_objects, code)

    list_objects = re.finditer(r'/\*[\s*\S*]*\*/', code)
    removeInCode(list_objects, code)

    list_objects = re.finditer(r'\([^\)\(]*\)', code)
    removeInCode(list_objects, code)

    list_objects = re.finditer(r'//[^\n]*\n', code)
    removeInCode(list_objects, code)

    list_objects = re.finditer(r'var[^\;]*;', code)
    removeInCode(list_objects, code)

    return code


def removeInCode(list_objects, code):
    delete_list = []

    for object in list_objects:
        input_index = object.span()[0]
        output_index =object.span()[1]
        delete_list.append(code[input_index: output_index])

    for item in delete_list:
        code = code.replace(item, '')


def noRecursOutput(n_graph):
    CONST_ADD = 2
    line = 0
    for key in n_graph:
        line += len(n_graph[key])

    count_dots = len(n_graph) + 1

    return line - count_dots + CONST_ADD


def getListStructures(code):
    lines_list = code.split('\n')
    delete_list = []
    for iteration in range(len(lines_list)):
        lines_list[iteration] = lines_list[iteration].expandtabs()
        lines_list[iteration] = lines_list[iteration].strip()

    for iteration in range(len(lines_list)):

        if lines_list[iteration].endswith('}') and iteration+1 != len(lines_list):
            lines_list[iteration+1] = '}' + lines_list[iteration+1]
            lines_list[iteration] = lines_list[iteration][:len(lines_list[iteration])-1]

        elif lines_list[iteration] == '{':
            lines_list[iteration-1] += '{'
            delete_list.append(iteration)

        elif lines_list[iteration] == '}':
            lines_list[iteration-1] += '}'
            delete_list.append(iteration)

    count_lines = lines_list.count('{')
    for iteration in range(count_lines):
        lines_list.remove('{')

    count_lines = lines_list.count('}')
    for iteration in range(count_lines):
        lines_list.remove('}')

    count_lines = lines_list.count('')
    for iteration in range(count_lines):
        lines_list.remove('')

    return lines_list


def findAll(list_structures, end_dot_graph, structure=None):
    global makkeyb_graph
    global buffer_if

    dot_graph= None

    for counter in range(len(list_structures)):

        if 'else' in list_structures[counter] and 'if' in list_structures[counter] and '{' in list_structures[counter]:
            position_end = findEnd(list_structures, counter)
            counter -= 1
            dot_graph += 1
            makkeyb_graph[end_dot_graph].append(dot_graph)
            buffer_if.append(dot_graph)
            structure = None

        elif 'else' in list_structures[counter] and 'if' in list_structures[counter]:
            dot_graph += 1
            makkeyb_graph[end_dot_graph].append(dot_graph)
            buffer_if.append(dot_graph)
            structure = None

        elif 'if' in list_structures[counter] and '{' in list_structures[counter]:
            position_end = findEnd(list_structures, counter)
            counter -= 1
            end_dot_graph, buffer_if = noIfStructureProcess(buffer_if, end_dot_graph)

            makkeyb_graph[end_dot_graph] = []
            dot_graph = end_dot_graph + 1
            makkeyb_graph[end_dot_graph].append(dot_graph)
            buffer_if.append(dot_graph)
            structure = 'if'

            #if positionend != counter and positionend != counter+1:
            #    findAll(liststructures[counter+1:positionend], dot_graph)

        elif 'else' in list_structures[counter] and '{' in list_structures[counter]:
            position_end = findEnd(list_structures, counter)
            counter -= 1
            dot_graph += 1
            makkeyb_graph[end_dot_graph].append(dot_graph)
            buffer_if.append(dot_graph)
            structure = None

            #if positionend != counter and positionend != counter+1:
            #    findAll(liststructures[counter+1:positionend], dot_graph)

        elif 'else' in list_structures[counter]:
            dot_graph += 1
            makkeyb_graph[end_dot_graph].append(dot_graph)
            buffer_if.append(dot_graph)
            structure = None

        elif 'if' in list_structures[counter]:
            end_dot_graph, buffer_if = noIfStructureProcess(buffer_if, end_dot_graph)
            makkeyb_graph[end_dot_graph] = []
            dot_graph = end_dot_graph + 1
            makkeyb_graph[end_dot_graph].append(dot_graph)
            buffer_if.append(dot_graph)
            structure = 'if'

        elif 'for' in list_structures[counter] and '{' in list_structures[counter]:
            position_end = findEnd(list_structures, counter)
            counter -= 1
            end_dot_graph, buffer_if = noIfStructureProcess(buffer_if, end_dot_graph)
            dot_graph = addPointInGraph(end_dot_graph, dot_graph)
            end_dot_graph = dot_graph+1

            #if positionend != counter and positionend != counter+1:
            #    findAll(liststructures[counter+1:positionend])

        elif 'for' in list_structures[counter]:
            position_end = findEnd(list_structures, counter)
            counter -= 1
            end_dot_graph, buffer_if = noIfStructureProcess(buffer_if, end_dot_graph)
            dot_graph = addPointInGraph(end_dot_graph, dot_graph)
            end_dot_graph = dot_graph+1

           # if positionend != counter and positionend != counter+1:
            #    findAll(liststructures[counter+1:positionend])

        elif 'while' in list_structures[counter] and '{' in list_structures[counter]:
            position_end = findEnd(list_structures, counter)
            counter -= 1
            end_dot_graph, buffer_if = noIfStructureProcess(buffer_if, end_dot_graph)
            dot_graph = addPointInGraph(end_dot_graph, dot_graph)
            end_dot_graph = dot_graph+1

            #if positionend != counter and positionend != counter+1:
            #    findAll(liststructures[counter+1:positionend])

        elif 'while' in list_structures[counter] and '}' not in list_structures[counter]:
            position_end = findEnd(list_structures, counter)
            counter -= 1
            end_dot_graph, buffer_if = noIfStructureProcess(buffer_if, end_dot_graph)
            dot_graph = addPointInGraph(end_dot_graph, dot_graph)
            end_dot_graph = dot_graph+1
            #if positionend != counter and positionend != counter+1:
            #    findAll(liststructures[counter+1:positionend])

        elif ' do' in list_structures[counter] and '{' in list_structures[counter]:
            position_end = findEnd(list_structures, counter)
            counter -= 1
            end_dot_graph, buffer_if = noIfStructureProcess(buffer_if, end_dot_graph)
            dot_graph = addPointInGraph(end_dot_graph, dot_graph)
            end_dot_graph = dot_graph + 1

            #if positionend != counter and positionend != counter+1:
            #    findAll(liststructures[counter+1:positionend])

        elif ' do ' in list_structures[counter]:
            position_end = findEnd(list_structures, counter)
            counter -= 1
            end_dot_graph, buffer_if = noIfStructureProcess(buffer_if, end_dot_graph)
            dot_graph = addPointInGraph(end_dot_graph, dot_graph)
            end_dot_graph = dot_graph + 1


    if structure == 'if':
        makkeyb_graph[end_dot_graph+1] = []
        dot_graph += 1
        makkeyb_graph[end_dot_graph].append(dot_graph)
        makkeyb_graph[end_dot_graph+1].append(dot_graph)
        end_dot_graph = dot_graph
        structure = None

    if buffer_if != []:

        for counter in buffer_if:
            makkeyb_graph[counter] = [max(buffer_if) + 1]


def noIfStructureProcess(buffer_if, end_dot_graph):
    global makkeyb_graph
    if buffer_if != []:

        if len(buffer_if) == 1:
            makkeyb_graph[end_dot_graph] += [max(buffer_if) + 1]

        end_dot_graph = max(buffer_if) + 1
        for j in buffer_if:
             makkeyb_graph[j] = [end_dot_graph]

        buffer_if = []

    return end_dot_graph, buffer_if


def addPointInGraph(end_dot_graph, dot_graph):
    global makkeyb_graph
    dot_graph = end_dot_graph + 1
    makkeyb_graph[end_dot_graph] = []
    makkeyb_graph[end_dot_graph].append(dot_graph)
    makkeyb_graph[dot_graph] = []
    makkeyb_graph[dot_graph].append(end_dot_graph)
    makkeyb_graph[dot_graph].append(dot_graph+1)

    return dot_graph


def findEnd(list_elements, index):
    left_brackets = 0
    right_brackets = 0
    while left_brackets != right_brackets:

        if '}' in list_elements[index]:
            right_brackets += 1

            if right_brackets == left_brackets:
                break

        if '{' in list_elements[index]:
            left_brackets += 1

        index += 1
        if index == len(list_elements) - 1:
            break

    return index


def searchFunctions(code):
    functions_list = []
    search_list = re.finditer(r'\s*function[\s*\n*]*[a-zA-Z_0-9]+\s*[\s*\n*]*\{', code)

    for function in search_list:
        left_brackets = 1
        right_brackets = 0
        index_brackets = function.span()[1]

        while left_brackets != right_brackets:

            if code[index_brackets] == '{':
                left_brackets += 1

            elif code[index_brackets] == '}':
                right_brackets += 1

            index_brackets += 1
        functions_list.append(code[function.span()[0]:index_brackets])

    for function in functions_list:
        code = code.replace(function, '')

    return functions_list, code


def getFunctionsDictionary(functions_list):
    dictionary={}
    for item in functions_list:
        function_code = item
        function_name_list = re.finditer(r'\s*function[\s*\n*]*[a-zA-Z_]',item)

        for name in function_name_list:
            delete_name = item[:name.span()[1]-1]
            item = item.replace(delete_name,'')

        function_name_list = re.finditer(r'[a-zA-Z_0-9]*\s*\{',item)
        for name in function_name_list:
            item = item[:name.span()[1]-1]
            index = function_code.index('{')
            dictionary[item] = function_code[index + 1: len(function_code)-1]

    return dictionary


def main():
    source_file = open('source1.js', 'r')
    code = source_file.read()
    code = deleteComments(code)
    functions_list, code = searchFunctions(code)
    functions_dictionary = getFunctionsDictionary(functions_list)

    for key in functions_dictionary.keys():
        code = code.replace(key,'\n'+functions_dictionary[key]+'\n')

    list_structures = getListStructures(code)
    findAll(list_structures, 0)


makkeyb_graph = {}
buffer_if = []
main()
file = open('result.txt', 'w')

for item in makkeyb_graph.items():
    file.writelines(str(item)+'\n')

print('\nMakkeyb:', noRecursOutput(makkeyb_graph))





















