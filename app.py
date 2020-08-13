#!bottle/bin/python

from bottle import (Bottle, request, template, TEMPLATE_PATH)
from pyqrcode import create
from os import path
from lotto import Lotto

VER = '2.3.4'
dir_path = path.dirname(path.realpath(__file__))
TEMPLATE_PATH.insert(0, path.join(dir_path, 'views'))

app = Bottle(__name__)


@app.route('/')
def index():
    lotto = Lotto(None)
    return template('index', version=VER, selected='',
                    games=lotto.games, base=False, exn='')


@app.route('/', method=['POST'])
def results():
    game_type = str(request.forms.get('game_type'))
    lotto = Lotto(game_type)

    base = lotto.get_base_nums()
    exn = lotto.get_exn()
    qrnums = lotto.get_game_code() + ''.join(base) + exn

    qr = create(qrnums)
    qr.png('{}/qrcode.png'.format(path.join(dir_path, 'static')), scale=6)

    return template('index', version=VER, selected=game_type,
                    games=lotto.games, base=base, exn=exn)


if __name__ == '__main__':
    app.run()
