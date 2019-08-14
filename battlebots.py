# Author: Jason Taylor 2019
# Copyright (c) Jason Taylor.

import pygame
import importlib
import sys
import random
import math
import battlebotspublic

# COLORS
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 200)
red = (175, 0, 0)
orange = (200, 100, 0)


class ObjectType:
    none = 0
    ship = 1
    bullet = 2
    powerup = 3


class States:
    pre = 0
    battle = 1
    player_1_wins = 2
    player_2_wins = 3
    draw = 4


class GameObject:
    def __init__(self, obj_type, image, health, x, y, direction, speed):
        self.obj_type = obj_type
        self.image = image
        self.health = health
        self.x = x
        self.y = y
        self.direction = direction
        self._cosTheta = math.cos(math.radians(direction))
        self._sinTheta = math.sin(math.radians(direction))
        self.speed = speed
        self.ticks_before_removal = -1

    def set_direction(self, direction):
        self.direction = direction
        self._cosTheta = math.cos(math.radians(direction))
        self._sinTheta = math.sin(math.radians(direction))

    def update(self):
        old_x = self.x
        old_y = self.y
        distance = self.speed * (1 / 60)
        self.x = self._cosTheta * distance + self.x
        self.y = self.y - self._sinTheta * distance

        if self.obj_type == ObjectType.ship:
            if (self.x < 0 + self.image.get_rect().width / 2 or
                    self.x > 800 - self.image.get_rect().width / 2 or
                    self.y < 0 + self.image.get_rect().height / 2 or
                    self.y > 600 - self.image.get_rect().height / 2):
                self.x = old_x
                self.y = old_y
                self.speed = 0
        elif self.obj_type == ObjectType.bullet:
            if self.x < -10 or self.x > 810 or self.y < -10 or self.y > 610:
                return True

        if self.ticks_before_removal > 0:
            self.ticks_before_removal -= 1
        if self.ticks_before_removal == 0:
            return True
        else:
            return False

    def render(self, screen):
        width = self.image.get_rect().width
        height = self.image.get_rect().height
        render_x = self.x - width / 2
        render_y = self.y - height / 2
        screen.blit(self.image, (render_x, render_y))
        # pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(render_x, render_y, width, height), 1)

    def collides_with(self, obj):
        self_multiplier = 1.0 if self.obj_type == ObjectType.bullet else 0.8
        obj_multiplier = 1.0 if obj.obj_type == ObjectType.bullet else 0.8
        width1 = self.image.get_rect().width * self_multiplier
        height1 = self.image.get_rect().height * self_multiplier
        width2 = obj.image.get_rect().width * obj_multiplier
        height2 = obj.image.get_rect().height * obj_multiplier

        r1 = pygame.Rect(self.x - width1 / 2,
                         self.y - height1 / 2,
                         width1,
                         height1)

        r2 = pygame.Rect(obj.x - width2 / 2,
                         obj.y - height2 / 2,
                         width2,
                         height2)

        return r1.colliderect(r2)


class PlayerObject(GameObject):
    def __init__(self, name, image, x, y):
        GameObject.__init__(self, ObjectType.ship, image, 10, x, y, 0, 0)
        self.name = name
        self.torpedoes = 5
        self.phasers = 5
        self.fired_last_turn = False

    def render(self, screen):
        GameObject.render(self, screen)
        font = pygame.font.Font('Eurostile.ttf', 10)
        text = font.render(self.name, True, white, black)
        text_rect = text.get_rect()
        text_rect.center = (self.x, self.y + self.image.get_rect().height / 2 + 6)
        screen.blit(text, text_rect)
        if self.health > 0:
            pygame.draw.line(screen, green, (self.x - 10, self.y + 27), (self.x - 10 + self.health * 2, self.y + 27), 2)


# *********************
# MAIN EXECUTION BEGINS
# *********************

if len(sys.argv) != 3:
    print("Invalid arguments!")
    print("Usage: battlebots.py <player1bot> <player2bot>")
    print("Example: battlebots.py samplebot1 samplebot2")
    exit(0)

pygame.init()
pygame.display.set_caption('Battle Bots')

game_screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# LOAD IMAGES & SOUNDS
images = dict()
images['p1'] = pygame.image.load('p1.png')
images['p2'] = pygame.image.load('p2.png')
images['b1'] = pygame.image.load('b1.png')
images['torpedo'] = pygame.image.load('torpedo.png')
images['e1'] = pygame.image.load('e1.png')
images['e2'] = pygame.image.load('e2.png')

sounds = dict()
sounds['phaser'] = pygame.mixer.Sound('phaser.wav')
sounds['torpedo'] = pygame.mixer.Sound('torpedo.wav')
sounds['hit'] = pygame.mixer.Sound('hit.wav')
sounds['explode'] = pygame.mixer.Sound('explode.wav')
sounds['bell'] = pygame.mixer.Sound('bell.wav')
sounds['horn'] = pygame.mixer.Sound('horn.wav')
sounds['gameover'] = pygame.mixer.Sound('gameover.wav')

