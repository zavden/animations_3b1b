from __future__ import annotations 

import numpy as np
import itertools as it
import random

from manimlib.constants import *
from manimlib.scene.scene import Scene
from manimlib.mobject.geometry import AnnularSector
from manimlib.mobject.geometry import Circle
from manimlib.mobject.geometry import Polygon
from manimlib.mobject.svg.text_mobject import Text
from manimlib.mobject.svg.tex_mobject import TexText
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.utils.bezier import interpolate
from manimlib.utils.space_ops import angle_of_vector
from manimlib.utils.rate_functions import squish_rate_func
from manimlib.utils.rate_functions import smooth
from manimlib.animation.animation import Animation
from manimlib.animation.transform import Restore
from manimlib.animation.transform import Transform
from manimlib.animation.composition import AnimationGroup
from manimlib.animation.composition import LaggedStartMap
from manimlib.animation.creation import Write


# CHANGE (converted/_lib): the 3Blue1Brown logo is a trademark, so it is not redistributed. Instead, a
# "TB" emblem (white letters on a black disk) with the same interface the scenes used: iris_background,
# spike_layers and pupil, and the methods add_iris_back, add_spikes and add_pupil, which some scenes
# redefine. The letters go in spike_layers and always stay on top.
class Logo(VMobject):
    pupil_radius: float = 1.0
    outer_radius: float = 2.0
    background_color: ManimColor = BLACK
    letters_color: ManimColor = WHITE
    rim_color: ManimColor = GREY_B
    rim_width: float = 3.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_iris_back()
        self.add_spikes()
        self.add_pupil()
        # A scene that redefines add_pupil may cover the center: the letters go back on top
        self.remove(self.spike_layers)
        self.add(self.spike_layers)

    def add_iris_back(self):
        disk = Circle(radius=self.outer_radius)
        disk.set_fill(self.background_color, 1)
        disk.set_stroke(self.rim_color, self.rim_width)
        self.iris_background = VGroup(disk)
        self.add(self.iris_background)

    def add_spikes(self):
        letters = Text("TB", font="Nunito", weight="BOLD")
        letters.set_fill(self.letters_color, 1)
        letters.set_stroke(width=0)
        letters.set_width(1.15 * self.outer_radius)
        self.spike_layers = VGroup(*letters)
        self.add(self.spike_layers)

    def add_pupil(self):
        # Same color as the disk: it is not visible, but it exists for the scenes that animate it
        self.pupil = Circle(radius=self.pupil_radius)
        self.pupil.set_fill(self.background_color, 1)
        self.pupil.set_stroke(width=0)
        self.add(self.pupil)

    def cut_pupil(self):
        return self

    def get_blue_part_and_brown_part(self):
        # The two halves of the emblem, for the scenes that animated the two parts of the eye
        return VGroup(self.iris_background, self.spike_layers[:1]), VGroup(self.pupil, self.spike_layers[1:])


# CHANGE (converted/_lib): the scenes that animated the construction of the 3Blue1Brown logo
# (LogoGeneration*, LogoTest, WrittenLogo, Vertical3B1B) were removed: they reproduced the trademark and
# no scene uses them.
