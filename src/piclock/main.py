import os
import time
import datetime
import numpy as np
import pygame
import pygame.gfxdraw

# make sure 

class PiClock:
    def __init__(self, screen_width=320, screen_height=240, use_framebuffer=False):
        os.environ["SDL_FBDEV"] = "/dev/fb1"
        os.environ["SDL_VIDEODRIVER"] = "fbcon"
        self.print_sdl_variables()
        try:
            pygame.init()
        except pygame.error:
            print("Driver '{0}' failed!".format(driver))
        self.screen_resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print("Detected screen size: {0}".format(self.screen_resolution))
        self.surface = pygame.display.set_mode(self.screen_resolution)
        pygame.display.set_caption("My Clock")
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.color_background = (255, 255, 255)
        self.color_hours = (0, 0, 0)
        self.color_minutes = (0, 0, 0)
        self.color_seconds = (200, 100, 0)
        status = pygame.font.init()

    def cleanup(self):
        pygame.font.quit()
        pygame.display.quit()

    def setup(self):
        self.print_sdl_variables()
        print("Setting SDL variables...")
        print("Done.")
        self.print_sdl_variables()

    def print_sdl_variables(self):
        print("Checking current env variables...")
        print("SDL_VIDEODRIVER = {0}".format(os.getenv("SDL_VIDEODRIVER")))
        print("SDL_FBDEV = {0}".format(os.getenv("SDL_FBDEV")))

    def update(self):
        pass

    def draw(self):
        self.surface.fill(self.color_background)
        self.draw_clock_bg()
        self.draw_ticks(3, (20, 20, 20))
        self.draw_hands(6, (0, 0, 0))
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

    def draw_ticks(self, width, color):
        center = 0.5 * np.array(self.screen_resolution)
        radius1 = 0.75
        radius2 = 0.95
        for hour in range(12):
            angle = hour / 12 * 2 * np.pi
            self.draw_hand(center, radius1, radius2, angle, width, color)

    def draw_hands(self, width, color):
        now = datetime.datetime.now()
        center = 0.5 * np.array(self.screen_resolution)
        # hour
        angle = now.hour / 12 * 2 * np.pi - 0.5 * np.pi
        angle += now.minute / 60 / 12 * 2 * np.pi
        self.draw_hand(center, 0.0, 0.66, angle, width, self.color_hours)
        # minute
        angle = now.minute / 60 * 2 * np.pi - 0.5 * np.pi
        self.draw_hand(center, 0.0, 0.95, angle, width, self.color_minutes)
        # seconds
        angle = now.second / 60 * 2 * np.pi - 0.5 * np.pi
        self.draw_hand(center, 0.0, 0.95, angle, 2, self.color_seconds)
        r = width * 2
        pygame.draw.circle(self.surface, self.color_hours, (int(center[0]), int(center[1])), int(r))
        # pygame.gfxdraw.aacircle(self.surface, int(center[0]), int(center[1]), int(r), self.color_hours)

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
            pygame.draw.line(self.surface, color, (x00, y00), (x10, y10), 3)
            # pygame.draw.aaline(self.surface, color, (x00, y00), (x10, y10), 1)

    def draw_clock_bg(self):
        center = 0.5 * np.array(self.screen_resolution)
        self.surface.fill((0, 0, 0))
        pygame.draw.circle(self.surface, self.color_background, (int(center[0]), int(center[1])), int(np.min(center)))



if __name__ == "__main__":
    clock = PiClock(screen_width=320, screen_height=240, use_framebuffer=True)
    clock.run()
