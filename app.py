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

    def get_num(pool):
        num = str(randint(1, pool))

        if len(num) == 1:
            num = '0{}'.format(num)

        return num

    def get_base_nums(self, pool, amount):
        base_nums = []

        while len(base_nums) < amount:
            temp = self.get_num(pool)

            if temp not in base_nums:
                base_nums.append(temp)

        return sorted(base_nums)

    @app.route('/')
    def index(self):

        return template('index', version=VER, selected='',
                        games=self.games, base=False, exn=False)

    @app.route('/', method=['POST'])
    def give_nums(self):
        game_type = str(request.forms.get('game_type'))

        if game_type == 'lotto_texas':
            base = self.get_base_nums(54, 6)
            exn = False
            game_code = 'WLD1JCMNS'

        elif game_type == 'power_ball':
            base = self.get_base_nums(69, 5)
            exn = self.get_num(26)
            game_code = 'WPD1JCMNS'

        elif game_type == 'mega_millions':
            base = self.get_base_nums(70, 5)
            exn = self.get_num(25)
            game_code = 'WMD1JCMNS'

        elif game_type == 'two_step':
            base = self.get_base_nums(35, 4)
            exn = self.get_num(35)
            game_code = 'WSD1S'

        qrnums = 'LOT21:{}{}'.format(game_code, ''.join(base))

        if exn:
            qrnums += exn

        qr = create(qrnums)
        qr.png('{}/qrcode.png'.format(path.join(dir_path, 'static')), scale=6)

        return template('index', version=VER, selected=game_type,
                        games=self.games, base=base, exn=exn)


if __name__ == '__main__':
    app.run()
