def brackets_parser(line, num_graph=2):
    try:
        struct = dict()
        i = 0
        size = len(line)

        while i < size:
            while i < size and (i < size and line[i] != '(' and line[i] != '|' and line[i] != '*' and line[i] != ')'):
                if size == 1:
                    struct.update({'q0': {line[i]: 'q1'}})
                    return struct, num_graph
                elif i == 0:
                    struct.update({'q0': {line[i]: 'q{}'.format(num_graph)}})
                elif i == size - 1:
                    struct.update({'q{}'.format(num_graph): {line[i]: 'q1'}})
                    return struct, num_graph
                else:
                    struct.update({'q{}'.format(num_graph): {line[i]: 'q{}'.format(num_graph + 1)}})
                    num_graph += 1
                i += 1

            slice_s = i
            if line[i] == '(':
                while i < size or line[i - 1] == '(':
                    if line[i] != ')':
                        i += 1
                    elif line[i] == ')' and i == size - 1 and slice_s == 0:
                        struct.update({'q0': {line[slice_s:i + 1]: 'q1'}})
                        return struct, num_graph
                    elif i <= 1:
                        struct.update({'q0': {line[slice_s:i + 1]: 'q1'}})
                        return struct, num_graph
                    elif slice_s == 0:
                        struct.update({'q0': {line[slice_s:i + 1]: 'q{}'.format(num_graph)}})
                        i += 1
                        break
                    elif i == size - 1:
                        struct.update({'q{}'.format(num_graph): {line[slice_s:i + 1]: 'q1'}})
                        return struct, num_graph
                    else:
                        struct.update({'q{}'.format(num_graph): {line[slice_s:i + 1]: 'q{}'.format(num_graph + 1)}})
                        num_graph += 1
                        i += 1
                        break

            if i < size and line[i] == '|':
                i += 1
                f_slice = False
                if line[i] == '(':
                    slice_s = i
                    f_slice = True
                    while line[i] != ')':
                        i += 1
                if struct.get('q{}'.format(num_graph - 1)) is None:
                    ver_start = 'q0'
                    last_dict = struct.get(ver_start)
                else:
                    ver_start = 'q{}'.format(num_graph - 1)
                    last_dict = struct.get(ver_start)
                vertex = list(last_dict.keys())
                vertex = last_dict.get(vertex[0])
                if f_slice:
                    struct[ver_start].update({line[slice_s:i + 1]: vertex})
                else:
                    struct[ver_start].update({line[i]: vertex})
                i += 1
                if i == size:
                    change = struct.get('q{}'.format(num_graph - 1))
                    if change is None:
                        change = struct.get('q0')
                    for key in list(change.keys()):
                        change[key] = 'q1'

            if i < size and line[i] == '*':
                if i != size - 1 and line[i + 1] == '|' and line[i - 1] != ')':
                    if num_graph == 2:
                        struct['q0'].update({'(' + line[i - 1:i + 1] + ')': 'q{}'.format(num_graph)})
                        struct['q0'].pop(line[i - 1:i])
                    else:
                        struct['q{}'.format(num_graph)].update({'(' + line[i - 1:i + 1] + ')': 'q{}'.format(num_graph)})
                        struct['q{}'.format(num_graph)].pop(line[i - 1:i])
                    i += 1
                    continue
                elem = struct.get('q{}'.format(num_graph - 1))
                if elem is None:
                    elem = struct.pop('q0')
                    elemN = elem.copy()
                    value = list(elem.values())
                    elem.clear()
                    elem.update({'ε': value[0]})
                    struct.update({'q0': elem})
                else:
                    struct.pop('q{}'.format(num_graph - 1))
                    elemN = elem.copy()
                    value = list(elem.values())
                    elem.clear()
                    elem.update({'ε': value[0]})
                    struct.update({'q{}'.format(num_graph - 1): elem})

                struct.update({'q{}'.format(num_graph): elemN})
                if i == size - 1:
                    elemN.update({'ε': 'q1'})
                else:
                    elemN.update({'ε': 'q{}'.format((num_graph + 1))})
                num_graph += 1
                i += 1
        return struct, num_graph
    except IndexError:
        print("String index out of range!")
        exit(1)


def regex_parser(line, num_graph, start_q=None, end_q=None):
    new_struct = dict()
    i = 0
    while i < len(line):
        if line[i] != '|' and line[i] != '(' and line[i] != ')' and line[i] != '*':
            if i != len(line) - 1 and (line[i + 1] == '*' or line[i + 1] == '|'):
                if i != len(line) - 1 and line[i + 2] == '|':
                    line  # что-то будет потом, случай *|
                elif i != len(line) - 1 and line[i + 1] == '|':
                    line  # что-то будет потом, случай |
            else:
                if i == len(line) - 1 and end_q == 'q1':
                    new_struct.update({'q{}'.format(num_graph): {line[i]: end_q}})
                    break
                elif i == len(line) - 1 and end_q != 'q1':
                    new_struct.update({'q{}'.format(num_graph): {line[i]: end_q}})
                elif i == 0:
                    new_struct.update({start_q: {line[i]: 'q{}'.format(num_graph + 1)}})
                else:
                    new_struct.update({'q{}'.format(num_graph - 1): {line[i]: 'q{}'.format(num_graph)}})
            num_graph += 1
        i += 1
    return new_struct, num_graph


def depth_search(struct, num_graph=2):
    try:
        i = 0
        items = list(struct.values())
        items_key = list(struct.keys())
        size_struct = len(struct)
        while i < size_struct:
            j = 0
            list_items = list(items[i].keys())
            size_item = len(items[i].keys())
            while j < size_item:
                if 2 > len(list_items[j]):
                    j += 1
                    continue
                else:
                    start_q = items_key[i]
                    end_q = struct[items_key[i]].get(list_items[j])
                    # чистим неверные ссылки q
                    if i < size_struct and i != 0:
                        save_values = struct[items_key[i]].pop(list_items[j])
                        struct.update({'q{}'.format(num_graph + 1): {list_items[j]: save_values}})
                        items_key.insert(i, 'q{}'.format(num_graph + 1))

                    edit_dict = regex_parser(list_items[j][1:len(list_items[j]) - 1], num_graph, start_q, end_q)
                    k = 0
                    keys = list(edit_dict[0].keys())
                    s_list = len(list_items)
                    if 1 < s_list:
                        while k < len(edit_dict[0]) and 1 < s_list:
                            try:
                                struct[keys[k]].update(edit_dict[0].get(keys[k]))
                            except KeyError:
                                struct.update({'{}'.format(keys[k]): edit_dict[0].get(keys[k])})
                            k += 1
                    else:
                        for key in list(edit_dict[0].keys()):
                            try:
                                struct[key].update(edit_dict[0].get(key))
                            except KeyError:
                                struct.update({'{}'.format(keys[k]): edit_dict[0].get(key)})
                            k += 1
                        # struct[items_key[i]].update(edit_dict[0])

                    struct[items_key[i]].pop(list_items[j])
                    items_key.sort()  # для упорядочевания items_key, гда элементы хранятся и дабавляются ссылки
                    num_graph = edit_dict[1]
                j += 1
            i += 1
        return struct
    except IndexError:
        print("String index out of range!")
        exit(1)
