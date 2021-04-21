from start import cin
from NKA.parser_to_dict import brackets_parser, depth_search


def main():
    # stt = cin()
    start_dict = brackets_parser('ab|((cd))')
    parser_dict = depth_search(start_dict[0], start_dict[1])
    print(parser_dict)


if __name__ == '__main__':
    main()
