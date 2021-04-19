from start import cin
from NKA.parser_to_dict import parser


def main():
    # stt = cin()
    dic = parser('a|(ab)|(vd)a(se)')
    print(dic)


if __name__ == '__main__':
    main()
