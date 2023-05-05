import random
import sys
from dataclasses import dataclass

import keyboard
import pyperclip


def r_int(mn: int, mx: int):
    return random.randrange(mn, mx + 1)


def r_float(mn: int, mx: int, fdiv: int = 100):
    return r_int(int(mn * fdiv), int(mx * fdiv)) / fdiv


def r_bool():
    return (r_int(0, 100) % 2) == 0


def r_byte():
    return hex(r_int(0, 256))[2:].zfill(2)


def r_color():
    return (r_byte() + r_byte() + r_byte() + "ff").upper()  # RGBA


@dataclass
class GENERAL_CROSSHAIR:
    advanced_options: bool = True

    def __str__(self):
        s = int(self.advanced_options)
        return f"s;{s};"


@dataclass
class GENERAL_OTHER:
    show_spectated_players_crosshair: bool = True
    fade_crosshair_with_firing_error: bool = True
    # disable_crosshair: bool = False (Doesn't matter)

    def __post_init__(self):
        self.show_spectated_players_crosshair = r_bool()
        self.fade_crosshair_with_firing_error = r_bool()

    def __str__(self):
        s = int(self.show_spectated_players_crosshair)
        f = int(self.fade_crosshair_with_firing_error)
        return f"P;f;{f};s;{s};"


@dataclass
class PRIMARY_CROSSHAIR:
    # crosshair_color: str = ""
    # always use custom crosshair color
    use_custom_color: bool = False
    custom_color: str = ""
    outlines: bool = False
    outline_color: str = ""
    outline_opacity: float = 0.0
    outline_thickness: int = 0
    center_dot: bool = False
    center_dot_opacity: float = 0.0
    center_dot_thickness: int = 0
    override_firing_error: bool = False
    overide_all_primary: bool = False

    def __post_init__(self):
        self.use_custom_color = r_bool()
        self.custom_color = r_color()
        self.outlines = r_bool()
        self.outline_color = r_color()
        self.outline_opacity = r_float(0.0, 1.0)
        self.outline_thickness = r_int(1, 6)
        self.center_dot = r_bool()
        self.center_dot_opacity = r_float(0.0, 1.0)
        self.center_dot_thickness = r_int(1, 6)
        self.override_firing_error = r_bool()
        self.overide_all_primary = r_bool()

    def __str__(self):
        ret_str = ""
        if not self.use_custom_color:
            ret_str += f"c;{random.randrange(8)};"
        else:
            ret_str += f"c;8;u;{self.custom_color};b;1;"

        # if self.use_custom_color:
        #     ret_str += ""

        h = int(self.outlines)
        ret_str += f"h;{h};"

        t = self.outline_thickness
        o = self.outline_opacity
        ret_str += f"t;{t};o;{o};"

        d = int(self.center_dot)
        z = self.center_dot_thickness
        a = self.center_dot_opacity
        ret_str += f"d;{d};z;{z};a;{a};"

        m = int(self.override_firing_error)
        ret_str += f"m;{m};"

        return ret_str


@dataclass
class PRIMARY_INNER_LINES:
    meta: int = 0
    show_lines: bool = True
    opacity: float = 0.8
    line_thickness: int = 2
    line_offset: int = 3
    line_length: int = 6
    allow_vert_scaling: bool = False
    line_length_vertical: int = 6
    show_movement_error: bool = False
    movement_error_scale: float = 1.0
    show_shooting_error: bool = False
    firing_error_scale: float = 1.0

    def __post_init__(self):
        # self.show_lines = r_bool() # Always show inner lines
        self.opacity = r_float(0.0, 1.0)
        self.line_thickness = r_int(1, 10)
        self.line_offset = r_int(1, 20)
        self.line_length = r_int(1, 20)
        self.allow_vert_scaling = r_bool()
        self.line_length_vertical = r_int(1, 20)
        self.show_movement_error = r_bool()
        self.movement_error_scale = r_float(0.0, 3.0)
        self.show_shooting_error = r_bool()
        self.firing_error_scale = r_float(0.0, 3.0)

    def __str__(self):
        ret_str = ""
        if not self.show_lines:
            return f"{int(self.meta)}b;0;"

        t = self.line_thickness
        ret_str += f"{int(self.meta)}t;{t};"

        a = self.opacity
        ret_str += f"{int(self.meta)}a;{a};"

        o = self.line_offset
        ret_str += f"{int(self.meta)}o;{o};"

        l = self.line_length
        ret_str += f"{int(self.meta)}l;{l};"

        if self.allow_vert_scaling:
            v = self.line_length_vertical
            ret_str += f"{int(self.meta)}v;{v};"
            ret_str += f"{int(self.meta)}g;1;"  # allow_vert_scaling

        if self.show_movement_error:
            ret_str += f"{int(self.meta)}m;1;"
            s = self.movement_error_scale
            ret_str += f"{int(self.meta)}s;{s};"

        if self.show_shooting_error:
            e = self.firing_error_scale
            ret_str += f"{int(self.meta)}e;{e};"
        else:
            ret_str += f"{int(self.meta)}f;0;"

        return ret_str


