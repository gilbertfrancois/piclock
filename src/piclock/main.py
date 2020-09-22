import os
import time
import datetime
import numpy as np
import pygame

import pygame.gfxdraw


class ClockTheme:
    BLACK = (0, 0, 0)
    DARK_GREY = (30, 30, 30)
    WHITE = (255, 255, 255)
    ORANGE = (200, 100, 0)
    RED = (200, 0, 0)
    NIGHT_RED = (60, 0, 0)
    NIGHT_RED2 = (40, 0, 0)

    def __init__(self, background, ticks, hours, minutes, seconds):
        self.background = background
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.ticks = ticks

class PiClock:
    def __init__(self, screen_width=320, screen_height=240, use_framebuffer=False):
        # os.environ["SDL_FBDEV"] = "/dev/fb1"
        # os.environ["SDL_VIDEODRIVER"] = "fbcon"
        self.print_sdl_variables()
        pygame.init()
        self.screen_resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print("Detected bit depth: ", pygame.display.Info().bitsize)

        print(f"Detected screen size: {self.screen_resolution}")
        print(f"Driver: {pygame.display.get_driver()}")
        print(f"Info:")
        print(pygame.display.Info())
        print("List modes:")
        print(pygame.display.list_modes(32))
        print("---")
        self.surface = pygame.display.set_mode(self.screen_resolution)
        pygame.display.set_caption("My Clock")
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.theme_day = ClockTheme(ClockTheme.WHITE, ClockTheme.DARK_GREY, ClockTheme.BLACK, ClockTheme.BLACK, ClockTheme.ORANGE)
        self.theme_night = ClockTheme(ClockTheme.BLACK, ClockTheme.DARK_GREY, ClockTheme.NIGHT_RED, ClockTheme.NIGHT_RED, ClockTheme.NIGHT_RED2)
        self.theme = self.theme_night
        self.now = datetime.datetime.now()
        status = pygame.font.init()

    def cleanup(self):
        pygame.font.quit()
        pygame.display.quit()

    def print_sdl_variables(self):
        print("Checking current env variables...")
        print("SDL_VIDEODRIVER = {0}".format(os.getenv("SDL_VIDEODRIVER")))
        print("SDL_FBDEV = {0}".format(os.getenv("SDL_FBDEV")))

    def update(self):
        self.now = datetime.datetime.now()
        if (self.now.hour >= 8 and self.now.hour < 22):
                self.theme = self.theme_day
        else:
            self.theme = self.theme_night

    def draw(self):
        self.draw_clock_bg()
        self.draw_ticks(3)
        self.draw_hands(6)
        self.on_event()
        self.clock.tick(30)
        pygame.display.update()

    def on_event(self):
        for event in pygame.event.get():
            # if event.type is pygame.QUIT:
                # self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.is_running = False

    def run(self):
        print("run()")
        self.is_running = True
        while self.is_running:
            self.update()
            self.draw()
        self.cleanup()

    def draw_ticks(self, width):
        center = 0.5 * np.array(self.screen_resolution)
        radius1 = 0.75
        radius2 = 0.95
        for hour in range(12):
            angle = hour / 12 * 2 * np.pi
            self.draw_hand(center, radius1, radius2, angle, width, self.theme.ticks)

    def draw_hands(self, width):
        center = 0.5 * np.array(self.screen_resolution)
        # hour
        angle = self.now.hour / 12 * 2 * np.pi - 0.5 * np.pi
        angle += self.now.minute / 60 / 12 * 2 * np.pi
        self.draw_hand(center, 0.0, 0.66, angle, width, self.theme.hours)
        # minute
        angle = self.now.minute / 60 * 2 * np.pi - 0.5 * np.pi
        self.draw_hand(center, 0.0, 0.95, angle, width, self.theme.minutes)
        # seconds
        angle = self.now.second / 60 * 2 * np.pi - 0.5 * np.pi
        self.draw_hand(center, 0.0, 0.95, angle, 2, self.theme.seconds)
        r = width * 2
        pygame.draw.circle(self.surface, self.theme.hours, (int(center[0]), int(center[1])), int(r))
        r = width
        pygame.draw.circle(self.surface, self.theme.background, (int(center[0]), int(center[1])), int(r))

    def draw_hand(self, center, radius1, radius2, angle, width, color):
        r1 = radius1 * np.min(center)
        r2 = radius2 * np.min(center)
        x0 = int(np.round(center[0] + r1 * np.cos(angle)))
        y0 = int(np.round(center[1] + r1 * np.sin(angle)))
        x1 = int(np.round(center[0] + r2 * np.cos(angle)))
        y1 = int(np.round(center[1] + r2 * np.sin(angle)))
        angle_p = angle - 0.5 * np.pi
        r_list = np.linspace(-width * 0.5, width * 0.5, 4 * width + 1).tolist()
        for r in r_list:
            x00 = x0 + r * np.cos(angle_p)
            y00 = y0 + r * np.sin(angle_p)
            x10 = x1 + r * np.cos(angle_p)
            y10 = y1 + r * np.sin(angle_p)
            # pygame.draw.line(self.surface, color, (x00, y00), (x10, y10), 3)
            pygame.draw.aaline(self.surface, color, (x00, y00), (x10, y10), 1)

    def draw_radial_line(self, center, radius1, radius2, angle, width, color):
        r1 = radius1 * np.min(center)
        r2 = radius2 * np.min(center)
        x0 = int(np.round(center[0] + r1 * np.cos(angle)))
        y0 = int(np.round(center[1] + r1 * np.sin(angle)))
        x1 = int(np.round(center[0] + r2 * np.cos(angle)))
        y1 = int(np.round(center[1] + r2 * np.sin(angle)))
        angle_p = angle - 0.5 * np.pi



    def draw_clock_bg(self):
        center = 0.5 * np.array(self.screen_resolution)
        self.surface.fill(self.theme.background)
        # pygame.draw.circle(self.surface, self.theme.background, (int(center[0]), int(center[1])), int(np.min(center)))



if __name__ == "__main__":
    clock = PiClock(screen_width=320, screen_height=240, use_framebuffer=True)
    clock.run()
