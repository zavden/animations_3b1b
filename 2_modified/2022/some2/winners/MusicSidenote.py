# ==============================================================================
# Scene:      MusicSidenote
# Source:     videos/_2022/some2/winners.py (lines 1149-1200)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MusicSidenote.py MusicSidenote -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - quarter-note.svg (placeholder quarter note, svg_images/; make_some2_assets.py)
# ==============================================================================

from manim_imports_ext import *

class MusicSidenote(InteractiveScene):
    def construct(self):
        # Randy
        randy = Randolph(height=2)
        randy.to_corner(DL)

        self.add(randy)

        # Add notes
        notes = SVGMobject("quarter-note").replicate(24)
        notes.arrange(RIGHT, buff=LARGE_BUFF)
        notes.set_width(FRAME_WIDTH + 5)
        notes.set_fill(GREY_B, 1)
        notes.set_stroke(WHITE, 0)
        for note in notes:
            note.shift(random.randint(0, 6) * 0.2 * UP)
        notes.center().to_edge(UP).to_edge(LEFT)

        self.play(
            LaggedStart(*(
                FadeIn(note, 0.2 * LEFT)
                for note in notes
            ), lag_ratio=0.3),
            randy.change("thinking", notes),
        )
        self.play(
            notes.animate.to_edge(RIGHT).set_anim_args(run_time=3),
            randy.change("tease"),
        )

        # Technical explanation
        outline = ScreenRectangle().set_height(4)
        outline.set_stroke(WHITE, 2)
        outline.next_to(randy, RIGHT, buff=1.0)
        outline.to_edge(DOWN, buff=1.0)

        self.play(
            ShowCreation(outline),
            randy.change("confused"),
        )
        self.play(Blink(randy))
        self.wait(2)

        self.play(
            LaggedStart(*(
                note.copy().animate.set_opacity(0).scale(0.5).move_to(randy.get_top())
                for note in notes
            ), lag_ratio=0.2),
            randy.change("concentrating")
        )
        self.play(Blink(randy))
        self.wait()
