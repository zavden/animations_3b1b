# ==============================================================================
# Scene:      MentionGenerality
# Source:     videos/_2017/borsuk.py (lines 974-1009)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MentionGenerality.py MentionGenerality -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - undefined name m1 in the sort key (NameError once init_points runs); sort the faces by z
#   - painter order: draw the faces from back to front (smaller z first); the first fix had the sign reversed
# ==============================================================================

from manim_imports_ext import *

class Jewel(VMobject):
    CONFIG = {
        "color" : WHITE,
        "fill_opacity" : 0.75,
        "stroke_width" : 0,
        "height" : 0.5,
        "num_equator_points" : 5,
        "sun_vect" : OUT+LEFT+UP,
    }
    def init_points(self):
        for vect in OUT, IN:
            compass_vects = list(compass_directions(self.num_equator_points))
            if vect is IN:
                compass_vects.reverse()
            for vect_pair in adjacent_pairs(compass_vects):
                self.add(Polygon(vect, *vect_pair))
        self.set_height(self.height)
        self.rotate(-np.pi/2-np.pi/24, RIGHT)        
        self.rotate(-np.pi/12, UP)
        self.submobjects.sort(
            # CHANGE: undefined name m1 in the sort key (NameError once init_points runs); sort the faces by z
            # CHANGE: painter order: draw the faces from back to front (smaller z first); the first fix had the sign reversed
            key=lambda m: m.get_center()[2]
        )
        return self


class Necklace(VMobject):
    CONFIG = {
        "width" : FRAME_WIDTH - 1,
        "jewel_buff" : MED_SMALL_BUFF,
        "chain_color" : GREY,
        "default_colors" : [(4, BLUE), (6, WHITE), (4, GREEN)]
    }
    def __init__(self, *colors, **kwargs):
        digest_config(self, kwargs, locals())
        if len(colors) == 0:
            self.colors = self.get_default_colors()
        VMobject.__init__(self, **kwargs)

    def get_default_colors(self):
        result = list(it.chain(*[
            num*[color]
            for num, color in self.default_colors
        ]))
        random.shuffle(result)
        return result

    def init_points(self):
        jewels = VGroup(*[
            Jewel(color = color)
            for color in self.colors
        ])
        jewels.arrange(buff = self.jewel_buff)
        jewels.set_width(self.width)
        jewels.center()
        j_to_j_dist = (jewels[1].get_center()-jewels[0].get_center())[0]

        chain = Line(
            jewels[0].get_center() + j_to_j_dist*LEFT/2, 
            jewels[-1].get_center() + j_to_j_dist*RIGHT/2, 
            color = self.chain_color,
        )
        self.add(chain, *jewels)
        self.chain = chain
        self.jewels = jewels


class MentionGenerality(TeacherStudentsScene, ThreeDScene):
    def construct(self):
        necklace = Necklace(width = FRAME_X_RADIUS)
        necklace.shift(2*UP)
        necklace.to_edge(RIGHT)
        arrow = OldTex("\\Leftrightarrow")
        arrow.scale(2)
        arrow.next_to(necklace, LEFT)
        q_marks = OldTex("???")
        q_marks.next_to(arrow, UP)
        arrow.add(q_marks)

        formula = OldTex("f(\\textbf{x}) = f(-\\textbf{x})")
        formula.next_to(self.get_students(), UP, buff = LARGE_BUFF)
        formula.to_edge(LEFT, buff = LARGE_BUFF)

        self.play(
            self.teacher.change_mode, "raise_right_hand",
            self.teacher.look_at, arrow
        )
        self.play(
            FadeIn(necklace, run_time = 2, lag_ratio = 0.5),
            Write(arrow),
            *[
                ApplyMethod(pi.look_at, arrow)
                for pi in self.get_pi_creatures()
            ]
        )
        self.play_student_changes("pondering", "erm", "confused")
        self.wait()
        self.play(*[
            ApplyMethod(pi.look_at, arrow)
            for pi in self.get_pi_creatures()
        ])
        self.play(Write(formula))
        self.wait(3)
