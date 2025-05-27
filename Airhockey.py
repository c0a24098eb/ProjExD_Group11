import os
import random
import sys
import time
import pygame as pg


WIDTH = 1100  # ゲームウィンドウの幅
HEIGHT = 650  # ゲームウィンドウの高さ

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pg.mixer.init() #音楽の初期化

pg.mixer.music.load("BGM.mp3") #音楽ファイルの指定
pg.mixer.music.play(-1) #音楽をループ

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

class Puck:
    """
    puckに関するクラス
    引数は色タプルと円の半径
    """
    def __init__(self, color: tuple[int, int, int], rad: int):
        """
        puck
        """
        self.img = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.img, color, (rad, rad), rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = 550, 325
        self.vx, self.vy = +1, +1

    def update(self, screen: pg.Surface):
        """
        puckを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        yoko, tate = check_bound(self.rct)
        if not yoko:
            self.vx *= -1
        if not tate:
            self.vy *= -1
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)
        # pg.display.update()

    


class Smasher1:
    """
    1Pが操作するスマッシャーに関するクラス
    delta1に応じて移動する赤色の円形オブジェクト
    """

    delta1 = {  # 押下キーと移動量の辞書(1P)
        pg.K_w: (0, -2),
        pg.K_s: (0, +2),
        pg.K_a: (-2, 0),
        pg.K_d: (+2, 0),
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
        # pg.display.update()

class Smasher2:
    """
    2Pが操作するスマッシャーに関するクラス
    delta2に応じて移動する青色の円形オブジェクト
    """

    delta2 = {  # 押下キーと移動量の辞書(2P)
        pg.K_UP:(0, -2,),
        pg.K_DOWN:(0, +2),
        pg.K_LEFT:(-2, 0),
        pg.K_RIGHT:(+2,0),
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
        # pg.display.update()

def render_outline_text(font, message, fg_color, outline_c, outline_width):
    """
    タイトル画面の文字列に外枠を増やす
    """

    base = font.render(message, True, fg_color)
    size = base.get_width() + 2 * outline_width, base.get_height() + 2 * outline_width
    outline = pg.Surface(size, pg.SRCALPHA)

    # 輪郭用の文字
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                img = font.render(message, True, outline_c)
                outline.blit(img, (dx + outline_width, dy + outline_width))

    # 中央に本来の文字
    outline.blit(base, (outline_width, outline_width))
    return outline

def title(screen):
    """
    タイトルに表情される画像のロード、文字の形態を決定
    タイトルや開始条件を表示しつつ、その間はプログラムを停止させている
    """

    bg_img = pg.image.load("pic/title.jpg") 
    fonto_title = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 120)
    fonto_start = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 40)
 

    while True:
        screen.blit(bg_img, (0, 0))
        title_w = render_outline_text(fonto_title, "エアホッケー", (255, 255, 0), (0, 0, 0), 3)
        screen.blit(title_w, (WIDTH // 2 - title_w.get_width() // 2, HEIGHT // 3))
        title_w = fonto_title.render("エアホッケー", True, (255, 255, 0))
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
            
def countdown(screen):
    """
    タイトルでスペースを押した後、
    ３秒のカウントダウン
    """
    bg_img = pg.image.load("pic/download.jpg")
    font_c = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 150)
    font_in = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 40)

    for i in range(4, 0, -1):
        screen.blit(bg_img, (0, 0))

        c_txt = font_c.render(str(i), True, (255, 255, 255))
        info1 = font_in.render("1P操作：WASDキー", True, (255, 100, 100))
        info2 = font_in.render("2P操作：↑ ↓ ← → キー", True, (100, 100, 255))
        info3 = font_in.render("スマッシャーでパックを弾いて相手のゴールを狙おう！", True, (255, 255, 0))

        screen.blit(c_txt, (WIDTH // 2 - c_txt.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, HEIGHT -150))
        screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, HEIGHT -100))
        screen.blit(info3, (WIDTH // 2 - info3.get_width() // 2, HEIGHT -50))

        pg.display.update()
        pg.time.delay(1000)  # 1sec


def main():
    pg.display.set_caption("Air hockey")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    title(screen)  #title関数を呼び出しタイトルを表示
    countdown(screen)   #countdown関数を呼び出して表示
    bg_img = pg.image.load("pic/download.jpg")
    screen.blit(bg_img, [0, 0])
    smasher1 = Smasher1([300, 200])
    smasher2 = Smasher2([800, 200])
    puck = Puck((105, 105, 105), 20)

    score1, score2 = 0, 0#スコア
    left_goal = pg.Rect(0, 280 - 75, 10, 250)#ゴール
    right_goal = pg.Rect(WIDTH - 10, 280 - 75, 10, 250)
    

    while True:
        screen.blit(bg_img, [0, 0])

        pg.draw.rect(screen, (255, 255, 0), left_goal)#ゴール
        pg.draw.rect(screen, (255, 255, 0), right_goal)

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 
            
        key_lst = pg.key.get_pressed()
        smasher1.update(key_lst, screen)
        smasher2.update(key_lst, screen)
        puck.update(screen)
        
        if smasher1.rct.colliderect(puck.rct):
            # スマッシャーに当たったらバウンド
            puck.vx *= -1
            puck.vy *= -1
        if smasher2.rct.colliderect(puck.rct):
            # スマッシャーに当たったらバウンド
            puck.vx *= -1
            puck.vy *= -1
            #Scoreクラスのインスタンスを作成し、updateメソッドでblit
            # score = Score(COUNTER)
            # score.update(screen)
    
            # tmr += 1
            # clock.tick(200)

        if puck.rct.colliderect(left_goal):
            score2 += 1
            puck.rct.center = (WIDTH//2, HEIGHT//2)
            puck.vx, puck.vy = 0, 0  # 一時停止
            screen.blit(bg_img, [0, 0])
            screen.blit(puck.img, puck.rct)
            screen.blit(smasher1.img, smasher1.rct)
            screen.blit(smasher2.img, smasher2.rct)
            pg.draw.rect(screen, (255, 255, 0), left_goal)
            pg.draw.rect(screen, (255, 255, 0), right_goal)
            font = pg.font.Font(None, 50)
            score_txt = font.render(f"P1: {score1}  P2: {score2}", True, (255, 255, 255))
            screen.blit(score_txt, (WIDTH//2 - 100, 10))
            pg.display.update()
            time.sleep(1)
            puck.vx = random.choice([1, 1])
            puck.vy = random.choice([-3, -2, 2, 3])

        # ← 変更点：右ゴールに入ったらP1得点
        if puck.rct.colliderect(right_goal):
            score1 += 1
            puck.rct.center = (WIDTH//2, HEIGHT//2)
            puck.vx, puck.vy = 0, 0  # 一時停止
            screen.blit(bg_img, [0, 0])
            screen.blit(puck.img, puck.rct)
            screen.blit(smasher1.img, smasher1.rct)
            screen.blit(smasher2.img, smasher2.rct)
            pg.draw.rect(screen, (255, 255, 0), left_goal)
            pg.draw.rect(screen, (255, 255, 0), right_goal)
            font = pg.font.Font(None, 50)
            score_txt = font.render(f"P1: {score1}  P2: {score2}", True, (255, 255, 255))
            screen.blit(score_txt, (WIDTH//2 - 100, 10))
            pg.display.update()
            time.sleep(1)
            puck.vx = random.choice([-1, -1])
            puck.vy = random.choice([-3, -2, 2, 3])

        # ← 変更点：スコアを画面に表示
        font = pg.font.Font(None, 50)
        score_txt = font.render(f"P1: {score1}  P2: {score2}", True, (255, 255, 255))
        screen.blit(score_txt, (WIDTH//2 - 100, 10))

        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()