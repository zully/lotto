#!bottle/bin/python

#  Lotto Generator

from bottle import (Bottle, request, template, TEMPLATE_PATH)
from random import randint
from pyqrcode import create
from os import path

VER = '2.2.9'
dir_path = path.dirname(path.realpath(__file__))
views_path = path.join(dir_path, 'views')
static_path = path.join(dir_path, 'static')
TEMPLATE_PATH.insert(0, views_path)

app = Bottle(__name__)

def get_num(pool):
    num = str(randint(1, pool))

    if len(num) == 1:
        num = '0{}'.format(num)

    return num


def get_base_nums(pool, amount):
    base_nums = []

    while len(base_nums) < amount:
        temp = get_num(pool)

        if temp not in base_nums:
            base_nums.append(temp)

    return sorted(base_nums)


def get_games():

    return {'two_step': 'Texas Two Step',
            'lotto_texas': 'Lotto Texas',
            'mega_millions': 'Mega Millions',
            'power_ball': 'Power Ball'}


@app.route('/')
def index():
    numdict = {'base': False, 'exn': False}

    return template('index', version=VER, selected='',
                    games=get_games(), nums=numdict)


@app.route('/', method=['POST'])
def give_nums():
    game_type = str(request.forms.get('game_type'))
    numdict = {}

    if game_type == 'lotto_texas':
        numdict['base'] = get_base_nums(54, 6)
        numdict['exn'] = False
        game_code = 'WLD1JCMNS'

    elif game_type == 'power_ball':
        numdict['base'] = get_base_nums(69, 5)
        numdict['exn'] = get_num(26)
        game_code = 'WPD1JCMNS'

    elif game_type == 'mega_millions':
        numdict['base'] = get_base_nums(70, 5)
        numdict['exn'] = get_num(25)
        game_code = 'WMD1JCMNS'

    elif game_type == 'two_step':
        numdict['base'] = get_base_nums(35, 4)
        numdict['exn'] = get_num(35)
        game_code = 'WSD1S'

    qrnums = 'LOT21:{}{}'.format(game_code, ''.join(numdict['base']))

    if numdict['exn']:
        qrnums += numdict['exn']

    qr = create(qrnums)
    qr.png('{}/qrcode.png'.format(static_path), scale=6)

    return template('index', version=VER, selected=game_type,
                    games=get_games(), nums=numdict)


if __name__ == '__main__':
    app.run()

