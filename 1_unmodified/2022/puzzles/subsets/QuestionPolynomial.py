# ==============================================================================
# Scene:      QuestionPolynomial
# Source:     videos/_2022/puzzles/subsets.py (lines 1669-1741)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuestionPolynomial.py QuestionPolynomial -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuestionPolynomial(InteractiveScene):
    def construct(self):
        # Start
        n_range = list(range(1, 6))
        poly = Tex(
            "p(x) = " + "".join(f"(1 + x^{{{n}}})" for n in n_range),
            tex_to_color_map=dict(zip(
                (f"{{{n}}}" for n in n_range),
                color_gradient([BLUE_B, BLUE_D], 5)
            )),
            isolate=["x"],
        )
        poly.move_to([-0.81438428, 2.25048456, 0.])
        self.add(poly)

        # Questions
        questions = VGroup(
            Text("Where does this\ncome from?", font_size=36),
            Text("What do polynomials\nhave to do with anything?", font_size=36),
            OldTexText("What is $x$?", font_size=60, color=TEAL).set_backstroke(width=8),
        )
        pis = VGroup(*(Randolph(color=c, height=2.5) for c in [BLUE_C, BLUE_E, BLUE_D]))
        pis.arrange(RIGHT, buff=LARGE_BUFF)
        pis.to_corner(DL)

        anims = []
        for pi, mode, question in zip(pis, ["maybe", "confused", "pleading"], questions):
            anim = PiCreatureSays(
                pi, question,
                target_mode=mode, look_at=poly,
                bubble_config=dict(width=4, height=2.5),
            )
            pi.set_opacity(0)
            anims.append(anim)
            if pi is pis[1]:
                anims.append(Animation(Mobject()))
        self.play(LaggedStart(*anims, lag_ratio=0.9))

        # Highlight xs
        xs = poly.select_parts("x")
        rects = VGroup(*(SurroundingRectangle(x, buff=0.05).round_corners() for x in xs))
        rects.set_stroke(TEAL, 2)

        self.play(LaggedStartMap(ShowCreationThenFadeOut, rects, lag_ratio=0.1))
        self.wait()

        # x is just a symbol
        words = OldTexText("$x$", " is just a symbol")
        words.to_edge(UP)
        words[0].set_color(TEAL)

        self.play(
            LaggedStartMap(
                RemovePiCreatureBubble, pis,
                look_at=poly,
            ),
            TransformFromCopy(xs[0], words[0]),
            Write(words[1], time_span=(1, 2))
        )
        self.wait()

        # Expansion
        expansion = Tex("1+x^{1}+x^{2}+2 x^{3}+2 x^{4}+3 x^{5}+3 x^{6}+3 x^{7}+3 x^{8}+3 x^{9}+3 x^{10}+2 x^{11}+2 x^{12}+x^{13}+x^{14}+x^{15}")
        expansion.set_width(FRAME_WIDTH - 1)
        expansion.next_to(poly, DOWN, MED_LARGE_BUFF)
        expansion.set_x(0)

        self.play(
            TransformMatchingShapes(poly[5:].copy(), expansion, run_time=3, lag_ratio=0.01),
            LaggedStart(*(pi.change("pondering", expansion) for pi in pis))
        )
        self.play(LaggedStartMap(Blink, pis))
        self.wait()
