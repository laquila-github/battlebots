# Author: Jason Taylor 2019
# Copyright (c) Jason Taylor.

import math
from abc import ABC, abstractmethod


# Class that gives a bot all the information about the game, which it utilizes to decide what actions to take.
class TurnInfo:
    """
        enemy_x, enemy_y        (x,y) coordinates of the enemy bot.
        enemy_direction         Direction the enemy bot is heading (at the end of the last turn).
        enemy_speed             Speed of enemy bot (at the end of the last turn).
        enemy_health            The health of the enemy bot.
        enemy_muzzle_flash      True if the enemy fired something on the last turn.
        my_torpedoes            Number of torpedoes your bot has left.
        my_phasers              Phaser energy your bot has (shooting a phaser takes 1 phaser energy).
        my_x, my_y              (x,y) coordinates of my bot.
        my_direction            Direction your bot is heading.
        my_speed                Speed of your bot.
        my_health               Health of your bot.
        time_left               Number of seconds left in the match.
    """
    def __init__(self, enemy_x, enemy_y, enemy_direction, enemy_speed, enemy_health, enemy_muzzle_flash,
                 my_torpedoes, my_phasers, my_x, my_y, my_direction, my_speed, my_health, time_left):
        self.enemy_x = enemy_x
        self.enemy_y = enemy_y
        self.enemy_direction = enemy_direction
        self.enemy_speed = enemy_speed
        self.enemy_health = enemy_health
        self.enemy_muzzle_flash = enemy_muzzle_flash
        self.my_torpedoes = my_torpedoes
        self.my_phasers = my_phasers
        self.my_x = my_x
        self.my_y = my_y
        self.my_direction = my_direction
        self.my_speed = my_speed
        self.my_health = my_health
        self.time_left = time_left


# Class that specifies what actions a bot should take.
class TurnAction:
    """
        direction        0 - 360 degrees, with 0 being right, 90 up, etc.
        speed            0 - 150 pps (pixels per second).
        fire_direction   0 - 360 degrees.
        fire_phaser      True or False, should bot fire phaser now?
        fire_torpedo     True or False, should bot fire torpedo now?
                         * Note: Phaser and Torpedo cannot be fired at the same time.
    """
    def __init__(self, direction, speed, fire_direction, fire_phaser, _fire_torpedo):
        self.direction = direction
        self.speed = speed
        self.fire_direction = fire_direction
        self.fire_phaser = fire_phaser
        self.fire_torpedo = _fire_torpedo


# Base class for a bot, players should create a class called MyBot that inherits from this class.
class PlayerBot(ABC):
    @staticmethod  # utility method that gets the direction and distance the enemy is from your bot.
    def get_enemy_direction_and_distance(enemy_x, enemy_y, my_x, my_y):
        enemy_direction = 360 - math.degrees(math.atan2(enemy_y - my_y, enemy_x - my_x))
        enemy_direction = enemy_direction - 360 if enemy_direction > 360 else enemy_direction
        distance = math.sqrt(((enemy_x - my_x) ** 2) + ((enemy_y - my_y) ** 2))
        return enemy_direction, distance

    @abstractmethod
    def take_turn(self, info):
        return None

    @abstractmethod
    def get_name(self):
        return None