bgmusic = "bg" + str(random.randint(1, 2)) + ".mp3"
pygame.mixer.music.load(bgmusic)
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play()

# GAME STATE & PLAYER SETUP
player_1_bullets = []
player_2_bullets = []
powerups = []
effects = []

p1_lib = importlib.import_module(sys.argv[1])
player_1_ai = p1_lib.MyBot()
p2_lib = importlib.import_module(sys.argv[2])
player_2_ai = p2_lib.MyBot()

# Setup Player 1
player_1_ship = PlayerObject(player_1_ai.get_name(), images['p1'], 100, 300)

# Setup Player 2
player_2_ship = PlayerObject(player_2_ai.get_name(), images['p2'], 700, 300)

state = States.pre
seconds_passed = 0
quarter_seconds_passed = 0


# Utility method to remove list of elements from a list (can this be done easier with a splice?)
def remove_elements(the_list, elements_to_remove):
    for element in elements_to_remove:
        try:
            the_list.remove(element)
        except ValueError:
            pass


# CREATE EXPLOSION OBJECT
def make_explosion(obj):
    image = images['e1'] if obj is not player_1_ship and obj is not player_2_ship else images['e2']
    exp = GameObject(ObjectType.none, image, 0, obj.x, obj.y, 0, 0)
    exp.ticks_before_removal = 10
    return exp


# GIVE PLAYER A TURN
def player_turn(player, player_ai, other_player):
    # Gather turn info
    info = battlebotspublic.TurnInfo(enemy_x=other_player.x, enemy_y=other_player.y,
                                     enemy_direction=other_player.direction, enemy_speed=other_player.speed,
                                     enemy_health=other_player.health, enemy_muzzle_flash=other_player.fired_last_turn,
                                     my_torpedoes=player.torpedoes, my_phasers=player.phasers, my_x=player.x,
                                     my_y=player.y, my_direction=player.direction, my_speed=player.speed,
                                     my_health=player.health, time_left=125-seconds_passed)

    # Send info to player AI & get back turn action
    action = player_ai.take_turn(info)
    return action


# PROCESS THE PLAYER'S ACTIONS
def process_player_action(action, player, player_bullets):
    action.speed = 0 if action.speed < 0 else action.speed
    action.speed = 150 if action.speed > 150 else action.speed
    player.set_direction(action.direction)
    player.speed = action.speed
    if action.fire_phaser and player.phasers >= 1:
        bullet = GameObject(ObjectType.bullet, images['b1'], 1, player.x, player.y, action.fire_direction, 400)
        player_bullets.append(bullet)
        player.phasers -= 1
        player.fired_last_turn = True
        sounds['phaser'].play()
    elif action.fire_torpedo and player.torpedoes > 0:
        bullet = GameObject(ObjectType.bullet, images['torpedo'], 5, player.x, player.y, action.fire_direction, 300)
        player_bullets.append(bullet)
        player.torpedoes -= 1
        player.fired_last_turn = True
        sounds['torpedo'].play()
    else:
        player.fired_last_turn = False
    # Player regenerates phaser energy 1 per second (or 0.25 per quarter second)
    player.phasers += 0.25


