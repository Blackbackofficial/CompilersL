def brackets_parser(line, num_graph=2):
    try:
        struct = dict()
        i = 0
        size = len(line)
        # случай пустой строки
        if size == 0:
            struct.update({'q0': {'ε': 'q1'}})

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
            if line[i] == '(' or line[i] == ')':
                next_brackets = 1
                while i < size or line[i - 1] == '(':
                    if next_brackets > 0:
                        i += 1
                        if next_brackets > 0 and line[i] == ')':
                            next_brackets -= 1
                        elif line[i] == '(':
                            next_brackets += 1
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
                next_brackets = 0
                if line[i] == '(':
                    slice_s = i
                    f_slice = True
                    while line[i] != ')' or next_brackets > 0:
                        i += 1
                        if line[i] == '(':
                            next_brackets += 1
                        elif line[i] == ')' and next_brackets > 0:
                            next_brackets -= 1
                            if i == size - 2:
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


def regex_parser(line, graph, start_q=None, end_q=None):
    try:
        new_dict = dict()
        i = 0
        if line[i] == '(' and line[len(line) - 1] == ')' and line[i + 1:len(line) - 1].count('(') > 0:
            return regex_parser(line[i + 1:len(line) - 1], graph, start_q, end_q)
        elif line[i] == '(' and line[len(line) - 1] == ')' and line[i + 1:len(line) - 2].count('(') == 0:
            return regex_parser(line[i + 1:len(line) - 1], graph, start_q, end_q)

        while i < len(line):
            if line[i] != '|' and line[i] != '(' and line[i] != ')' and line[i] != '*':
                if i != len(line) - 1 and (line[i + 1] == '*' or line[i + 1] == '|'):
                    if i + 4 < len(line) and line[i + 1] == '*' and line[i + 2] == '|' and line[i + 4] == '*':
                        if i == 0:  # случай a*|b*
                            new_dict.update({start_q: {'ε': 'q{}'.format(graph) + ', ' + 'q{}'.format(graph + 1)}})
                            new_dict.update({'q{}'.format(graph): {line[i]: 'q{}'.format(graph)}})
                            new_dict['q{}'.format(graph)].update({'ε': 'q{}'.format(graph+2)})
                            new_dict.update({'q{}'.format(graph+1): {line[i+3]: 'q{}'.format(graph + 1)}})
                            new_dict['q{}'.format(graph+1)].update({'ε': 'q{}'.format(graph + 2)})
                            if i + 4 == len(line) - 1:
                                new_dict['q{}'.format(graph)]['ε'] = end_q
                                new_dict['q{}'.format(graph + 1)]['ε'] = end_q
                            graph += 2
                            # i += 3
                        else:
                            new_dict.update({'q{}'.format(graph): {'ε': 'q{}'.format(graph+1)+', '+'q{}'.format(graph+2)}})
                            new_dict.update({'q{}'.format(graph+1): {line[i]: 'q{}'.format(graph+1)}})
                            new_dict['q{}'.format(graph+1)].update({'ε': 'q{}'.format(graph + 3)})
                            new_dict.update({'q{}'.format(graph + 2): {line[i + 3]: 'q{}'.format(graph + 3)}})
                            new_dict['q{}'.format(graph + 2)].update({'ε': 'q{}'.format(graph + 3)})
                            if i + 4 == len(line) - 1:
                                new_dict['q{}'.format(graph + 1)]['ε'] = end_q
                                new_dict['q{}'.format(graph + 2)]['ε'] = end_q
                            graph += 3
                        i += 4
                    if i < len(line) and i + 2 < len(line) - 1 and line[i + 2] == '|':  # случай a*|b
                        start = i
                        if i == 0 and start_q == 'q0':
                            new_dict.update({'q0': {'ε': 'q{}'.format(graph)}})
                            new_dict.update({'q{}'.format(graph): {'ε': 'q{}'.format(graph + 1)}})

                            if i + 3 != '(':
                                i += 3
                                if len(line) - 1 == i:
                                    new_dict['q0'].update({line[i]: end_q})
                                    new_dict['q2'].update({'ε': end_q})
                                    try:
                                        new_dict['q{}'.format(graph)].update({line[start]: 'q{}'.format(graph)})
                                    except KeyError:
                                        new_dict.update({'q{}'.format(graph): {line[start]: 'q{}'.format(graph)}})
                                else:
                                    new_dict['q{}'.format(graph)].update({line[start]: 'q{}'.format(graph)})
                                    new_dict['q{}'.format(graph)].update({'ε': 'q{}'.format(graph + 1)})
                                    try:
                                        new_dict['q{}'.format(graph)].update({line[i]: 'q{}'.format(graph + 1)})
                                    except KeyError:
                                        new_dict.update({'q{}'.format(graph): {line[i]: 'q{}'.format(graph + 1)}})
                            graph += 1
                        else:
                            new_dict.update({'q{}'.format(graph): {'ε': 'q{}'.format(graph + 1)}})
                            new_dict.update({'q{}'.format(graph + 1): {'ε': 'q{}'.format(graph + 2)}})
                            graph += 1

                            if i + 3 != '(':
                                i += 3
                                if len(line) - 1 == i:
                                    new_dict['q{}'.format(graph-1)].update({line[i]: end_q})
                                    new_dict['q{}'.format(graph)].update({'ε': end_q})
                                    try:
                                        new_dict['q{}'.format(graph)].update({line[start]: 'q{}'.format(graph)})
                                    except KeyError:
                                        new_dict.update({'q{}'.format(graph): {line[start]: 'q{}'.format(graph)}})
                                else:
                                    new_dict['q{}'.format(graph)].update({line[start]: 'q{}'.format(graph)})
                                    new_dict['q{}'.format(graph)].update({'ε': 'q{}'.format(graph + 1)})
                                    try:
                                        new_dict['q{}'.format(graph)].update({line[i]: 'q{}'.format(graph + 1)})
                                    except KeyError:
                                        new_dict.update({'q{}'.format(graph): {line[i]: 'q{}'.format(graph + 1)}})
                            graph += 1
                    elif i + 3 < len(line) and line[i + 1] == '|' and line[i + 3] == '*':
                        s = line[i]
                        e = line[i+2:i+4]
                        line = line[:i] + e + '|' + s + line[i+4:]
                        continue
                    elif i < len(line) - 1 and line[i + 1] == '|':  # случай a|b
                        if line[i + 2] != '(' and i == 0:
                            # (a|sb|i|e|r)
                            new_dict.update({start_q: {line[i]: end_q}})
                            i += 2
                            new_dict[start_q].update({line[i]: end_q})
                            while i < len(line) - 1 and line[i + 1] == '|':
                                i += 2
                                new_dict[start_q].update({line[i]: end_q})
                            if i != len(line) - 1:
                                for elem in new_dict[start_q]:
                                    new_dict[start_q].update({elem: 'q{}'.format(graph)})
                        else:
                            if line[i + 2] != '(':
                                new_dict.update({'q{}'.format(graph): {line[i]: 'q{}'.format(graph + 1)}})
                                i += 2
                                new_dict['q{}'.format(graph)].update({line[i]: 'q{}'.format(graph + 1)})
                                # (z|t|z|e|p|o|i)
                                while i < len(line) - 1 and line[i + 1] == '|':
                                    i += 2
                                    new_dict['q{}'.format(graph)].update({line[i]: 'q{}'.format(graph + 1)})
                                if i == len(line) - 1 or line[i] == ')':
                                    for elem in new_dict['q{}'.format(graph)]:
                                        new_dict['q{}'.format(graph)].update({elem: end_q})
                                graph += 1
                            elif line[i + 2] == '(':
                                if i == 0:
                                    new_dict.update({start_q: {line[i]: 'q{}'.format(graph + 1)}})
                                else:
                                    new_dict.update({'q{}'.format(graph): {line[i]: 'q{}'.format(graph + 1)}})
                                start = i + 3
                                while line[i] != ')':
                                    i += 1
                                if i == len(line) - 1:
                                    if start - 3 == 0:
                                        new_dict.update({start_q: {line[start-3]: end_q}})
                                    else:
                                        new_dict.update({'q{}'.format(graph): {line[start - 3]: end_q}})
                                struct = regex_parser(line[start:i], graph, 'q{}'.format(graph), end_q)

                                if i == len(line) - 1 and graph <= 2:
                                    new_dict['q0'].update(struct[0].get('q{}'.format(graph)))
                                    struct[0].pop('q{}'.format(graph))
                                # (za|(mi|e))
                                for elem in struct[0]:
                                    try:
                                        new_dict[elem].update(struct[0].get(elem))
                                    except KeyError:
                                        new_dict.update({elem: struct[0].get(elem)})
                                graph = struct[1]
                                if i == len(line) - 1:
                                    try:
                                        for elem in new_dict['q{}'.format(graph)]:
                                            new_dict['q{}'.format(graph)].update({elem: end_q})
                                    except KeyError:
                                        continue
                    elif i < len(line) - 1 and line[i + 1] == '*':
                        if i == 0:
                            new_dict.update({start_q: {'ε': 'q{}'.format(graph + 1)}})
                        else:
                            new_dict.update({'q{}'.format(graph): {'ε': 'q{}'.format(graph + 1)}})
                        if i == len(line) - 2:
                            new_dict.update({'q{}'.format(graph + 1): {'ε': end_q}})
                        else:
                            new_dict.update({'q{}'.format(graph + 1): {'ε': 'q{}'.format(graph + 2)}})
                        new_dict['q{}'.format(graph + 1)].update({line[i]: 'q{}'.format(graph + 1)})
                        graph += 2
                else:
                    if i == len(line) - 1:
                        if i == 0:
                            new_dict.update({start_q: {line[i]: end_q}})
                            break
                        new_dict.update({'q{}'.format(graph): {line[i]: end_q}})
                        break
                    elif i == 0:
                        new_dict.update({start_q: {line[i]: 'q{}'.format(graph + 1)}})
                    else:
                        # надо подумать (ad)|(mie)
                        new_dict.update({'q{}'.format(graph): {line[i]: 'q{}'.format(graph+1)}})
                    graph += 1
            elif line[i] == '(':
                start = i + 1
                while line[i] != ')':
                    i += 1

                if start == 1:
                    struct = regex_parser(line[start:i + 1], graph, start_q, 'q{}'.format(graph))
                    graph = struct[1]
                    if line[i + 1] == '|' and line[i + 2] != '(':
                        if i + 2 == len(line) - 1:
                            struct_p = regex_parser(line[i + 2], graph-1, start_q, end_q)
                        else:
                            struct_p = regex_parser(line[i + 2], graph-1, start_q, 'q{}'.format(graph))
                        struct[0]['q{}'.format(graph-1)].update(struct_p[0].get('q{}'.format(graph-1)))

                        if list(struct_p[0].get('q{}'.format(graph - 1)).values())[0] == 'q1':
                            for elem in struct[0]['q{}'.format(graph-1)]:
                                struct[0]['q{}'.format(graph-1)][elem] = 'q1'
                        i += 2
                        graph -= 1
                    new_dict.update(struct[0])
                else:
                    if i == len(line) - 1:
                        struct = regex_parser(line[start:i], graph, start_q, end_q)
                        new_dict.update(struct[0])
                    else:
                        struct = regex_parser(line[start:i], graph, 'q{}'.format(graph), 'q{}'.format(graph))
                        new_dict.update(struct[0])
                graph = struct[1]
            i += 1
        return new_dict, graph
    except Exception as ex:
        print("Exceptions in regex_parser: {}".format(ex.args[-1]))
        exit(1)


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
                                p = 0
                                # доделать * в *
                                for ke in list(edit_dict[0][keys[k]].keys()):
                                    if ke[p] in struct[keys[k]]:
                                        second_str = edit_dict[0][keys[k]].get(ke)
                                        first_str = struct[keys[k]][ke]
                                        long_str = first_str+', '+second_str
                                        struct[keys[k]][ke] = long_str
                                    else:
                                        struct[keys[k]].update(edit_dict[0].get(keys[k]))
                                        break
                                    p += 1
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

                    struct[items_key[i]].pop(list_items[j])
                    if len(struct[items_key[i]]) == 0:
                        struct.pop(items_key[i])
                    items_key.sort()  # для упорядочевания items_key, гда элементы хранятся и дабавляются ссылки
                    num_graph = edit_dict[1]
                j += 1
            i += 1
        return struct
    except IndexError:
        print("String index out of range!")
        exit(1)


def parser_to_nka(line):
    start_dict = brackets_parser(line)
    parser_dict = depth_search(start_dict[0], start_dict[1])
    print(parser_dict)
    return parser_dict
