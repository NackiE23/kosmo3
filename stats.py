import pygame

pygame.font.init()
stats_font = pygame.font.SysFont("comicsans", 24)


class Stats:
    def __init__(self, level, player_vel, power, numbers_of_dead):
        self.level = level
        self.player_vel = player_vel
        self.power = power
        self.numbers_of_dead = numbers_of_dead
        with open("assets/high_score.txt", "r") as f:
            self.high_score = int(f.readline())

    def draw(self, window, height):
        level_label = stats_font.render(f"Wave: {self.level}", True, (154, 134, 23))
        player_vel_label = stats_font.render(f"Player speed: {self.player_vel}", True, (154, 134, 23))
        power_label = stats_font.render(f"Player power: {self.power}", True, (154, 134, 23))
        # high_score_label = stats_font.render(f"Best score: {self.high_score}", True, (154, 134, 23))
        numbers_of_dead_label = stats_font.render(f"Numbers of murders: {self.numbers_of_dead}", True, (154, 134, 23))

        window.blit(level_label, (5, height - 24*4))
        window.blit(player_vel_label, (5, height - 24*3))
        window.blit(power_label, (5, height - 24*2))
        window.blit(numbers_of_dead_label, (5, height - 24))
