# ==============================================================================
# Scene:      NewContrastThreeContexts
# Source:     videos/_2020/med_test.py (lines 2793-3003)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NewContrastThreeContexts.py NewContrastThreeContexts -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - OldTexText("\\,", ...) no longer leaves the empty part as a submobject; the last part is taken
# ==============================================================================

from manim_imports_ext import *

class WomanIcon(SVGMobject):
    CONFIG = {
        "fill_color": GREY_B,
        "stroke_width": 0,
    }

    def __init__(self, **kwargs):
        super().__init__("woman_icon", **kwargs)
        self.remove(self[0])


class NewContrastThreeContexts(Scene):
    def construct(self):
        # Background
        bg_rect = FullScreenFadeRectangle()
        bg_rect.set_fill(GREY_E, 1)
        self.add(bg_rect)

        # Scene templates
        screens = VGroup(*(
            ScreenRectangle() for x in range(3)
        ))
        screens.set_stroke(WHITE, 2)
        screens.set_fill(BLACK, 1)
        screens.arrange(DOWN, buff=LARGE_BUFF)
        screens.set_height(FRAME_HEIGHT - 1)
        screens.next_to(ORIGIN, RIGHT)

        self.add(screens)

        # Prevalence values
        dots_template = VGroup(*(Dot() for x in range(1000)))
        dots_template.arrange_in_grid(20, 50, buff=SMALL_BUFF)
        dots_template.set_fill(GREY_B)
        dot_groups = VGroup()
        for screen, n in zip(screens, [1, 10, 100]):
            dots = dots_template.copy()
            dots.match_width(screen)
            dots.scale(0.9)
            dots.move_to(screen, DOWN)
            dots.shift(0.1 * UP)
            for dot in random.sample(list(dots), n):
                dot.set_fill(YELLOW)
            dot_groups.add(dots)

        prevalence_labels = VGroup(
            OldTexText("Prevalence: ", "0.1\\%"),
            OldTexText("Prevalence: ", "1\\%"),
            OldTexText("Prevalence: ", "10\\%"),
        )
        for label, dots in zip(prevalence_labels, dot_groups):
            label.scale(0.75)
            label[1].set_color(YELLOW)
            label.next_to(dots, UP, buff=0.15)

        self.add(prevalence_labels)
        self.add(dot_groups)

        # Words
        words = VGroup(
            OldTexText("Same", " test"),
            OldTexText("Same", " accuracy"),
            OldTexText("Same", " result"),
        )
        words.scale(1.5)
        words.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        words.to_edge(LEFT)
        words.set_stroke(BLACK, 3, background=True)

        for word in words[:2]:
            self.add(word)
            self.wait()

        # Show receiving results
        def get_positive_result():
            woman = WomanIcon()
            clipboard = SVGMobject(
                "clipboard",
                stroke_width=0,
                fill_color=interpolate_color(GREY_BROWN, WHITE, 0.2)
            )
            clipboard.set_width(1)
            clipboard.next_to(woman, LEFT)
            content = OldTexText("+\\\\", "Cancer\\\\detected")
            content[0].scale(2, about_edge=DOWN)
            content[0].set_color(GREEN)
            content[0].set_stroke(GREEN, 3)
            content[0].shift(SMALL_BUFF * UP)
            content.set_width(0.7 * clipboard.get_width())
            content.move_to(clipboard)
            content.shift(SMALL_BUFF * DOWN)
            clipboard.add(content)
            result = VGroup(woman, clipboard)
            result.scale(0.7)
            return result

        globals()['get_positive_result'] = get_positive_result

        positive_results = VGroup(*(
            get_positive_result() for screen in screens
        ))
        positive_results.generate_target()
        positive_results.set_opacity(0)
        for screen, result in zip(screens, positive_results.target):
            result.set_height(screen.get_height() * 0.5)
            result.next_to(screen, RIGHT, MED_LARGE_BUFF, aligned_edge=DOWN)
            result.shift(0.25 * UP)

        self.add(words[2])
        self.play(MoveToTarget(positive_results))
        self.wait()

        # Different results
        probs = VGroup(*(
            Integer(0, unit="\\%").next_to(result, UP)
            for result in positive_results
        ))
        probs.set_fill(GREEN)

        result_change_anims = [
            ChangeDecimalToValue(probs[0], 1),
            ChangeDecimalToValue(probs[1], 9),
            ChangeDecimalToValue(probs[2], 53),
            UpdateFromAlphaFunc(
                Mobject(),
                lambda m, a, probs=probs: probs.set_opacity(a),
                remover=True,
            ),
        ]

        # Odds
        prior_probs = VGroup(*(pl[1] for pl in prevalence_labels))
        prior_odds = VGroup(
            OldTexText("1:999"),
            OldTexText("1:99"),
            OldTexText("1:9"),
        )
        prior_odds.set_color(YELLOW)
        for po, pp in zip(prior_odds, prior_probs):
            po.match_height(pp)
            po.scale(0.8)
            po.move_to(pp, LEFT)

        post_odds = VGroup(
            OldTexText("10:999"),
            OldTexText("10:99"),
            OldTexText("10:9"),
        )
        for po, prob in zip(post_odds, probs):
            po.match_color(prob)
            po.match_height(prob)
            po.scale(0.8)
            po.move_to(prob, LEFT)

        # Show updates
        arrows = VGroup(*(
            Arrow(
                prior.get_corner(UR), post.get_corner(UL),
                buff=0.1,
                path_arc=-45 * DEGREES,
            )
            for prior, post in zip(prior_odds, post_odds)
        ))
        arrows.set_color(BLUE)

        # What test accuracy does
        ta_words = VGroup(
            OldTexText("Test", " accuracy"),
            OldTexText("\\emph{alone} ", "does not"),
            OldTexText("determine", "."),
            OldTexText("\\,", "your chances"),
        )
        ta_words[2][1].set_opacity(0)
        ta_words[1].set_color_by_tex("not", RED)

        up_words = VGroup(
            OldTexText("Test", " accuracy"),
            OldTexText("determine", "s"),
            OldTexText("how", " your chances"),
            OldTexText("are", " \\emph{updated}"),
        )
        up_words[3][1].set_color(BLUE)
        up_words[3].shift(SMALL_BUFF * UP)
        up_words[0].shift(SMALL_BUFF * DOWN)

        for group in ta_words, up_words:
            group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            group.scale(1.5)
            group.to_edge(LEFT)
            group.set_stroke(BLACK, 3, background=True)

        self.play(*result_change_anims)
        self.play(
            FadeOut(words[0][0]),
            FadeOut(words[1][0]),
            FadeOut(words[2]),
            ReplacementTransform(words[0][1], ta_words[0][0]),
            ReplacementTransform(words[1][1], ta_words[0][1]),
            LaggedStartMap(FadeIn, ta_words[1:]),
        )
        self.add(ta_words)
        self.wait()

        self.play(
            FadeOut(prior_probs, 0.25 * UP),
            FadeOut(probs, 0.25 * UP),
            FadeIn(prior_odds, 0.25 * UP),
            FadeIn(post_odds, 0.25 * UP),
        )

        self.play(
            ReplacementTransform(ta_words[0], up_words[0]),
            ReplacementTransform(ta_words[2], up_words[1]),
            FadeIn(up_words[2][0], scale=2),
            # CHANGE: OldTexText("\\,", ...) no longer leaves the empty part as a submobject; the last part is taken
            ReplacementTransform(ta_words[3][-1], up_words[2][1]),
            FadeOut(ta_words[1], scale=0.5),
        )
        self.play(
            Write(up_words[3]),
            LaggedStartMap(DrawBorderThenFill, arrows),
        )
        self.wait()
