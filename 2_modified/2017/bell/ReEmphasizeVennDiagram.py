# ==============================================================================
# Scene:      ReEmphasizeVennDiagram
# Source:     videos/_2017/bell.py (lines 2029-2377)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/waves.py
#
# Run from this folder:
#     manimgl ReEmphasizeVennDiagram.py ReEmphasizeVennDiagram -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cairo scale(factor, point) positional point -> about_point kwarg (GL's 2nd positional is min_scale_factor).
#   - Python 3: zip()/map()/filter() return iterators, wrap in list() before slicing.
# ==============================================================================

from manim_imports_ext import *
from tqdm import tqdm as ProgressDisplay
import warnings


# ----- From _2017/waves.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2017/bell.py -----

class VennDiagramProofByContradiction(Scene):
    CONFIG = {
        "circle_colors" : [RED, GREEN, BLUE]
    }
    def construct(self):
        self.setup_venn_diagram_sections()
        self.draw_venn_diagram()
        self.show_100_photons()
        self.show_one_photon_answering_questions()
        self.put_all_photons_in_A()
        self.separate_by_B()
        self.separate_by_C()
        self.show_two_relevant_subsets()

    def draw_venn_diagram(self, send_to_corner = True):
        A, B, C = venn_diagram = VGroup(*[
            Circle(
                radius = 3,
                stroke_width = 3,
                stroke_color = c,
                fill_opacity = 0.2,
                fill_color = c,
            ).shift(vect)
            for c, vect in zip(
                self.circle_colors,
                compass_directions(3, UP)
            )
        ])
        self.A_to_B_vect = B.get_center() - A.get_center()
        self.A_to_C_vect = C.get_center() - A.get_center()

        venn_diagram.center()
        labels = VGroup()
        alt_labels = VGroup()
        props = [1./12, 0.5, 0]
        angles = [0, np.pi/8, np.pi/4]
        for circle, char, prop, angle in zip(venn_diagram, "ABC", props, angles):
            label, alt_label = [
                OldTexText(
                    "%s \\\\"%start,
                    "through", char + "$\\! \\uparrow$"
                ).set_color_by_tex(char, circle.get_color())
                for start in ("Would pass", "Pass")
            ]
            for mob in label, alt_label:
                mob[-1][-1].rotate(-angle)
                mob[-1][-1].shift(0.5*SMALL_BUFF*UP)
            center = circle.get_center()
            label.move_to(center)
            label.generate_target()
            point = circle.point_from_proportion(prop)
            alt_label.scale(2)
            for mob in label.target, alt_label:
                mob.next_to(point, point-center, SMALL_BUFF)

            circle.label = label
            circle.alt_label = alt_label
            labels.add(label)
            alt_labels.add(alt_label)

        last_circle = None
        for circle in venn_diagram:
            added_anims = []
            if last_circle:
                added_anims.append(MoveToTarget(last_circle.label))
            self.play(
                DrawBorderThenFill(circle, run_time = 2),
                Write(circle.label, run_time = 2),
                *added_anims
            )
            last_circle = circle
        self.play(MoveToTarget(last_circle.label))
        self.wait()

        if hasattr(self, "A_segments"):
            A.add(self.A_segments)

        if send_to_corner:
            group = VGroup(venn_diagram, labels)
            target = VGroup(venn_diagram.copy(), alt_labels)
            target.scale(0.25)
            target.to_corner(UP+RIGHT)
            self.play(Transform(group, target))
            self.remove(group)
            for circle in venn_diagram:
                circle.label = circle.alt_label
                self.add(circle)
        for circle in venn_diagram:
            self.add(circle.label)

        self.venn_diagram = venn_diagram

    def show_100_photons(self):
        photon = FunctionGraph(
            lambda x : -np.cos(3*np.pi*x)*np.exp(-x*x),
            x_min = -2, 
            x_max = 2,
            color = YELLOW,
            stroke_width = 2,
        )
        photon.shift(LEFT + 2*UP)
        eyes = Eyes(photon)
        photon.eyes = eyes

        hundred, photon_word, s = words = OldTexText(
            "100 ", "Photon", "s",
            arg_separator = ""
        )
        words.next_to(eyes, UP)

        self.play(
            ShowCreation(photon),
            FadeIn(photon.eyes),
            Write(photon_word, run_time = 1.5)
        )
        photon.add(photon.eyes)

        #Split to hundred
        photons = VGroup(*[photon.deepcopy() for x in range(100)])
        self.arrange_photons_in_circle(photons)
        photons.set_height(6)
        photons.next_to(words, DOWN)
        photons.to_edge(LEFT)

        self.play(
            Write(hundred), Write(s),
            ReplacementTransform(
                VGroup(photon), photons,
                lag_ratio = 0.5
            )
        )

        self.photons = photons
        self.photon_words = words

    def show_one_photon_answering_questions(self):
        photon = self.photons[89]
        photon.save_state()
        photon.generate_target()

        answers = OldTexText(
            "Pass through A?", "Yes\\\\",
            "Pass through B?", "No\\\\",
            "Pass through C?", "No\\\\",
        )
        answers.set_color_by_tex_to_color_map({
            "Yes" : GREEN,
            "No" : RED,
        })
        bubble = ThoughtBubble()
        bubble.add_content(answers)
        bubble.resize_to_content() 
        answers.shift(SMALL_BUFF*(RIGHT+UP))
        bubble_group = VGroup(bubble, answers)
        bubble_group.scale(0.25)
        bubble_group.next_to(photon, UP+RIGHT, buff = 0)

        group = VGroup(photon, bubble_group)
        group.save_state()
        bubble_group.set_fill(opacity = 0)
        bubble_group.set_stroke(width = 0)

        self.play(
            group.restore,
            group.scale, 4,
            group.to_corner, DOWN + RIGHT,
        )
        self.play(photon.eyes.blink_anim())
        self.wait()
        self.play(
            FadeOut(bubble_group),
            photon.restore,
        )

    def put_all_photons_in_A(self):
        A, B, C = circles = self.venn_diagram[:3]
        A_group, B_group, C_group = [
            VGroup(circle, circle.label)
            for circle in circles
        ]
        B_group.save_state()
        C_group.save_state()

        A.generate_target()
        A.target.scale(4)
        A.target.shift(
            (FRAME_Y_RADIUS-MED_LARGE_BUFF)*UP - \
            A.target.get_top()
        )
        A.label.generate_target()
        A.label.target.scale(2)
        A.label.target.next_to(
            A.target.point_from_proportion(0.1),
            UP+RIGHT, SMALL_BUFF
        )

        self.play(
            B_group.fade, 1,
            C_group.fade, 1,
            MoveToTarget(A),
            MoveToTarget(A.label),
            FadeOut(self.photon_words),
            self.photons.set_height,
                0.85*A.target.get_height(),
            self.photons.space_out_submobjects, 0.8,
            self.photons.move_to, A.target,
        )
        self.wait()

        self.A_group = A_group
        self.B_group = B_group
        self.C_group = C_group

    def separate_by_B(self):
        A_group = self.A_group
        B_group = self.B_group
        photons = self.photons
        B = B_group[0]

        B.target, B.label.target = B_group.saved_state
        B.target.scale(4)
        B.target.move_to(A_group[0])
        B.target.shift(self.A_to_B_vect)
        B.label.target.scale(2)
        B.label.target.next_to(
            B.target.point_from_proportion(0.55),
            LEFT, SMALL_BUFF
        )

        B_center = B.target.get_center()
        photons.sort(
            lambda p : get_norm(p-B_center)
        )
        in_B = VGroup(*photons[:85])
        out_of_B = VGroup(*photons[85:])
        out_of_B.sort(lambda p : np.dot(p, 2*UP+LEFT))

        self.play(
            MoveToTarget(B),
            MoveToTarget(B.label),
            in_B.shift, 0.5*DOWN+0.2*LEFT,
            out_of_B.scale, 1./0.8,
            out_of_B.shift, 0.15*(UP+RIGHT),
        )

        words1 = OldTexText("85 also \\\\", "pass ", "B")
        words1.set_color_by_tex("B", GREEN)
        words1.scale(0.8)
        words1.next_to(A_group, LEFT, LARGE_BUFF).shift(UP)
        arrow1 = Arrow(
            words1.get_right(), 
            in_B.get_corner(UP+LEFT) + MED_LARGE_BUFF*(DOWN+RIGHT)
        )
        arrow1.set_color(GREEN)

        words2 = OldTexText("15 blocked \\\\", "by ", "B")
        words2.set_color_by_tex("B", GREEN)
        words2.scale(0.8)
        words2.next_to(A_group, LEFT, MED_LARGE_BUFF, UP)
        arrow2 = Arrow(words2.get_right(), out_of_B[-1])
        arrow2.set_color(RED)

        self.play(
            Write(words1, run_time = 1),
            ShowCreation(arrow1),
            self.in_A_in_B.set_fill, GREEN, 0.5,
            Animation(in_B),
        )
        self.wait()
        self.play(
            ReplacementTransform(words1, words2),
            ReplacementTransform(arrow1, arrow2),
            self.in_A_in_B.set_fill, None, 0,
            Animation(in_B),
            self.in_A_out_B.set_fill, RED, 0.5,
            Animation(out_of_B)
        )
        self.wait()
        self.play(ApplyMethod(
            VGroup(self.in_A_out_B, out_of_B).shift,
            MED_LARGE_BUFF*UP, 
            rate_func = wiggle,
            run_time = 1.5,
        ))
        self.wait(0.5)

        self.in_B = in_B
        self.out_of_B = out_of_B
        self.out_of_B_words = words2
        self.out_of_B_arrow = arrow2

    def separate_by_C(self):
        A_group = self.A_group
        B_group = self.B_group
        C_group = self.C_group
        in_B = self.in_B
        A, B, C = self.venn_diagram

        C.target, C.label.target = C_group.saved_state
        C.target.scale(4)
        C.target.move_to(A)
        C.target.shift(self.A_to_C_vect)
        C_center = C.target.get_center()
        C.label.target.scale(2)
        C.label.target.next_to(
            C.target.point_from_proportion(0),
            DOWN+RIGHT, buff = SMALL_BUFF
        )

        in_B.sort(
            lambda p : get_norm(p - C_center)
        )
        in_C = VGroup(*in_B[:-11])
        out_of_C = VGroup(*in_B[-11:])
        in_C_out_B = VGroup(*self.out_of_B[:6])

        words = OldTexText(
            "$15\\%$", "passing", "B \\\\",
            "get blocked by ", "C",
        )
        words.scale(0.8)
        words.set_color_by_tex_to_color_map({
            "B" : GREEN,
            "C" : BLUE,
        })
        words.next_to(self.out_of_B_words, DOWN, LARGE_BUFF)
        words.to_edge(LEFT)
        percent = words[0]
        pound = OldTex("\\#")
        pound.move_to(percent, RIGHT)
        less_than_15 = OldTex("<15")
        less_than_15.next_to(words, DOWN)


        arrow = Arrow(words.get_right(), out_of_C)
        arrow.set_color(GREEN)

        C_copy = C.copy()
        C_copy.set_fill(BLACK, opacity = 1)

        self.play(
            self.in_A_in_B.set_fill, GREEN, 0.5,
            rate_func = there_and_back,
        )
        self.play(
            MoveToTarget(C),
            MoveToTarget(C.label),
            in_C.shift, 0.2*DOWN+0.15*RIGHT,
            out_of_C.shift, SMALL_BUFF*(UP+LEFT),
            in_C_out_B.shift, 0.3*DOWN
        )
        self.play(
            self.in_A_in_B_out_C.set_fill, GREEN, 0.5,
            Write(words, run_time = 1),
            ShowCreation(arrow),
            Animation(out_of_C),
        )
        self.play(ApplyMethod(
            VGroup(self.in_A_in_B_out_C, out_of_C).shift,
            MED_LARGE_BUFF*UP,
            rate_func = wiggle
        ))
        self.wait()
        C.save_state()
        self.play(C.set_fill, BLACK, 1)
        self.wait()
        self.play(C.restore)
        self.wait(2)
        self.play(Transform(percent, pound))
        self.play(Write(less_than_15, run_time = 1))
        self.wait()

        self.in_C = in_C
        self.out_of_C = out_of_C
        words.add(less_than_15)
        self.out_of_C_words = words
        self.out_of_C_arrow = arrow

    def show_two_relevant_subsets(self):
        A, B, C = self.venn_diagram

        all_out_of_C = VGroup(*it.chain(
            self.out_of_B[6:],
            self.out_of_C,
        ))
        everything = VGroup(*self.get_top_level_mobjects())
        photon_groups = [all_out_of_C, self.out_of_C, self.out_of_B]
        regions = [self.in_A_out_C, self.in_A_in_B_out_C, self.in_A_out_B]
        self.play(*[
            ApplyMethod(
                m.scale, 0.7, 
                method_kwargs = {
                    "about_point" : FRAME_Y_RADIUS*DOWN
                }
            )
            for m in everything
        ])

        terms = VGroup(
            OldTex("N(", "A", "\\checkmark", ",", "C", ")", "\\le"),
            OldTex(
                "N(", "A", "\\checkmark", ",", 
                "B", "\\checkmark", ",", "C", ")"
            ),
            OldTex("+\\, N(", "A", "\\checkmark", ",", "B", ")"),
        )
        terms.arrange(RIGHT)
        terms.to_edge(UP)
        for term, index, group in zip(terms, [-3, -2, -2], photon_groups):
            term.set_color_by_tex("checkmark", "#00ff00")
            cross = Cross(term[index])
            cross.set_color("#ff0000")
            cross.set_stroke(width = 8)
            term[index].add(cross)

        less_than = terms[0][-1]
        terms[0].remove(less_than)
        plus = terms[2][0][0]
        terms[2][0].remove(plus)
        rects = list(map(SurroundingRectangle, terms))
        terms[2][0].add_to_back(plus)
        last_rects = VGroup(*rects[1:])

        should_be_50 = OldTexText("Should be 50 \\\\", "...somehow")
        should_be_50.scale(0.8)
        should_be_50.next_to(rects[0], DOWN)

        lt_fifteen = VGroup(self.out_of_C_words[-1]).copy()
        something_lt_15 = OldTexText("(Something", "$<15$", ")")
        something_lt_15.scale(0.8)
        something_lt_15.next_to(rects[1], DOWN)
        lt_fifteen.target = something_lt_15

        fifteen = VGroup(*self.out_of_B_words[0][:2]).copy()
        fifteen.generate_target()
        fifteen.target.scale(1.5)
        fifteen.target.next_to(rects[2], DOWN)

        nums = [should_be_50, lt_fifteen, fifteen]

        cross = Cross(less_than)
        cross.set_color("#ff0000")
        cross.set_stroke(width = 8)

        tweaser_group = VGroup(
            self.in_A_in_B_out_C.copy(),
            self.in_A_out_B.copy(),
        )
        tweaser_group.set_fill(TEAL, 1)
        tweaser_group.set_stroke(TEAL, 5)

        #Fade out B circle
        faders = VGroup(
            B, B.label,
            self.out_of_B_words, self.out_of_C_words,
            self.out_of_B_arrow, self.out_of_C_arrow,
            *regions[1:]
        )
        faders.save_state()

        self.play(faders.fade, 1)
        self.play(Write(terms[0]), run_time = 1)
        self.wait()
        self.photon_thinks_in_A_out_C()
        regions[0].set_stroke(YELLOW, width = 8)
        regions[0].set_fill(YELLOW, opacity = 0.25)
        self.play(
            VGroup(regions[0], all_out_of_C).shift, 0.5*UP,
            run_time = 1.5,
            rate_func = wiggle,
        )
        self.wait(2)

        #Photons jump
        self.photons.save_state()
        self.play(Write(should_be_50[0], run_time = 1))
        self.photons_jump_to_A_not_C_region()
        self.wait()
        self.play(
            faders.restore,
            self.photons.restore,
        )

        self.play(
            faders.restore,
            regions[0].set_fill, None, 0,
            Animation(self.photons)
        )

        #Funny business
        everything_copy = everything.copy().scale(1./3)
        braces = VGroup(
            Brace(everything_copy, LEFT),
            Brace(everything_copy, RIGHT),
        ).scale(3)
        funny_business = OldTexText("Funny business")
        funny_business.scale(1.5)
        funny_business.to_edge(UP)
        funny_business.shift(RIGHT)

        self.play(
            FadeIn(funny_business),
            *list(map(Write, braces)),
            run_time = 1
        )
        self.wait()
        self.play(
            FadeIn(less_than),
            *list(map(FadeOut, [funny_business, braces]))
        )

        for term, group, region, num in list(zip(terms, photon_groups, regions, nums))[1:]:  # CHANGE: Python 3: zip()/map()/filter() return iterators, wrap in list() before slicing.
            group.set_stroke(WHITE)
            self.play(Write(term, run_time = 1))
            self.wait()
            self.play(
                ApplyMethod(
                    VGroup(region, group).shift, 0.5*UP,
                    rate_func = wiggle,
                    run_time = 1.5,
                ),
            )
            self.play(MoveToTarget(num))
            self.wait()
        self.wait()

        self.play(ShowCreation(rects[0]))
        self.play(
            VGroup(regions[0], all_out_of_C).shift, 0.5*UP,
            run_time = 1.5,
            rate_func = wiggle,
        )
        self.wait()
        self.play(Transform(rects[0], last_rects))
        self.in_A_out_B.save_state()
        self.in_A_in_B_out_C.save_state()
        self.play(
            self.in_A_out_B.set_fill, YELLOW, 0.5,
            self.in_A_in_B_out_C.set_fill, YELLOW, 0.5,
            Animation(self.photons)
        )
        self.wait()
        self.play(
            FadeOut(rects[0]),
            self.in_A_out_B.restore,
            self.in_A_in_B_out_C.restore,
            Animation(self.in_A_out_C),
            Animation(self.photons)
        )
        self.wait()
        self.play(
            FadeIn(should_be_50[1]),
            ShowCreation(cross)
        )

        morty = Mortimer()
        morty.to_corner(DOWN+RIGHT)
        contradiction = OldTexText("Contradiction!")
        contradiction.next_to(morty, UP, aligned_edge = RIGHT)
        contradiction.set_color(RED)

        self.play(FadeIn(morty))
        self.play(
            morty.change, "confused", should_be_50,
            Write(contradiction, run_time = 1)
        )
        self.play(Blink(morty))
        self.wait()

    def photons_jump_to_A_not_C_region(self):
        in_C = self.in_C
        in_C.sort(lambda p : np.dot(p, DOWN+RIGHT))
        movers = VGroup(*self.in_C[:30])
        for mover in movers:
            mover.generate_target()
            mover.target.shift(1.2*UP + 0.6*LEFT)
            mover.target.set_stroke(WHITE)
        self.play(LaggedStartMap(
            MoveToTarget, movers,
            path_arc = np.pi,
            lag_ratio = 0.3
        ))

    def photon_thinks_in_A_out_C(self):
        photon = self.photons[-1]
        photon.save_state()
        photon.generate_target()
        photon.target.scale(4)
        photon.target.center().to_edge(LEFT).shift(DOWN)
        bubble = ThoughtBubble()
        content = OldTex("A", "\\checkmark", ",", "C")
        content.set_color_by_tex("checkmark", "#00ff00")
        cross = Cross(content[-1])
        cross.set_color("#ff0000")
        content.add(cross)
        bubble.add_content(content)
        bubble.resize_to_content()
        bubble.add(bubble.content)
        bubble.pin_to(photon.target).shift(SMALL_BUFF*RIGHT)
        bubble.save_state()
        bubble.scale(0.25)
        bubble.move_to(photon.get_corner(UP+RIGHT), DOWN+LEFT)
        bubble.fade()

        self.play(
            MoveToTarget(photon),
            bubble.restore,
        )
        self.play(photon.eyes.blink_anim())
        self.play(
            photon.restore, 
            FadeOut(bubble)
        )


    #######

    def setup_venn_diagram_sections(self):
        in_A_out_B, in_A_in_B_out_C, in_A_out_C, in_A_in_B = segments = VGroup(*[
            SVGMobject(
                file_name = "VennDiagram_" + s,
                stroke_width = 0,
                fill_opacity = 0.5,
                fill_color = YELLOW,
            )
            for s in ("in_A_out_B", "in_A_in_B_out_C", "in_A_out_C", "in_A_in_B")
        ])

        in_A_out_B.scale(2.59)
        in_A_out_B.move_to(3.74*UP + 2.97*RIGHT, UP+RIGHT)

        in_A_in_B_out_C.scale(1.84)
        in_A_in_B_out_C.move_to(2.23*UP, UP+RIGHT)

        in_A_out_C.scale(2.56)
        in_A_out_C.move_to(3*LEFT + (3.69)*UP, UP+LEFT)

        in_A_in_B.scale(2.24)
        in_A_in_B.move_to(2.23*UP + 3*LEFT, UP+LEFT)

        segments.set_fill(BLACK, opacity = 0)

        self.in_A_out_B = in_A_out_B
        self.in_A_in_B_out_C = in_A_in_B_out_C
        self.in_A_out_C = in_A_out_C
        self.in_A_in_B = in_A_in_B
        self.A_segments = segments

    def arrange_photons_in_circle(self, photons):
        R = np.sqrt(len(photons) / np.pi)
        pairs = []
        rejected = []
        for x, y in it.product(*[list(range(-int(R)-1, int(R)+2))]*2):
            if x**2 + y**2 < R**2:
                pairs.append((x, y))
            else:
                rejected.append((x, y))
        rejected.sort(
            kay=lambda x, y: (x**2 + y**2)
        )
        for i in range(len(photons) - len(pairs)):
            pairs.append(rejected.pop())
        for photon, (x, y) in zip(photons, pairs):
            photon.set_width(0.7)
            photon.move_to(x*RIGHT + y*UP)
        return photons


