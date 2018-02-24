import json
import re
from utils import (
    log,
    format,
    conv_zhs,
)


class Yun:
    def __init__(self):
        with open('yun.json') as f:
            self.yun = json.loads(f.read())

    def yun_from_char(self, char: str):
        y = self.yun.get(char)
        if not y:
            char = conv_zhs(char)
        return self.yun.get(char)

    def check_tail(self, song: list):
        err = []
        y = None
        tail_yuns = []
        for i, line in enumerate(song):
            if i % 2 != 0:
                # 对句
                if not y:
                    y = self.yun_from_char(line[-1])
                    tail_yuns.append(y)
                else:
                    tail_yun = self.yun_from_char(line[-1])
                    tail_yuns.append(tail_yun)
                    # log(y, line, tail_yun)
                    if [i for i in tail_yun if i in y] == []:
                        # 韵部不同
                        err.append(format('rule3 error: 句尾韵部不同. line',
                                          i+1, line, y, tail_yun))

        return tail_yuns, err


class Parser:
    def __init__(self):
        with open('pingze.json') as f:
            self.pingze = json.loads(f.read())

    def pz_from_char(self, char):
        pz = self.pingze.get(char)
        if pz:
            return pz
        else:
            char_zhs = conv_zhs(char)
            pz = self.pingze.get(char_zhs)
            if pz:
                return pz
            else:
                return char

    def parse(self, song: str):
        result = [self.pz_from_char(char) for char in song]
        return ''.join(result)


def song_list(song: str) -> list:
    p = re.compile('[\n ]')
    song = p.sub('', song)
    p = re.compile('[,.，。]')
    s = [i for i in p.split(song) if i]
    return s


def same_line(line_pz: str, pingze: str, force: bool=True) -> bool:
    # line_pz_len = len(line_pz)
    # if line_pz_len < len(pingze):
    pingze = pingze[-len(line_pz):]

    for i, char in enumerate(line_pz):
        if force:
            if (pingze[i] != '中') and (char != pingze[i]):
                return False
        else:
            if (char != '中') and (pingze[i] != '中') and (char != pingze[i]):
                return False
    else:
        return True


# def test_same_line():
#     line_pz = '仄平仄平仄'
#     pingze = '中平中平仄平仄'
#
#     log(same_line(line_pz, pingze))
#     exit()
#
#
# test_same_line()


def oushuzi(line: str):
    _oushuzi = [char for i, char in enumerate(line) if i % 2 != 0]
    oushuzi = ''.join(_oushuzi)
    return oushuzi


def rule1(song: list):
    # 1. 句内 偶数字（2、4、6）之间平仄是否相反，即是否为仄平仄、平仄平、平仄、仄平，如果是，则合律。
    # （中仄）中平仄平仄；（中平）中仄中仄仄，（中仄）中平平仄平。两句特殊句式，也合律。
    err = []
    for index, line in enumerate(song):
        o = oushuzi(line)
        if '平平' in o or '仄仄' in o:
            err.append(format('rule1 error: 句内 偶数字（2、4、6）之间平仄未相反. line',
                       index+1))

    return err


def compare_oushuzi(line1: str, line2: str, should_same: bool):
    o1 = oushuzi(line1)
    o2 = oushuzi(line2)
    for i1, i2 in zip(o1, o2):
        if i1 == '中' or i2 == '中':
            ...
        elif should_same:
            if i1 != i2:
                return False
        else:
            if i1 == i2:
                return False
    else:
        return True


def rule2(song: list):
    # 句间 偶数字（2、4、6）同一联的出句和对句，偶数字平仄是否相反，如果相反，则合律。
    # 每联间的对句和出句，偶数字平仄是否相同，如果相同，则合律。
    err = []
    for i, line in enumerate(song):
        if i % 2 == 0:
            if not compare_oushuzi(line, song[i+1], should_same=False):
                err.append(format('rule2-1 error: 同一联的出句和对句，偶数字平仄未相反. line',
                                  i+1))
        elif i + 1 < len(song):
            if not compare_oushuzi(line, song[i+1], should_same=True):
                err.append(format('rule2-2 error: 每联间的对句和出句，偶数字平仄不相同. line',
                                  i+1))

    return err


def rule3(song: list, song_pz: list, yun: Yun):
    # 检测句末最后一个字是否在同一韵部（提供给你的平水韵），偶数句最后一个字都在同一韵部，
    # 奇数句除第一句外（因为第一句可以押韵也可以不押韵）的最后一个字的平仄与偶数句最后一个字的平仄相反，则合律。
    tail_yuns, err = yun.check_tail(song)

    for i, line in enumerate(song_pz):
        if i == 0 or i == 1:
            ...
        elif i % 2 == 0:
            pz = line[-1]
        else:
            tail_pz = line[-1]
            if pz != '中' and tail_pz != '中' and tail_pz == pz:
                err.append(format('rule3-2 error: 奇数句除第一句外的最后一个字的平仄\
与偶数句最后一个字的平仄未相反. line', i+1, line))

    return tail_yuns, err


def rule4(song_pz: list):
    # 检测是否出现中仄仄平仄仄平，仄平仄仄平（孤平），中平中仄平平平，中仄平平平（三连平）出现，如果有，则不合律。
    err = []
    for i, line in enumerate(song_pz):
        if same_line(line, '中仄仄平仄仄平') or same_line(line, '中平中仄平平平'):
            err.append(format('rule4 error: 出现孤平／三连平. line', i+1))

    return err


def spec_pz(song_pz: list):
    tmp_song_pz = []
    for i, line in enumerate(song_pz):
        if same_line(line, '中仄中平仄平仄', force=False):
            # log('spec1,')
            tmp_song_pz.append('中仄平平平仄仄'[-len(line):])
        elif same_line(line, '中平中仄中仄仄', force=False) and \
                same_line(song_pz[i+1], '中仄中平平仄平', force=False):
            tmp_song_pz.append('中平中仄中平仄'[-len(line):])
        else:
            tmp_song_pz.append(line)

    return tmp_song_pz


class Baozi:
    def __init__(self):
        self.parser = Parser()
        self.yun = Yun()

    def check_song(self, song: str):
        parser = self.parser
        yun = self.yun

        song_l = song_list(song)
        song_pz_str = parser.parse(song)
        song_pz_bak = song_list(song_pz_str)
        song_pz = spec_pz(song_pz_bak)
        # song_pz = ['仄平仄仄平平仄', '仄仄平平仄仄平', '平仄中平中仄仄', '平平平仄中平平']

        err = rule1(song_pz)
        err.extend(rule2(song_pz))
        tail_yuns, err3 = rule3(song_l, song_pz, yun)
        err.extend(err3)
        err.extend(rule4(song_pz))

        return dict(
            song_pz=song_pz_bak,
            tail_yuns=tail_yuns,
            err=err
        )


if __name__ == '__main__':
    song1 = '床前明月光，疑是地上霜。举头望明月，低头思故乡。'
    song2 = '''
    舍南舍北皆春水，
    但见群鸥日日来。
    花径不曾缘客扫，
    蓬门今始为君开。
    盘飧市远无兼味，
    樽酒家贫只旧醅。
    肯与邻翁相对饮，
    隔篱呼取尽馀杯。'''
    song3 = '''畫樓吹笛妓，金椀酒家胡。
    錦石稱貞女，青松學大夫。
    脫貂貰桂醑，射雁與山廚。
    聞道高陽會，愚公谷正愚。'''
    song4 = '江边踏青罢，回首见旌旗。风起春城暮，高楼鼓角悲。'
    song = song4
    bz = Baozi()
    log(bz.check_song(song))
