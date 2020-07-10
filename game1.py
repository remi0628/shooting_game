import pygame, math
from pygame.locals import *
import os
import sys
import re
import random
'''
画像を扱う[pygame.image],図形を描写する[pygame.draw]などPygameの基本的なモジュールは全てpygameの中にあるのでimport.
[pygame.locals]はpygameの様々な定数を格納したモジュール。
'''

START, PLAY, GAMEOVER, TEST, CLEAR, NETA = (0, 1, 2, 3, 4, 5) #ゲーム状態
SCR = Rect(0, 0, 1000, 800)       # スクリーンサイズ(px指定)
x = 0


class Main:
    global x, f, b, t, po1, po2
    C_key = 0

    def __init__(self):
        self.a = 0 # out()
        self.flag = 0
        pygame.init() # Pygame 初期化
        screen = pygame.display.set_mode(SCR.size) # スクリーンサイズの画面作成
        pygame.display.set_caption("Shooting Game")   # タイトルバーの文字
        # imageのロード
        self.load_images()
        # ゲームオブジェクトの初期化
        self.init_game()
        # メインループ
        clock = pygame.time.Clock()
        while True:
            clock.tick(60) # 60fps
            self.update()
            self.draw(screen)
            self.tags.draw(screen)
            pygame.display.update() # 画面を更新
            
            # イベント処理
            for event in pygame.event.get():
                if event.type == QUIT: sys.exit() # 終了イベント
                if event.type == KEYDOWN: # キーを押した時
                    if event.key == K_ESCAPE: sys.exit() # ESC
                    if event.key == K_s:
                        if self.game_state == START:
                            self.game_state = PLAY
                        if self.game_state == GAMEOVER:
                            self.init_game() # ゲームを初期化
                            self.game_state = START
                        if self.game_state == CLEAR:
                            self.init_game()
                            self.game_state = START
                        if self.game_state == NETA:
                            self.game_state = START
                    if event.key == K_t:
                        if self.game_state == START:
                            self.game_state = TEST
                        if self.game_state == GAMEOVER:
                            self.init_game()
                            self.game_state = TEST
                        if self.game_state == CLEAR:
                            self.init_game()
                            self.game_state = TEST
                    if event.key == K_p:
                        if self.game_state == START:
                            self.game_state = NETA
                    # 単発モード
                    if Main.C_key == 0:
                        if event.type == KEYDOWN and event.key == K_SPACE:
                            Shot.shot_sound.play() # 音
                            if t == 1: # 初期弾
                                Shot(self.player.rect.center)
                            if t == 2: # 青いアイテムを取ったら
                                Shot2(self.player.rect.center)
                    if event.key == K_c:
                        if Main.C_key == 0:
                            Main.C_key = 1
                            self.tags.change_char('R') # Repeated
                        elif Main.C_key == 1:
                            Main.C_key = 0
                            self.tags.change_char('T') # One shot
            
    def init_game(self):
        """ゲームオブジェクトを初期化"""
        self.game_state = START
        # スプライトグループを作成して登録(衝突判定に必要)
        self.all      = pygame.sprite.RenderUpdates()
        self.test     = pygame.sprite.RenderUpdates()
        self.players  = pygame.sprite.Group() # プレイヤーグループ
        self.shots    = pygame.sprite.Group() # 弾[自機]グループ
        self.shots2   = pygame.sprite.Group() # 弾2[自機]グループ
        self.enemys   = pygame.sprite.Group() # 敵グループ
        self.mediums  = pygame.sprite.Group() # 中ボスグループ
        self.boss     = pygame.sprite.Group() # ボスグループ
        self.beams    = pygame.sprite.Group() # 弾[敵]グループ
        self.boms     = pygame.sprite.Group() # 弾[boss]グループ
        self.dist     = pygame.sprite.Group() # 弾[散弾]グループ
        self.beams2   = pygame.sprite.Group() # 弾(ビーム)[boss]グループ
        self.items    = pygame.sprite.Group() # アイテムグループ
        # デフォルトスプライトグループを登録
        Player.containers = self.all, self.players, self.test  # プレイヤー       [判]
        Shot.containers   = self.all, self.shots,   self.test  # 弾[自機]グループ  [判]
        Shot2.containers  = self.all, self.shots2              # 弾2[自機]グループ [判]
        Enemy.containers  = self.all, self.enemys              # 敵グループ       [判]
        Medium.containers = self.all, self.mediums             # 中ボスグループ    [判]
        Boss.containers   = self.all, self.boss,    self.test  # ボスグループ      [判]
        Beam.containers   = self.all, self.beams,   self.test  # 弾[敵]グループ    [判]
        Bomb.containers   = self.all, self.boms,    self.test  # 弾[敵]グループ    [判]
        Dist.containers   = self.all, self.dist,    self.test  # 弾[敵]グループ    [判]
        Beam2.containers  = self.all, self.beams2,  self.test  # 弾(ビーム)[boss]グループ [判]
        Explosion.containers = self.all                        # 爆発グループ
        Item.containers = self.all, self.items                 # アイテムグループ   [判]

        # 敵の作成
        for i in range(0, 20): # 出現数を設定
            x = 20 + (i % 10)  * 40
            y = 20 + (i // 10) * 40
            enemys = Enemy((x,y))

        self.player = Player((SCR.width / 2, SCR.bottom)) # 自機の作成
        #計算
        Bomb.player = self.player  # 発射角度を計算するのに必要

        self.tags = Tag() # 情報の表示

        global t
        t = 1

    def update(self):
        """ゲーム状態の更新"""
        global f # 敵2の複製を制限するため
        global b # ボスの複製を制限するため
        if self.game_state == START:
            f = 0
            b = 0
        if self.game_state == PLAY:
            self.all.update()
            # 衝突判定
            self.coll_del()
            # 敵1が全部倒されたら敵2の出現
            if len(self.enemys.sprites()) == 0:
                if f == 0:
                    self.out() # 敵2出現
                # 敵2が全部倒されたら終わり
                if len(self.mediums.sprites()) == 0:
                    if b == 0:
                        self.boss_out() #ボス出現
                        if (self.boss.sprites()) == 0:
                            self.game_state = CLEAR
            # プレイヤーがやられたら終わり
            if len(self.players.sprites()) == 0:
                self.game_state = GAMEOVER
        if self.game_state == GAMEOVER:
            f = 0
            b = 0
        if self.game_state == TEST:
            self.test.update()
            # 衝突判定
            self.coll_del()
            if b == 0:
                self.boss_out()
                if (self.boss.sprites()) == 0:
                    self.game_state = CLEAR
            # プレイヤーがやられたら終わり
            if len(self.players.sprites()) == 0:
                self.game_state = GAMEOVER


    def draw(self, screen):
        screen.fill((0, 0, 0)) # 画面を指定の色で塗りつぶす [full]=塗りつぶす
        if self.game_state == START:      # スタート画面
            # タイトル表示
            title_font = pygame.font.SysFont(None, 80)
            title = title_font.render("Shooting Game", False, (255, 255, 255))
            screen.blit(title, ((SCR.width-title.get_width()) /2, SCR.height / 5))
            # PUSH表示
            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH 'S' KEY", False, (255,255,255))
            screen.blit(push_space, ((SCR.width-push_space.get_width())/2, (SCR.height / 5) * 3))
        elif self.game_state == PLAY:     # ゲームプレイ画面
            self.all.draw(screen)
        elif self.game_state == GAMEOVER: # ゲームオーバー画面
            # GAME OVERを表示
            gameover_font = pygame.font.SysFont(None, 80)
            gameover = gameover_font.render("GAME OVER", False, (255,0,0))
            screen.blit(gameover, ((SCR.width-gameover.get_width()) /2, SCR.height / 5))
            # PUSH表示
            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH 'S' KEY", False, (255,255,255))
            screen.blit(push_space, ((SCR.width-push_space.get_width())/2, (SCR.height / 5) * 3))
        elif self.game_state == TEST:     # テスト画面
            self.test.draw(screen)
        elif self.game_state == CLEAR:    #クリア画面
            # CLEARを表示
            clear_font = pygame.font.SysFont(None, 80)
            clear = clear_font.render("GAME CLEAR!!", False, (255,255,255))
            screen.blit(clear, ((SCR.width-clear.get_width()) /2, SCR.height / 5))
            # PUSH表示
            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH 'S' KEY", False, (255,255,255))
            screen.blit(push_space, ((SCR.width-push_space.get_width())/2, (SCR.height / 5) * 3))
        elif self.game_state == NETA: # ネタ画面
            # GAME OVERを表示
            gameover_font = pygame.font.SysFont(None, 80)
            gameover = gameover_font.render("thankyou!!", False, (255,0,0))
            screen.blit(gameover, ((SCR.width-gameover.get_width()) /2, SCR.height / 5))
            #ネタ
            netaImg = load_image("neta.jpg")
            screen.blit(netaImg, ((SCR.width-netaImg.get_width()) /2,SCR.height / 3))
            push_font = pygame.font.SysFont(None, 25)
            push_space = push_font.render("creator remi", False, (255,255,255))
            screen.blit(push_space, ((((SCR.width-push_space.get_width())/4) * 3), (SCR.height / 6) * 5))
        
    def load_images(self):
        """イメージロード"""
        #スプライト画面登録
        Player.image     = load_image("player/player_1.png")                    # 自機
        Shot.image       = load_image("shot/player_shot_1.png")                 # 自機の弾
        Shot2.images     = split_image(load_image("shot/player_shot_2.png"), 2) # 自機の弾2
        Explosion.images = split_image(load_image("bow.png"), 16)               # 爆発
        Explosion.images2= split_image(load_image("bow.png"), 16)               # 爆発(boss)
        Enemy.images     = split_image(load_image("enemy/enemy_1.png"), 4)      # 敵
        Medium.images    = split_image(load_image("enemy/enemy_2.png"), 5)      # 敵2
        Boss.images      = load_image("enemy/boss.png")
        Bomb.images      = split_image(load_image("shot/boss_shot_2.png"), 6)   # 敵[boss]の弾2
        Dist.image       = load_image("shot/enemy_shot_1.png")
        Beam.image       = load_image("shot/enemy_shot_1.png")                  # 敵の弾
        Beam2.images     = split_image(load_image("shot/boss_shot_1.png"), 5)   # 敵[boss]のビーム
        Item.images      = split_image(load_image("item/item_shot_1.png"), 4)   # item1

    
    def coll_del(self):
        """衝突判定"""
        global x, t
        pro_item1 = 0.5 # item1のドロップ確率
        """playersとenemyとの衝突判定"""
        players_collided = pygame.sprite.groupcollide(self.players, self.enemys, True, True)
        for enemy in players_collided.keys():
            Player.kill_sound.play()
        """playersとmediumsの衝突判定"""
        players_collided2 = pygame.sprite.groupcollide(self.players, self.mediums, True, True)
        """playersとbossの衝突判定"""
        players_collided3 = pygame.sprite.groupcollide(self.players, self.boss, True, True)
        if players_collided2 or players_collided3:
            Player.kill_sound.play()
        """shotとenemyの衝突判定"""
        enemy_collided = pygame.sprite.groupcollide(self.shots, self.enemys, True, True)
        for enemy in enemy_collided.keys():
            Enemy.kill_sound.play()      # 爆発音
            Explosion(enemy.rect.center) # 敵の中心で爆発
            if random.random() < pro_item1:
                Item(enemy.rect.center)  # 敵の中心からアイテムをドロップ
        """shot2とenemyの衝突判定"""
        enemy_collided2 = pygame.sprite.groupcollide(self.shots2, self.enemys, True, True)
        for enemy in enemy_collided2.keys():
            Enemy.kill_sound.play()      # 爆発音
            Explosion(enemy.rect.center) # 敵の中心で爆発
            if random.random() < pro_item1:
                Item(enemy.rect.center)  # 敵の中心からアイテムをドロップ
        """shotとmediumの衝突判定"""
        if x == 1: # 敵が開いた時
            medium_collided  = pygame.sprite.groupcollide(self.mediums, self.shots, True, True)
            medium_collided2 = pygame.sprite.groupcollide(self.mediums, self.shots2, True, True)
            for medium in medium_collided or medium_collided2:
                Enemy.kill_sound.play()      # 爆発音
                Explosion(medium.rect.center) # 敵の中心で爆発
        elif x == 0: # 開いていない時
            medium_nokill_collided  = pygame.sprite.groupcollide(self.mediums, self.shots, False, True)
            medium_nokill_collided2 = pygame.sprite.groupcollide(self.mediums, self.shots2, False, True)
            if medium_nokill_collided or medium_nokill_collided2:
                Medium.nokill_sound.play()
        """bossとshotsの衝突判定"""
        if Boss.boss_hp >= 1:
            boss_collided  = pygame.sprite.groupcollide(self.boss, self.shots, False, True)
            boss_collided2 = pygame.sprite.groupcollide(self.boss, self.shots2, False, True)
            if boss_collided or boss_collided2:
                Boss.boss_hp = Boss.boss_hp - 1
                Boss.nokill_sound.play()
        elif Boss.boss_hp == 0:
            boss_kill  = pygame.sprite.groupcollide(self.boss, self.shots, True, True)
            boss_kill2 = pygame.sprite.groupcollide(self.boss, self.shots2, True, True)
            if boss_kill or boss_kill2:
                Boss.kill_sound.play()
                self.game_state = CLEAR
        """beamとplayerの衝突判定"""
        player_collided = pygame.sprite.groupcollide(self.beams, self.players, True, True)
        """beam2とplayerの衝突判定"""
        player_collided2 = pygame.sprite.groupcollide(self.beams2, self.players, True, True)
        """bombとplayerの衝突判定"""
        player_collided3 = pygame.sprite.groupcollide(self.boms, self.players, True, True)
        """distとplayerの衝突判定"""
        player_collided4 = pygame.sprite.groupcollide(self.dist, self.players, True, True)
        if player_collided or player_collided2 or player_collided3 or player_collided4:
            Player.kill_sound.play()
        """アイテムと自機の衝突判定"""
        item1_collided = pygame.sprite.groupcollide(self.items, self.players, True, False)
        if item1_collided:
            Item.item_sound.play()
            t = 2

    def out(self):
        """敵2出現"""
        global f
        i = SCR.width / 6 # ウィンドウの全体の幅 / 6
        for run in range(5): # ウィンドウより外に配置されないように(5)
            medium = Medium((i + self.a, SCR.height / 3)) # 敵2配置
            self.a += i
        self.a = 0 # 初期化
        f = 1 # 1度のみ

    def boss_out(self):
        """ボス出現"""
        global b
        Boss.boss_hp = 20
        self.bos = Boss((SCR.width / 2, 0)) #ボス配置
        Dist.boss = self.bos # ボスの座標
        b = 1
    """
    #BGMを再生
    pygame.mixer.init(44100, -16,2,2048)
    pygame.mixer.music.load("./sound/BGM.wav")
    pygame.mixer.music.play(-1)
    """

def split_image(image, n):
    image_list = []
    w = image.get_width()
    h = image.get_height()
    w1 = int(w / n)
    for i in range(0, w, w1):
        surface = pygame.Surface((w1,h))
        surface.blit(image, (0,0), (i,0,w1,h))
        surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
        surface.convert_alpha()
        image_list.append(surface)
    return image_list


def load_image(filename, colorkey=None):
    filename = os.path.join("image", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image:", filename)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


class Tag():
    def __init__(self):
        self.sysfont = pygame.font.SysFont("VL-PGothic-Regular.ttf", 40)
        self.char = "T"
    def draw(self, screen):
        score_img = self.sysfont.render(str(self.char), True, (255,255,255))
        screen.blit(score_img, (10, SCR.height - 30))
    def change_char(self, x):
        self.char = x



class Player(pygame.sprite.Sprite):
    """自機"""
    speed = 8 #移動速度
    reload_time = 5 # リロード時間
    pygame.mixer.init(44100, -16,2,2048)
    kill_sound = pygame.mixer.Sound("./sound/se_player_del_1.wav") # 弾衝突時の音源
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.rect.bottom = SCR.bottom # プレイヤーが画面の一番下
        self.reload_timer = 0         # リロード時間初期化
    def update(self):
        # 押されているキーを取得
        # 十字移動(W,A,S,D　キーにも対応)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        # 斜め移動
        if pressed_keys[K_LEFT] and pressed_keys[K_UP] or pressed_keys[K_a] and pressed_keys[K_w]:
            self.rect.move_ip(-self.speed / 5, -self.speed / 5)
        if pressed_keys[K_LEFT] and pressed_keys[K_DOWN] or pressed_keys[K_a] and pressed_keys[K_s]:
            self.rect.move_ip(-self.speed / 5, self.speed / 5)
        if pressed_keys[K_RIGHT] and pressed_keys[K_UP] or pressed_keys[K_d] and pressed_keys[K_w]:
            self.rect.move_ip(self.speed / 5, -self.speed / 5)
        if pressed_keys[K_RIGHT] and pressed_keys[K_DOWN] or pressed_keys[K_d] and pressed_keys[K_s]:
            self.rect.move_ip(self.speed / 5, self.speed / 5)
        self.rect.clamp_ip(SCR) # 画面外に出ないように
        # 弾発射
        global t
        pressed_keys = pygame.key.get_pressed()
        if Main.C_key == 1: # [R]状態かを確認
            if pressed_keys[K_SPACE]:
                if self.reload_timer > 0: # 0になるまでリロード
                    # リロード中
                    self.reload_timer -= 1
                else:
                    # 発射
                    Shot.shot_sound.play()  # 弾発射時の音源
                    self.reload_timer = self.reload_time #リロード時間の初期化
                    if t == 1:
                        self.reload_time = 5
                        Shot(self.rect.center)  # 作成すると同時にallに追加される
                    if t == 2: # 青いアイテムを取ったら
                        self.reload_time = 2
                        Shot2(self.rect.center)

class Enemy(pygame.sprite.Sprite):
    """敵"""
    speed = 2        # 移動速度
    animcycle = 18   # アニメーション速度
    frame = 0        # フレームの初期値
    move_width = SCR.width - 400 # 横方向の移動範囲
    pro_beam = 0.005 # 弾を発射する確率
    pygame.mixer.init(44100, -16,2,2048)
    kill_sound = pygame.mixer.Sound("./sound/se_enemy_del_1.wav")
    def __init__(self, pos):
        # imagesとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.radius = 4 # 当たり判定円の半径
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.left = pos[0]  # 移動できる左端
        self.right = self.left + self.move_width  # 移動できる右端
    def update(self):
        # 横方向への移動
        self.rect.move_ip(self.speed, 0)
        if self.rect.center[0] < self.left or self.rect.center[0] > self.right:
            self.speed = -self.speed
        # ビームを発射
        if random.random() < self.pro_beam:
            Beam(self.rect.center)
            Beam.shot_sound.play()
        # キャラクターアニメーション
        self.frame += 1
        self.image = self.images[int(self.frame / self.animcycle % 4)]

class Medium(pygame.sprite.Sprite):
    """敵2"""
    speed = 2         # 移動速度
    animcycle = 18    # アニメーション速度
    frame = 0         # フレームの初期値
    move_width = 230  # 横方向の移動範囲
    pro_beam = 0.5 # 弾を発射する確率
    pygame.mixer.init(44100, -16,2,2048)
    nokill_sound = pygame.mixer.Sound("./sound/se_medium_nodel_1.wav")
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.transform.rotate(self.images[0], 90)
        self.radius = 4 #当たり判定円の半径
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.max_frame = len(self.images) * self.animcycle  #最後のフレーム
    def update(self):
        global x
        self.frame += 1
        self.image = pygame.transform.rotate(self.images[int(self.frame / self.animcycle % 5)], 90)
        #敵が開いた時に攻撃を受けるように
        if self.images[int(self.frame / self.animcycle % 5)] == self.images[4]:
            x = 1
            if random.random() < self.pro_beam:
                Beam(self.rect.center)
                Beam.shot_sound.play()
        else :
            x = 0

class Boss(pygame.sprite.Sprite):
    """敵 Boss"""
    gun   = (35, 124)  # 銃口[左]の位置
    gun2  = (7, 116)   # 銃口[左]の位置
    gun3  = (0, 90)    # 銃口[左]の位置
    gun4  = (248, 124) # 銃口[右]の位置
    gun5  = (275, 115) # 銃口[右]の位置
    gun6  = (283, 90)  # 銃口[右]の位置
    gun7  = (73, 159)  # 銃口[左]の位置
    gun8  = (210, 159) # 銃口[右]の位置
    gun9  = (94, 142)  # 銃口[左]の位置
    gun10 = (188, 142) # 銃口[左]の位置
    gun11 = (112, 159) # 銃口[左]の位置
    gun12 = (170, 159) # 銃口[左]の位置
    gun12 = (141, 160) # 銃口[中心]の位置
    speed = 2
    speed2 = 2
    pro_beam  = 0.02
    boss_beam = 0.01
    po_dist   = 0.06
    boss_hp = 20
    move_height = 100 # 横方向の移動範囲
    pygame.mixer.init(44100, -16,2,2048)
    beam_sound = pygame.mixer.Sound("./sound/se_boss_beam_2.wav")
    nokill_sound = pygame.mixer.Sound("./sound/se_boss_nodel_1.wav")
    kill_sound = pygame.mixer.Sound("./sound/se_boss_del_1.wav")
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.hp = 20
        self.image = self.images
        self.rect = self.image.get_rect()
        self.rect.left = pos[0]
        self.rect.center = pos
    def update(self):
        global po1, po2, ok
        # 移動
        # 縦方向への移動
        if self.rect.bottom < SCR.height - ((SCR.height / 4) * 3):
            self.rect.move_ip(0, self.speed)
        else :
            self.rect.move_ip(self.speed2, 0)

        if self.rect.left < SCR.width - (SCR.width / 4 * 4) or self.rect.left > SCR.width - (SCR.width / 3):
           self.speed2 = -self.speed2
        
        # 左右からの弾幕
        if random.random() < self.pro_beam: # gun1
            #Beam(self.rect.center)
            Bomb((self.rect.left+self.gun[0], self.rect.top+self.gun[1]))
            Beam.shot_sound.play()
        if random.random() < self.pro_beam: # gun2
            Bomb((self.rect.left+self.gun2[0], self.rect.top+self.gun2[1]))
            Beam.shot_sound.play()
        if random.random() < self.pro_beam: # gun3
            Bomb((self.rect.left+self.gun3[0], self.rect.top+self.gun3[1]))
            Beam.shot_sound.play()
        if random.random() < self.pro_beam: # gun4
            Bomb((self.rect.left+self.gun4[0], self.rect.top+self.gun4[1]))
            Beam.shot_sound.play()
        if random.random() < self.pro_beam: # gun5
            Bomb((self.rect.left+self.gun5[0], self.rect.top+self.gun5[1]))
            Beam.shot_sound.play()
        if random.random() < self.pro_beam: # gun6
            Bomb((self.rect.left+self.gun6[0], self.rect.top+self.gun6[1]))
            Beam.shot_sound.play()
        # 長い銃口からのビーム
        if random.random() < self.boss_beam: # gun7,gun8 
            Beam2((self.rect.left+self.gun7[0], self.rect.top+self.gun7[1]))
            Beam2((self.rect.left+self.gun8[0], self.rect.top+self.gun8[1]))
            Boss.beam_sound.play()
        # 左右から三方向への弾
        if random.random() < self.po_dist: # gun9
            po1, po2 = 90, -48 
            Dist((self.rect.left+self.gun9[0], self.rect.top+self.gun9[1]))
            po1, po2 = 90, -28
            Dist((self.rect.left+self.gun9[0], self.rect.top+self.gun9[1]))
            po1, po2 = 90, -68
            Dist((self.rect.left+self.gun9[0], self.rect.top+self.gun9[1]))
        if random.random() < self.po_dist: # gun10
            po1, po2 = 90, 46
            Dist((self.rect.left+self.gun10[0], self.rect.top+self.gun10[1]))
            po1, po2 = 90, 26
            Dist((self.rect.left+self.gun10[0], self.rect.top+self.gun10[1]))
            po1, po2 = 90, 66
            Dist((self.rect.left+self.gun10[0], self.rect.top+self.gun10[1]))

class Bomb(pygame.sprite.Sprite):
    """boss"""
    speed = 5
    animcycle = 5 # アニメーション速度
    frame = 0      # フレーム初期値
    def __init__(self, gun):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        # 引数で与えた銃口から発射
        self.rect.centerx, self.rect.centery = gun[0], gun[1]
        # 浮動小数点数の座標
        self.fpx = float(self.rect.centerx)
        self.fpy = float(self.rect.centery)
        # 銃口と自機の角度を計算（self.planeはMainで要セット）
        angle = math.atan2(self.player.rect.centery-gun[1], self.player.rect.centerx-gun[0])
        # 移動速度を計算（浮動小数点数）
        self.fpdx = self.speed * math.cos(angle)
        self.fpdy = self.speed * math.sin(angle)
    def update(self):
        # 移動は浮動小数点数で計算（座標が正確）
        self.fpx = self.fpx + self.fpdx
        self.fpy = self.fpy + self.fpdy
        # 描画は整数で（self.rectはスプライトの描画時に使われる）
        self.rect.centerx = int(self.fpx)
        self.rect.centery = int(self.fpy)
        # 画面外だったら消滅
        if not SCR.contains(self.rect):
            self.kill()
        # アニメーション
        self.frame += 1
        self.image = self.images[int(self.frame/self.animcycle%6)]

class Dist(pygame.sprite.Sprite):
    """boss"""
    global po1, po2
    speed = 5
    def __init__(self, gun):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        # 引数で与えた銃口から発射
        self.rect.centerx, self.rect.centery = gun[0], gun[1]
        # 浮動小数点数の座標
        self.fpx = float(self.rect.centerx)
        self.fpy = float(self.rect.centery)
        # 銃口と自機の角度を計算（self.planeはMainで要セット）
        angle = math.atan2(self.boss.rect.centery-gun[1]+po1, self.boss.rect.centerx-gun[0]+po2)
        # 移動速度を計算（浮動小数点数）
        self.fpdx = self.speed * math.cos(angle)
        self.fpdy = self.speed * math.sin(angle)
    def update(self):
        # 移動は浮動小数点数で計算（座標が正確）
        self.fpx = self.fpx + self.fpdx
        self.fpy = self.fpy + self.fpdy
        # 描画は整数で（self.rectはスプライトの描画時に使われる）
        self.rect.centerx = int(self.fpx)
        self.rect.centery = int(self.fpy)
        # 画面外だったら消滅
        if not SCR.contains(self.rect):
            self.kill()

class Explosion(pygame.sprite.Sprite):
    """爆発"""
    animcycle = 2  # アニメーション速度
    frame = 0      # フレームの初期値
    def __init__(self, pos):
        # imagesとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.max_frame = len(self.images) * self.animcycle # 消滅するフレーム
    def update(self):
        # キャラクターアニメーション
        self.image = self.images[int(self.frame/self.animcycle)]
        self.frame += 1
        # フレームが最後までいったら消滅
        if self.frame == self.max_frame:
            self.kill()  #消滅

class Shot(pygame.sprite.Sprite):
    """プレイヤーから放たれる弾"""
    speed = 11 # 速度
    pygame.mixer.init(44100, -16,2,2048)
    shot_sound = pygame.mixer.Sound("./sound/se_player_shot_1.wav")
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos # 中心座標
    def update(self):
        self.rect.move_ip(0, -self.speed) # 上へ
        if self.rect.top < 0: # 上端に到達したら消滅
            self.kill()

class Shot2(pygame.sprite.Sprite):
    """プレイヤーから放たれる弾"""
    speed = 11 # 速度
    animcycle = 30 # アニメーション速度
    frame = 0      # フレーム初期値
    pygame.mixer.init(44100, -16,2,2048)
    shot_sound = pygame.mixer.Sound("./sound/se_player_shot_1.wav")
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos # 中心座標
    def update(self):
        self.rect.move_ip(0, -self.speed) # 上へ
        if self.rect.top < 0: # 上端に到達したら消滅
            self.kill()
        # アニメーション
        self.frame += 1
        self.image = self.images[int(self.frame/self.animcycle%2)]

class Beam(pygame.sprite.Sprite):
    """敵から放たれる弾"""
    speed = 8  # 移動速度
    pygame.mixer.init(44100, -16,2,2048)
    shot_sound = pygame.mixer.Sound("./sound/se_enemy_shot_1.wav")
    def __init__(self, pos):
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos # それぞれの中心座標
    def update(self):
        self.rect.move_ip(0, self.speed)   # 下へ
        if self.rect.bottom > SCR.height:  # 下端に達したら除去
            self.kill()

class Beam2(pygame.sprite.Sprite):
    """boss"""
    speed = 8
    animcycle = 5 # アニメーション速度
    frame = 0      # フレーム初期値
    def __init__(self, gun):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        # 引数で与えた銃口から発射
        self.rect.centerx, self.rect.centery = gun[0], gun[1]
        # 浮動小数点数の座標
        self.fpx = float(self.rect.centerx)
        self.fpy = float(self.rect.centery)
    def update(self):
        self.rect.move_ip(0, self.speed)   # 下へ
        if self.rect.bottom > SCR.height:  # 下端に達したら除去
            self.kill()

class Item(pygame.sprite.Sprite):
    """アイテム"""
    speed = 5      # 移動速度
    animcycle = 20 # アニメーション速度
    frame = 0      # フレーム初期値
    pygame.mixer.init(44100, -16,2,2048)
    item_sound = pygame.mixer.Sound("./sound/se_item_1.wav")
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
        self.rect.move_ip(0, self.speed) #下
        if self.rect.bottom > SCR.height: #下に到達したら削除
            self.kill()
        # キャラクターアニメーション
        self.frame += 1
        self.image = self.images[int(self.frame/self.animcycle%4)]




if __name__ == "__main__":
    Main()