class ReEmphasizeVennDiagram(VennDiagramProofByContradiction):
    def construct(self):
        self.draw_venn_diagram(send_to_corner = False)
        self.rescale_diagram()
        self.setup_faded_circles()
        self.shift_B_circle()
        self.shift_C_circle()
        self.show_A_not_C_region()
        self.shorten_labels()
        self.show_inequality_with_circle()
        # self.emphasize_containment()
        self.write_50_percent()
        self.write_assumption()
        self.adjust_circles()

    def rescale_diagram(self):
        group = VGroup(self.venn_diagram, *[
            c.label for c in self.venn_diagram
        ])
        self.play(
            group.scale, 0.7,
            group.to_edge, DOWN, MED_SMALL_BUFF,
        )
        self.clear()
        self.add_foreground_mobjects(*group)

    def setup_faded_circles(self):
        self.circles = self.venn_diagram[:3]
        self.black_circles = VGroup(*[
            circ.copy().set_stroke(width = 0).set_fill(BLACK, 1)
            for circ in self.circles
        ])
        self.filled_circles = VGroup(*[
            circ.copy().set_stroke(width = 0).set_fill(circ.get_color(), 1)
            for circ in self.circles
        ])

    def shift_B_circle(self):
        A, B, C = self.circles
        A0, B0, C0 = self.black_circles
        A1, B1, C1 = self.filled_circles

        words = OldTexText("Should be 15\\% \\\\ of circle ", "A")
        words.scale(0.7)
        words.set_color_by_tex("A", RED)
        words.next_to(A, UP, LARGE_BUFF)
        words.shift(RIGHT)
        arrow = Arrow(
            words.get_bottom(),
            A.get_top() + MED_SMALL_BUFF*RIGHT,
            color = RED
        )

        self.play(FadeIn(A1))
        self.play(FadeIn(B0))
        self.play(
            FadeIn(words, lag_ratio = 0.5),
            ShowCreation(arrow)
        )
        self.wait()
        vect = 0.6*(A.get_center() - B.get_center())
        self.play(
            B0.shift, vect,
            B.shift, vect,
            B.label.shift, vect,
            run_time = 2,
            rate_func = running_start,
        )
        B1.shift(vect)
        self.wait()

        self.in_A_out_B_words = words
        self.in_A_out_B_arrow = arrow
        for mob in words, arrow:
            mob.save_state()

    def shift_C_circle(self):
        A, B, C = self.circles
        A0, B0, C0 = self.black_circles
        A1, B1, C1 = self.filled_circles

        words = OldTexText("Should be 15\\% \\\\ of circle ", "B")
        words.scale(0.7)
        words.set_color_by_tex("B", GREEN)
        words.next_to(B, LEFT)
        words.shift(2.5*UP)
        arrow = Arrow(
            words.get_bottom(),
            B.point_from_proportion(0.4),
            color = GREEN
        )

        self.play(
            FadeOut(A1),
            FadeOut(B0),
            self.in_A_out_B_words.fade, 1,
            self.in_A_out_B_arrow.fade, 1,
            FadeIn(B1),
            FadeIn(words, lag_ratio = 0.5),
            ShowCreation(arrow)
        )
        self.play(FadeIn(C0))
        self.wait(2)
        vect = 0.5*(B.get_center() - C.get_center())
        self.play(
            C0.shift, vect,
            C.shift, vect,
            C.label.shift, vect,
            run_time = 2,
            rate_func = running_start,
        )
        C1.shift(vect)
        self.wait()

        for mob in words, arrow:
            mob.save_state()
        self.in_B_out_C_words = words
        self.in_B_out_C_arrow = arrow

    def show_A_not_C_region(self):
        A, B, C = self.circles
        A0, B0, C0 = self.black_circles
        A1, B1, C1 = self.filled_circles
        A1_yellow_copy = A1.copy().set_fill(YELLOW)

        self.play(
            FadeOut(B1),
            FadeOut(C0),
            self.in_B_out_C_words.fade, 1,
            self.in_B_out_C_arrow.fade, 1,
            FadeIn(A1_yellow_copy)
        )
        self.play(FadeIn(C0))
        self.wait()
        self.A1_yellow_copy = A1_yellow_copy

    def shorten_labels(self):
        A, B, C = self.circles
        A0, B0, C0 = self.black_circles
        A1, B1, C1 = self.filled_circles
        for circle in A, B, C:
            circle.pre_label = VGroup(*circle.label[:-1])
            circle.letter = circle.label[-1]

        self.play(
            A.pre_label.fade, 1,
            A.letter.scale, 2,
            A.letter.move_to, A.pre_label, LEFT,
            B.pre_label.fade, 1,
            # CHANGE: Cairo scale(factor, point) positional point -> about_point kwarg (GL's 2nd positional is min_scale_factor).
            B.letter.scale, 2, {"about_point": B.letter.get_right()},
            C.pre_label.fade, 1,
            C.letter.scale, 2,
            C.letter.move_to, C.pre_label, LEFT,
            C.letter.shift, DOWN+0.5*LEFT,
        )
        for circle in A, B, C:
            circle.remove(circle.label)
            self.remove(circle.label)
            circle.add(circle.letter)
            self.add(circle.letter)

    def show_inequality_with_circle(self):
        A, B, C = self.circles
        A0, B0, C0 = self.black_circles
        A1, B1, C1 = self.filled_circles
        A1_yellow_copy = self.A1_yellow_copy

        inequality = VGroup(
            OldTex("N(", "A", "\\checkmark", ",", "C", ")"),
            OldTex("N(", "B", "\\checkmark", ",", "C", ")"),
            OldTex("N(", "A", "\\checkmark", ",", "B", ")"),
        )
        inequality.arrange(RIGHT)
        for tex in inequality:
            tex.set_color_by_tex("checkmark", "#00ff00")
            if len(tex) > 1:
                cross = Cross(tex[-2], color = "#ff0000")
                cross.set_stroke(width = 8)
                tex[-2].add(cross)
        inequality.space_out_submobjects(2.1)
        big_le = OldTex("\\le").scale(2)
        big_plus = OldTex("+").scale(2)
        big_le.move_to(2.75*LEFT)
        big_plus.move_to(2.25*RIGHT)

        groups = VGroup(*[
            VGroup(
                m2.copy(), m1.copy(),
                VGroup(*self.circles).copy()
            )
            for m1, m2 in [(C0, A1_yellow_copy), (C0, B1), (B0, A1)]
        ])
        for group, vect in zip(groups[1:], [UP, 5*RIGHT+UP]):
            group.scale(0.5)
            group.shift(vect)
            group.save_state()
            group.shift(-vect[0]*RIGHT + 5*LEFT)
        inequality.shift(2.25*DOWN + 0.25*LEFT)

        self.in_B_out_C_words.restore()
        self.in_B_out_C_words.move_to(2*UP)
        self.in_A_out_B_words.restore()
        self.in_A_out_B_words.move_to(5*RIGHT+2*UP)

        self.clear()
        self.play(
            groups[0].scale, 0.5,
            groups[0].shift, 5*LEFT + UP,
            Write(inequality[0], run_time = 1),
            FadeIn(big_le),
        )
        self.wait()
        self.play(FadeIn(groups[1]))
        self.play(
            groups[1].restore, 
            FadeIn(inequality[1]),
            FadeIn(self.in_B_out_C_words),
            FadeIn(big_plus),
        )
        self.play(FadeIn(groups[2]))
        self.play(
            groups[2].restore,
            FadeIn(inequality[2]),
            FadeIn(self.in_A_out_B_words),
        )
        self.wait(2)

        self.groups = groups
        self.inequality = inequality

    def emphasize_containment(self):
        groups = self.groups
        c1, c2 = [VGroup(*group[:2]).copy() for group in groups[1:]]
        foreground = VGroup(groups[0][-1], *groups[1:])

        rect = SurroundingRectangle(groups[0])

        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        self.play(
            ApplyMethod(
                c1.shift, 4*LEFT,
                path_arc = -np.pi/2,
            ),
            Animation(foreground)
        )
        self.play(
            ApplyMethod(
                c2.shift, 8*LEFT,
                path_arc = -np.pi/2,
            ),
            Animation(c1),
            Animation(foreground),
            run_time = 1.5
        )
        self.play(
            FadeOut(c2),
            FadeOut(c1),
            Animation(foreground),
            run_time = 2
        )
        self.wait()

    def write_50_percent(self):
        words = OldTexText(
            "Should be 50\\% \\\\ of circle ", "A",
            "...somehow"
        )
        words.scale(0.7)
        words.set_color_by_tex("A", RED)
        words.move_to(5*LEFT + 2*UP)

        self.play(Write(words))
        self.wait()

    def write_assumption(self):
        words = OldTexText("Assume circles have the same size$^*$")
        words.scale(0.8)
        words.to_edge(UP)

        footnote = OldTexText("""
            *If you prefer, you can avoid the need for that 
            assumption by swapping the roles of A and C here 
            and writing a second inequality for added constraint.
        """)
        footnote.scale(0.5)
        footnote.to_corner(DOWN+RIGHT)
        footnote.add(words[-1])
        words.remove(words[-1])

        self.footnote = footnote

        self.play(FadeIn(words))

    def adjust_circles(self):
        groups = self.groups
        A_group = VGroup(
            groups[0][0],
            groups[2][0],
            groups[0][2][0],
            groups[1][2][0],
            groups[2][2][0],
        )
        B_group = VGroup(
            groups[1][0],
            groups[2][1],
            groups[0][2][1],
            groups[1][2][1],
            groups[2][2][1],
        )
        C_group = VGroup(
            groups[0][1],
            groups[1][1],
            groups[0][2][2],
            groups[1][2][2],
            groups[2][2][2],
        )

        def center_of_mass(mob):
            return np.apply_along_axis(np.mean, 0, mob.get_points())

        movers = [A_group, B_group, C_group]
        A_ref, B_ref, C_ref = [g[4] for g in movers]
        B_center = center_of_mass(B_ref)
        B_to_A = center_of_mass(A_ref) - B_center
        B_to_C = center_of_mass(C_ref) - B_center

        A_freq = 1
        C_freq = -0.7

        self.time = 0
        dt = 1 / self.camera.frame_rate

        def move_around(total_time):
            self.time
            t_range = list(range(int(total_time/dt)))
            for x in ProgressDisplay(t_range):
                self.time += dt
                new_B_to_A = rotate_vector(B_to_A, self.time*A_freq)
                new_B_to_C = rotate_vector(B_to_C, self.time*C_freq)
                A_group.shift(B_center + new_B_to_A - center_of_mass(A_ref))
                C_group.shift(B_center + new_B_to_C - center_of_mass(C_ref))
                self.wait(dt)

        move_around(3)
        self.add(self.footnote)
        move_around(1)
        self.remove(self.footnote)
        move_around(15)
