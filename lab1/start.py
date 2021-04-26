from CompilersL.lab1.DKA.nka_to_dka import parser_to_dka
from CompilersL.lab1.NKA.parser_to_dict import parser_to_nka


def cin():
    print("Регулярное выражение:")
    str_in_reg = str(input())
    print("Выражение:")
    str_in_value = str(input())
    return str_in_reg, str_in_value


def start_l1():
    # stt = cin()
    nka_dict = parser_to_nka('(ix*|y*o)')
    dka_dict = parser_to_dka(nka_dict)
