import os
import random
import sys
import time
import pygame as pg
import pygame


WIDTH = 1100  # ゲームウィンドウの幅
HEIGHT = 650  # ゲームウィンドウの高さ
NUM_OF_PACKS = 0

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.mixer.init() #音楽の初期化

pygame.mixer.music.load("BGM.mp3") #音楽ファイルの指定
pygame.mixer.music.play(-1) #音楽をループ

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




class Score:
    """
    イニシャライザではフォントと文字色、文字サイズ、
    表示位置の設定を行い、updateメソッドでSurfaceを作成しblit
    """
    def __init__(self, score):
        self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.img = self.fonto.render("スコア：" + str(score), True, (0, 0, 255))
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = (100, HEIGHT-50)

    def update(self, screen: pg.Surface):
        screen.blit(self.img, self.rct)

def title(screen):
    #タイトルに表情される画像のロード、文字の形態を決定
    #タイトルや開始条件を表示しつつ、その間はプログラムを停止させている

    bg_img = pg.image.load("pic/title.jpg") 
    fonto_title1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 120)
    fonto_start = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 40)

    while True:
        screen.blit(bg_img, (0, 0))
        title_w = fonto_title1.render("エアホッケー", True, (255, 255, 0))
        start_UI = fonto_start.render("スペースキーでスタート", True, (100, 100, 100))
        screen.blit(title_w, (WIDTH//2 - title_w.get_width()//2, HEIGHT//3))
        screen.blit(start_UI, (WIDTH//2 - start_UI.get_width()//2, HEIGHT//2 + 100))

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                return


def main():
    pg.display.set_caption("たたかえ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    title(screen)  #title関数を呼び出しタイトルを表示
    bg_img = pg.image.load("pic/download.jpg")
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                # スペースキー押下でBeamクラスのインスタンス生成
                beam = Beam(bird)            
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        bird.update(key_lst, screen) 
        #Scoreクラスのインスタンスを作成し、updateメソッドでblit
        score = Score(COUNTER)
        score.update(screen)
        if beam is not None:
            beam.update(screen)
        for bomb in bombs:
            bomb.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()