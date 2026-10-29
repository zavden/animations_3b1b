# ==============================================================================
# Scene:      CompoundInterestPopulationAndEpidemic
# Source:     videos/_2021/matrix_exp.py (lines 3164-3231)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompoundInterestPopulationAndEpidemic.py CompoundInterestPopulationAndEpidemic -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CompoundInterestPopulationAndEpidemic(Scene):
    def construct(self):
        N = 16000
        points = 2 * np.random.random((N, 3)) - 1
        points[:, 2] = 0
        points = points[[get_norm(p) < 1 for p in points]]
        points *= 2 * FRAME_WIDTH
        points = np.array(list(sorted(
            points, key=lambda p: get_norm(p) + 0.5 * random.random()
        )))

        dollar = OldTex("\\$")
        dollar.set_fill(GREEN)
        person = SVGMobject("person")
        person.set_fill(GREY_B, 1)
        virus = SVGMobject("virus")
        virus.set_fill([RED, RED_D])
        virus.remove(virus[1:])
        virus[0].set_points(virus[0].get_subpaths()[0])
        templates = [dollar, person, virus]
        mob_height = 0.25

        for mob in templates:
            mob.set_stroke(BLACK, 1, background=True)
            mob.set_height(mob_height)

        dollars, people, viruses = groups = [
            VGroup(*(mob.copy().move_to(point) for point in points))
            for mob in templates
        ]

        dollars.set_submobjects(dollars[:20])
        people.set_submobjects(people[:500])

        start_time = self.time

        def get_n():
            time = self.time - start_time
            return int(math.exp(0.75 * time))

        def update_group(group):
            group.set_opacity(0)
            group[:get_n()].set_opacity(0.9)

        def update_height(group, alpha):
            for mob in group:
                mob.set_height(max(alpha * mob_height, 1e-4))

        for group in groups:
            group.add_updater(update_group)

        frame = self.camera.frame
        frame.set_height(2)
        frame.add_updater(lambda m, dt: m.set_height(m.get_height() * (1 + 0.2 * dt)))
        self.add(frame)

        self.add(dollars)
        self.wait(3)
        self.play(
            UpdateFromAlphaFunc(people, update_height),
            UpdateFromAlphaFunc(dollars, update_height, rate_func=lambda t: smooth(1 - t), remover=True),
        )
        self.wait(4)
        self.play(
            UpdateFromAlphaFunc(viruses, update_height),
            UpdateFromAlphaFunc(people, update_height, rate_func=lambda t: smooth(1 - t), remover=True),
        )
        self.wait(4)
