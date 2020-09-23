import datetime

import numpy as np
import pygame
import pygame.gfxdraw


class Theme:
    BLACK = (0, 0, 0)
    LIGHT_GRAY = (210, 210, 210)
    DARK_GRAY = (60, 60, 60)
    WHITE = (255, 255, 255)
    ORANGE = (200, 100, 0)
    RED = (200, 0, 0)
    NIGHT_RED = (100, 0, 0)
    NIGHT_RED2 = (60, 0, 0)

    def __init__(self, background, ticks, hours, minutes, seconds, pivot, logo, date):
        self.settings = {
            "background": {"color1": Theme.BLACK, "color2": background, "center": [0.0, 0.0], "radius1": 0.0},
            "ticks": {"color": ticks, "center": [0.0, 0.0], "radius1": 0.75, "radius2": 0.95, "width": 0.04},
            "hours": {"color": hours, "center": [0.0, 0.0], "radius1": 0.0, "radius2": 0.66, "width": 0.04},
            "minutes": {"color": minutes, "center": [0.0, 0.0], "radius1": 0.0, "radius2": 0.95, "width": 0.04},
            "seconds": {"color": seconds, "center": [0.0, 0.0], "radius1": 0.0, "radius2": 0.95, "width": 0.02},
            "pivot": {"color": pivot, "center": [0.0, 0.0], "radius1": 0.04},
            "logo": {"color": logo, "font_size": 24 / 240, "center": [0.0, -(0.5 * 0.75)], "label": "TREBLIG"},
            "date": {"color": date, "font_size": 36 / 240, "label": "", "border_margin": [-0.03, -0.015, 0.03, 0.015]}
        }
        self.settings["date"]["center"] = \
            [self.settings.get("ticks").get("radius1") - self.settings.get("date").get("font_size"), 0.0]
        self.settings = self.to_numpy(self.settings)

    def to_numpy(self, val: dict):
        for k, v in val.items():
            if isinstance(v, dict):
                v = self.to_numpy(v)
                val[k] = v
            elif isinstance(v, list):
                val[k] = np.array(v)
        return val

    def to_list(self, val: dict):
        for k, v in val.items():
            if isinstance(v, dict):
                val[k] = self.to_list(v)
            elif isinstance(v, np.ndarray):
                val[k] = v.tolist()
        return val

    def get(self, key):
        return self.settings[key]

    def set(self, key1, key2, value):
        self.settings[key1][key2] = value

    def load(self, filepath):
        pass

    def save(self, filepath):
        pass


class Alarm:
    def __init__(self):
        self.alarm_dict = {}

    def add(self, hour: int, minute: int, is_snooze=False):
        if is_snooze:
            key = "snooze"
        else:
            key = f"{hour:02d}{minute:02d}"
        self.alarm_dict[key] = {"hour": hour, "minute": minute, "is_set": True, "is_beeping": False}

    def delete(self, hour: int, minute: int):
        key = f"{hour:02d}{minute:02d}"
        if key in self.alarm_dict.keys():
            self.alarm_dict.pop(key)

    def update_beeping(self, now):
        for key, alarm in self.alarm_dict.items():
            if (now.hour == alarm["hour"]
                    and now.minute == alarm["minute"]
                    and int(now.second) == 0
                    and not alarm["is_beeping"]):
                alarm["is_beeping"] = True
                print("Activated alarm")

    def stop_beeping(self):
        for key, alarm in self.alarm_dict.items():
            alarm["is_beeping"] = False
            print("event_beep_off")

    def stop_snoozing(self):
        if "snooze" in self.alarm_dict.keys():
            self.alarm_dict.pop("snooze")

    def is_beeping(self):
        _is_beeping = False
        for key, alarm in self.alarm_dict.items():
            if alarm["is_beeping"]:
                _is_beeping = True
        return _is_beeping

    def is_snoozing(self):
        return "snooze" in self.alarm_dict.keys()


