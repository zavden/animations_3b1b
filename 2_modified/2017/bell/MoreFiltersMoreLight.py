# ==============================================================================
# Scene:      MoreFiltersMoreLight
# Source:     videos/_2017/bell.py (lines 227-337)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/waves.py
#
# Run from this folder:
#     manimgl MoreFiltersMoreLight.py MoreFiltersMoreLight -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cairo post-processed camera frames (camera.get_image / get_frame) to map filter-overlap colours to grey levels; skipped in GL, the translucent coloured filters are shown instead.
#
# Notes:
#   Cairo remapped each filter-overlap colour to a grey light level by post-processing camera frames (camera.get_image / get_frame); not possible per frame in GL, so the translucent coloured filters are shown instead.
# ==============================================================================

from manim_imports_ext import *
import warnings
from functools import reduce


# ----- From _2017/waves.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class PolarizingFilter(Circle):
    CONFIG = {
        "stroke_color" : GREY_D,
        "fill_color" : GREY_B,
        "fill_opacity" : 0.5,
        "label_tex" : None,
        "filter_angle" : 0,
        "include_arrow_label" : True,
        "arrow_length" : 0.7,
    }
    def __init__(self, **kwargs):
        Circle.__init__(self, **kwargs)

        if self.label_tex:
            self.label = OldTex(self.label_tex)
            self.label.next_to(self.get_top(), DOWN, MED_SMALL_BUFF)
            self.add(self.label)

        arrow = Arrow(
            ORIGIN, self.arrow_length*UP, 
            color = WHITE,
            buff = 0,
        )
        arrow.shift(self.get_top())
        arrow.rotate(-self.filter_angle)
        self.add(arrow)
        self.arrow = arrow
        shade_in_3d(self)

        if self.include_arrow_label:
            arrow_label = OldTex(
                "%.1f^\\circ"%(self.filter_angle*180/np.pi)
            )
            arrow_label.add_background_rectangle()
            arrow_label.next_to(arrow.get_tip(), UP)
            self.add(arrow_label)
            self.arrow_label = arrow_label


class FilterScene(ThreeDScene):
    CONFIG = {
        "filter_x_coordinates" : [0],
        "pol_filter_configs" : [{}],
        "EMWave_config" : {
            "start_point" : FRAME_X_RADIUS*LEFT + DOWN+OUT
        },
        "axes_config" : {},
        "start_phi" : 0.8*np.pi/2,
        "start_theta" : -0.6*np.pi,
        "ambient_rotation_rate" : 0.01,
    }
    def setup(self):
        self.axes = ThreeDAxes(**self.axes_config)
        self.add(self.axes)
        for x in range(len(self.filter_x_coordinates) - len(self.pol_filter_configs)):
            self.pol_filter_configs.append({})
        self.pol_filters = VGroup(*[
            PolarizingFilter(**config)
            for config in self.pol_filter_configs
        ])
        self.pol_filters.rotate(np.pi/2, RIGHT)
        self.pol_filters.rotate(-np.pi/2, OUT)
        pol_filter_shift = np.array(self.EMWave_config["start_point"])
        pol_filter_shift[0] = 0
        self.pol_filters.shift(pol_filter_shift)
        for x, pf in zip(self.filter_x_coordinates, self.pol_filters):
            pf.shift(x*RIGHT)
        self.add(self.pol_filters)
        self.pol_filter = self.pol_filters[0]

        self.set_camera_orientation(self.start_phi, self.start_theta)
        if self.ambient_rotation_rate > 0:
            self.begin_ambient_camera_rotation(self.ambient_rotation_rate)

    def get_filter_absorption_animation(self, pol_filter, photon):
        x = pol_filter.get_center()[0]
        alpha = (x + FRAME_X_RADIUS) / (FRAME_WIDTH)
        return ApplyMethod(
            pol_filter.set_fill, RED,
            run_time = photon.run_time,
            rate_func = squish_rate_func(there_and_back, alpha - 0.1, alpha + 0.1)
        )



# ----- From _2017/bell.py -----

class MoreFiltersMoreLight(FilterScene):
    CONFIG = {
        "filter_x_coordinates" : list(range(-2, 3)),
        "pol_filter_configs" : [
            {
                "include_arrow_label" : False,
                "filter_angle" : angle
            }
            for angle in np.linspace(0, np.pi/2, 5)
        ],
        "ambient_rotation_rate" : 0,
        "arrow_rgb" : (0, 0, 0),
        "background_rgb" : (245, 245, 245), 
    }
    def construct(self):
        self.remove(self.axes)
        pfs = VGroup(*reversed(self.pol_filters))
        self.color_filters(pfs)
        self.remove(pfs)
        self.build_color_map(pfs)
        self.add(pfs[0], pfs[2], pfs[4])
        pfs.center().scale(1.5)

        self.move_camera(
            phi = 0.9*np.pi/2,
            theta = -0.95*np.pi,
        )
        self.play(
            Animation(pfs[0]),
            pfs[2].shift, 3*OUT,
            Animation(pfs[4]),
        )
        self.wait()
        self.play(
            Animation(pfs[0]),
            pfs[2].shift, 3*IN,
            Animation(pfs[4]),
        )

        pfs[1].shift(8*OUT)
        self.play(
            Animation(pfs[0]),
            pfs[1].shift, 8*IN,
            Animation(VGroup(pfs[2], pfs[4])),
            run_time = 2
        )
        self.wait()

        pfs[3].shift(8*OUT)
        self.play(
            Animation(VGroup(*pfs[:3])),
            pfs[3].shift, 8*IN,
            Animation(VGroup(*pfs[4:])),
            run_time = 2
        )
        self.wait()

    def color_filters(self, pfs):
        colors = [RED, GREEN, BLUE, MAROON_B, PURPLE_C]
        for pf, color in zip(pfs, colors):
            pf.set_fill(color, 0.5)
            pf.arrow.set_fill(WHITE, 1)
        turn_off_3d_shading(pfs)

    # CHANGE: Cairo post-processed camera frames (camera.get_image / get_frame) to map filter-overlap colours to grey levels; skipped in GL, the translucent coloured filters are shown instead.
    def build_color_map(self, pfs):
        # (Cairo captured the camera image to remap every overlap colour to a grey light level; not possible per frame in GL,
        # so the coloured translucent filters are shown as they are.)
        pass

    def update_frame(self, mobjects = None, image = None):
        FilterScene.update_frame(self, mobjects)

    def get_frame(self):
        frame = FilterScene.get_frame(self)
        bool_arrays = [
            (frame[:,:,0] == r) & (frame[:,:,1] == g) & (frame[:,:,2] == b)
            for (r, g, b) in self.original_rgbas
        ]
        for ba, new_rgb in zip(bool_arrays, self.new_rgbas):
            frame[ba] = new_rgb
        covered = reduce(
            lambda b1, b2 : b1 | b2,
            bool_arrays
        )
        frame[~covered] = [65, 65, 65]
        return frame
