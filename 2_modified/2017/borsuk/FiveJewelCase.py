# ==============================================================================
# Scene:      FiveJewelCase
# Source:     videos/_2017/borsuk.py (lines 488-513)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FiveJewelCase.py FiveJewelCase -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - undefined name m1 in the sort key (NameError once init_points runs); sort the faces by z
#   - Python 2 integer division in slice indices
#   - GL get_color() is a hex string while color is a colour.Color: wrap for the comparison
#   - sorted(list, cmp_function) and cmp() are Python 2: sort with key=
#   - painter order: draw the faces from back to front (smaller z first); the first fix had the sign reversed
#   - broken 2to3 conversion of the cmp lambda (m1.get): sort the jewels left to right by x
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
            # CHANGE: GL get_color() is a hex string while color is a colour.Color: wrap for the comparison
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


class FiveJewelCase(IntroduceStolenNecklaceProblem):
    CONFIG = {
        "jewel_colors" : [BLUE, GREEN, WHITE, RED, YELLOW],
        "num_per_jewel" : [6, 4, 4, 2, 8],
        "forced_binary_choices" : (0, 1, 0, 1, 0, 1),
    }
    def construct(self):
        random.seed(self.random_seed)
        self.add(self.get_necklace())
        jewels = self.necklace.jewels
        self.shuffle_jewels(jewels, run_time = 0)
        self.jewel_types = self.get_jewels_organized_by_type(jewels)     
        self.add_title()
        self.add_thieves()
        for thief in self.thieves:
            ApplyMethod(thief.change_mode, "pondering").update(1)
            thief.look_at(self.necklace)
        self.divvy_with_n_cuts()

    def add_title(self):
        n_cuts = len(self.jewel_colors)
        title = OldTexText(
            "%d jewel types, %d cuts"%(n_cuts, n_cuts)
        )
        title.to_edge(UP)
        self.add(title)