@dataclass
class PRIMARY_OUTER_LINES(PRIMARY_INNER_LINES):
    meta: int = 1
    ...


@dataclass
class AIMDOWNSIGHTS_COPY_PRIMARY_CROSSHAIR:
    copy_primary_crosshair: bool = True


@dataclass
class AIMDOWNSIGHTS_CROSSHAIR(PRIMARY_CROSSHAIR):
    ...


@dataclass
class AIMDOWNSIGHTS_INNER_LINES(PRIMARY_INNER_LINES):
    ...


@dataclass
class AIMDOWNSIGHTS_OUTER_LINES(PRIMARY_OUTER_LINES):
    ...


@dataclass
class SNIPERSCOPE_GENERAL:
    display_center_dot: bool = False
    use_custom_center_dot_color: bool = False
    center_dot_color_custom: str = ""
    center_dot_thickness: int = 1
    center_dot_opacity: float = 0.75

    def __post_init__(self):
        self.display_center_dot = r_bool()
        self.use_custom_center_dot_color = r_bool()
        self.center_dot_color_custom = r_color()
        self.center_dot_thickness = r_int(1, 6)
        self.center_dot_opacity = r_float(0.0, 1.0)

    def __str__(self):
        ret_str = ""
        if not self.display_center_dot:
            ret_str += "d;0;"
            return ret_str

        if not self.use_custom_center_dot_color:
            ret_str += f"c;{random.randrange(8)};"
        else:
            ret_str += f"c;8;t;{self.center_dot_color_custom};"

        if self.use_custom_center_dot_color:
            ret_str += "b;1;"

        s = self.center_dot_thickness
        ret_str += f"s;{s};"

        o = self.center_dot_opacity
        ret_str += f"o;{o};"

        return ret_str


@dataclass
class GENERAL:
    crosshair: GENERAL_CROSSHAIR
    other: GENERAL_OTHER

    def __str__(self):
        return str(self.crosshair) + str(self.other)


@dataclass
class PRIMARY:
    crosshair: PRIMARY_CROSSHAIR
    inner_lines: PRIMARY_INNER_LINES
    outer_lines: PRIMARY_OUTER_LINES

    def __str__(self):
        ret_str = ""
        # if self.crosshair.overide_all_primary:
        #     ret_str += "c;1;"

        # ret_str += "P;"
        ret_str += str(self.crosshair) + str(self.inner_lines) + str(self.outer_lines)
        return ret_str


@dataclass
class AIMDOWNSIGHTS:
    # copy_primary_crosshair: AIMDOWNSIGHTS_COPY_PRIMARY_CROSSHAIR
    crosshair: AIMDOWNSIGHTS_CROSSHAIR
    inner_lines: AIMDOWNSIGHTS_INNER_LINES
    outer_lines: AIMDOWNSIGHTS_OUTER_LINES

    def __str__(self):
        ret_str = "A;"
        ret_str += str(self.crosshair) + str(self.inner_lines) + str(self.outer_lines)
        return ret_str


@dataclass
class SNIPERSCOPE:
    general: SNIPERSCOPE_GENERAL

    def __str__(self):
        ret_str = "S;"
        ret_str += str(self.general)
        return ret_str


def randomize():
    g = GENERAL(GENERAL_CROSSHAIR(), GENERAL_OTHER())
    p = PRIMARY(PRIMARY_CROSSHAIR(), PRIMARY_INNER_LINES(), PRIMARY_OUTER_LINES())
    a = AIMDOWNSIGHTS(
        AIMDOWNSIGHTS_CROSSHAIR(),
        AIMDOWNSIGHTS_INNER_LINES(),
        AIMDOWNSIGHTS_OUTER_LINES(),
    )
    s = SNIPERSCOPE(SNIPERSCOPE_GENERAL())

    return "0;" + str(g) + str(p) + str(a) + str(s)[:-1]


if len(sys.argv) < 2:

    def helper_randomize():
        r = randomize()
        pyperclip.copy(r)
        keyboard.send("ctrl + v")
        print(f"Hotkey: Generating new crosshair! <{r}>")

    keyboard.register_hotkey("f12", helper_randomize)
    input()

else:
    while True:
        x = input(">>> ")

        if not x:
            r = randomize()
            print(r)
            pyperclip.copy(r)
            continue

        if x.lower() in ["q", "exit", "quit"]:
            print("Cya!")
            break

        try:
            n = int(x)
        except ValueError:
            print("Enter a valid number!")
            continue

        for _ in range(n):
            print(randomize())
