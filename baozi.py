import re
from pprint import pprint


def read_file():
    data = {}
    type = '平'
    p1 = re.compile('\[.+?\]')
    p2 = re.compile('<.+?>')
    with open('data.txt') as f:
        for line_ in iter(lambda: f.readline(), ''):
            line = line_.rstrip()
            if '：' in line:
                if '平' in line:
                    type = '平'
                elif '声' in line:
                    type = '仄'
                else:
                    pass

            else:
                line = p1.sub('', line)
                line = p2.sub('', line)
                for i in line:
                    data[i] = type

    return data


def main():
    data = read_file()
    # pprint(data['['])


if __name__ == '__main__':
    main()
