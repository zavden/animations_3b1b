# ==============================================================================
# Scene:      TotalLengthOfEachJewelEquals
# Source:     videos/_2017/borsuk.py (lines 2144-2263)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TotalLengthOfEachJewelEquals.py TotalLengthOfEachJewelEquals -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - undefined name m1 in the sort key (NameError once init_points runs); sort the faces by z
#   - Python 2 integer division in slice indices
#   - Python 2 integer division in slice indices
#   - GL get_color() is a hex string: wrap in Color for the comparison
#   - colour.Color vs GL hex-string colors: compare through Color / hex_l
#   - colour.Color vs GL hex-string colors: compare through Color / hex_l
#   - colour.Color vs GL hex-string colors: compare through Color / hex_l
#   - colour.Color vs GL hex-string colors: compare through Color / hex_l
#   - colour.Color vs GL hex-string colors: compare through Color / hex_l
#   - colour.Color vs GL hex-string colors: compare through Color / hex_l
#   - colour.Color vs GL hex-string colors: compare through Color / hex_l
#   - sorted(list, cmp_function) and cmp() are Python 2: sort with key=
#   - colour.Color is unhashable: key the counts by hex string
#   - painter order: draw the faces from back to front (smaller z first); the first fix had the sign reversed
#   - broken 2to3 conversion of the cmp lambda (m1.get): sort the jewels left to right by x
#   - Python 2 integer division used as an index
#   - Python 2 integer division used as an index
#   - Python 2 integer division used as an index
# ==============================================================================

from manim_imports_ext import *
from functools import reduce

class Jewel(VMobject):
    CONFIG = {
        "color" : WHITE,
        "fill_opacity" : 0.75,
        "stroke_width" : 0,
        "height" : 0.5,
        "num_equator_points" : 5,
        "sun_vect" : OUT+LEFT+UP,
    }
    def init_points(self):
        for vect in OUT, IN:
            compass_vects = list(compass_directions(self.num_equator_points))
            if vect is IN:
                compass_vects.reverse()
            for vect_pair in adjacent_pairs(compass_vects):
                self.add(Polygon(vect, *vect_pair))
        self.set_height(self.height)
        self.rotate(-np.pi/2-np.pi/24, RIGHT)        
        self.rotate(-np.pi/12, UP)
        self.submobjects.sort(
            # CHANGE: undefined name m1 in the sort key (NameError once init_points runs); sort the faces by z
            # CHANGE: painter order: draw the faces from back to front (smaller z first); the first fix had the sign reversed
            key=lambda m: m.get_center()[2]
        )
        return self


class Necklace(VMobject):
    CONFIG = {
        "width" : FRAME_WIDTH - 1,
        "jewel_buff" : MED_SMALL_BUFF,
        "chain_color" : GREY,
        "default_colors" : [(4, BLUE), (6, WHITE), (4, GREEN)]
    }
    def __init__(self, *colors, **kwargs):
        digest_config(self, kwargs, locals())
        if len(colors) == 0:
            self.colors = self.get_default_colors()
        VMobject.__init__(self, **kwargs)

    def get_default_colors(self):
        result = list(it.chain(*[
            num*[color]
            for num, color in self.default_colors
        ]))
        random.shuffle(result)
        return result

    def init_points(self):
        jewels = VGroup(*[
            Jewel(color = color)
            for color in self.colors
        ])
        jewels.arrange(buff = self.jewel_buff)
        jewels.set_width(self.width)
        jewels.center()
        j_to_j_dist = (jewels[1].get_center()-jewels[0].get_center())[0]

        chain = Line(
            jewels[0].get_center() + j_to_j_dist*LEFT/2, 
            jewels[-1].get_center() + j_to_j_dist*RIGHT/2, 
            color = self.chain_color,
        )
        self.add(chain, *jewels)
        self.chain = chain
        self.jewels = jewels


