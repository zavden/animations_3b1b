# ==============================================================================
# Scene:      RightAnglesOverlay
# Source:     videos/_2018/basel/basel.py (lines 4462-4524)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RightAnglesOverlay.py RightAnglesOverlay -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - flash_arcs is a local function of another scene in the original (NameError also in Cairo); the call is dropped
# ==============================================================================

from manim_imports_ext import *
from once_useful_constructs.light import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class RightAnglesOverlay(Scene):

    def construct(self):

        BASELINE_YPOS = -2.5
        OBSERVER_POINT = [0,BASELINE_YPOS,0]
        LAKE0_RADIUS = 1.5 * 2
        INDICATOR_RADIUS = 0.6
        TICK_SIZE = 0.5
        LIGHTHOUSE_HEIGHT = 0.2
        LAKE_COLOR = BLUE
        LAKE_OPACITY = 0.15
        LAKE_STROKE_WIDTH = 5.0
        LAKE_STROKE_COLOR = BLUE
        TEX_SCALE = 0.8
        DOT_COLOR = BLUE

        RIGHT_ANGLE_SIZE = 0.3


        def right_angle(pointA, pointB, pointC, size = 1):

            v1 = pointA - pointB
            v1 = size * v1/get_norm(v1)
            v2 = pointC - pointB
            v2 = size * v2/get_norm(v2)
            
            P = pointB
            Q = pointB + v1
            R = Q + v2
            S = R - v1
            angle_sign = VMobject()
            angle_sign.set_points_as_corners([P,Q,R,S,P])
            angle_sign.mark_paths_closed = True
            angle_sign.set_fill(color = WHITE, opacity = 1)
            angle_sign.set_stroke(width = 0)
            return angle_sign


        lake_center = OBSERVER_POINT + LAKE0_RADIUS * UP
        points = []
        lines = VGroup()
        for i in range(4):
            theta = -TAU/4 + (i+0.5)*TAU/4
            v = np.array([np.cos(theta), np.sin(theta), 0])
            P = lake_center + LAKE0_RADIUS * v
            points.append(P)
            lines.add(Line(lake_center, P, stroke_width = 8))

        self.play(FadeIn(lines))

        self.wait()

        for i in range(4):
            sign = right_angle(points[i-1], lake_center, points[i],RIGHT_ANGLE_SIZE)
            self.play(FadeIn(sign))
            self.play(FadeOut(sign))

        self.wait()

        self.play(FadeOut(lines))

        # CHANGE: flash_arcs is a local function of another scene in the original (NameError also in Cairo); the call is dropped
        pass
