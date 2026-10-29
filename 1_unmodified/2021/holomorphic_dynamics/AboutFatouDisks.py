# ==============================================================================
# Scene:      AboutFatouDisks
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2992-3046)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AboutFatouDisks.py AboutFatouDisks -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AboutFatouDisks(Scene):
    disk_style = {
        "fill_color": YELLOW,
        "fill_opacity": 0.5,
        "stroke_color": YELLOW,
        "stroke_width": 1,
    }

    def construct(self):
        words = Text("(Small enough) disks around points in the Fatou set...")
        words.to_edge(UP)

        disks, arrows = self.get_disks_and_arrow()
        arrows[-1].add(OldTex("\\dots").next_to(arrows[-1], RIGHT))
        group = VGroup(disks, arrows)
        group.next_to(words, DOWN)

        shrink_words = Text("...eventually shrink to 0")
        shrink_words.next_to(group, DOWN, aligned_edge=RIGHT)

        self.add(words)
        self.play_disk_progression(disks, arrows)
        self.play(
            FadeIn(arrows[-1]),
            Write(shrink_words, run_time=2)
        )
        self.wait()

    def play_disk_progression(self, disks, arrows):
        self.add(disks[0])
        for d1, d2, arrow in zip(disks, disks[1:], arrows):
            self.play(
                TransformFromCopy(d1.copy().fade(1), d2),
                FadeIn(arrow),
            )

    def get_disks(self):
        radii = [
            *np.linspace(0.5, 1, 3),
            *np.linspace(1, 0, 7)**2 + 0.05,
        ]
        disks = VGroup(*(Circle(radius=r, **self.disk_style) for r in radii))

        for disk in disks:
            disk.add(Dot(disk.get_center(), radius=0.01))

        return disks

    def get_disks_and_arrow(self):
        disks = self.get_disks()
        arrows = OldTex("\\rightarrow").replicate(len(disks))
        group = VGroup(*it.chain(*zip(disks, arrows)))
        group.arrange(RIGHT)
        group.set_width(FRAME_WIDTH - 2)
        return disks, arrows
