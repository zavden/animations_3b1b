# ==============================================================================
# Scene:      WideSpreadTesting
# Source:     videos/_2020/sir.py (lines 2962-3047)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WideSpreadTesting.py WideSpreadTesting -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - In float32 the person ends up exactly on the wall (distance 0) and 1/0 gives inf/NaN (the people disappear); the distance is bounded to 1e-6
# ==============================================================================

from manim_imports_ext import *

COLOR_MAP = {
    "S": BLUE,
    "I": RED,
    "R": GREY_D,
}


def update_time(mob, dt):
    mob.time += dt


class Person(VGroup):
    CONFIG = {
        "status": "S",  # S, I or R
        "height": 0.2,
        "color_map": COLOR_MAP,
        "infection_ring_style": {
            "stroke_color": RED,
            "stroke_opacity": 0.8,
            "stroke_width": 0,
        },
        "infection_radius": 0.5,
        "infection_animation_period": 2,
        "symptomatic": False,
        "p_symptomatic_on_infection": 1,
        "max_speed": 1,
        "dl_bound": [-FRAME_WIDTH / 2, -FRAME_HEIGHT / 2],
        "ur_bound": [FRAME_WIDTH / 2, FRAME_HEIGHT / 2],
        "gravity_well": None,
        "gravity_strength": 1,
        "wall_buffer": 1,
        "wander_step_size": 1,
        "wander_step_duration": 1,
        "social_distance_factor": 0,
        "social_distance_color_threshold": 2,
        "n_repulsion_points": 10,
        "social_distance_color": YELLOW,
        "max_social_distance_stroke_width": 5,
        "asymptomatic_color": YELLOW,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.time = 0
        self.last_step_change = -1
        self.change_anims = []
        self.velocity = np.zeros(3)
        self.infection_start_time = np.inf
        self.infection_end_time = np.inf
        self.repulsion_points = []
        self.num_infected = 0

        self.center_point = VectorizedPoint()
        self.add(self.center_point)
        self.add_body()
        self.add_infection_ring()
        self.set_status(self.status, run_time=0)

        # Updaters
        self.add_updater(update_time)
        self.add_updater(lambda m, dt: m.update_position(dt))
        self.add_updater(lambda m, dt: m.update_infection_ring(dt))
        self.add_updater(lambda m: m.progress_through_change_anims())

    def add_body(self):
        body = self.get_body()
        body.set_height(self.height)
        body.move_to(self.get_center())
        self.add(body)
        self.body = body

    def get_body(self, status):
        person = SVGMobject(file_name="person")
        person.set_stroke(width=0)
        return person

    def set_status(self, status, run_time=1):
        start_color = self.color_map[self.status]
        end_color = self.color_map[status]

        if status == "I":
            self.infection_start_time = self.time
            self.infection_ring.set_stroke(width=0, opacity=0)
            if random.random() < self.p_symptomatic_on_infection:
                self.symptomatic = True
            else:
                self.infection_ring.set_color(self.asymptomatic_color)
                end_color = self.asymptomatic_color
        if self.status == "I":
            self.infection_end_time = self.time
            self.symptomatic = False

        anims = [
            UpdateFromAlphaFunc(
                self.body,
                lambda m, a: m.set_color(interpolate_color(
                    start_color, end_color, a
                )),
                run_time=run_time,
            )
        ]
        for anim in anims:
            self.push_anim(anim)

        self.status = status

    def push_anim(self, anim):
        anim.suspend_mobject_updating = False
        anim.begin()
        anim.start_time = self.time
        self.change_anims.append(anim)
        return self

    def pop_anim(self, anim):
        anim.update(1)
        anim.finish()
        self.change_anims.remove(anim)

    def add_infection_ring(self):
        self.infection_ring = Circle(
            radius=self.height / 2,
        )
        self.infection_ring.set_style(**self.infection_ring_style)
        self.add(self.infection_ring)
        self.infection_ring.time = 0
        return self

    def update_position(self, dt):
        center = self.get_center()
        total_force = np.zeros(3)

        # Gravity
        if self.wander_step_size != 0:
            if (self.time - self.last_step_change) > self.wander_step_duration:
                vect = rotate_vector(RIGHT, TAU * random.random())
                self.gravity_well = center + self.wander_step_size * vect
                self.last_step_change = self.time

        if self.gravity_well is not None:
            to_well = (self.gravity_well - center)
            dist = get_norm(to_well)
            if dist != 0:
                total_force += self.gravity_strength * to_well / (dist**3)

        # Potentially avoid neighbors
        if self.social_distance_factor > 0:
            repulsion_force = np.zeros(3)
            min_dist = np.inf
            for point in self.repulsion_points:
                to_point = point - center
                dist = get_norm(to_point)
                if 0 < dist < min_dist:
                    min_dist = dist
                if dist > 0:
                    repulsion_force -= self.social_distance_factor * to_point / (dist**3)
            sdct = self.social_distance_color_threshold
            self.body.set_stroke(
                self.social_distance_color,
                width=clip(
                    (sdct / min_dist) - sdct,
                    # 2 * (sdct / min_dist),
                    0,
                    self.max_social_distance_stroke_width
                ),
                background=True,
            )
            total_force += repulsion_force

        # Avoid walls
        wall_force = np.zeros(3)
        for i in range(2):
            to_lower = center[i] - self.dl_bound[i]
            to_upper = self.ur_bound[i] - center[i]

            # Bounce
            if to_lower < 0:
                self.velocity[i] = abs(self.velocity[i])
                self.set_coord(self.dl_bound[i], i)
            if to_upper < 0:
                self.velocity[i] = -abs(self.velocity[i])
                self.set_coord(self.ur_bound[i], i)

            # Repelling force
            # CHANGE: In float32 the person ends up exactly on the wall (distance 0) and 1/0 gives inf/NaN (the people disappear); the distance is bounded to 1e-6
            wall_force[i] += max((-1 / self.wall_buffer + 1 / max(to_lower, 1e-6)), 0)
            wall_force[i] -= max((-1 / self.wall_buffer + 1 / max(to_upper, 1e-6)), 0)
        total_force += wall_force

        # Apply force
        self.velocity += total_force * dt

        # Limit speed
        speed = get_norm(self.velocity)
        if speed > self.max_speed:
            self.velocity *= self.max_speed / speed

        # Update position
        self.shift(self.velocity * dt)

    def update_infection_ring(self, dt):
        ring = self.infection_ring
        if not (self.infection_start_time <= self.time <= self.infection_end_time + 1):
            return self

        ring_time = self.time - self.infection_start_time
        period = self.infection_animation_period

        alpha = (ring_time % period) / period
        ring.set_height(interpolate(
            self.height,
            self.infection_radius,
            smooth(alpha),
        ))
        ring.set_stroke(
            width=interpolate(
                0, 5,
                there_and_back(alpha),
            ),
            opacity=min([
                min([ring_time, 1]),
                min([self.infection_end_time + 1 - self.time, 1]),
            ]),
        )

        return self

    def progress_through_change_anims(self):
        for anim in self.change_anims:
            if anim.run_time == 0:
                alpha = 1
            else:
                alpha = (self.time - anim.start_time) / anim.run_time
            anim.interpolate(alpha)
            if alpha >= 1:
                self.pop_anim(anim)

    def get_center(self):
        return self.center_point.get_points()[0]


class DotPerson(Person):
    def get_body(self):
        return Dot()


class WideSpreadTesting(Scene):
    def construct(self):
        # Add dots
        dots = VGroup(*[
            DotPerson(
                height=0.2,
                infection_radius=0.6,
                max_speed=0,
                wander_step_size=0,
                p_symptomatic_on_infection=0.8,
            )
            for x in range(600)
        ])
        dots.arrange_in_grid(20, 30)
        dots.set_height(FRAME_HEIGHT - 1)

        self.add(dots)
        sick_dots = VGroup()
        for x in range(36):
            sicky = random.choice(dots)
            sicky.set_status("I")
            sick_dots.add(sicky)
            self.wait(0.1)
        self.wait(2)

        healthy_dots = VGroup()
        for dot in dots:
            if dot.status != "I":
                healthy_dots.add(dot)

        # Show Flash
        rings = self.get_rings(ORIGIN, FRAME_WIDTH + FRAME_HEIGHT, 0.1)
        rings.shift(7 * LEFT)
        for i, ring in enumerate(rings):
            ring.shift(0.05 * i**1.2 * RIGHT)

        self.play(LaggedStartMap(
            FadeIn, rings,
            lag_ratio=3 / len(rings),
            run_time=2.5,
            rate_func=there_and_back,
        ))

        # Quarantine
        box = Square()
        box.set_height(2)
        box.to_corner(DL)
        box.shift(LEFT)

        anims = []
        points = VGroup()
        points_target = VGroup()
        for dot in sick_dots:
            point = VectorizedPoint(dot.get_center())
            point.generate_target()
            points.add(point)
            points_target.add(point.target)

            dot.push_anim(MaintainPositionRelativeTo(dot, point, run_time=3))
            anims.append(MoveToTarget(point))

        points_target.arrange_in_grid()
        points_target.set_width(box.get_width() - 1)
        points_target.move_to(box)

        self.play(
            ShowCreation(box),
            LaggedStartMap(MoveToTarget, points, lag_ratio=0.05),
            self.camera.frame.shift, LEFT,
            run_time=3,
        )
        self.wait(9)

    def get_rings(self, center, max_radius, delta_r):
        radii = np.arange(0, max_radius, delta_r)
        rings = VGroup(*[
            Circle(
                radius=r,
                stroke_opacity=0.75 * (1 - fdiv(r, max_radius)),
                stroke_color=TEAL,
                stroke_width=100 * delta_r,
            )
            for r in radii
        ])
        rings.move_to(center)
        return rings