class PiClock:
    STEP_CLOCK = 0
    STEP_SET_ALARM = 1

    def __init__(self, screen_resolution=None):
        # os.environ["SDL_FBDEV"] = "/dev/fb1"
        # os.environ["SDL_VIDEODRIVER"] = "fbcon"
        pygame.init()
        if screen_resolution is None:
            self.screen_resolution = np.array([pygame.display.Info().current_w, pygame.display.Info().current_h])
        else:
            self.screen_resolution = np.array(screen_resolution)
        self.surface = pygame.display.set_mode(self.screen_resolution)
        pygame.display.set_caption("My Clock")
        pygame.mouse.set_visible(False)
        pygame.font.init()
        self.clock = pygame.time.Clock()
        # self.scale = 0.5*np.min(np.array(self.screen_resolution)) * np.ones(2)
        # self.offset = 0.5 * np.abs(self.screen_resolution - np.min(self.screen_resolution))
        self.offset = 0.5 * self.screen_resolution
        self.scale = np.min(self.offset) * np.ones(2)
        self.angles = [0, 0, 0]
        self.theme_day = Theme(Theme.WHITE, Theme.DARK_GRAY, Theme.BLACK, Theme.BLACK, Theme.ORANGE, Theme.BLACK,
                               Theme.LIGHT_GRAY, Theme.BLACK)
        self.theme_night = Theme(Theme.BLACK, Theme.DARK_GRAY, Theme.NIGHT_RED, Theme.NIGHT_RED, Theme.NIGHT_RED2,
                                 Theme.BLACK, Theme.DARK_GRAY, Theme.BLACK)
        self.theme = self.theme_day
        self.now = datetime.datetime.now()
        self.alarm = Alarm()
        self.alarm.add(17, 10)
        self.is_running = False
        print(f"Info:")
        print(pygame.display.Info())
        print("PiClock === Copyright 2020 Gilbert Francois Duivesteijn")

    @staticmethod
    def cleanup():
        pygame.font.quit()
        pygame.display.quit()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.update()
            self.draw()
        self.cleanup()

    def update(self):
        self.update_theme()
        self.update_time()
        self.alarm.update_beeping(self.now)
        self.mouse = pygame.mouse.get_pos()

    def draw(self):
        self.mouse = pygame.mouse.get_pos()
        self.draw_clock_bg()
        self.draw_logo()
        self.draw_date()
        self.draw_alarm_beeping()
        self.draw_ticks()
        self.draw_hands()
        self.draw_pivot()
        self.on_event()
        self.clock.tick(30)
        # self.draw_button(None)
        pygame.display.update()

    def update_theme(self):
        if 8 <= self.now.hour < 22:
            self.theme = self.theme_day
        else:
            self.theme = self.theme_night

    def update_time(self):
        self.now = datetime.datetime.now()
        self.angles[0] = self.now.hour / 12 * 2 * np.pi - 0.5 * np.pi + self.now.minute / 60 / 12 * 2 * np.pi
        self.angles[1] = self.now.minute / 60 * 2 * np.pi - 0.5 * np.pi
        self.angles[2] = self.now.second / 60 * 2 * np.pi - 0.5 * np.pi

    def event_beep_off(self):
        self.alarm.stop_beeping()

    def draw_alarm_beeping(self):
        if self.alarm.is_beeping():
            c = self.to_pixels(np.array([0.0, 0.0]))
            r = self.to_pixels(0.5)
            color = (0, 200, 100)
            pygame.gfxdraw.aacircle(self.surface, c[0], c[1], r, color)

    def on_event(self):
        for event in pygame.event.get():
            # if event.type is pygame.QUIT:
            # self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.is_running = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_a:
                    self.event_beep_off()
                    self.event_stop_snoozing()
                if event.key == pygame.K_s:
                    self.event_beep_off()
                    self.event_start_snoozing()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("click detected")
                params = {}
                params["rect"] = np.array([0.8, 0.8, 0.95, 0.95])
                _rect = self.to_pygrect(params["rect"])
                if _rect[0] < self.mouse[0] < _rect[0] + _rect[2] and _rect[1] < self.mouse[1] < _rect[1] + _rect[3]:
                    print("click inside button detected")

    def event_start_snoozing(self):
        self.alarm.add(self.now.hour, self.now.minute + 1, is_snooze=True)
        self.event_beep_off()
        print("event_snooze_on")
        print(self.alarm.alarm_dict)

    def event_stop_snoozing(self):
        self.alarm.stop_snoozing()
        print("event_snooze_off")

    def draw_ticks(self):
        for hour in range(12):
            angle = hour / 12 * 2 * np.pi
            self.draw_polar_line(angle, self.theme.get("ticks"))

    def draw_hands(self):
        self.draw_polar_line(self.angles[0], self.theme.get("hours"))
        self.draw_polar_line(self.angles[1], self.theme.get("minutes"))
        self.draw_polar_line(self.angles[2], self.theme.get("seconds"))

    def draw_pivot(self):
        params = self.theme.get("pivot")
        color = params["color"]
        c = self.to_pixels(params["center"])
        r1 = self.to_pixels(params["radius1"])
        pygame.gfxdraw.aacircle(self.surface, c[0], c[1], r1, color)
        pygame.gfxdraw.filled_circle(self.surface, c[0], c[1], r1, color)

    def draw_polar_line(self, angle, params):
        c = params["center"]
        r1 = params["radius1"]
        r2 = params["radius2"]
        w = params["width"]
        color = params["color"]
        t = np.array([np.cos(angle), np.sin(angle)])
        x0 = c + t * r1
        x1 = c + t * r2
        a = x0 + 0.5 * w * np.array([np.sin(angle), -np.cos(angle)])
        b = x1 + 0.5 * w * np.array([np.sin(angle), -np.cos(angle)])
        c = x1 + 0.5 * w * np.array([-np.sin(angle), np.cos(angle)])
        d = x0 + 0.5 * w * np.array([-np.sin(angle), np.cos(angle)])
        a = self.to_pixels(a)
        b = self.to_pixels(b)
        c = self.to_pixels(c)
        d = self.to_pixels(d)
        pygame.gfxdraw.aapolygon(self.surface, [a, b, c, d], color)
        pygame.gfxdraw.filled_polygon(self.surface, [a, b, c, d], color)

    # def draw_button(self, params):
    #     params = {}
    #     params["rect"] = np.array([0.8, 0.8, 0.95, 0.95])
    #     r = params["rect"]
    #     _rect = self.to_pygrect(params["rect"])
    #     pygame.draw.rect(self.surface, (220, 220, 220), _rect)
    #     font_size = self.to_pixels(24 / 240)
    #     font_big = pygame.font.Font(None, font_size)
    #     text_surface = font_big.render("test", True, (0, 0, 0))
    #     center = self.to_pixels(r[:2] + 0.5 * (r[2:] - r[:2]))
    #     rect = text_surface.get_rect(center=center)
    #     self.surface.blit(text_surface, rect)

    def draw_logo(self):
        params = self.theme.get("logo")
        self.draw_label(params)

    def draw_date(self):
        params = self.theme.get("date")
        params["label"] = f"{self.now.day}"
        # Add margin to the date label border.
        rect = self.draw_label(params)
        rect = self.to_posrect(rect)
        rect = rect + params["border_margin"] * np.array([1, -1, 1, -1])
        rect = self.to_pygrect(rect)
        # rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        rect = pygame.Rect(*rect)
        pygame.gfxdraw.rectangle(self.surface, rect, params.get("color"))

    def draw_label(self, params):
        font = pygame.font.Font(None, self.to_pixels(params["font_size"]))
        text_surface = font.render(params["label"], True, params["color"])
        rect = text_surface.get_rect(center=self.to_pixels(params["center"]))
        self.surface.blit(text_surface, rect)
        return rect

    def to_pixels(self, v):
        if isinstance(v, np.ndarray):
            return np.round(v * self.scale + self.offset).astype(np.int).tolist()
        else:
            return int(np.round(v * self.scale[0]))

    def to_pos(self, v):
        if isinstance(v, list):
            v = np.array(v)
        if isinstance(v, np.ndarray):
            return (v - self.offset) / self.scale * np.array([1, -1])
        else:
            return v / self.scale

    def to_pygrect(self, rect):
        x0 = self.to_pixels(rect[:2])
        x1 = self.to_pixels(rect[2:])
        return [x0[0], x0[1], x1[0] - x0[0], x1[1] - x0[1]]

    def to_posrect(self, rect):
        rect = np.array(rect)
        x0 = rect[:2]
        x1 = rect[:2] + rect[2:]
        x0 = self.to_pos(x0)
        x1 = self.to_pos(x1)
        return np.array([x0[0], x0[1], x1[0], x1[1]])

    def draw_clock_bg(self):
        params = self.theme.get("background")
        color1 = params.get("color1")
        color2 = params.get("color2")
        c = self.to_pixels(params.get("center"))
        r1 = self.to_pixels(params.get("radius1"))
        self.surface.fill(color1)
        if r1 > 0:
            pygame.gfxdraw.aacircle(self.surface, c[0], c[1], r1, color2)
            pygame.gfxdraw.filled_circle(self.surface, c[0], c[1], r1, color2)
        else:
            self.surface.fill(color2)


if __name__ == "__main__":
    clock = PiClock((640, 480))
    clock.run()