# UPDATE OBJECTS, CALCULATE COLLISIONS, UPDATE GAME STATE
def update(time_for_player_turn):
    global state
    # Give each player a turn if it's time
    if state == States.battle and time_for_player_turn:
        action1 = player_turn(player_1_ship, player_1_ai, player_2_ship)
        action2 = player_turn(player_2_ship, player_2_ai, player_1_ship)
        process_player_action(action1, player_1_ship, player_1_bullets)
        process_player_action(action2, player_2_ship, player_2_bullets)

    # Update all game objects
    update_object_list(effects)
    if state == States.battle:
        player_1_ship.update()
        player_2_ship.update()
        update_object_list(powerups)
        update_object_list(player_1_bullets)
        update_object_list(player_2_bullets)

    # Check for collisions
    player_1_died = False
    player_2_died = False
    if state == States.battle:
        # Check for ship collisions
        if player_1_ship.collides_with(player_2_ship):
            if player_1_ship.health > player_2_ship.health:
                player_2_ship.health = 0
                player_2_died = True
                player_1_ship.health -= player_2_ship.health
                effects.append(make_explosion(player_2_ship))
            elif player_2_ship.health > player_1_ship.health:
                player_1_ship.health = 0
                player_1_died = True
                player_2_ship.health -= player_1_ship.health
                effects.append(make_explosion(player_1_ship))
            else:
                player_1_ship.health = player_2_ship.health = 0
                player_1_died = player_2_died = True
                effects.append(make_explosion(player_1_ship))
                effects.append(make_explosion(player_2_ship))

        objects_to_remove = []
        # Check for bullet to ship collisions
        for bullet in player_2_bullets:
            if player_1_ship.collides_with(bullet):
                player_1_ship.health -= bullet.health
                objects_to_remove.append(bullet)
                effects.append(make_explosion(bullet))
                sounds['hit'].play()
                if player_1_ship.health <= 0:
                    player_1_ship.health = 0
                    player_1_died = True
                    effects.append(make_explosion(player_1_ship))
                    break
        remove_elements(player_2_bullets, objects_to_remove)
        objects_to_remove.clear()
        for bullet in player_1_bullets:
            if player_2_ship.collides_with(bullet):
                player_2_ship.health -= bullet.health
                objects_to_remove.append(bullet)
                effects.append(make_explosion(bullet))
                sounds['hit'].play()
                if player_2_ship.health <= 0:
                    player_2_ship.health = 0
                    player_2_died = True
                    effects.append(make_explosion(player_2_ship))
                    break
        remove_elements(player_1_bullets, objects_to_remove)
        objects_to_remove.clear()

        # Check for bullet to bullet collisions
        for bullet1 in player_1_bullets:
            for bullet2 in player_2_bullets:
                if bullet1 not in objects_to_remove and bullet2 not in objects_to_remove:
                    if bullet1.collides_with(bullet2):
                        objects_to_remove.append(bullet1)
                        objects_to_remove.append(bullet2)
                        effects.append(make_explosion(bullet1))
                        effects.append(make_explosion(bullet2))
                        sounds['hit'].play()
        remove_elements(player_1_bullets, objects_to_remove)
        remove_elements(player_2_bullets, objects_to_remove)
        objects_to_remove.clear()

        # Check for ship / powerup collisions
        # TODO

    # Did anyone die?
    if player_1_died and player_2_died:
        state = States.draw
        sounds['gameover'].play()
    elif player_1_died and not player_2_died:
        state = States.player_2_wins
        sounds['gameover'].play()
    elif player_2_died and not player_1_died:
        state = States.player_1_wins
        sounds['gameover'].play()

    # Is time up for the match?
    if state == States.battle:
        sec = 125 - seconds_passed
        if sec <= 0:
            if player_1_ship.health > player_2_ship.health:
                state = States.player_1_wins
                sounds['gameover'].play()
            elif player_2_ship.health > player_1_ship.health:
                state = States.player_2_wins
                sounds['gameover'].play()
            else:
                state = States.draw
                sounds['gameover'].play()


def update_object_list(the_list):
    objects_to_remove = []
    for obj in the_list:
        if obj.update():
            objects_to_remove.append(obj)
    remove_elements(the_list, objects_to_remove)
    objects_to_remove.clear()


def draw_text(text, size, color,  x, y):
    font = pygame.font.Font('Eurostile.ttf', size)
    text = font.render(text, True, color, black)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    game_screen.blit(text, text_rect)


def draw_start_countdown():
    global state
    msg = player_1_ai.get_name() + " vs " + player_2_ai.get_name()
    countdown = 5 - seconds_passed
    if countdown > 0:
        draw_text(msg, 50, red, 400, 200)
        draw_text(str(countdown), 50, red, 400, 250)
    elif countdown == 0:
        draw_text("Begin", 50, red, 400, 200)
    else:
        state = States.battle


def draw_outcome():
    msg = "Draw"
    if state == States.player_1_wins:
        msg = player_1_ai.get_name() + " wins!"
    elif state == States.player_2_wins:
        msg = player_2_ai.get_name() + " wins!"
    draw_text(msg, 50, blue, 400, 200)


def digital_time(seconds):
    mins, seconds = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d' % (mins, seconds)


# RENDER
def render():
    game_screen.fill((0, 0, 0))
    if state == States.battle:
        seconds = 125 - seconds_passed
        if seconds >= 10:
            draw_text(digital_time(seconds), 16, white, 400, 10)
        else:
            if quarter_seconds_passed % 2 == 0:
                draw_text(digital_time(seconds), 16, white, 400, 10)
    if player_1_ship.health > 0:
        player_1_ship.render(game_screen)
    if player_2_ship.health > 0:
        player_2_ship.render(game_screen)
    for obj in powerups:
        obj.render(game_screen)
    for obj in player_1_bullets:
        obj.render(game_screen)
    for obj in player_2_bullets:
        obj.render(game_screen)
    for obj in effects:
        obj.render(game_screen)
    if state == States.pre:
        draw_start_countdown()
    elif state == States.draw or state == States.player_1_wins or state == States.player_2_wins:
        draw_outcome()
    pygame.display.flip()


# GAME LOOP
frame = 0
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("mouse at (%d, %d)" % event.pos)

    turn = True if (frame == 0 or frame == 15 or frame == 30 or frame == 45) else False
    update(turn)
    render()
    clock.tick(60)
    frame += 1
    if frame == 15 or frame == 30 or frame == 45 or frame == 60:
        quarter_seconds_passed += 1
    if frame == 60:
        frame = 0
        seconds_passed += 1
        # Play horn sound when match begins
        if seconds_passed == 5:
            sounds['horn'].play()
        # Play ticking sounds when match is almost over
        if state == States.battle:
            secs = 125 - seconds_passed
            if secs == 10:
                sounds['bell'].play()