def parser(string):
    num = 1
    start = 'q0'
    end = 'q1'
    num_of_graph = 2
    struct = dict()
    i = 0
    size = len(string)

    if size == 1:
        struct.update({start: {string[i]: end}})
    elif i == 0:
        struct.update({start: {string[i]: 'q{}'.format(num_of_graph)}})
        # while i < size:
    while i < size and string[i] != '(' and string[i] != '|' and string[i] != '*':

        if i == size - 1:
            struct.update({'q{}'.format(num): {string[i]: end}})
            num_of_graph += 1
        else:
            struct.update({'q{}'.format(num): {string[i]: 'q{}'.format(num_of_graph + 1)}})
            num_of_graph += 1
        num += 1
        i += 1

        # while i < size or string[i] == '(':
        #     if i == size - 1:
        #         struct.update({'q{}'.format(num): {string[i]: 'q{}'.format(end)}})
        #     i += 1
        #     if 'q{}'.format(num) in struct:
        #         struct['q{}'.format(num)].update({string[i]: 'q{}'.format(1 + num)})
        #     num += 1

    return struct
