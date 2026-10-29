# ==============================================================================
# Scene:      Promotion
# Source:     videos/_2018/uncertainty.py (lines 4385-4523)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Promotion.py Promotion -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL Arrow is a single filled shape without a .tip attribute; dropped the small tip shift
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class Promotion(PiCreatureScene):
    CONFIG = {
        "camera_class" : ThreeDCamera,
        "seconds_to_blink" : 5,
    }
    def construct(self):
        aops_logo = AoPSLogo()
        aops_logo.next_to(self.pi_creature, UP+LEFT)
        url = OldTexText(
            "AoPS.com/", "3b1b",
            arg_separator = ""
        )
        url.to_corner(UP+LEFT)
        url_rect = Rectangle(color = BLUE)
        url_rect.replace(
            url.get_part_by_tex("3b1b"),
            stretch = True
        )

        url_rect.stretch_in_place(1.1, dim = 1)

        rect = Rectangle(height = 9, width = 16)
        rect.set_height(4.5)
        rect.next_to(url, DOWN)
        rect.to_edge(LEFT)
        rect.set_stroke(width = 0)
        mathy = Mathematician()
        mathy.flip()
        mathy.to_corner(DOWN+RIGHT)
        morty = self.pi_creature
        morty.save_state()
        book = ImageMobject("AoPS_volume_2")
        book.set_height(2)
        book.next_to(mathy, UP+LEFT).shift(MED_LARGE_BUFF*LEFT)
        mathy.get_center = mathy.get_top

        words = OldTexText("""
            Interested in working for \\\\ 
            one of my favorite math\\\\ 
            education companies?
        """, alignment = "")
        words.to_edge(UP)

        arrow = Arrow(
            aops_logo.get_top(),
            morty.get_top(),
            path_arc = -0.4*TAU,
            stroke_width = 5,
            tip_length = 0.5,
        )
        # CHANGE: GL Arrow is a single filled shape without a .tip attribute; dropped the small tip shift
        pass  # arrow.tip.shift(SMALL_BUFF*DOWN)

        self.add(words)
        self.play(
            self.pi_creature.change_mode, "raise_right_hand",
            *[
                DrawBorderThenFill(
                    submob,
                    run_time = 2,
                    rate_func = squish_rate_func(double_smooth, a, a+0.5)
                )
                for submob, a in zip(aops_logo, np.linspace(0, 0.5, len(aops_logo)))
            ]
        )
        self.play(
            words.scale, 0.75,
            words.next_to, url, DOWN, LARGE_BUFF,
            words.shift_onto_screen,
            Write(url),
        )
        self.wait(2)
        self.play(
            LaggedStartMap(
                ApplyFunction, aops_logo,
                lambda mob : (lambda m : m.shift(0.2*UP).set_color(YELLOW), mob),
                rate_func = there_and_back, 
                run_time = 1,
            ),
            morty.change, "thinking"
        )
        self.wait()
        self.play(ShowCreation(arrow))
        self.play(FadeOut(arrow))
        self.wait()

        # To teacher
        self.play(
            morty.change_mode, "plain",
            morty.flip,
            morty.scale, 0.7,
            morty.next_to, mathy, LEFT, LARGE_BUFF,
            morty.to_edge, DOWN,
            FadeIn(mathy),
        )
        self.play(
            PiCreatureSays(
                mathy, "",
                bubble_config = {"width" : 5},
                look_at = morty.eyes,
            ),
            morty.change, "happy",
            aops_logo.shift, 1.5*UP + 0.5*RIGHT
        )
        self.play(Blink(mathy))
        self.wait()
        self.play(
            RemovePiCreatureBubble(
                mathy, target_mode = "raise_right_hand"
            ),
            aops_logo.to_corner, UP+RIGHT,
            aops_logo.shift, MED_SMALL_BUFF*DOWN,
            GrowFromPoint(book, mathy.get_corner(UP+LEFT)),
        )
        self.play(morty.change, "pondering", book)
        self.wait(3)
        self.play(Blink(mathy))
        self.wait()
        self.play(
            Animation(
                BackgroundRectangle(book, fill_opacity = 1),
                remover = True
            ),
            FadeOut(book),
        )
        print(self.num_plays)
        self.play(
            FadeOut(words),
            ShowCreation(rect),
            morty.restore,
            morty.change, "happy", rect,
            FadeOut(mathy),
        )
        self.wait(10)
        self.play(ShowCreation(url_rect))
        self.play(
            FadeOut(url_rect),
            url.get_part_by_tex("3b1b").set_color, BLUE,
        )
        self.wait(15)
