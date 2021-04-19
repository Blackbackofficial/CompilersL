from start import cin
from NKA.parser_to_dict import parser, depth_search


def main():
    # stt = cin()
    start_dict = parser('a*|b')
    edit_dict = depth_search(start_dict[0], start_dict[1])
    print(start_dict[0])


if __name__ == '__main__':
    main()
