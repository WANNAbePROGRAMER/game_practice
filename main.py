
import pygame
import random
import os

FPS = 60

WIDTH = 500
HEIGHT = 600

WHITE = (255,255,255)
GREEN = (0,255,0)
RED   = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

pygame.init()
#把pygame裡的東西都做初始化的動作
screen = pygame.display.set_mode((WIDTH,HEIGHT))
#可以傳入一個元組 畫面的寬度和高度不會去動他所以設成元組
pygame.display.set_caption("太空打飛機")
#可以改遊戲的標題               
clock = pygame.time.Clock()
#創建一個物件來對時間管理和操控


#載入圖片
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
#os.path代表現在PYTHON這個檔的位置，然後去找img資料夾，再去找background.png
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()


#sprite是Pygame內建的類別可以用來表示畫面上顯示的所有東西
class Player(pygame.sprite.Sprite):
#讓Player去繼承sprite的類別
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #先CO內建的sprite的初始函式
        self.image = pygame.transform.scale(player_img, (50,38))
        #可以轉變圖片長寬
        self.image.set_colorkey(BLACK)
        #把黑色變透明   
        self.rect = self.image.get_rect()
        #把飛機框起來 
        self.radius = 20 
        #寬度50決定的
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        #在這張圖片上畫圓形，圓心是在這張圖片的中心點，圓形半徑25
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        #飛船的起始位置中心點的X在中間Y在底部上面一點
        self.speedx = 8


    def update(self):
        key_pressed = pygame.key.get_pressed()
        #會回傳一整串的布靈值，代表鍵盤上的每個案件有沒有被按
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        #右鍵有被按所以座標向右
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx   
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        #跑超過寬度就會卡在邊邊
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet) 
        #把子彈加到all_sprites群組這樣才會畫出來
        bullets.add(bullet) 


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = rock_img
        #存還未轉動的圖片
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        #存放轉動過後的圖片
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2 
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        #會從0到後面那個數之間隨機一個數出來當作石頭出現的位置，
        #因為石頭有寬度所以要記得減掉
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)
        #石頭掉下來時的速度(y座標的移動速度)
        self.total_degree = 0
        self.rot_degree = 3
        #轉動幾度


    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree %360
        #轉超過360度等於沒轉
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        #利用PYGAME原本就有的函式把石頭的照片變成轉動的石頭照片
        #因為如果一直用轉動過的石頭照片繼續轉動會失真
        #所以特地存了一個沒轉動動過的石頭照片每次轉動都是轉沒轉過的石頭照片
        center = self.rect.center
        self.rect = self.image.get_rect()
        #因為每次的轉動都沒從新定位這個圖形的位置，所以每次的旋轉
        #都不會繞著同樣的中心點最旋轉，有危和感
        #所以記住原本圖形中心的位置，繞著同個中心做旋轉
        self.rect.center = center
    
    def update(self): 
        self.rotate()
        #石頭會自轉
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right <0:
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,10) 
            self.speedx = random.randrange(-3,3)
        #如果石頭超出寬度或是掉到下面，從新隨機1次(石頭重新掉落)


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
    #因為子彈是從飛船是從飛船射出，
    #所以需要輸入飛船的位置
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(RED)  
        #顯示石頭的顏色
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        #子彈的中心點的X座標就在飛船現在的位置
        self.rect.bottom = y
        self.speedy = -10
        #子彈是往我們視窗上面射(Y軸減少)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
        #子彈射到程式上方超出螢幕，去所有的SPRITE群組把子彈刪除
    
    



all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
#把player加到sprite的群組
for i in range(8):
    r = Rock()
    all_sprites.add(r)
#這個迴圈會跑8次所以總共會有8顆石頭掉下
    rocks.add(r)
#石頭創建的時候也把他加到石頭的群組        





#遊戲的迴圈 = 取得玩家的輸入>>更新遊戲>>把它渲染顯示到畫面上
running = True
while running:
    clock.tick(FPS)
    #代表這個迴圈在一秒鐘之內最多只能執行十次
    #取得輸入
    for event in pygame.event.get():
    #會回傳現在遊戲發生的所有事件 例如:滑鼠點擊
    #回傳的列表會用迴圈去跑他每個值(所有發生的事件)
        if event.type == pygame.QUIT:
           #關閉遊戲
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        #如果這個事件是(按下鍵盤鍵)就判斷他按的是不是空白鍵    
        # 是的話會去呼叫飛船的函式(射擊)   



    #更新遊戲


    all_sprites.update()
    #會去執行這個群組每個物件的update函式
    #把所有物件的位置做更新
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    #sprites提供內建的函式來判斷這兩個群組的東西有沒有碰撞到
    #後面兩個布林值式第一個表示石頭和子彈碰撞到的話，石頭要不要刪掉
    #第二個是子彈要不要刪掉
    for hit in hits:
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
    #因為hits會收到函式回傳的字典，裡面寫的是碰撞到的石頭和子彈
    #所以用個FOR迴圈每次只要有碰撞消失的石頭就補一顆    
    hits = pygame.sprite.spritecollide(player, rocks, False,pygame.sprite.collide_circle)
    #第三個也是布林值當飛船和石頭撞到石要不要把石頭刪掉
    #函數的預設碰撞判斷式矩形，並沒有那麼精準所以多傳一個參數把它換成碰撞判斷
    #改成圓形
    #就得額外給player和飛船額外radius的屬性
    if hits:
        running = False
    #如果有值代表飛船有撞到直接遊戲關掉


    #畫面顯示
    screen.fill(WHITE)
    screen.blit(background_img, (0,0))
    #代表把BACKGROUND畫到(0,0)的位置(這樣才可以占滿整個畫面)  
    all_sprites.draw(screen)
    #把這個群組的東西都畫到畫面上
    pygame.display.update()

pygame.quit()            
