# ==============================================================================
# Scene:      ODEvsPDEinFrames
# Source:     videos/_2019/diffyq/part1/staging.py (lines 1916-2034)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl ODEvsPDEinFrames.py ODEvsPDEinFrames -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

def get_ode():
    tex_config = {
        "tex_to_color_map": {
            "{\\theta}": BLUE,
            "{\\dot\\theta}": RED,
            "{\\ddot\\theta}": YELLOW,
            "{t}": WHITE,
            "{\\mu}": WHITE,
        }
    }
    ode = OldTex(
        "{\\ddot\\theta}({t})", "=",
        "-{\\mu} {\\dot\\theta}({t})",
        "-{g \\over L} \\sin\\big({\\theta}({t})\\big)",
        **tex_config,
    )
    return ode



# ----- From _2019/diffyq/part1/staging.py -----

class ODEvsPDEinFrames(Scene):
    CONFIG = {
        "camera_config": {"background_color": GREY_E}
    }

    def construct(self):
        frames = VGroup(*[
            ScreenRectangle(
                height=3.5,
                fill_opacity=1,
                fill_color=BLACK,
                stroke_width=0,
            )
            for x in range(2)
        ])
        frames.arrange(RIGHT, buff=LARGE_BUFF)
        frames.shift(0.5 * DOWN)

        animated_frames = VGroup(*[
            AnimatedBoundary(
                frame,
                cycle_rate=0.2,
                max_stroke_width=1,
            )
            for frame in frames
        ])

        titles = VGroup(
            # OldTexText("ODEs"),
            # OldTexText("PDEs"),
            OldTexText("Ordinary", "Differential", "Equations"),
            OldTexText("Partial", "Differential", "Equations"),
        )
        for title, frame in zip(titles, frames):
            title.arrange(
                DOWN,
                buff=MED_SMALL_BUFF,
                aligned_edge=LEFT
            )
            title.next_to(frame, UP, MED_LARGE_BUFF)
            title.initials = VGroup(*[
                part[0] for part in title
            ])
        titles[0][1].shift(0.05 * UP)

        # ODE content
        ode = get_ode()
        ode.set_width(frames[0].get_width() - MED_LARGE_BUFF)
        ode.next_to(frames[0].get_top(), DOWN)
        ts = ode.get_parts_by_tex("{t}")
        one_input = OldTexText("One input")
        one_input.next_to(frames[0].get_bottom(), UP)
        o_arrows = VGroup(*[
            Arrow(
                one_input.get_top(),
                t.get_bottom(),
                buff=0.2,
                color=WHITE,
                max_tip_length_to_length_ratio=0.075,
                path_arc=pa
            )
            for t, pa in zip(ts, [-0.7, 0, 0.7])
        ])
        o_arrows.set_stroke(width=3)
        frames[0].add(ode, one_input, o_arrows)

        # PDE content
        pde = OldTex(
            """
            \\frac{\\partial T}{\\partial t}
            {(x, y, t)} =
            \\frac{\\partial^2 T}{\\partial x^2}
            {(x, y, t)} +
            \\frac{\\partial^2 T}{\\partial y^2}
            {(x, y, t)}
            """,
            tex_to_color_map={"{(x, y, t)}": WHITE}
        )
        pde.set_width(frames[1].get_width() - MED_LARGE_BUFF)
        pde.next_to(frames[1].get_top(), DOWN)
        inputs = pde.get_parts_by_tex("{(x, y, t)}")
        multi_input = OldTexText("Multiple inputs")
        multi_input.next_to(frames[1].get_bottom(), UP)
        p_arrows = VGroup(*[
            Arrow(
                multi_input.get_top(),
                mob.get_bottom(),
                buff=0.2,
                color=WHITE,
                max_tip_length_to_length_ratio=0.075,
                path_arc=pa
            )
            for mob, pa in zip(inputs, [-0.7, 0, 0.7])
        ])
        p_arrows.set_stroke(width=3)
        frames[1].add(pde, multi_input, p_arrows)

        self.add(
            frames[0],
            animated_frames[0],
            titles[0]
        )
        self.play(
            Write(one_input),
            ShowCreation(o_arrows, lag_ratio=0.5)
        )
        self.wait(2)
        self.play(titles[0].initials.set_color, BLUE)
        self.wait(7)

        # Transition
        self.play(
            TransformFromCopy(*titles),
            TransformFromCopy(*frames),
        )
        self.play(VFadeIn(animated_frames[1]))
        self.wait()
        self.play(titles[1].initials.set_color, YELLOW)
        self.wait(30)
