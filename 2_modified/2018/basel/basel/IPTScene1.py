# ==============================================================================
# Scene:      IPTScene1
# Source:     videos/_2018/basel/basel.py (lines 2056-2244)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IPTScene1.py IPTScene1 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cairo camera.frame_shape/frame_center setters: zoom the GL camera frame onto C instead
# ==============================================================================

from manim_imports_ext import *
from once_useful_constructs.light import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


A = np.array([5.,-3.,0.])


B = np.array([-5.,3.,0.])


C = np.array([-5.,-3.,0.])


xA = A[0]


yA = A[1]


xB = B[0]


yB = B[1]


xC = C[0]


yC = C[1]


# find the coords of the altitude point H
# as the solution of a certain LSE
prelim_matrix = np.array([[yA - yB, xB - xA], [xA - xB, yA - yB]]) # sic


prelim_vector = np.array([xB * yA - xA * yB, xC * (xA - xB) + yC * (yA - yB)])


H2 = np.linalg.solve(prelim_matrix,prelim_vector)


H = np.append(H2, 0.)


class IPTScene1(PiCreatureScene):

    def construct(self):

        show_detail = True

        SCREEN_SCALE = 0.1
        SCREEN_THICKNESS = 0.2


        # use the following for the zoomed inset
        if show_detail:
            # CHANGE: Cairo camera.frame_shape/frame_center setters: zoom the GL camera frame onto C instead
            self.frame.set_height(0.02 * FRAME_HEIGHT)
            self.frame.move_to(C)
            SCREEN_SCALE = 0.01
            SCREEN_THICKNESS = 0.02





        morty = self.get_primary_pi_creature()
        self.remove(morty)
        morty.scale(0.3).flip()
        right_pupil = morty.pupils[1]
        morty.next_to(C, LEFT, buff = 0, submobject_to_align = right_pupil)
        
        if not show_detail:
            self.add_foreground_mobject(morty)

        stroke_width = 6
        line_a = Line(B,C,stroke_width = stroke_width)
        line_b = Line(A,C,stroke_width = stroke_width)
        line_c = Line(A,B,stroke_width = stroke_width)
        line_h = Line(C,H,stroke_width = stroke_width)

        length_a = line_a.get_length()
        length_b = line_b.get_length()
        length_c = line_c.get_length()
        length_h = line_h.get_length()

        label_a = OldTex("a")
        label_a.next_to(line_a, LEFT, buff = 0.5)
        label_b = OldTex("b")
        label_b.next_to(line_b, DOWN, buff = 0.5)
        label_h = OldTex("h")
        label_h.next_to(line_h.get_center(), RIGHT, buff = 0.5)

        self.add_foreground_mobject(line_a)
        self.add_foreground_mobject(line_b)
        self.add_foreground_mobject(line_c)
        self.add_foreground_mobject(line_h)
        self.add_foreground_mobject(label_a)
        self.add_foreground_mobject(label_b)
        self.add_foreground_mobject(label_h)
        
        if not show_detail:
            self.add_foreground_mobject(morty)

        ls1 = LightSource(radius = 10)
        ls1.move_source_to(B)

        self.add(ls1.lighthouse)

        if not show_detail:
            self.play(
                SwitchOn(ls1.ambient_light)
            )

        self.wait()

        # adding the first screen

        screen_width_a = SCREEN_SCALE * length_a
        screen_width_b = SCREEN_SCALE * length_b
        screen_width_ap = screen_width_a * length_a / length_c
        screen_width_bp = screen_width_b * length_b / length_c
        screen_width_c = SCREEN_SCALE * length_c

        screen_thickness_a = SCREEN_THICKNESS
        screen_thickness_b = SCREEN_THICKNESS

        screen1 = Rectangle(width = screen_width_b,
            height = screen_thickness_b, 
            stroke_width = 0, 
            fill_opacity = 1.0)
        screen1.move_to(C + screen_width_b/2 * RIGHT + screen_thickness_b/2 * DOWN)
        
        if not show_detail:
            self.add_foreground_mobject(morty)

        self.play(
            FadeIn(screen1)
        )
        self.add_foreground_mobject(screen1)

        ls1.set_screen(screen1)
        screen_tracker = ScreenTracker(ls1)
        self.add(screen_tracker)
        #self.add(ls1.shadow)

        if not show_detail:
            self.play(
                SwitchOn(ls1.ambient_light)
            )

        self.play(
            SwitchOn(ls1.spotlight),
            SwitchOff(ls1.ambient_light)
        )



        # now move the light source to the height point
        # while shifting scaling the screen
        screen1p = screen1.deepcopy()
        screen1pp = screen1.deepcopy()
        #self.add(screen1p)
        angle = np.arccos(length_b / length_c)
        
        screen1p.stretch_to_fit_width(screen_width_bp)
        screen1p.move_to(C + (screen_width_b - screen_width_bp/2) * RIGHT + SCREEN_THICKNESS/2 * DOWN)
        screen1p.rotate(-angle, about_point = C + screen_width_b * RIGHT)
        

        self.play(
            ls1.move_source_to,H,
            Transform(screen1,screen1p)
        )

        # add and move the second light source and screen
        ls2 = ls1.deepcopy()
        ls2.move_source_to(A)
        screen2 = Rectangle(width = screen_width_a,
            height = screen_thickness_a, 
            stroke_width = 0, 
            fill_opacity = 1.0)
        screen2.rotate(-TAU/4)
        screen2.move_to(C + screen_width_a/2 * UP + screen_thickness_a/2 * LEFT)

        self.play(
            FadeIn(screen2)
        )
        self.add_foreground_mobject(screen2)

        if not show_detail:
            self.add_foreground_mobject(morty)

        # the same scene adding sequence as before
        ls2.set_screen(screen2)
        screen_tracker2 = ScreenTracker(ls2)
        self.add(screen_tracker2)

        if not show_detail:
            self.play(
                SwitchOn(ls2.ambient_light)
            )

        self.wait()

        self.play(
            SwitchOn(ls2.spotlight),
            SwitchOff(ls2.ambient_light)
        )



        # now move the light source to the height point
        # while shifting scaling the screen
        screen2p = screen2.deepcopy()
        screen2pp = screen2.deepcopy()
        angle = np.arccos(length_a / length_c)
        screen2p.stretch_to_fit_height(screen_width_ap)
        screen2p.move_to(C + (screen_width_a - screen_width_ap/2) * UP + screen_thickness_a/2 * LEFT)
        screen2p.rotate(angle, about_point = C + screen_width_a * UP)
        # we can reuse the translation vector
        # screen2p.shift(vector)

        self.play(
            ls2.move_source_to,H,
            SwitchOff(ls1.ambient_light),
            Transform(screen2,screen2p)
        )

        # now transform both screens back
        self.play(
            Transform(screen1, screen1pp),
            Transform(screen2, screen2pp),
        )
