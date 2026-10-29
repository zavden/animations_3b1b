# ==============================================================================
# Scene:      BroughtToYouBy
# Source:     videos/_2018/div_curl.py (lines 4135-4257)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BroughtToYouBy.py BroughtToYouBy -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - _2017.eoc.zeta is not part of this project; local copy of its zeta() (mpmath) as in videos/_2016/zeta.py, with the removed np.complex replaced by complex
#   - new class PatreonLogo: own code-drawn replacement for the Patreon brand logo (the svg came from the deleted videos/assets)
#
# Placeholder assets (not Grant's originals):
#   - svg_images/patreon_logo.svg replaced by an in-scene own drawing (class PatreonLogo in the scene: coral disc + LaTeX heart), no generator file
# ==============================================================================

from manim_imports_ext import *

# CHANGE: new class PatreonLogo: own code-drawn replacement for the Patreon brand logo (the svg came from the deleted videos/assets)
class PatreonLogo(VGroup):
    # Own replacement for the brand logo (Patreon svg came from videos/assets): coral disc with a white heart, same width (4) and fill color.
    def __init__(self, width=4, **kwargs):
        disc = Circle(radius=1, fill_color="#F96854", fill_opacity=1, stroke_width=0)
        heart = OldTex("\\heartsuit")
        heart.set_color(WHITE)
        heart.set_height(0.9)
        heart.move_to(disc)
        super().__init__(disc, heart, **kwargs)
        self.set_width(width)
        self.center()


class BroughtToYouBy(PiCreatureScene):
    CONFIG = {
        "pi_creatures_start_on_screen": False,
    }

    def construct(self):
        self.brought_to_you_by()
        self.just_you_and_me()

    def brought_to_you_by(self):
        so_words = OldTexText("So", "...", arg_separator="")
        so_words.scale(2)

        btyb = OldTexText("Brought to you", "by")
        btyb.scale(1.5)
        btyb_line = Line(LEFT, RIGHT)
        btyb_line.next_to(btyb, RIGHT, SMALL_BUFF)
        btyb_line.align_to(btyb[0], DOWN)
        btyb_group = VGroup(btyb, btyb_line)
        btyb_group.center()

        you_word = OldTexText("\\emph{you}")
        you_word.set_color(YELLOW)
        you_word.scale(1.75)
        you_word.move_to(btyb_line)
        you_word.align_to(btyb, DOWN)

        only_word = OldTexText("(only)")
        only_word.scale(1.25)
        only_brace = Brace(only_word, DOWN, buff=SMALL_BUFF)
        only_group = VGroup(only_word, only_brace)
        only_group.next_to(
            VGroup(btyb[0][-1], btyb[1][0]), UP, SMALL_BUFF
        )
        only_group.set_color(RED)

        full_group = VGroup(btyb_group, only_group, you_word)
        full_group.generate_target()
        full_group.target.scale(0.4)
        full_group.target.to_corner(UL)

        patreon_logo = PatreonLogo()
        patreon_logo.scale(0.4)
        patreon_logo.next_to(full_group.target, DOWN)

        self.play(
            Write(so_words[0]),
            LaggedStartMap(
                DrawBorderThenFill, so_words[1],
                run_time=5
            ),
        )
        self.play(
            so_words.shift, DOWN,
            so_words.fade, 1,
            remover=True
        )
        self.play(FadeInFromDown(btyb_group))
        self.wait()
        self.play(Write(you_word))
        self.play(
            GrowFromCenter(only_brace),
            Write(only_word)
        )
        self.wait()
        self.play(MoveToTarget(
            full_group,
            rate_func=running_start,
        ))
        self.play(LaggedStartMap(
            DrawBorderThenFill, patreon_logo
        ))
        self.wait()

    def just_you_and_me(self):
        randy, morty = self.pi_creatures
        for pi in self.pi_creatures:
            pi.change("pondering")
        math = OldTex("\\sum_{n=1}^\\infty \\frac{1}{n^s}")
        math.scale(2)
        math.move_to(self.pi_creatures)

        spiral = Line(0.5 * RIGHT, 0.5 * RIGHT + 70 * UP)
        spiral.insert_n_curves(1000)
        # CHANGE: _2017.eoc.zeta is not part of this project; local copy of its zeta() (mpmath) as in videos/_2016/zeta.py, with the removed np.complex replaced by complex
        import mpmath

        def zeta(z):
            try:
                return complex(mpmath.zeta(z))
            except Exception:
                return complex(FRAME_X_RADIUS, 0)
        spiral.apply_complex_function(zeta)
        step = 0.1
        spiral = VGroup(*[
            VMobject().pointwise_become_partial(
                spiral, a, a + step
            )
            for a in np.arange(0, 1, step)
        ])
        spiral.set_color_by_gradient(BLUE, YELLOW, RED)
        spiral.scale(0.5)
        spiral.move_to(math)

        self.play(FadeInFromDown(randy))
        self.play(FadeInFromDown(morty))
        self.play(
            Write(math),
            randy.change, "hooray",
            morty.change, "hooray",
        )
        self.look_at(math)
        self.play(
            ShowCreation(spiral, run_time=6, rate_func=linear),
            math.scale, 0.5,
            math.shift, 3 * UP,
            randy.change, "thinking",
            morty.change, "thinking",
        )
        self.play(LaggedStartMap(FadeOut, spiral, run_time=3))
        self.wait(3)

    # Helpers
    def create_pi_creatures(self):
        randy = Randolph(color=BLUE_C)
        randy.to_edge(DOWN).shift(4 * LEFT)
        morty = Mortimer()
        morty.to_edge(DOWN).shift(4 * RIGHT)
        return VGroup(randy, morty)
