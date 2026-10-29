# ==============================================================================
# Scene:      ViralSpreadModelWithShuffling
# Source:     videos/_2020/covid.py (lines 1309-1339)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ViralSpreadModelWithShuffling.py ViralSpreadModelWithShuffling -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SICKLY_GREEN = "#9BBD37"


class ViralSpreadModel(Scene):
    CONFIG = {
        "num_neighbors": 5,
        "infection_probability": 0.3,
        "random_seed": 1,
    }

    def construct(self):
        # Init population
        randys = self.get_randys()
        self.add(*randys)

        # Show the sicko
        self.show_patient0(randys)

        # Repeatedly spread
        for x in range(20):
            self.spread_infection(randys)

    def get_randys(self):
        randys = VGroup(*[
            Randolph()
            for x in range(150)
        ])
        for randy in randys:
            randy.set_height(0.5)
        randys.arrange_in_grid(10, 15, buff=0.5)
        randys.set_height(FRAME_HEIGHT - 1)

        for i in range(0, 10, 2):
            randys[i * 15:(i + 1) * 15].shift(0.25 * RIGHT)
        for randy in randys:
            randy.shift(0.2 * random.random() * RIGHT)
            randy.shift(0.2 * random.random() * UP)
            randy.infected = False
        randys.center()
        return randys

    def show_patient0(self, randys):
        patient0 = random.choice(randys)
        patient0.infected = True

        circle = Circle()
        circle.set_stroke(SICKLY_GREEN)
        circle.replace(patient0)
        circle.scale(1.5)
        self.play(
            patient0.change, "sick",
            patient0.set_color, SICKLY_GREEN,
            ShowCreationThenFadeOut(circle),
        )

    def spread_infection(self, randys):
        E = self.num_neighbors
        inf_p = self.infection_probability

        cough_anims = []
        new_infection_anims = []

        for randy in randys:
            if randy.infected:
                cough_anims.append(Flash(
                    randy,
                    color=SICKLY_GREEN,
                    num_lines=16,
                    line_stroke_width=1,
                    flash_radius=0.5,
                    line_length=0.1,
                ))
        random.shuffle(cough_anims)
        self.play(LaggedStart(
            *cough_anims,
            run_time=1,
            lag_ratio=1 / len(cough_anims),
        ))

        newly_infected = []
        for randy in randys:
            if randy.infected:
                distances = [
                    get_norm(r2.get_center() - randy.get_center())
                    for r2 in randys
                ]
                for i in np.argsort(distances)[1:E + 1]:
                    r2 = randys[i]
                    if random.random() < inf_p and not r2.infected and r2 not in newly_infected:
                        newly_infected.append(r2)
                        r2.generate_target()
                        r2.target.change("sick")
                        r2.target.set_color(SICKLY_GREEN)
                        new_infection_anims.append(MoveToTarget(r2))
        random.shuffle(new_infection_anims)
        self.play(LaggedStart(*new_infection_anims, run_time=1))

        for randy in newly_infected:
            randy.infected = True


class ViralSpreadModelWithShuffling(ViralSpreadModel):
    def construct(self):
        # Init population
        randys = self.get_randys()
        self.add(*randys)

        # Show the sicko
        self.show_patient0(randys)

        # Repeatedly spread
        for x in range(15):
            self.spread_infection(randys)
            self.shuffle_randys(randys)

    def shuffle_randys(self, randys):
        indices = list(range(len(randys)))
        np.random.shuffle(indices)

        anims = []
        for i, randy in zip(indices, randys):
            randy.generate_target()
            randy.target.move_to(randys[i])
            anims.append(MoveToTarget(
                randy, path_arc=30 * DEGREES,
            ))

        self.play(LaggedStart(
            *anims,
            lag_ratio=1 / len(randys),
            run_time=3
        ))
