# -*- coding: utf-8 -*-
import re


def remove_in_code(list_objects, code):
    delete_object_list = []

    for object_delete in list_objects:
        input_index = object_delete.span()[0]
        output_index = object_delete.span()[1]
        delete_object_list.append(code[input_index: output_index])

    for object_item in delete_object_list:
        code = code.replace(object_item, '')

    return code


def delete_comments(code):

    list_objects = re.finditer(r'/\*[\s*\S*\n*]*\*/', code)
    code = remove_in_code(list_objects, code)

    list_objects = re.finditer(r'\'[^\']*\'', code)
    code = remove_in_code(list_objects, code)

    list_objects = re.finditer(r'\"[^\"]*\"', code)
    code = remove_in_code(list_objects, code)

    list_objects = re.finditer(r'//[^\n]*\n', code)
    code = remove_in_code(list_objects, code)

    return code


def search_functions(code):
    functions_list = []
    list_objects = re.finditer(r'\s*function[\s*\n*]*[a-zA-Z_0-9]+\s*\([^\)]*\)[\s*\n*]*\{',
                               code)

    for object_item in list_objects:
        left_brackets = 1
        right_brackets = 0
        index_out = object_item.span()[1]

        while left_brackets != right_brackets:
            if code[index_out] == '{':
                left_brackets += 1

            elif code[index_out] == '}':
                right_brackets += 1

            index_out += 1

        functions_list.append(code[object_item.span()[0]:index_out])

    for function in functions_list:
        code = code.replace(function, '')

    return functions_list, code


def get_count_vars(code):
    return_vars_list = []
    variables_string_list = re.findall(r'var[^;]*;', code)

    for variable_string in variables_string_list:
        variable_string = variable_string[4:]
        delete_list = re.findall(r'=[^\,\;]*', variable_string)

        for delete_object in delete_list:
            variable_string = variable_string.replace(delete_object, '')

        return_vars_list += re.findall(r'[[a-zA-Z_]+[0-9]*]*(?=\s*,*=*\s*;*)',
                                       variable_string)

    return return_vars_list


def get_local_vars_list(global_vars_dictionary, function):
    global result_file
    global spen_number

    send_variables = function[function.find('(')+1:function.find(')')]
    local_vars_list = get_count_vars(function)
    local_vars_list += re.findall(r'[[a-zA-Z_]+[0-9]*]*(?=\s*,*=*\s*;*)',
                                  send_variables)

    function_name = function[:function.find('(')].strip()
    local_vars_dictionary = {}
    for variable in local_vars_list:
        local_vars_dictionary[variable] = len(re.findall(r'[^a-z0-9A-Z_]{1}%s[^0-9a-zA-Z_]{1}'
                                                         % variable, function)) - 1
        spen_number += local_vars_dictionary[variable]

    for variable in global_vars_dictionary:
        if variable not in local_vars_list:
            global_vars_dictionary[variable] += len(re.findall(r'[^a-z0-9A-Z_]{1}%s[^0-9a-zA-Z_]{1}'
                                                               % variable, function))

    print(function_name)
    print(local_vars_dictionary)
    print()
    result_file.writelines(str(function_name)+'\n')
    result_file.writelines(str(local_vars_dictionary)+'\n')


def main():
    global result_file
    global spen_number

    source_file = open('source.js', 'r')
    code = source_file.read()
    code = delete_comments(code)
    functions_list, code = search_functions(code)
    global_vars_list = get_count_vars(code)

    global_vars_dictionary = {}
    for variable in global_vars_list:
        global_vars_dictionary[variable] = len(re.findall(r'[^a-z0-9A-Z_]{1}%s[^0-9a-zA-Z_]{1}'
                                                          % variable, code)) - 1

    for function in functions_list:
        get_local_vars_list(global_vars_dictionary, function)

    for variable in global_vars_dictionary:
        spen_number += global_vars_dictionary[variable]

    result_file.writelines('\nГлобальные переменные'+'\n')
    result_file.writelines(str(global_vars_dictionary)+'\n')
    result_file.writelines('\nРезультирующий спен: '+str(spen_number)+'\n')
    print('Глобальные переменные')
    print(global_vars_dictionary)
    print('\nРезультирующий спен: ', spen_number)


spen_number = 0
result_file = open('result.txt', 'w')
main()
