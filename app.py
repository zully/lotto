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

    def __init__(self, game_type):
        self.game_type = game_type
        self.games = {'two_step': 'Texas Two Step',
                      'lotto_texas': 'Lotto Texas',
                      'mega_millions': 'Mega Millions',
                      'power_ball': 'Power Ball'}

        if game_type == 'two_step':
            self.game_config = {'pool': 35,
                                'amount': 4,
                                'exn_pool': 35,
                                'game_code': 'WSD1S'}
        elif game_type == 'lotto_texas':
            self.game_config = {'pool': 54,
                                'amount': 6,
                                'exn_pool': False,
                                'game_code': 'WLD1JCMNS'}
        elif game_type == 'mega_millions':
            self.game_config = {'pool': 70,
                                'amount': 5,
                                'exn_pool': 25,
                                'game_code': 'WMD1JCMNS'}
        elif game_type == 'power_ball':
            self.game_config = {'pool': 69,
                                'amount': 5,
                                'exn_pool': 26,
                                'game_code': 'WPD1JCMNS'}
        else:
            self.game_config = None

    def get_num(self, pool):
        num = str(randint(1, pool))

        if len(num) == 1:
            num = '0{}'.format(num)

        return num

    def get_exn(self):
        if not self.game_config['exn_pool']:
            return False

        return self.get_num(self.game_config['exn_pool'])

    def get_base_nums(self):
        base_nums = []

        while len(base_nums) < self.game_config['amount']:
            temp = self.get_num(self.game_config['pool'])

            if temp not in base_nums:
                base_nums.append(temp)

        return sorted(base_nums)

    def get_game_code(self):

        return self.game_config['game_code']


@app.route('/')
def index():
    lotto = Lotto(None)
    return template('index', version=VER, selected='',
                    games=lotto.games, base=False, exn=False)


@app.route('/', method=['POST'])
def results():
    game_type = str(request.forms.get('game_type'))
    lotto = Lotto(game_type)

    base = lotto.get_base_nums()
    exn = lotto.get_exn()

    qrnums = 'LOT21:{}{}'.format(lotto.get_game_code(), ''.join(base))

    if exn:
        qrnums += exn

    qr = create(qrnums)
    qr.png('{}/qrcode.png'.format(path.join(dir_path, 'static')), scale=6)

    return template('index', version=VER, selected=game_type,
                    games=lotto.games, base=base, exn=exn)


if __name__ == '__main__':
    app.run()
