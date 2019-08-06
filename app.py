#!bottle/bin/python

#  Lotto Generator

from bottle import (Bottle, request, template, TEMPLATE_PATH)
from random import randint
from pyqrcode import create
from os import path

VER = '2.2.9'
dir_path = path.dirname(path.realpath(__file__))
TEMPLATE_PATH.insert(0, path.join(dir_path, 'views'))

app = Bottle(__name__)


class Lotto:

    def __init__(self):
        self.games = {'two_step': 'Texas Two Step',
                      'lotto_texas': 'Lotto Texas',
                      'mega_millions': 'Mega Millions',
                      'power_ball': 'Power Ball'}
        self.two_step = {'pool': 35,
                         'amount': 4,
                         'exn_pool': 35,
                         'game_code': 'WSD1S'}
        self.lotto_texas = {'pool': 54,
                            'amount': 6,
                            'exn_pool': False,
                            'game_code': 'WLD1JCMNS'}
        self.mega_millions = {'pool': 70,
                              'amount': 5,
                              'exn_pool': 25,
                              'game_code': 'WMD1JCMNS'}
        self.power_ball = {'pool': 69,
                           'amount': 5,
                           'exn_pool': 26,
                           'game_code': 'WPD1JCMNS'}

    def get_num(pool):
        if not pool:
            return False

        num = str(randint(1, pool))

        if len(num) == 1:
            num = '0{}'.format(num)

        return num

    def get_exn(self, game_type):

        return self.get_num(self.game_type['exn_pool'])

    def get_base_nums(self, game_type):
        base_nums = []

        while len(base_nums) < self.game_type['amount']:
            temp = self.get_num(self.game_type['pool'])

            if temp not in base_nums:
                base_nums.append(temp)

        return sorted(base_nums)

    def get_game_code(self, game_type):

        return self.game_type['game_code']


lotto = Lotto()


@app.route('/')
def index():

    return template('index', version=VER, selected='',
                    games=lotto.games, base=False, exn=False)


@app.route('/', method=['POST'])
def give_nums():
    game_type = str(request.forms.get('game_type'))

    base = lotto.get_base_nums(game_type)
    exn = lotto.get_num(game_type)
    game_code = lotto.get_game_code(game_type)

    qrnums = 'LOT21:{}{}'.format(game_code, ''.join(base))

    if exn:
        qrnums += exn

    qr = create(qrnums)
    qr.png('{}/qrcode.png'.format(path.join(dir_path, 'static')), scale=6)

    return template('index', version=VER, selected=game_type,
                    games=lotto.games, base=base, exn=exn)


if __name__ == '__main__':
    app.run()
