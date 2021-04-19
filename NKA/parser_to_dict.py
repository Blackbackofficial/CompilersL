def parser(str):
    num = 1
    num_of_graph = 2
    struct = dict()
    i = 0
    size = len(str)

    while i < size:
        while i < size and (i < size and str[i] != '(' and str[i] != '|' and str[i] != '*' and str[i] != ')'):
            if size == 1:
                struct.update({'q0': {str[i]: 'q1'}})
                return struct
            elif i == 0:
                struct.update({'q0': {str[i]: 'q{}'.format(num_of_graph)}})
            elif i == size - 1:
                struct.update({'q{}'.format(num): {str[i]: 'q1'}})
                return struct
            else:
                struct.update({'q{}'.format(num): {str[i]: 'q{}'.format(num_of_graph + 1)}})
                num_of_graph += 1
            num += 1
            i += 1

        slice_s = i
        while (i <= size - 1 or str[i-1] == '(') and str[i] != '|' and str[i] != '*':
            if str[i] != ')':
                i += 1
            elif i <= 1:
                struct.update({'q0': {str[slice_s:i+1]: 'q1'}})
                return struct
            elif slice_s == 0:
                struct.update({'q0': {str[slice_s:i + 1]: 'q{}'.format(num_of_graph)}})
                num += 1
                i += 1
                break
            elif i == size - 1:
                struct.update({'q{}'.format(num): {str[slice_s:i+1]: 'q1'}})
                return struct
            else:
                struct.update({'q{}'.format(num): {str[slice_s:i+1]: 'q{}'.format(num_of_graph + 1)}})
                num += 1
                i += 1
                break

        if str[i] == '|':
            i += 1
            f_slice = False
            if str[i] == '(':
                slice_s = i
                f_slice = True
                while str[i] != ')':
                    i += 1
            if struct.get('q{}'.format(num_of_graph-1)) is None:
                ver_start = 'q0'
                last_dict = struct.get(ver_start)
            else:
                ver_start = 'q{}'.format(num_of_graph-1)
                last_dict = struct.get(ver_start)
            vertex = list(last_dict.keys())
            vertex = last_dict.get(vertex[0])
            if f_slice:
                struct[ver_start].update({str[slice_s:i+1]: vertex})
            else:
                struct[ver_start].update({str[i]: vertex})
            i += 1
            if i == size:
                change = struct.get('q{}'.format(num_of_graph - 1))
                if change is None:
                    change = struct.get('q0')
                for key in list(change.keys()):
                    change[key] = 'q1'


    return struct


def find_multiplication(size, string):
    size += 1


# def find_bracket():
