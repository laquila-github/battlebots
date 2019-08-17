# Author: Jerry James 2019
# Copyright (c) Jerry James.
# Released under the terms of GPLv3 or, at your option, any later version of
# the GPL.

import configparser


class MatchConfig:
    """
    Match-specific configuration options, namely:
    - count_secs: the number of seconds to do the beginning countdown
    - match_secs: time limit on a match
    - bell_secs: a bell rings when this many seconds are left in the match
    - tick_rate: number of game ticks per second
    - ticks_per_turn: number of game ticks per player turn
    """

    __slots__ = ["count_secs", "match_secs", "bell_secs", "tick_rate",
                 "ticks_per_turn"]

    def __init__(self, config):
        self.count_secs = int(config['MATCH']['CountSecs'])
        self.match_secs = int(config['MATCH']['MatchSecs'])
        self.bell_secs = int(config['MATCH']['BellSecs'])
        self.tick_rate = int(config['MATCH']['TickRate'])
        self.ticks_per_turn = int(config['MATCH']['TicksPerTurn'])


class ArenaConfig:
    """
    Arena-specific configuration options, namely:
    - width: the width of the arena in pixels
    - height: the height of the arena in pixels
    - start1x: Player 1's starting X position
    - start1y: Player 1's starting Y position
    - start2x: Player 2's starting X position
    - start2y: Player 2's starting Y position
    """

    __slots__ = ["width", "height", "start1x", "start1y", "start2x", "start2y"]

    def __init__(self, config):
        self.width = int(config['ARENA']['Width'])
        self.height = int(config['ARENA']['Height'])
        self.start1x = int(config['ARENA']['Start1X'])
        self.start1y = int(config['ARENA']['Start1Y'])
        self.start2x = int(config['ARENA']['Start2X'])
        self.start2y = int(config['ARENA']['Start2Y'])


class PlayerConfig:
    """
    Player-specific configuration options, namely:
    - width: the width of a player's icon
    - height: the height of a player's icon
    - multiplier: size multiplier used for collision detection
    - health: starting health for a player
    - torpedoes: initial number of photon torpedoes
    - phasers: initial number of phaser shots
    - max_speed: maximum speed of a battle bot in pixels per second
    - phaser_charge: amount of phaser charge gained per turn
    """

    __slots__ = ["width", "height", "multiplier", "health", "torpedoes",
                 "phasers", "max_speed", "phaser_charge"]

    def __init__(self, config):
        self.width = int(config['PLAYER']['Width'])
        self.height = int(config['PLAYER']['Height'])
        self.multiplier = float(config['PLAYER']['Multiplier'])
        self.health = int(config['PLAYER']['Health'])
        self.torpedoes = int(config['PLAYER']['Torpedoes'])
        self.phasers = int(config['PLAYER']['Phasers'])
        self.max_speed = int(config['PLAYER']['MaxSpeed'])
        self.phaser_charge = float(config['PLAYER']['PhaserCharge'])


class PhaserConfig:
    """
    Phaser-specific configuration options, namely:
    - width: the width of a phaser blast
    - height: the height of a phaser blast
    - damage: damage done by a phaser hit
    - speed: speed of a phaser blast
    """

    __slots__ = ["width", "height", "multiplier", "damage", "speed"]

    def __init__(self, config):
        self.width = 6
        self.height = 6
        self.damage = int(config['PHASER']['Damage'])
        self.speed = int(config['PHASER']['Speed'])


class TorpedoConfig:
    """
    Photon torpedo-specific configuration options, namely:
    - width: the width of a photon torpedo
    - height: the height of a photon torpedo
    - damage: damage done by a photon torpedo hit
    - speed: speed of a photon torpedo
    """

    __slots__ = ["width", "height", "multiplier", "damage", "speed"]

    def __init__(self, config):
        self.width = 10
        self.height = 10
        self.damage = int(config['TORPEDO']['Damage'])
        self.speed = int(config['TORPEDO']['Speed'])


class Config:
    """
    Game configuration:
    - match: match-specific configuration
    - arena: arena-specific configuration
    - player: player-specific configuration
    - phaser: phaser-specific configuration
    - torpedo: photon torpedo-specific configuration
    """

    __slots__ = ["match", "arena", "player", "phaser", "torpedo"]

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.match = MatchConfig(config)
        self.arena = ArenaConfig(config)
        self.player = PlayerConfig(config)
        self.phaser = PhaserConfig(config)
        self.torpedo = TorpedoConfig(config)
