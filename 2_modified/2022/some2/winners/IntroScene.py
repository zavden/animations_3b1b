# ==============================================================================
# Scene:      IntroScene
# Source:     videos/_2022/some2/winners.py (lines 102-177)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroScene.py IntroScene -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The logo in _lib/custom/logo.py passes sheen=0.0 to Circle (an argument manimgl no longer has): add_pupil is redefined without sheen in a local subclass
# ==============================================================================

from manim_imports_ext import *


# CHANGE: Logo (_lib/custom/logo.py) passes sheen=0.0 to Circle and manimgl no longer has that argument; add_pupil is redefined without sheen
class Logo(Logo):
    def add_pupil(self):
        self.pupil = Circle(
            radius=self.pupil_radius,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0,
            stroke_color=BLACK,
        )
        self.pupil.rotate(90 * DEGREES)
        self.add(self.pupil)


class IntroScene(InteractiveScene):
    def construct(self):
        # Intro
        logos = Group(ImageMobject("Leios"), Logo())
        for logo in logos:
            logo.set_height(1.5)
        logos.arrange(DOWN, buff=LARGE_BUFF)
        logos.to_edge(LEFT)
        title = Text("Summer of Math\nExposition", font_size=96)
        title.move_to(midpoint(logos.get_right(), RIGHT_SIDE))

        self.add(title)
        self.play(LaggedStart(
            FadeIn(logos[0], LEFT),
            Write(logos[1], run_time=1, lag_ratio=0.01, stroke_width=0.1, stroke_color=BLACK),
            lag_ratio=0.3,
        ))
        self.wait()

        # Compress name
        words = ["Summer", "of", "Math", "Exposition"]
        inits = VGroup()
        to_fade = VGroup()
        for word in words:
            part = title.select_part(word)
            inits.add(part[0])
            to_fade.add(*part[1:])

        inits.generate_target()
        inits.target.arrange(RIGHT, aligned_edge=DOWN, buff=SMALL_BUFF)
        inits.target.set_height(0.8)
        inits.target.set_stroke(WHITE, 1)
        inits.target.center().to_edge(UP)

        self.play(
            FadeOut(to_fade, lag_ratio=0.1, shift=UP, run_time=1.5),
            MoveToTarget(inits, time_span=(0.25, 1.5)),
            FadeOut(logos, LEFT)
        )

        # Add 2
        two = Text("2")
        two.match_height(inits)
        two.set_color(YELLOW)
        inits.generate_target()
        inits.target.shift(0.25 * LEFT)
        two.next_to(inits.target, RIGHT, buff=0.2, aligned_edge=DOWN)

        self.play(
            LaggedStart(*(
                FadeTransform(init.copy(), two)
                for init in inits
            ), lag_ratio=0.1),
            MoveToTarget(inits),
        )
        inits.add(two)
        self.wait()

        # View count
        count = VGroup(
            Integer(7000000, edge_to_fix=RIGHT),
            Text("collective views"),
        )
        count.arrange(RIGHT, aligned_edge=UP)
        count.set_height(0.6)
        count.to_corner(UR)

        self.play(
            inits.animate.set_height(0.6).to_corner(UL),
            FadeIn(count[1]),
            CountInFrom(count[0], 0, run_time=3),
        )
        self.add(count)
        count[0].edge_to_fix = LEFT
        count[0].add_updater(lambda m, dt: m.increment_value(int(dt * 1000)))
        self.wait(5)
