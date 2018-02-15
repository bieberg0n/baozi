# coding:utf-8
from pprint import pprint
import re
import json


def log(*args):
    if len(args) == 1:
        pprint(*args)
    else:
        print(*args)


def parse(line: str, yun: dict, pingze: dict):
    p = re.compile('\[.+?\]')
    line = p.sub('', line)
    # try:
    k, v = line.split('　')
    # except ValueError as e:
    #     log(e, line)
    #     exit()
    # yun[k] = v

    voice = '平' if '平' in k else '仄'
    for char in v:
        if yun.get(char):
            yun[char].append(k)
        else:
            yun[char] = [k]
        if pingze.get(char) and pingze.get(char) != voice:
            pingze[char] = '中'
        else:
            pingze[char] = voice


def main():
    yun = {}
    pingze = {}

    with open('平水韵.txt', encoding='utf-8') as f:
        for line in iter(lambda: f.readline(), ''):
            txt = line.rstrip('\n')
            if txt:
                # log(txt)
                parse(txt, yun, pingze)

    with open('yun.json', 'w') as f:
        f.write(json.dumps(yun, ensure_ascii=False, indent=2))
    with open('pingze.json', 'w') as f:
        f.write(json.dumps(pingze, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
