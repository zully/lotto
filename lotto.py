#!/usr/bin/python

from random import (randint, seed)
from time import time


class Lotto:

    def __init__(self, game_type):

        self.game_type = game_type
        self.games = {
            'two_step': 'Texas Two Step',
            'lotto_texas': 'Lotto Texas',
            'mega_millions': 'Mega Millions',
            'power_ball': 'Power Ball'
        }

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

    def get_num(self, exn=False):
        pool = self.game_config['pool']

        if exn:
            pool = self.game_config['exn_pool']

        seed(25695975 + time())
        num = str(randint(1, pool))

        if len(num) == 1:
            num = '0{}'.format(num)

        return num

    def get_exn(self):
        if not self.game_config['exn_pool']:
            return ''

        return self.get_num(True)

    def get_base_nums(self):
        base_nums = []

        while len(base_nums) < self.game_config['amount']:
            temp = self.get_num()

            if temp not in base_nums:
                base_nums.append(temp)

        return sorted(base_nums)

    def get_game_code(self):

        return 'LOT21:{}'.format(self.game_config['game_code'])
