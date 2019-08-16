import battlebotspublic


class MyBot(battlebotspublic.PlayerBot):
    def __init__(self, config):
        self.seconds = 0
        self.config = config

    def get_name(self):
        return "Timmy"

    def take_turn(self, info):
        e_dir, e_dist = battlebotspublic.PlayerBot.get_enemy_direction_and_distance(info.enemy_x, info.enemy_y,
                                                                                    info.my_x, info.my_y)
        direction = 270
        if self.seconds < 2:
            direction = 90
        self.seconds += self.config.match.ticks_per_turn / self.config.match.tick_rate
        if self.seconds >= 4:
            self.seconds = 0
        action = battlebotspublic.TurnAction(direction, 100, e_dir, True, True)
        return action
