import os
import random
import sys
import time
import pygame as pg


WIDTH = 1100  # ゲームウィンドウの幅
HEIGHT = 650  # ゲームウィンドウの高さ
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：スマッシャーやパックなどのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


class Smasher1:
    """
    1Pが操作するスマッシャーに関するクラス
    """

    delta1 = {  # 押下キーと移動量の辞書(1P)
        pg.K_w: (0, -1),
        pg.K_s: (0, +1),
        pg.K_a: (-1, 0),
        pg.K_d: (+1, 0),
    }

    def __init__(self, xy: tuple[int, int]):
        self.img = pg.Surface((100, 100))
        pg.draw.circle(self.img, (255, 0, 0), (50, 50), 50)
        self.img.set_colorkey((0, 0, 0))
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy

    def update(self, key_lst: list[bool], screen: pg.Surface):
        sum_mv = [0, 0]
        for k, mv in __class__.delta1.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rct.move_ip(sum_mv)
        if check_bound(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(self.img, self.rct)

class Smasher2:
    """
    2Pが操作するスマッシャーに関するクラス
    """

    delta2 = {  # 押下キーと移動量の辞書(2P)
        pg.K_UP:(0, -1,),
        pg.K_DOWN:(0, +1),
        pg.K_LEFT:(-1, 0),
        pg.K_RIGHT:(+1,0),
    }

    def __init__(self, xy: tuple[int, int]):
        self.img = pg.Surface((100, 100))
        pg.draw.circle(self.img, (0, 0, 255), (50, 50), 50)
        self.img.set_colorkey((0, 0, 0))
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy

    def update(self, key_lst: list[bool], screen: pg.Surface):
        sum_mv = [0, 0]
        for k, mv in __class__.delta2.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rct.move_ip(sum_mv)
        if check_bound(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(self.img, self.rct)

def main():
    pg.display.set_caption("Air hockey")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("pg_bg.jpg")
    smasher1 = Smasher1([300, 200])
    smasher2 = Smasher2([800, 200])

    while True:
        screen.blit(bg_img, [0, 0])
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 

        key_lst = pg.key.get_pressed()
        smasher1.update(key_lst, screen)
        smasher2.update(key_lst, screen)
        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()