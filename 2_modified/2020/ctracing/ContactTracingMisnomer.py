# ==============================================================================
# Scene:      ContactTracingMisnomer
# Source:     videos/_2020/ctracing.py (lines 200-234)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ContactTracingMisnomer.py ContactTracingMisnomer -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Write only accepts VMobject: the self.mobjects that are not are filtered out (VGroup fails with other types)
# ==============================================================================

from manim_imports_ext import *

class ContactTracingMisnomer(Scene):
    def construct(self):
        # Word play
        words = OldTexText("Contact ", "Tracing")
        words.scale(2)
        rects = VGroup(*[
            SurroundingRectangle(word, buff=0.2)
            for word in words
        ])
        expl1 = OldTexText("Doesn't ``trace'' you...")
        expl2 = OldTexText("...or your contacts")
        expls = VGroup(expl1, expl2)
        colors = [RED, BLUE]

        self.add(words)
        for vect, rect, expl, color in zip([UP, DOWN], reversed(rects), expls, colors):
            arrow = Vector(-vect)
            arrow.next_to(rect, vect, SMALL_BUFF)
            expl.next_to(arrow, vect, SMALL_BUFF)
            rect.set_color(color)
            arrow.set_color(color)
            expl.set_color(color)

            self.play(
                FadeIn(expl, -vect),
                GrowArrow(arrow),
                ShowCreation(rect),
            )
            self.wait()

        self.play(Write(
            # CHANGE: Write only accepts VMobject; the self.mobjects that are not (images, etc.) are filtered out
            VGroup(*(m for m in self.mobjects if isinstance(m, VMobject))),
            rate_func=lambda t: smooth(1 - t),
            run_time=3,
        ))