class IntroduceStolenNecklaceProblem(ThreeDScene):
    CONFIG = {
        "jewel_colors" : [BLUE, GREEN, WHITE, RED],
        "num_per_jewel" : [8, 10, 4, 6],
        "num_shuffles" : 1,
        "necklace_center" : UP,
        "random_seed" : 2,
        "forced_binary_choices" : (0, 1, 0, 1, 0),
    }
    def construct(self):
        random.seed(self.random_seed)
        self.add_thieves()
        self.write_title()
        self.introduce_necklace()
        self.divvy_by_cutting_all()
        self.divvy_with_n_cuts()
        self.shuffle_jewels(self.necklace.jewels)
        self.divvy_with_n_cuts()

    def add_thieves(self):
        thieves = VGroup(
            Randolph(),
            Mortimer()
        )
        thieves.arrange(RIGHT, buff = 4*LARGE_BUFF)
        thieves.to_edge(DOWN)
        thieves[0].make_eye_contact(thieves[1])

        self.add(thieves)
        self.thieves = thieves

    def write_title(self):
        title = OldTexText("Stolen necklace problem")
        title.to_edge(UP)
        self.play(
            Write(title),
            *[
                ApplyMethod(pi.look_at, title)
                for pi in self.thieves
            ]
        )
        self.title = title

    def introduce_necklace(self):
        necklace = self.get_necklace()
        jewels = necklace.jewels
        jewel_types = self.get_jewels_organized_by_type(jewels)

        enumeration_labels = VGroup()
        for jewel_type in jewel_types:
            num_mob = OldTex(str(len(jewel_type)))
            jewel_copy = jewel_type[0].copy().scale(2)
            jewel_copy.next_to(num_mob)
            label = VGroup(num_mob, jewel_copy)
            enumeration_labels.add(label)
        enumeration_labels.arrange(RIGHT, buff = LARGE_BUFF)
        enumeration_labels.to_edge(UP)

        self.play(
            FadeIn(
                necklace,
                lag_ratio = 0.5,
                run_time = 3
            ),
            *it.chain(*[
                [pi.change_mode, "conniving", pi.look_at, necklace]
                for pi in self.thieves
            ])
        )
        self.play(*[
            ApplyMethod(
                jewel.rotate, np.pi/6, UP, 
                rate_func = there_and_back
            )
            for jewel in jewels
        ])
        self.play(Blink(self.thieves[0]))
        for jewel_type in jewel_types:
            self.play(
                jewel_type.shift, 0.2*UP,
                rate_func = wiggle
            )
        self.wait()
        for x in range(self.num_shuffles):
            self.shuffle_jewels(jewels)
        self.play(FadeOut(self.title))
        for jewel_type, label in zip(jewel_types, enumeration_labels):
            jewel_type.submobjects.sort(
                # CHANGE: broken 2to3 conversion of the cmp lambda (m1.get): sort the jewels left to right by x
                key=lambda m: m.get_center()[0]
            )
            jewel_type.save_state()
            jewel_type.generate_target()
            jewel_type.target.arrange()
            jewel_type.target.scale(2)
            jewel_type.target.move_to(2*UP)
            self.play(
                MoveToTarget(jewel_type), 
                Write(label)
            )
            self.play(jewel_type.restore)
        self.play(Blink(self.thieves[1]))

        self.enumeration_labels = enumeration_labels
        self.jewel_types = jewel_types

    def divvy_by_cutting_all(self):
        enumeration_labels = self.enumeration_labels
        necklace = self.necklace
        jewel_types = self.jewel_types
        thieves = self.thieves

        both_half_labels = VGroup()
        for thief, vect in zip(self.thieves, [LEFT, RIGHT]):
            half_labels = VGroup()
            for label in enumeration_labels:
                tex, jewel = label
                num = int(tex.get_tex())
                half_label = VGroup(
                    OldTex(str(num/2)),
                    jewel.copy()
                )
                half_label.arrange()
                half_labels.add(half_label)
            half_labels.arrange(DOWN)
            half_labels.set_height(thief.get_height())
            half_labels.next_to(
                thief, vect, 
                buff = MED_LARGE_BUFF,
                aligned_edge = DOWN
            )
            both_half_labels.add(half_labels)

        for half_labels in both_half_labels:
            self.play(ReplacementTransform(
                enumeration_labels.copy(), 
                half_labels
            ))
        self.play(*[ApplyMethod(pi.change_mode, "pondering") for pi in thieves])
        self.wait()

        for type_index, jewel_type in enumerate(jewel_types):
            jewel_type.save_state()
            jewel_type_copy = jewel_type.copy()
            n_jewels = len(jewel_type)
            halves = [
                # CHANGE: Python 2 integer division in slice indices
                VGroup(*jewel_type_copy[:n_jewels//2]),
                # CHANGE: Python 2 integer division used as an index
                VGroup(*jewel_type_copy[n_jewels//2:]),
            ]
            for half, thief, vect in zip(halves, thieves, [RIGHT, LEFT]):
                half.arrange(DOWN)
                half.next_to(
                    thief, vect, 
                    buff = SMALL_BUFF + type_index*half.get_width(),
                    aligned_edge = DOWN
                )
            self.play(
                Transform(jewel_type, jewel_type_copy),
                *[
                    ApplyMethod(thief.look_at, jewel_type_copy)
                    for thief in thieves
                ]
            )
        self.play(*it.chain(*[
            [thief.change_mode, "happy", thief.look_at, necklace]
            for thief in thieves
        ]))
        self.wait()
        self.play(*[
            jewel_type.restore
            for jewel_type in jewel_types
        ])
        self.play(*it.chain(*[
            [thief.change_mode, "confused", thief.look_at, necklace]
            for thief in thieves
        ]))

    def divvy_with_n_cuts(
        self, 
        with_thieves = True, 
        highlight_groups = True,
        show_matching_after_divvying = True,
        ):
        necklace = self.necklace
        jewel_types = self.jewel_types
        # CHANGE: sorted(list, cmp_function) and cmp() are Python 2: sort with key=
        jewels = sorted(
            necklace.jewels, 
            key = lambda m : m.get_center()[0]
        )
        slice_indices, binary_choices = self.find_slice_indices(jewels, jewel_types)
        subgroups = [
            VGroup(*jewels[i1:i2])
            for i1, i2 in zip(slice_indices, slice_indices[1:])
        ]
        buff = (jewels[1].get_left()[0]-jewels[0].get_right()[0])/2
        v_lines = VGroup(*[
            DashedLine(UP, DOWN).next_to(group, RIGHT, buff = buff)
            for group in subgroups[:-1]
        ])
        strand_groups = [VGroup(), VGroup()]
        for group, choice in zip(subgroups, binary_choices):
            strand = Line(
                group[0].get_center(), group[-1].get_center(),
                color = necklace.chain.get_color()
            )
            strand.add(*group)
            strand_groups[choice].add(strand)
            self.add(strand)

        self.play(ShowCreation(v_lines))
        self.play(
            FadeOut(necklace.chain),
            *it.chain(*[
                list(map(Animation, group))
                for group in strand_groups
            ])
        )
        for group in strand_groups:
            group.save_state()
        self.play(
            strand_groups[0].shift, UP/2.,
            strand_groups[1].shift, DOWN/2.,
        )
        if with_thieves:
            self.play(*it.chain(*[
                [thief.change_mode, "happy", thief.look_at, self.necklace]
                for thief in self.thieves
            ]))
            self.play(Blink(self.thieves[1]))
        else:
            self.wait()

        if highlight_groups:
            for group in strand_groups:
                box = Rectangle(
                    width = group.get_width()+2*SMALL_BUFF,
                    height = group.get_height()+2*SMALL_BUFF,
                    stroke_width = 0,
                    fill_color = YELLOW,
                    fill_opacity = 0.3,
                )
                box.move_to(group)
                self.play(FadeIn(box))
                self.wait()
                self.play(FadeOut(box))

        self.wait()
        if show_matching_after_divvying:
            for jewel_type in jewel_types:
                self.play(
                    *[
                        ApplyMethod(jewel.scale, 1.5)
                        for jewel in jewel_type
                    ],
                    rate_func = there_and_back,
                    run_time = 2
                )
            self.wait()
        self.play(
            FadeOut(v_lines),
            FadeIn(necklace.chain),
            *[
                group.restore for group in strand_groups
            ]
        )
        self.remove(*strand_groups)
        self.add(necklace)

    ########

    def get_necklace(self, **kwargs):
        colors = reduce(op.add, [
            num*[color]
            for num, color in zip(self.num_per_jewel, self.jewel_colors)
        ])
        self.necklace = Necklace(*colors, **kwargs)
        self.necklace.shift(self.necklace_center)
        return self.necklace

    def get_jewels_organized_by_type(self, jewels):
        return [
            # CHANGE: GL get_color() is a hex string: wrap in Color for the comparison
            VGroup(*[m for m in jewels if Color(m.get_color()) == color])
            for color in map(Color, self.jewel_colors)
        ]

    def shuffle_jewels(self, jewels, run_time = 2, path_arc = np.pi/2, **kwargs):
        shuffled_indices = list(range(len(jewels)))
        random.shuffle(shuffled_indices)
        target_group = VGroup(*[
            jewel.copy().move_to(jewels[shuffled_indices[i]])
            for i, jewel in enumerate(jewels)
        ])
        self.play(Transform(
            jewels, target_group,
            run_time = run_time,            
            path_arc = path_arc,
            **kwargs
        ))

    def find_slice_indices(self, jewels, jewel_types):

        def jewel_to_type_number(jewel):
            for i, jewel_type in enumerate(jewel_types):
                if jewel in jewel_type:
                    return i
            raise Exception("Not in any jewel_types")
        type_numbers = list(map(jewel_to_type_number, jewels))

        n_types = len(jewel_types)
        for slice_indices in it.combinations(list(range(1, len(jewels))), n_types):
            slice_indices = [0] + list(slice_indices) + [len(jewels)]
            if self.forced_binary_choices is not None:
                all_binary_choices = [self.forced_binary_choices]
            else:
                all_binary_choices = it.product(*[list(range(2))]*(n_types+1))
            for binary_choices in all_binary_choices:
                subsets = [
                    type_numbers[i1:i2]
                    for i1, i2 in zip(slice_indices, slice_indices[1:])
                ]
                left_sets, right_sets = [
                    [
                        subset
                        for subset, index in zip(subsets, binary_choices)
                        if index == target_index
                    ]
                    for target_index in range(2)
                ]
                flat_left_set = np.array(list(it.chain(*left_sets)))
                flat_right_set = np.array(list(it.chain(*right_sets)))


                match_array = [
                    sum(flat_left_set == n) == sum(flat_right_set == n)
                    for n in range(n_types)
                ]
                if np.all(match_array):
                    return slice_indices, binary_choices
        raise Exception("No fair division found")


class MakeTwoJewelCaseContinuous(IntroduceStolenNecklaceProblem):
    CONFIG = {
        "jewel_colors" : [BLUE, GREEN],
        "num_per_jewel" : [8, 10],
        "random_seed" : 2,
        "forced_binary_choices" : (0, 1, 0),
        "show_matching_after_divvying" : True,
        "necklace_center" : ORIGIN,
        "necklace_width" : FRAME_WIDTH - 3,
        "random_seed" : 0,
        "num_continuous_division_searches" : 4,
    }
    def construct(self):
        random.seed(self.random_seed)
        self.introduce_necklace()
        self.divvy_with_n_cuts()
        self.identify_necklace_with_unit_interval()
        self.color_necklace()
        self.find_continuous_fair_division()
        self.show_continuous_fair_division()
        self.set_color_continuous_groups()
        self.mention_equivalence_to_discrete_case()
        self.shift_divide_off_tick_marks()

    def introduce_necklace(self):
        self.get_necklace(
            width = self.necklace_width,
        )
        self.play(FadeIn(
            self.necklace,
            lag_ratio = 0.5
        ))
        self.shuffle_jewels(self.necklace.jewels)
        jewel_types = self.get_jewels_organized_by_type(
            self.necklace.jewels
        )
        self.wait()
        self.count_jewel_types(jewel_types)
        self.wait()

        self.jewel_types = jewel_types

    def count_jewel_types(self, jewel_types):
        enumeration_labels = VGroup()
        for jewel_type in jewel_types:
            num_mob = OldTex(str(len(jewel_type)))
            jewel_copy = jewel_type[0].copy()
            # jewel_copy.set_height(num_mob.get_height())
            jewel_copy.next_to(num_mob)
            label = VGroup(num_mob, jewel_copy)
            enumeration_labels.add(label)
        enumeration_labels.arrange(RIGHT, buff = LARGE_BUFF)
        enumeration_labels.to_edge(UP)

        for jewel_type, label in zip(jewel_types, enumeration_labels):
            jewel_type.sort()
         
            jewel_type.save_state()
            jewel_type.generate_target()
            jewel_type.target.arrange()
            jewel_type.target.move_to(2*UP)
            self.play(
                MoveToTarget(jewel_type), 
                Write(label)
            )
            self.play(jewel_type.restore)

    def divvy_with_n_cuts(self):
        IntroduceStolenNecklaceProblem.divvy_with_n_cuts(
            self, 
            with_thieves = False, 
            highlight_groups = False,
            show_matching_after_divvying = True,
        )

    def identify_necklace_with_unit_interval(self):
        interval = UnitInterval(
            tick_frequency = 1./sum(self.num_per_jewel),
            tick_size = 0.2,
            big_tick_numbers = [],
        )
        interval.stretch_to_fit_width(self.necklace.get_width())
        interval.move_to(self.necklace)
        tick_marks = interval.tick_marks
        tick_marks.set_stroke(WHITE, width = 2)

        brace = Brace(interval)
        brace_text = brace.get_text("Length = 1")

        self.play(
            GrowFromCenter(brace),
            Write(brace_text)
        )
        self.wait()
        self.play(
            ShowCreation(interval.tick_marks),
        )
        self.wait()

        self.tick_marks = interval.tick_marks
        self.length_brace = VGroup(brace, brace_text)

    def color_necklace(self):
        # CHANGE: Python 2 integer division used as an index
        example_index = len(self.necklace.jewels)//2
        jewels = self.necklace.jewels
        chain = self.necklace.chain
        self.remove(self.necklace)
        self.add(chain, jewels)

        jewels.submobjects.sort(
            key=lambda m: m.get_center()[0]
        )
        remaining_indices = list(range(len(jewels)))
        remaining_indices.remove(example_index)

        example_segment = self.color_necklace_by_indices(example_index)
        remaining_segments = self.color_necklace_by_indices(*remaining_indices)
        self.remove(chain)
        segments = VGroup(example_segment[0], *remaining_segments)
        segments.submobjects.sort(
            key=lambda m: m.get_center()[0]
        )
        segment_types = VGroup(*[
            # CHANGE: colour.Color vs GL hex-string colors: compare through Color / hex_l
            VGroup(*[m for m in segments if Color(m.get_color()) == Color(color)])
            for color in self.jewel_colors
        ])

        for group in segment_types:
            length_tex = OldTex("\\frac{%d}{%d}"%(
                len(group),
                len(jewels)
             ))
            length_tex.next_to(group, UP)
            length_tex.shift(UP)
            self.play(
                group.shift, UP,
                Write(length_tex, run_time = 1),
            )
            self.wait()
            self.play(
                group.shift, DOWN,
                FadeOut(length_tex)
            )
        self.play(FadeOut(self.length_brace))

        self.segments = segments

    def color_necklace_by_indices(self, *indices):
        chain = self.necklace.chain
        jewels = VGroup(*[
            self.necklace.jewels[i]
            for i in indices
        ])
        n_jewels = len(self.necklace.jewels)

        segments = VGroup(*[
            Line(
                chain.point_from_proportion(index/float(n_jewels)),
                chain.point_from_proportion((index+1)/float(n_jewels)),
                color = jewel.get_color()
            )
            for index, jewel in zip(indices, jewels)
        ])
        for jewel in jewels:
            jewel.save_state()

        self.play(jewels.shift, jewels.get_height()*UP)
        self.play(ReplacementTransform(
            jewels, segments,
            lag_ratio = 0.5,
            run_time = 2
        ))
        self.wait()
        return segments

    def find_continuous_fair_division(self):
        chain = self.necklace.chain
        n_jewels = len(self.necklace.jewels)

        slice_indices, ignore = self.find_slice_indices(
            self.necklace.jewels,
            self.jewel_types
        )
        cut_proportions = [
            sorted([random.random(), random.random()])
            for x in range(self.num_continuous_division_searches)
        ]
        cut_proportions.append([
            float(i)/n_jewels
            for i in slice_indices[1:-1]
        ])
        cut_points = [
            list(map(chain.point_from_proportion, pair))
            for pair in cut_proportions
        ]
        v_lines = VGroup(*[DashedLine(UP, DOWN) for x in range(2)])

        for line, point in zip(v_lines, cut_points[0]):
            line.move_to(point)

        self.play(ShowCreation(v_lines))
        self.wait()
        for target_points in cut_points[1:]:
            self.play(*[
                ApplyMethod(line.move_to, point)
                for line, point in zip(v_lines, target_points)
            ])
            self.wait()

        self.slice_indices = slice_indices
        self.v_lines = v_lines

    def show_continuous_fair_division(self):
        slice_indices = self.slice_indices

        groups = [
            VGroup(
                VGroup(*self.segments[i1:i2]),
                VGroup(*self.tick_marks[i1:i2]),
            )
            for i1, i2 in zip(slice_indices, slice_indices[1:])
        ]
        groups[-1].add(self.tick_marks[-1])
        vects = [[UP, DOWN][i] for i in self.forced_binary_choices]

        self.play(*[
            ApplyMethod(group.shift, 0.5*vect)
            for group, vect in zip(groups, vects)
        ])
        self.wait()

        self.groups = groups

    def set_color_continuous_groups(self):
        top_group = VGroup(self.groups[0], self.groups[2])
        bottom_group = self.groups[1]
        boxes = VGroup()
        for group in top_group, bottom_group:
            box = Rectangle(
                width = FRAME_WIDTH-2,
                height = group.get_height()+SMALL_BUFF,
                stroke_width = 0,
                fill_color = WHITE,
                fill_opacity = 0.25,
            )
            box.shift(group.get_center()[1]*UP)
            boxes.add(box)

        weight_description = VGroup(*[
            VGroup(
                OldTex("\\frac{%d}{%d}"%(
                    # CHANGE: Python 2 integer division used as an index
                    len(jewel_type)//2, len(self.segments)
                )),
                Jewel(color = jewel_type[0].get_color())
            ).arrange()
            for jewel_type in self.jewel_types
        ])
        weight_description.arrange(buff = LARGE_BUFF)
        weight_description.next_to(boxes, UP, aligned_edge = LEFT)

        self.play(FadeIn(boxes))
        self.play(Write(weight_description))
        self.wait()

        self.set_color_box = boxes
        self.weight_description = weight_description

    def mention_equivalence_to_discrete_case(self):
        morty = Mortimer()
        morty.flip()
        morty.to_edge(DOWN)
        morty.shift(LEFT)
        self.play(FadeIn(morty))
        self.play(PiCreatureSays(
            morty, 
            """This is equivalent to
            the discrete case. """,
            bubble_config = {
                "height" : 3, 
                "direction" : LEFT,
            }
        ))
        self.play(Blink(morty))
        self.wait()
        self.play(*list(map(FadeOut, [
            morty, morty.bubble, morty.bubble.content
        ])))
        
    def shift_divide_off_tick_marks(self):
        groups = self.groups
        slice_indices = self.slice_indices
        v_lines = self.v_lines

        left_segment = groups[1][0][0]
        left_tick = groups[1][1][0]
        right_segment = groups[-1][0][0]
        right_tick = groups[-1][1][0]

        segment_width = left_segment.get_width()

        for mob in left_segment, right_segment:
            mob.parts = VGroup(
                mob.copy().pointwise_become_partial(mob, 0, 0.5),
                mob.copy().pointwise_become_partial(mob, 0.5, 1),
            )
            self.remove(mob)
            self.add(mob.parts)
        restorers = [left_segment.parts, left_tick, right_segment.parts, right_tick]
        for mob in restorers:
            mob.save_state()

        emerald_segments = VGroup(*[
            segment
            for segment in list(groups[0][0])+list(groups[2][0])
            # CHANGE: colour.Color vs GL hex-string colors: compare through Color / hex_l
            if Color(segment.get_color()) == Color(self.jewel_colors[1])
            if segment is not right_segment
        ])
        emerald_segments.add(
            left_segment.parts[0],
            right_segment.parts[1],
        )
        emerald_segments.sort()

        self.play(v_lines.shift, segment_width*RIGHT/2)
        self.play(*[
            ApplyMethod(mob.shift, vect)
            for mob, vect in [
                (left_segment.parts[0], UP),
                (left_tick, UP),
                (right_segment.parts[0], DOWN),
                (right_tick, DOWN),
            ]
        ])
        self.wait()

        words = OldTexText("Cut part way through segment")
        words.to_edge(RIGHT)
        words.shift(2*UP)
        arrow1 = Arrow(words.get_bottom(), left_segment.parts[0].get_right())
        arrow2 = Arrow(words.get_bottom(), right_segment.parts[1].get_left())
        VGroup(words, arrow1, arrow2).set_color(RED)

        self.play(Write(words), ShowCreation(arrow1))
        self.wait()

        emerald_segments.save_state()
        emerald_segments.generate_target()
        emerald_segments.target.arrange()
        emerald_segments.target.move_to(2*DOWN)
        brace = Brace(emerald_segments.target, DOWN)
        label = VGroup(
            OldTex("5\\left( 1/18 \\right)"),
            Jewel(color = self.jewel_colors[1])
        ).arrange()
        label.next_to(brace, DOWN)
        self.play(MoveToTarget(emerald_segments))
        self.play(GrowFromCenter(brace))
        self.play(Write(label))
        self.wait()
        broken_pair = VGroup(*emerald_segments[2:4])
        broken_pair.save_state()
        self.play(broken_pair.shift, 0.5*UP)
        vect = broken_pair[1].get_left()-broken_pair[1].get_right()
        self.play(
            broken_pair[0].shift, -vect/2,
            broken_pair[1].shift, vect/2,
        )
        self.wait()
        self.play(broken_pair.space_out_submobjects)
        self.play(broken_pair.restore)
        self.wait()
        self.play(
            emerald_segments.restore,
            *list(map(FadeOut, [brace, label]))
        )

        self.wait()
        self.play(ShowCreation(arrow2))
        self.wait()
        self.play(*list(map(FadeOut, [words, arrow1, arrow2])))

        for line in v_lines:
            self.play(line.shift, segment_width*LEFT/2)
        self.play(*[mob.restore for mob in restorers])
        self.remove(left_segment.parts, right_segment.parts)
        self.add(left_segment, right_segment)


class ChoicesInNecklaceCutting(ReconfigurableScene):
    CONFIG = {
        "num_continuous_division_searches" : 4,
        "denoms" : [6, 3, 2],
        "necklace_center" : DOWN,
        "thief_box_offset" : 1.2,
    }
    def construct(self):
        self.add_necklace()
        self.choose_places_to_cut()
        self.show_three_numbers_adding_to_one()
        self.make_binary_choice()

    def add_necklace(self):
        width, colors, num_per_color = [
            MakeTwoJewelCaseContinuous.CONFIG[key]
            for key in [
                "necklace_width", "jewel_colors", "num_per_jewel"
            ]
        ]
        color_list = list(it.chain(*[
            num*[color] 
            for num, color in zip(num_per_color, colors)
        ]))
        random.shuffle(color_list)

        interval = UnitInterval(
            tick_frequency = 1./sum(num_per_color),
            tick_size = 0.2,
            big_tick_numbers = [],
        )
        interval.stretch_to_fit_width(width)
        interval.shift(self.necklace_center)
        tick_marks = interval.tick_marks
        tick_marks.set_stroke(WHITE, width = 2)

        segments = VGroup()
        for l_tick, r_tick, color in zip(tick_marks, tick_marks[1:], color_list):
            segment = Line(
                l_tick.get_center(),
                r_tick.get_center(),
                color = color
            )
            segments.add(segment)

        self.necklace = VGroup(segments, tick_marks)
        self.add(self.necklace)

        self.interval = interval        

    def choose_places_to_cut(self):
        v_lines = VGroup(*[DashedLine(UP, DOWN) for x in range(2)])
        final_num_pair = np.cumsum([1./d for d in self.denoms[:2]])

        num_pairs = [
            sorted([random.random(), random.random()])
            for x in range(self.num_continuous_division_searches)
        ] + [final_num_pair]

        point_pairs = [
            list(map(self.interval.number_to_point, num_pair))
            for num_pair in num_pairs
        ]
        
        for line, point in zip(v_lines, point_pairs[0]):
            line.move_to(point)
        self.play(ShowCreation(v_lines))
        for point_pair in point_pairs[1:]:
            self.wait()
            self.play(*[
                ApplyMethod(line.move_to, point)
                for line, point in zip(v_lines, point_pair)
            ])
        self.wait()

        self.division_points = list(it.chain(
            [self.interval.get_left()],
            point_pairs[-1],
            [self.interval.get_right()]
        ))

        self.v_lines = v_lines

    def show_three_numbers_adding_to_one(self):
        points = self.division_points
        braces = [
            Brace(Line(p1+SMALL_BUFF*RIGHT/2, p2+SMALL_BUFF*LEFT/2))
            for p1, p2 in zip(points, points[1:])
        ]
        for char, denom, brace in zip("abc", self.denoms, braces):
            brace.label = brace.get_text("$%s$"%char)
            brace.concrete_label = brace.get_text("$\\frac{1}{%d}$"%denom)
            VGroup(
                brace.label,
                brace.concrete_label
            ).set_color(YELLOW)

        words = OldTexText(
            "1) Choose", "$a$, $b$, $c$", "so that", "$a+b+c = 1$"
        )
        words[1].set_color(YELLOW)
        words[3].set_color(YELLOW)
        words.to_corner(UP+LEFT)

        self.play(*it.chain(*[
            [GrowFromCenter(brace), Write(brace.label)]
            for brace in braces
        ]))
        self.play(Write(words))
        self.wait(2)
        self.play(*[
            ReplacementTransform(brace.label, brace.concrete_label)
            for brace in braces
        ])
        self.wait()
        self.wiggle_v_lines()
        self.wait()
        self.transition_to_alt_config(denoms = [3, 3, 3])
        self.wait()
        self.play(*list(map(FadeOut, list(braces) + [
            brace.concrete_label for brace in braces
        ])))

        self.choice_one_words = words

    def make_binary_choice(self):
        groups = self.get_groups()
        boxes, labels = self.get_boxes_and_labels()
        arrow_pairs, curr_arrows = self.get_choice_arrow_pairs(groups)
        words = OldTexText("2) Make a binary choice for each segment")
        words.next_to(
            self.choice_one_words, DOWN, 
            buff = MED_LARGE_BUFF, 
            aligned_edge = LEFT
        )

        self.play(Write(words))
        self.play(*list(map(FadeIn, [boxes, labels])))
        for binary_choices in it.product(*[[0, 1]]*3):
            self.play(*[
                ApplyMethod(group.move_to, group.target_points[choice])
                for group, choice in zip(groups, binary_choices)
            ] + [
                Transform(
                    curr_arrow, arrow_pair[choice],
                    path_arc = np.pi
                )
                for curr_arrow, arrow_pair, choice in zip(
                    curr_arrows, arrow_pairs, binary_choices
                )
            ])
            self.wait()

    ######

    def get_groups(self, indices = None):
        segments, tick_marks = self.necklace
        if indices is None:
            n_segments = len(segments)
            # CHANGE: Python 2 integer division in slice indices
            indices = [0, n_segments//6, n_segments//2, n_segments]

        groups = [
            VGroup(
                VGroup(*segments[i1:i2]),
                VGroup(*tick_marks[i1:i2]),
            )
            for i1, i2 in zip(indices, indices[1:])
        ]
        for group, index in zip(groups, indices[1:]):
            group[1].add(tick_marks[index].copy())
        groups[-1][1].add(tick_marks[-1])

        for group in groups:
            group.target_points = [
                group.get_center() + self.thief_box_offset*vect
                for vect in (UP, DOWN)
            ]

        return groups

    def get_boxes_and_labels(self):
        box = Rectangle(
            height = self.necklace.get_height()+SMALL_BUFF,
            width = self.necklace.get_width()+2*SMALL_BUFF,
            stroke_width = 0,
            fill_color = WHITE,
            fill_opacity = 0.25
        )
        box.move_to(self.necklace)

        boxes = VGroup(*[
            box.copy().shift(self.thief_box_offset*vect)
            for vect in (UP, DOWN)
        ])
        labels = VGroup(*[
            OldTexText(
                "Thief %d"%(i+1)
            ).next_to(box, UP, aligned_edge = RIGHT)
            for i, box in enumerate(boxes)
        ])
        return boxes, labels

    def get_choice_arrow_pairs(self, groups):
        arrow = OldTex("\\uparrow")
        arrow_pairs = [
            [arrow.copy(), arrow.copy().rotate(np.pi)]
            for group in groups
        ]
        pre_arrow_points = [
            VectorizedPoint(group.get_center())
            for group in groups
        ]
        for point, arrow_pair in zip(pre_arrow_points, arrow_pairs):
            for arrow, color in zip(arrow_pair, [GREEN, RED]):
                arrow.set_color(color)
                arrow.move_to(point.get_center())
        return arrow_pairs, pre_arrow_points

    def wiggle_v_lines(self):
        self.play(
            *it.chain(*[
                [
                    line.rotate, np.pi/12, vect,
                    line.set_color, RED
                ]
                for line, vect in zip(self.v_lines, [OUT, IN])
            ]),
            rate_func = wiggle
        )


class NecklaceDivisionSphereAssociation(ChoicesInNecklaceCutting):
    CONFIG = {
        "xyz_colors" : color_gradient([GREEN_B, BLUE], 3),
        "necklace_center" : DOWN,
        "thief_box_offset" : 1.6,
        "denoms" : [6, 3, 2],
    }
    def construct(self):
        self.add_necklace()
        self.add_sphere_point_label()
        self.choose_places_to_cut()
        self.add_braces()
        self.add_boxes_and_labels()
        self.show_binary_choice_association()
        self.ask_about_antipodal_pairs()

    def add_sphere_point_label(self):
        label = OldTexText(
            "$(x, y, z)$",
            "such that",
            "$x^2 + y^2 + z^2 = 1$"
        )
        for i, j_list in (0, [1, 3, 5]), (2, [0, 3, 6]):
            for j, color in zip(j_list, self.xyz_colors):
                label[i][j].set_color(color)
        label.to_corner(UP+RIGHT)

        ghost_sphere_point = VectorizedPoint()
        ghost_sphere_point.to_corner(UP+LEFT, buff = LARGE_BUFF)
        ghost_sphere_point.shift(2*RIGHT)

        arrow = Arrow(
            label.get_left(), ghost_sphere_point,
            color = WHITE
        )

        self.add(label, arrow)

        self.sphere_point_label = label

    def add_braces(self):
        points = self.division_points
        braces = [
            Brace(
                Line(p1+SMALL_BUFF*RIGHT/2, p2+SMALL_BUFF*LEFT/2),
                UP
            )
            for p1, p2 in zip(points, points[1:])
        ]
        for char, brace, color, denom in zip("xyz", braces, self.xyz_colors, self.denoms):
            brace.label = brace.get_text(
                "$%s^2$"%char, "$= 1/%d$"%denom,
                buff = SMALL_BUFF
            )
            brace.label.set_color(color)
            if brace.label.get_right()[0] > brace.get_right()[0]:
                brace.label.next_to(
                    brace, UP, buff = SMALL_BUFF,
                    aligned_edge = RIGHT
                )

        self.play(*it.chain(
            list(map(GrowFromCenter, braces)),
            [Write(brace.label) for brace in braces]
        ))
        self.wait()

        self.braces = braces

    def add_boxes_and_labels(self):
        boxes, labels = self.get_boxes_and_labels()
        self.play(*list(map(FadeIn, [boxes, labels])))
        self.wait()

    def show_binary_choice_association(self):
        groups = self.get_groups()
        self.swapping_anims = []
        final_choices = [1, 0, 1]
        quads = list(zip(self.braces, self.denoms, groups, final_choices))
        for brace, denom, group, final_choice in quads:
            char = brace.label.args[0][1]
            choices = [
                OldTex(
                    char, "=", sign, "\\sqrt{\\frac{1}{%d}}"%denom
                )
                for sign in ("+", "-")
            ]
            for choice, color in zip(choices, [GREEN, RED]):
                # choice[0].set_color(brace.label.get_color())
                choice[2].set_color(color)
                choice.scale(0.8)
                choice.move_to(group)
                if choice.get_width() > 0.8*group.get_width():
                    choice.next_to(group.get_right(), LEFT, buff = MED_SMALL_BUFF)
            original_choices = [m.copy() for m in choices]

            self.play(
                ReplacementTransform(
                    VGroup(brace.label[0], brace, brace.label[1]), 
                    choices[0]
                ),
                group.move_to, group.target_points[0]
            )
            self.wait()
            self.play(
                Transform(*choices),
                group.move_to, group.target_points[1]
            )
            self.wait()
            if final_choice == 0:
                self.play(
                    Transform(choices[0], original_choices[0]),
                    group.move_to, group.target_points[0]
                )
            self.swapping_anims += [
                Transform(choices[0], original_choices[1-final_choice]),
                group.move_to, group.target_points[1-final_choice]
            ]

    def ask_about_antipodal_pairs(self):
        question = OldTexText("What do antipodal points signify?")
        question.move_to(self.sphere_point_label, LEFT)
        question.set_color(MAROON_B)
        antipodal_tex = OldTex(
            "(x, y, z) \\rightarrow (-x, -y, -z)"
        )
        antipodal_tex.next_to(question, DOWN, aligned_edge = LEFT)

        self.play(FadeOut(self.sphere_point_label))
        self.play(FadeIn(question))
        self.wait()
        self.play(Write(antipodal_tex))
        self.wait()
        self.wiggle_v_lines()
        self.wait()
        self.play(*self.swapping_anims)
        self.wait()


class TotalLengthOfEachJewelEquals(NecklaceDivisionSphereAssociation, ThreeDScene):
    CONFIG = {
        "random_seed" : 1,
        "thief_box_offset" : 1.2,
    }
    def construct(self):
        random.seed(self.random_seed)
        self.add_necklace()
        self.add_boxes_and_labels()
        self.find_fair_division()
        self.demonstrate_fair_division()
        self.perform_antipodal_swap()

    def find_fair_division(self):
        segments, tick_marks = self.necklace
        segments.sort()
        segment_colors = [
            segment.get_color()
            for segment in segments
        ]
        indices = self.get_fair_division_indices(segment_colors)
        groups = self.get_groups(
            [0] + list(np.array(indices)+1) + [len(segments)]
        )
        self.add(*groups)
        binary_choice = [0, 1, 0]

        v_lines = VGroup(*[DashedLine(UP, DOWN) for x in range(2)])
        v_lines.move_to(self.necklace)
        self.play(ShowCreation(v_lines))
        self.play(*[
            ApplyMethod(line.move_to, segments[index].get_right())
            for line, index in zip(v_lines, indices)
        ])
        self.wait()
        self.play(*[
            ApplyMethod(group.move_to, group.target_points[choice])
            for group, choice in zip(groups, binary_choice)
        ])
        self.wait()

        self.groups = groups
        self.v_lines = v_lines

    def get_fair_division_indices(self, colors):
        # CHANGE: colour.Color vs GL hex-string colors: compare through Color / hex_l
        colors = np.array([Color(c).get_hex_l() for c in colors])
        color_types = list(map(Color, set(colors)))
        type_to_count = dict([
            # CHANGE: colour.Color vs GL hex-string colors: compare through Color / hex_l
            # CHANGE: colour.Color is unhashable: key the counts by hex string
            (color.get_hex_l(), sum(colors == color.get_hex_l()))
            for color in color_types
        ])
        for i1, i2 in it.combinations(list(range(1, len(colors)-1)), 2):
            bools = [
                # CHANGE: colour.Color vs GL hex-string colors: compare through Color / hex_l
                # CHANGE: colour.Color is unhashable: key the counts by hex string
                sum(colors[i1:i2] == color.get_hex_l()) == type_to_count[color.get_hex_l()]/2
                for color in color_types
            ]
            if np.all(bools):
                return i1, i2
        raise Exception("No fair division found")

    def demonstrate_fair_division(self):
        segments, tick_marks = self.necklace
        color_types = list(map(Color, set([
            # CHANGE: colour.Color vs GL hex-string colors: compare through Color / hex_l
            Color(segment.get_color()).get_hex_l()
            for segment in segments
        ])))
        top_segments = VGroup(*it.chain(
            self.groups[0][0],
            self.groups[2][0],
        ))
        bottom_segments = self.groups[1][0]
        for color in color_types:
            monochrome_groups = [
                # CHANGE: colour.Color vs GL hex-string colors: compare through Color / hex_l
                VGroup(*[segment for segment in segment_group if Color(segment.get_color()) == color])
                for segment_group in (top_segments, bottom_segments)
            ]
            labels = VGroup()
            for i, group in enumerate(monochrome_groups):
                group.save_state()
                group.generate_target()
                group.target.arrange(buff = SMALL_BUFF)
                brace = Brace(group.target, UP)
                label = VGroup(
                    OldTexText("Thief %d"%(i+1)),
                    Jewel(color = group[0].get_color())
                )
                label.arrange()
                label.next_to(brace, UP)
                full_group = VGroup(group.target, brace, label)
                vect = LEFT if i == 0 else RIGHT
                full_group.next_to(ORIGIN, vect, buff = MED_LARGE_BUFF)
                full_group.to_edge(UP)
                labels.add(VGroup(brace, label))
            equals = OldTex("=")
            equals.next_to(monochrome_groups[0].target, RIGHT)
            labels[-1].add(equals)

            for group, label in zip(monochrome_groups, labels):
                self.play(
                    MoveToTarget(group),
                    FadeIn(label),
                )
                self.wait()
            self.play(
                FadeOut(labels),
                *[group.restore for group in monochrome_groups]
            )
        self.wait()

    def perform_antipodal_swap(self):
        binary_choices_list = [(1, 0, 1), (0, 1, 0)]
        for binary_choices in binary_choices_list:
            self.play(*[
                ApplyMethod(
                    group.move_to,
                    group.target_points[choice]
                )
                for group, choice in zip(self.groups, binary_choices)
            ])
            self.wait()
