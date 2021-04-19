def parser(string, num_of_graph=2, struct=None):
    if struct is None:
        struct = dict()
    struct = dict()
    i = 0
    size = len(string)

    while i < size:
        while i < size and (i < size and string[i] != '(' and string[i] != '|' and string[i] != '*' and string[i] != ')'):
            if size == 1:
                struct.update({'q0': {string[i]: 'q1'}})
                return struct, num_of_graph
            elif i == 0:
                struct.update({'q0': {string[i]: 'q{}'.format(num_of_graph)}})
            elif i == size - 1:
                struct.update({'q{}'.format(num_of_graph): {string[i]: 'q1'}})
                return struct, num_of_graph
            else:
                struct.update({'q{}'.format(num_of_graph): {string[i]: 'q{}'.format(num_of_graph + 1)}})
                num_of_graph += 1
            i += 1

        slice_s = i
        if string[i] == '(':
            while i <= size - 1 or string[i - 1] == '(':
                if string[i] != ')':
                    i += 1
                elif i <= 1:
                    struct.update({'q0': {string[slice_s:i + 1]: 'q1'}})
                    return struct, num_of_graph
                elif slice_s == 0:
                    struct.update({'q0': {string[slice_s:i + 1]: 'q{}'.format(num_of_graph)}})
                    i += 1
                    break
                elif i == size - 1:
                    struct.update({'q{}'.format(num_of_graph): {string[slice_s:i + 1]: 'q1'}})
                    return struct, num_of_graph
                else:
                    struct.update({'q{}'.format(num_of_graph): {string[slice_s:i + 1]: 'q{}'.format(num_of_graph + 1)}})
                    num_of_graph += 1
                    i += 1
                    break

        if i < size and string[i] == '|':
            i += 1
            f_slice = False
            if string[i] == '(':
                slice_s = i
                f_slice = True
                while string[i] != ')':
                    i += 1
            if struct.get('q{}'.format(num_of_graph - 1)) is None:
                ver_start = 'q0'
                last_dict = struct.get(ver_start)
            else:
                ver_start = 'q{}'.format(num_of_graph - 1)
                last_dict = struct.get(ver_start)
            vertex = list(last_dict.keys())
            vertex = last_dict.get(vertex[0])
            if f_slice:
                struct[ver_start].update({string[slice_s:i + 1]: vertex})
            else:
                struct[ver_start].update({string[i]: vertex})
            i += 1
            if i == size:
                change = struct.get('q{}'.format(num_of_graph - 1))
                if change is None:
                    change = struct.get('q0')
                for key in list(change.keys()):
                    change[key] = 'q1'

        if i < size and string[i] == '*':
            if i != size-1 and string[i+1] == '|' and string[i-1] != ')':
                if num_of_graph == 2:
                    struct['q0'].update({'('+string[i-1:i+1]+')': 'q{}'.format(num_of_graph)})
                    struct['q0'].pop(string[i-1:i])
                else:
                    struct['q{}'.format(num_of_graph)].update({'('+string[i-1:i+1]+')': 'q{}'.format(num_of_graph)})
                    struct['q{}'.format(num_of_graph)].pop(string[i - 1:i])
                i += 1
                continue
            elem = struct.get('q{}'.format(num_of_graph - 1))
            if elem is None:
                elem = struct.pop('q0')
                elemN = elem.copy()
                value = list(elem.values())
                elem.clear()
                elem.update({'ε': value[0]})
                struct.update({'q0': elem})
            else:
                struct.pop('q{}'.format(num_of_graph - 1))
                elemN = elem.copy()
                value = list(elem.values())
                elem.clear()
                elem.update({'ε': value[0]})
                struct.update({'q{}'.format(num_of_graph - 1): elem})

            struct.update({'q{}'.format(num_of_graph): elemN})
            if i == size - 1:
                elemN.update({'ε': 'q1'})
            else:
                elemN.update({'ε': 'q{}'.format((num_of_graph + 1))})

            num_of_graph += 1
            i += 1

    return struct, num_of_graph


# def depth_search(struct, num_of_graph):
#     i = 0
#     num_of_graph = 0
#     items = list(struct.values())
#     items_key = list(struct.keys())
#     size_struct = len(struct)
#     while i < size_struct:
#         list_items = list(items[i].keys())
#         j = 0
#         while j < len(items[i].keys()):
#             if 1 >= len(list_items[j]):
#                 j += 1
#                 continue
#             else:
#                 edit_dict = parser(list_items[j][1:len(list_items[j])-1], num_of_graph, struct)
#                 # if num_of_graph == 2:
#                 #     struct[items_key[i]].pop(list_items[j])
#                 #     struct[items_key[i]].update(edit_dict[0]['q0'])
#                 #     struct.update({'q2': edit_dict[0]['q2']})
#                 # else:
#                 struct[items_key[i]].pop(list_items[j])
#                 struct[items_key[i]].update(edit_dict[0]['q{}'.format(num_of_graph)])
#                 struct.update({'q2': edit_dict[0]['q{}'.format(num_of_graph)]})
#                 struct.update(edit_dict[0])
#             j += 1
#         i += 1
#     return struct
