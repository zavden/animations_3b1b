# ==============================================================================
# Scene:      Simulation
# Source:     videos/_2026/monthly_mindbenders/ladybug.py (lines 102-168)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Simulation.py Simulation -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2026/monthly_mindbenders/ladybug.svg
#   - _lib/assets/svg_images/ladybug.svg
#
# Notes:
#   ladybug.svg is a placeholder SVG (a ladybug seen from above: head, shell ring, center line, spots, legs and antennae) generated with _lib/assets/generated/2026/monthly_mindbenders/make_ladybug_svg.py and copied to _lib/assets/svg_images/ because the code calls SVGMobject('ladybug'). It is drawn in gray over a red dot, as in the original.
# ==============================================================================

from manim_imports_ext import *

class Ladybug(InteractiveScene):
    # random_seed = 3 # ends with 6
    # random_seed = 6 # ends with 3
    # random_seed = 7 # ends with 10
    # random_seed = 8 # ends with 4
    # random_seed = 9 # ends with 9
    # random_seed = 10 # ends with 2
    # random_seed = 11 # ends with 11
    # random_seed = 12 # ends with 7
    # random_seed = 14 # ends with 1
    # random_seed = 15 # ends with 5
    # random_seed = 18 # ends with 2
    random_seed = 19  # ends with 3

    def construct(self):
        # Add clock
        clock = self.get_clock()
        clock_points = [tick.get_start() for tick in clock.ticks]
        clock_anim = cycle_animation(ClockPassesTime(clock, 12 * 60, 12))
        self.add(clock_anim)

        # Lady bug lands on it
        ladybug = SVGMobject("ladybug")
        ladybug.set_height(0.7)
        ladybug.set_color(GREY_A)
        ladybug.set_shading(0.5, 0.5, 0)
        circle = Dot(fill_color=RED_E, radius=0.36 * ladybug.get_height())
        circle.move_to(ladybug, DOWN)
        bug = Group(circle, Point(), ladybug)
        bug.move_to(clock.ticks[0].get_start())

        path = VMobject()
        path.start_new_path(ORIGIN)
        for n in range(5):
            step = rotate_vector(RIGHT, PI * random.random())
            path.add_line_to(path.get_end() + step)
        path.make_smooth()
        path.put_start_and_end_on(7 * LEFT, clock_points[0])

        self.play(MoveAlongPath(bug, path, run_time=3))
        self.play(clock.numbers[0].animate.set_color(RED))

        bug.shift(UP)

        # Run simulation
        curr_number = 0
        covered_numbers = {0}
        while len(covered_numbers) < 12:
            step = random.choice([+1, -1])
            next_number = curr_number + step
            path_arc = -step * TAU / 12
            arrow = Arrow(
                1.2 * clock_points[curr_number],
                1.2 * clock_points[next_number],
                buff=0,
                fill_color=YELLOW,
                path_arc=path_arc,
                thickness=5,
            )

            end_color = RED
            if len(covered_numbers) == 11 and next_number not in covered_numbers:
                end_color = TEAL
            self.play(
                VFadeInThenOut(arrow),
                bug.animate.move_to(clock_points[next_number]).set_anim_args(path_arc=path_arc, time_span=(0, 0.5)),
                clock.numbers[next_number].animate.set_color(end_color)
            )
            curr_number = next_number
            covered_numbers.add(curr_number)

    def get_clock(self, radius=2):
        # Add clock (Todo, add these modifications as options to the Clock class)
        clock = Clock()
        clock.set_height(2 * radius)
        for line in [clock.hour_hand, clock.minute_hand, *clock.ticks]:
            line.scale(0.75, about_point=line.get_start())

        numbers = VGroup(Integer(n) for n in [12, *range(1, 12)])
        for number, theta in zip(numbers, np.arange(0, TAU, TAU / 12)):
            number.move_to(0.75 * radius * rotate_vector(UP, -theta))

        clock.numbers = numbers
        clock.add(numbers)
        return clock


class Simulation(Ladybug):
    def construct(self):
        random.seed(8)

        num_trials = 1000
        trialTracker = ValueTracker(0)
        trialCounter = Integer(1, color=YELLOW, font_size=35)
        trialCounter.add_updater(lambda c: c.set_value(trialTracker.get_value()))
        trialLabel = VGroup(
            Text("Trial: ", color=WHITE, font_size=35),
            trialCounter
        )
        results = [int(0) for _ in range(11)]

        def get_hist():
            proportions = [x / (max(trialTracker.get_value(), 1)) for x in results]
            hist = BarChart(
                values=proportions,
                n_ticks=0,
                bar_names=[str(x) for x in list(range(1, 12))],
                bar_colors=[BLUE]
            )
            hist.y_axis_labels.set_opacity(0)
            yAxisLabel = Tex(r"\%\ \text{occurrence}", font_size=30).next_to(hist.y_axis, LEFT)
            hist.add(yAxisLabel)

            hist.center().scale(0.6).to_edge(DOWN, buff=1.5).shift(LEFT * 0.3)
            return hist
        hist = get_hist()
        self.add(hist, trialLabel)
        trialLabel.add_updater(lambda label: label.arrange(buff=0.3).next_to(hist.x_axis, DOWN, buff=0.6))

        clock = self.get_clock()
        clock_points = [tick.get_start() for tick in clock.ticks]
        ladybug = SVGMobject("ladybug")
        ladybug.set_height(0.7)
        ladybug.set_color(GREY_A)
        ladybug.set_shading(0.5, 0.5, 0)
        ladybug.set_z_index(100)
        circle = Dot(fill_color=RED_E, radius=0.36 * ladybug.get_height())
        circle.move_to(ladybug, DOWN)
        bug = Group(circle, Point(), ladybug)
        self.add(Group(clock, bug).scale(0.6).to_edge(UP, buff=1).set_opacity(0))

        for trial in range(num_trials):
            trialTracker.increment_value(1)
            final_number = None
            covered_numbers = {0}
            curr_number = 0
            while len(covered_numbers) < 12:
                if random.random() > 0.5:
                    curr_number = (curr_number + 1) % 12
                else:
                    curr_number = (curr_number - 1) % 12
                covered_numbers.add(curr_number)
            final_number = curr_number
            if trial >= 2:
                bug.move_to(clock.ticks[final_number].get_start())
                clock.numbers.set_color(RED)
                clock.numbers[final_number].set_color(TEAL)
                Group(clock, bug).set_opacity(1)
                clock[0].set_fill(opacity=0)

            results[final_number - 1] += 1
            new_hist = get_hist()
            self.play(hist.animate.become(new_hist))
        self.wait(3)
