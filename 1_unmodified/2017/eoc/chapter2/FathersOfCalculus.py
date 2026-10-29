# ==============================================================================
# Scene:      FathersOfCalculus
# Source:     videos/_2017/eoc/chapter2.py (lines 163-210)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FathersOfCalculus.py FathersOfCalculus -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FathersOfCalculus(Scene):
    CONFIG = {
        "names" : [
            "Barrow",
            "Newton", 
            "Leibniz",
            "Cauchy",
            "Weierstrass",
        ],
        "picture_height" : 2.5,
    }
    def construct(self):
        title = OldTexText("(A few) Fathers of Calculus")
        title.to_edge(UP)
        self.add(title)

        men = Mobject()
        for name in self.names:
            image = ImageMobject(name, invert = False)
            image.set_height(self.picture_height)
            title = OldTexText(name)
            title.scale(0.8)
            title.next_to(image, DOWN)
            image.add(title)
            men.add(image)
        men.arrange(RIGHT, aligned_edge = UP)
        men.shift(DOWN)

        discover_brace = Brace(Mobject(*men[:3]), UP)
        discover = discover_brace.get_text("Discovered it")
        VGroup(discover_brace, discover).set_color(BLUE)
        rigor_brace = Brace(Mobject(*men[3:]), UP)
        rigor = rigor_brace.get_text("Made it rigorous")
        rigor.shift(0.1*DOWN)
        VGroup(rigor_brace, rigor).set_color(YELLOW)


        for man in men:
            self.play(FadeIn(man))
        self.play(
            GrowFromCenter(discover_brace),
            Write(discover, run_time = 1)
        )
        self.play(
            GrowFromCenter(rigor_brace),
            Write(rigor, run_time = 1)
        )
        self.wait()
