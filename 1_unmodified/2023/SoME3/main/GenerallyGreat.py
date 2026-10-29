# ==============================================================================
# Scene:      GenerallyGreat
# Source:     videos/_2023/SoME3/main.py (lines 290-368)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GenerallyGreat.py GenerallyGreat -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GenerallyGreat(InteractiveScene):
    def construct(self):
        # Set up audience types
        audience_names = [
            "a child",
            "a middle school student",
            "a high school student",
            "an undergraduate in math",
            "an undergraduate in engineering",
            "a college student who doesn't like math",
            "a math Ph.D. student",
            "a professional in a technical field",
            "a person who hasn't thought about math for a decade",
        ]
        audiences = VGroup(*(
            Text(f"for {name}")
            for name in audience_names
        ))
        audiences.scale(0.9)
        audiences.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        audiences.to_corner(UR)
        dots = Tex(R"\vdots")
        dots.next_to(audiences, DOWN)
        dots.shift(3 * LEFT + 0.25 * DOWN)

        self.add(audiences, dots)

        # Quality
        GREEN_YELLOW = interpolate_color(GREEN, YELLOW, 0.25)
        qualities1 = VGroup(*map(Text, ["Good"] * len(audiences))).set_color(GREEN)
        qualities2 = VGroup(*map(Text, ["Pretty good"] * len(audiences))).set_color(YELLOW)
        qualities3 = VGroup(
            Text("Terrible").set_color(RED),
            Text("Bad").set_color(RED),
            Text("Okay").set_color(YELLOW),
            Text("Good").set_color(GREEN_YELLOW),
            Text("Great").set_color(GREEN),
            Text("Bad").set_color(RED),
            Text("Okay").set_color(YELLOW),
            Text("Good").set_color(GREEN_YELLOW),
            Text("Bad").set_color(RED),
        )

        for group in [qualities1, qualities2, qualities3]:
            group.scale(0.9)
            for quality, audience in zip(group, audiences):
                quality.next_to(audience, LEFT, buff=0.25)

        annotations = VGroup(
            Text("Not\nPossible", font_size=90, fill_color=RED, alignment="LEFT"),
            Text("Rare, but\nPossible", font_size=90, fill_color=YELLOW, alignment="LEFT"),
            Text("", font_size=90, fill_color=GREEN, alignment="LEFT"),
        )
        for annotation in annotations:
            annotation.to_corner(UR)

        rect = SurroundingRectangle(VGroup(qualities3[4], audiences[4]))
        rect.set_stroke(GREEN, 2)

        self.play(
            LaggedStartMap(FadeIn, qualities1),
            FadeIn(annotations[0])
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, qualities1, shift=LEFT),
            LaggedStartMap(FadeIn, qualities2, shift=LEFT),
            FadeOut(annotations[0], LEFT),
            FadeIn(annotations[1], LEFT),
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, qualities2, shift=LEFT),
            LaggedStartMap(FadeIn, qualities3, shift=LEFT),
            FadeIn(rect),
            FadeOut(annotations[1], LEFT),
            FadeIn(annotations[2], LEFT),
        )
        self.wait()
