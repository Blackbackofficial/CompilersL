from start import cin
from NKA.parser_to_dict import parser
from dot import dict_dot_notate


def main():
    # stt = cin()
    dic = parser('(a|b)(a|b)')

    print(dic)


if __name__ == '__main__':
    main()
