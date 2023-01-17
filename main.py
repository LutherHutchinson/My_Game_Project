import random
import sqlite3
import sys

import pygame

ALL_SPRITES = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(ALL_SPRITES)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


RUNNING_IMAGE_COLLECT_GARBAGE = pygame.image.load('images/john_run.png')
RUNNING_IMAGE_COLLECT_GARBAGE = pygame.transform.scale(
    RUNNING_IMAGE_COLLECT_GARBAGE, (780, 66))
PARTS_OF_RUNNING_IMAGE_COLLECT_GARBAGE = AnimatedSprite(
    RUNNING_IMAGE_COLLECT_GARBAGE, 10, 1, 0, 220)


class Main_Window:
    def __init__(self):
        self.MAIN_RUNNING = True
        self.SCREEN_WIDTH = 626
        self.SCREEN_HEIGHT = 375
        self.SCREEN_TITLE = 'Экологичная игра'

    def draw(self, inf, text_y, screen, size, color):
        pygame.font.init()
        font = pygame.font.Font(None, size)
        text = font.render(inf, True, color)
        text_w = text.get_width()
        text_x = 313 - text_w // 2
        screen.blit(text, (text_x, text_y))

    def play(self):
        pygame.init()
        pygame.display.init()
        pygame.mixer.music.load('music/Back_Music.mp3')
        pygame.mixer.music.play(-1)
        self.MAIN_SCREEN = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.ICON = pygame.image.load('images/icon.png')
        pygame.display.set_caption(self.SCREEN_TITLE)
        pygame.display.set_icon(self.ICON)
        while self.MAIN_RUNNING:
            self.MAIN_SCREEN.fill((56, 159, 228))
            self.draw('Добро пожаловать в игру!', 100, self.MAIN_SCREEN, 60,
                      (255, 255, 255))
            self.draw('Чтобы играть в мини-игру 1, нажми 1', 160,
                      self.MAIN_SCREEN,
                      40, (255, 255, 255))
            self.draw('Чтобы играть в мини-игру 2, нажми 2', 200,
                      self.MAIN_SCREEN,
                      40, (255, 255, 255))
            self.draw('Чтобы выйти, нажми Esc', 240, self.MAIN_SCREEN,
                      40,
                      (255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.MAIN_RUNNING = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        collect_garbage = Collect_Garbage()
                        collect_garbage.play()
                    if event.key == pygame.K_2:
                        kill_garbage = Kill_Garbage(ALL_SPRITES)
                        kill_garbage.play()
                    if event.key == pygame.K_ESCAPE:
                        self.MAIN_RUNNING = False
                        sys.exit()

            pygame.display.flip()
        pygame.quit()


class Make_Sprite(pygame.sprite.Sprite):
    def __init__(self, y, fall_surf, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = fall_surf
        self.rect = self.image.get_rect(center=(650, y))
        self.add(group)

    def update(self, *args):
        if self.rect.x > 0:
            self.rect.x -= 10
        else:
            self.kill()


class Kill_Garbage:
    def __init__(self, ALL_SPRITES):
        pygame.init()
        self.ALL_SPRITES = ALL_SPRITES
        self.RUNNING_KILL_GARBAGE = True
        self.SCREEN_WIDTH = 626
        self.SCREEN_HEIGHT = 375
        self.SCREEN_TITLE_KILL_GARBAGE = 'Сбор мусора'
        self.POINTS = 0
        self.HIGH_JUMP = 10
        self.PLANT_X = 630
        self.PERSON_Y = 220
        self.BACKGROUND_X = 0
        self.IS_START = False
        self.IS_JUMP = False
        self.IS_RUN = False
        self.ALL_PLANTS = pygame.sprite.Group()
        self.ALL_GARBE = pygame.sprite.Group()
        self.WIN_MUSIC = pygame.mixer.Sound('music/Win_Music.mp3')
        pygame.time.set_timer(pygame.USEREVENT, 1500)

    def draw(self, inf, text_y, screen, size, color):
        pygame.font.init()
        font = pygame.font.Font(None, size)
        text = font.render(inf, True, color)
        text_w = text.get_width()
        text_x = 313 - text_w // 2
        screen.blit(text, (text_x, text_y))

    def collide_fall(self):
        for i in self.ALL_PLANTS:
            if self.STAND_IMAGE_RECT.collidepoint(i.rect.center):
                self.RUNNING_COLLECT_GARBAGE = False
                pygame.quit()
                lost_collect_garbage = Lost_Kill_Garbage(
                    self.POINTS)
                lost_collect_garbage.play()
        for j in self.ALL_GARBE:
            if self.STAND_IMAGE_RECT.collidepoint(j.rect.center):
                self.WIN_MUSIC.play()
                self.POINTS += 1
                j.kill()

    def make_fall(self):
        index = random.randint(0, 1)
        x = 270
        if index == 0:
            chosen = pygame.image.load('images/plant.png')
            group = self.ALL_PLANTS
        else:
            chosen = pygame.image.load('images/garbage.png')
            group = self.ALL_GARBE
        return Make_Sprite(x, chosen, group)

    def play(self):
        pygame.init()
        pygame.display.init()
        self.SCREEN_KILL_GARBAGE = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.BACKGROUND = pygame.image.load(
            'images/background.jpg').convert()
        self.STAND_IMAGE = pygame.image.load(
            'images/john_stand_looking_up.png').convert_alpha()
        self.STAND_IMAGE = pygame.transform.scale(self.STAND_IMAGE, (78, 66))
        self.STAND_IMAGE_RECT = self.STAND_IMAGE.get_rect()
        self.CLOCK = pygame.time.Clock()
        while self.RUNNING_KILL_GARBAGE:
            self.SCREEN_KILL_GARBAGE.blit(self.BACKGROUND,
                                          (self.BACKGROUND_X, 0))
            self.SCREEN_KILL_GARBAGE.blit(self.BACKGROUND,
                                          (self.BACKGROUND_X + 626, 0))

            self.CLOCK.tick(15)
            if self.IS_START:
                self.BACKGROUND_X -= 9
                if self.BACKGROUND_X <= -626:
                    self.BACKGROUND_X = 0
                if self.IS_RUN:
                    self.ALL_SPRITES.update()
                    self.ALL_SPRITES.draw(self.SCREEN_KILL_GARBAGE)
                keys = pygame.key.get_pressed()
                if not self.IS_JUMP:
                    if keys[pygame.K_SPACE]:
                        self.IS_JUMP = True
                        self.IS_RUN = False
                    else:
                        self.IS_RUN = True
                else:
                    if self.HIGH_JUMP >= -10:
                        if self.HIGH_JUMP > 0:
                            self.STAND_IMAGE_RECT.y -= self.HIGH_JUMP ** 2 / 3
                            self.PERSON_Y -= self.HIGH_JUMP ** 2 / 3
                            print('+')
                        else:
                            self.STAND_IMAGE_RECT.y += self.HIGH_JUMP ** 2 / 3
                            self.PERSON_Y += self.HIGH_JUMP ** 2 / 3
                            print('-')
                        self.HIGH_JUMP -= 1
                    else:
                        self.IS_JUMP = False
                        self.HIGH_JUMP = 10
                self.draw(f'Счёт: {self.POINTS}', 10, self.SCREEN_KILL_GARBAGE,
                          40, (118, 74, 35))
            else:
                self.draw('Стреляй по мусору, но не наступай на растения', 310,
                          self.SCREEN_KILL_GARBAGE, 30, (255, 255, 255))
                self.draw('Нажми B для старта', 340, self.SCREEN_KILL_GARBAGE,
                          30, (255, 255, 255))

            if not self.IS_START or self.IS_JUMP:
                self.SCREEN_KILL_GARBAGE.blit(self.STAND_IMAGE,
                                              (0, self.PERSON_Y))
            self.ALL_PLANTS.update()
            self.ALL_PLANTS.draw(self.SCREEN_KILL_GARBAGE)
            self.ALL_GARBE.update()
            self.ALL_GARBE.draw(self.SCREEN_KILL_GARBAGE)
            pygame.display.update()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.make_fall()
                if event.type == pygame.QUIT:
                    self.RUNNING_KILL_GARBAGE = False
                    pygame.quit()
                    lost = Lost_Kill_Garbage(self.POINTS)
                    lost.play()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.RUNNING_KILL_GARBAGE = False
                        pygame.quit()
                        lost = Lost_Kill_Garbage(self.POINTS)
                        lost.play()
                    if event.key == pygame.K_b:
                        self.IS_START = True


class Lost_Kill_Garbage:
    def __init__(self, POINTS):
        pygame.init()
        self.POINTS = POINTS
        self.RUNNING_LOST_KILL_GARBAGE = True
        self.SCREEN_WIDTH = 626
        self.SCREEN_HEIGHT = 375
        self.SCREEN_TITLE_LOST_KILL_GARBAGE = 'Выстрел в мусор'
        self.LOST_MUSIC = pygame.mixer.Sound('music/Lost_Music.mp3')
        self.con = sqlite3.connect("Project.sqlite")
        self.cur = self.con.cursor()
        text = f"""INSERT INTO All_Results (Type_of_game, result) VALUES (2, {self.POINTS});"""
        count = self.cur.execute(text)
        self.con.commit()
        self.cur.close()

    def draw(self, inf, text_y, screen, size, color):
        pygame.font.init()
        font = pygame.font.Font(None, size)
        text = font.render(inf, True, color)
        text_w = text.get_width()
        text_x = 313 - text_w // 2
        screen.blit(text, (text_x, text_y))

    def play(self):
        pygame.init()
        pygame.display.init()
        self.SCREEN_LOST_KILL_GARBAGE = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.DEAD_IMAGE_COLLECT_GARBAGE = pygame.image.load(
            'images/john_dead_soul.png').convert_alpha()
        self.DEAD_IMAGE_COLLECT_GARBAGE = pygame.transform.scale(
            self.DEAD_IMAGE_COLLECT_GARBAGE, (156, 180))
        pygame.display.set_caption(self.SCREEN_TITLE_LOST_KILL_GARBAGE)
        while self.RUNNING_LOST_KILL_GARBAGE:
            self.LOST_MUSIC.play()
            self.SCREEN_LOST_KILL_GARBAGE.fill((56, 159, 228))
            self.draw(f'Счёт: {self.POINTS}', 100,
                      self.SCREEN_LOST_KILL_GARBAGE, 60, (255, 255, 255))
            self.draw(f'Чтобы вернуться в главное меню, нажми 1', 30,
                      self.SCREEN_LOST_KILL_GARBAGE, 40, (255, 255, 255))
            self.SCREEN_LOST_KILL_GARBAGE.blit(self.DEAD_IMAGE_COLLECT_GARBAGE,
                                               (240, 150))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUNNING_LOST_KILL_GARBAGE = False
                    pygame.quit()
                    main_window = Main_Window()
                    main_window.play()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.RUNNING_LOST_KILL_GARBAGE = False
                        pygame.quit()
                        main_window = Main_Window()
                        main_window.play()
                    if event.key == pygame.K_1:
                        self.RUNNING_LOST_KILL_GARBAGE = False
                        pygame.quit()
                        main_window = Main_Window()
                        main_window.play()


class Make_Sprite(pygame.sprite.Sprite):
    def __init__(self, x, fall_surf, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = fall_surf
        self.rect = self.image.get_rect(center=(x, 0))
        self.add(group)

    def update(self, *args):
        if self.rect.y < 375:
            self.rect.y += 10
        else:
            self.kill()


class Collect_Garbage:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        self.RUNNING_COLLECT_GARBAGE = True
        self.SCREEN_WIDTH = 626
        self.SCREEN_HEIGHT = 375
        self.SCREEN_TITLE_COLLECT_GARBAGE = 'Сбор мусора'
        self.ALL_PLANTS = pygame.sprite.Group()
        self.ALL_GARBE = pygame.sprite.Group()
        self.IS_START = False
        self.POINTS = 0
        self.WIN_MUSIC = pygame.mixer.Sound('music/Win_Music.mp3')
        pygame.time.set_timer(pygame.USEREVENT, 500)

    def draw(self, inf, text_y, screen, size, color):
        pygame.font.init()
        font = pygame.font.Font(None, size)
        text = font.render(inf, True, color)
        text_w = text.get_width()
        text_x = 313 - text_w // 2
        screen.blit(text, (text_x, text_y))

    def make_fall(self):
        index = random.randint(0, 1)
        x = random.randint(45, 585)
        if index == 0:
            chosen = pygame.image.load('images/plant.png')
            group = self.ALL_PLANTS
        else:
            chosen = pygame.image.load('images/garbage.png')
            group = self.ALL_GARBE
        return Make_Sprite(x, chosen, group)

    def collide_fall(self):
        for i in self.ALL_PLANTS:
            if self.BIN_RECT.collidepoint(i.rect.center):
                self.RUNNING_COLLECT_GARBAGE = False
                pygame.quit()
                lost_collect_garbage = Lost_Collect_Garbage(
                    self.POINTS)
                lost_collect_garbage.play()
        for j in self.ALL_GARBE:
            if self.BIN_RECT.collidepoint(j.rect.center):
                self.WIN_MUSIC.play()
                self.POINTS += 1
                j.kill()

    def play(self):
        pygame.init()
        pygame.display.init()
        self.CLOCK = pygame.time.Clock()
        self.SCREEN_COLLECT_GARBAGE = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.ICON_COLLECT_GARBAGE = pygame.image.load(
            'images/icon_collect_garbage.png')
        self.BACKGROUND = pygame.image.load(
            'images/background.jpg').convert()
        self.BIN = pygame.image.load('images/bin.png').convert_alpha()
        self.BIN_RECT = self.BIN.get_rect(centerx=self.SCREEN_WIDTH // 2,
                                          bottom=self.SCREEN_HEIGHT - 44)

        pygame.display.set_caption(self.SCREEN_TITLE_COLLECT_GARBAGE)
        pygame.display.set_icon(self.ICON_COLLECT_GARBAGE)
        while self.RUNNING_COLLECT_GARBAGE:
            self.collide_fall()
            self.SCREEN_COLLECT_GARBAGE.blit(self.BACKGROUND, (0, 0))
            pos = pygame.mouse.get_pos()
            if not self.IS_START:
                self.draw('Собирай мусор, но не касайся растений!', 200,
                          self.SCREEN_COLLECT_GARBAGE, 30, (255, 255, 255))
                self.draw('Нажми B для старта', 240,
                          self.SCREEN_COLLECT_GARBAGE, 30, (255, 255, 255))
                self.SCREEN_COLLECT_GARBAGE.blit(self.BIN,
                                                 (self.SCREEN_WIDTH // 2,
                                                  self.SCREEN_HEIGHT - 44))
            if self.IS_START:
                self.BIN_RECT.x = pos[0]
                self.BIN_RECT.y = self.SCREEN_HEIGHT - 44
                self.SCREEN_COLLECT_GARBAGE.blit(self.BIN, (pos[0],
                                                            self.SCREEN_HEIGHT - 44))
                self.ALL_PLANTS.update()
                self.ALL_PLANTS.draw(self.SCREEN_COLLECT_GARBAGE)
                self.ALL_GARBE.update()
                self.ALL_GARBE.draw(self.SCREEN_COLLECT_GARBAGE)
                self.draw(f'Счёт: {self.POINTS}', 10,
                          self.SCREEN_COLLECT_GARBAGE,
                          40, (118, 74, 35))

            self.CLOCK.tick(15)
            pygame.display.update()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUNNING_COLLECT_GARBAGE = False
                    pygame.quit()
                    lost_collect_garbage = Lost_Collect_Garbage(
                        self.POINTS)
                    lost_collect_garbage.play()
                if event.type == pygame.USEREVENT:
                    self.make_fall()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.IS_START = True
                    if event.key == pygame.K_ESCAPE:
                        self.RUNNING_COLLECT_GARBAGE = False
                        pygame.quit()
                        lost_collect_garbage = Lost_Collect_Garbage(
                            self.POINTS)
                        lost_collect_garbage.play()


class Lost_Collect_Garbage:
    def __init__(self, POINTS):
        pygame.init()
        self.POINTS = POINTS
        self.RUNNING_LOST_COLLECT_GARBAGE = True
        self.SCREEN_WIDTH = 626
        self.SCREEN_HEIGHT = 375
        self.SCREEN_TITLE_LOST_COLLECT_GARBAGE = 'Сбор мусора'
        self.LOST_MUSIC = pygame.mixer.Sound('music/Lost_Music.mp3')
        self.con = sqlite3.connect("Project.sqlite")
        self.cur = self.con.cursor()
        text = f"""INSERT INTO All_Results VALUES (1, {self.POINTS});"""
        count = self.cur.execute(text).fetchall()
        self.con.commit()
        self.cur.close()

    def draw(self, inf, text_y, screen, size, color):
        pygame.font.init()
        font = pygame.font.Font(None, size)
        text = font.render(inf, True, color)
        text_w = text.get_width()
        text_x = 313 - text_w // 2
        screen.blit(text, (text_x, text_y))

    def play(self):
        pygame.init()
        pygame.display.init()
        self.SCREEN_LOST_KILL_GARBAGE = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.DEAD_IMAGE_COLLECT_GARBAGE = pygame.image.load(
            'images/john_dead.png').convert_alpha()
        self.DEAD_IMAGE_COLLECT_GARBAGE = pygame.transform.scale(
            self.DEAD_IMAGE_COLLECT_GARBAGE, (156, 132))
        pygame.display.set_caption(self.SCREEN_TITLE_LOST_COLLECT_GARBAGE)
        while self.RUNNING_LOST_COLLECT_GARBAGE:
            self.LOST_MUSIC.play()
            self.SCREEN_LOST_KILL_GARBAGE.fill((56, 159, 228))
            self.draw(f'Счёт: {self.POINTS}', 100,
                      self.SCREEN_LOST_KILL_GARBAGE, 60, (255, 255, 255))
            self.draw(f'Чтобы вернуться в главное меню, нажми 1', 30,
                      self.SCREEN_LOST_KILL_GARBAGE, 40, (255, 255, 255))
            self.SCREEN_LOST_KILL_GARBAGE.blit(self.DEAD_IMAGE_COLLECT_GARBAGE,
                                               (240, 150))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUNNING_LOST_COLLECT_GARBAGE = False
                    pygame.quit()
                    main_window = Main_Window()
                    main_window.play()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.RUNNING_LOST_COLLECT_GARBAGE = False
                        pygame.quit()
                        main_window = Main_Window()
                        main_window.play()
                    if event.key == pygame.K_1:
                        self.RUNNING_LOST_COLLECT_GARBAGE = False
                        pygame.quit()
                        main_window = Main_Window()
                        main_window.play()


if __name__ == '__main__':
    main_window = Main_Window()
    main_window.play()
