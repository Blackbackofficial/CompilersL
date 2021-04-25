from CompilersL.lab1.NKA.parser_to_dict import parser_to_nka


def cin():
    print("Регулярное выражение:")
    str_in_reg = str(input())
    print("Выражение:")
    str_in_value = str(input())
    return str_in_reg, str_in_value


def out(dict):
    print(dict)


def start_l1():
    # stt = cin()
    parser_to_nka('(aba)|(ba)|(aab)|(aaab)|(baa)')
