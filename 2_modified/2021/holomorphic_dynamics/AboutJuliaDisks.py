# ==============================================================================
# Scene:      AboutJuliaDisks
# Source:     videos/_2021/holomorphic_dynamics.py (lines 3113-3181)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AboutJuliaDisks.py AboutJuliaDisks -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - VFadeIn/VFadeOut: suspend_updating -> suspend_mobject_updating (kwarg name in this manimgl)
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


class AboutJuliaDisks(AboutFatouDisks):
    def construct(self):
        words1 = Text("Any tiny disk around a Julia set point...")
        words1.to_edge(UP)
        disks, arrows = self.get_disks_and_arrow()
        group = VGroup(disks, arrows)
        group.next_to(words1, DOWN)
        arrows[-1].add(disks[-1].copy().scale(5).next_to(arrows[-1], RIGHT))

        words2 = Text("...eventually hits every point in the plane,")
        words2.next_to(disks, DOWN, aligned_edge=RIGHT)
        words2.get_part_by_text("every point in the plane").set_color(BLUE)

        words3 = Text("with at most two exceptions.")
        words3.next_to(words2, DOWN, MED_LARGE_BUFF, aligned_edge=RIGHT)

        words4 = OldTexText(
            "``Stuff goes everywhere'' principle of Julia sets",
            font_size=60
        )
        words4.to_edge(DOWN, LARGE_BUFF)

        VGroup(words1, words2, words3, words4).set_stroke(BLACK, 5, background=True)

        plane = ComplexPlane((-100, 100), (-50, 50))
        plane.scale(2)
        plane.add_coordinate_labels()
        plane.add(BackgroundRectangle(plane, opacity=0.25))
        plane.set_stroke(background=True)
        plane.add_updater(lambda m, dt: m.scale(1 - 0.15 * dt))

        self.add(words1)
        self.play_disk_progression(disks, arrows)
        self.add(plane, *self.mobjects)
        self.play(
            FadeIn(arrows[-1]),
            FadeIn(words2, run_time=2, lag_ratio=0.1),
            # CHANGE: the kwarg is called suspend_mobject_updating in this manimgl
            VFadeIn(plane, suspend_mobject_updating=False),
        )
        self.wait()
        self.play(
            FadeIn(words3, run_time=2, lag_ratio=0.1),
        )
        self.wait(2)
        self.play(Write(words4))
        self.wait(6)
        # CHANGE: the kwarg is called suspend_mobject_updating in this manimgl
        self.play(VFadeOut(plane, suspend_mobject_updating=False))

    def get_disks(self):
        c = -0.18 + 0.77j
        z = -0.491 - 0.106j
        plane = ComplexPlane()
        disk = Circle(radius=0.1, **self.disk_style)
        disk.move_to(plane.n2p(z))
        disk.insert_n_curves(200)

        disks = VGroup(disk)
        for n in range(5):
            new_disk = disks[-1].copy()
            new_disk.apply_complex_function(lambda z: z**2 + c)
            new_disk.make_smooth(approx=True)
            disks.add(new_disk)

        for disk in disks:
            disk.center()

        disks.set_height(1)

        return disks
