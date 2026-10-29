# ==============================================================================
# Scene:      BreakUpMicroPatterns
# Source:     videos/_2017/nn/part1.py (lines 1766-1874)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BreakUpMicroPatterns.py BreakUpMicroPatterns -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - Python 2 integer division used as an index/count -> //.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2017/nn/nn_pkg/mnist_mini.npz (synthetic MNIST stand-in, built from the 100 real digits of image_map by make_nn_support.py)
# ==============================================================================

import sys
import os.path
from manim_imports_ext import *
import warnings
# CHANGE: Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
import sys, os.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # CL17-B
from nn.network import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class WrappedImage(Group):
    CONFIG = {
        "rect_kwargs" : {
            "color" : BLUE,
            "buff" : SMALL_BUFF,
        }
    }
    def __init__(self, image_mobject, **kwargs):
        Group.__init__(self, **kwargs)
        rect = SurroundingRectangle(
            image_mobject, **self.rect_kwargs
        )
        self.add(rect, image_mobject)


class PixelsAsSquares(VGroup):
    CONFIG = {
        "height" : 2,
    }
    def __init__(self, image_mobject, **kwargs):
        VGroup.__init__(self, **kwargs)
        for row in image_mobject.pixel_array:
            for rgba in row:
                square = Square(
                    stroke_width = 0, 
                    fill_opacity = rgba[3]/255.0,
                    fill_color = rgba_to_color(rgba/255.0),
                )
                self.add(square)
        self.arrange_in_grid(
            *image_mobject.pixel_array.shape[:2],
            buff = 0
        )
        self.replace(image_mobject)


class PixelsFromVect(PixelsAsSquares):
    def __init__(self, vect, **kwargs):
        PixelsAsSquares.__init__(self,
            ImageMobject(layer_to_image_array(vect)),
            **kwargs
        )


class MNistMobject(WrappedImage):
    def __init__(self, vect, **kwargs):
        WrappedImage.__init__(self, 
            ImageMobject(layer_to_image_array(vect)),
            **kwargs
        )


class NetworkMobject(VGroup):
    CONFIG = {
        "neuron_radius" : 0.15,
        "neuron_to_neuron_buff" : MED_SMALL_BUFF,
        "layer_to_layer_buff" : LARGE_BUFF,
        "neuron_stroke_color" : BLUE,
        "neuron_stroke_width" : 3,
        "neuron_fill_color" : GREEN,
        "edge_color" : GREY_B,
        "edge_stroke_width" : 2,
        "edge_propogation_color" : YELLOW,
        "edge_propogation_time" : 1,
        "max_shown_neurons" : 16,
        "brace_for_large_layers" : True,
        "average_shown_activation_of_large_layer" : True,
        "include_output_labels" : False,
    }
    def __init__(self, neural_network, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.neural_network = neural_network
        self.layer_sizes = neural_network.sizes
        self.add_neurons()
        self.add_edges()

    def add_neurons(self):
        layers = VGroup(*[
            self.get_layer(size)
            for size in self.layer_sizes
        ])
        layers.arrange(RIGHT, buff = self.layer_to_layer_buff)
        self.layers = layers
        self.add(self.layers)
        if self.include_output_labels:
            self.add_output_labels()

    def get_layer(self, size):
        layer = VGroup()
        n_neurons = size
        if n_neurons > self.max_shown_neurons:
            n_neurons = self.max_shown_neurons
        neurons = VGroup(*[
            Circle(
                radius = self.neuron_radius,
                stroke_color = self.neuron_stroke_color,
                stroke_width = self.neuron_stroke_width,
                fill_color = self.neuron_fill_color,
                fill_opacity = 0,
            )
            for x in range(n_neurons)
        ])   
        neurons.arrange(
            DOWN, buff = self.neuron_to_neuron_buff
        )
        for neuron in neurons:
            neuron.edges_in = VGroup()
            neuron.edges_out = VGroup()
        layer.neurons = neurons
        layer.add(neurons)

        if size > n_neurons:
            dots = OldTex("\\vdots")
            dots.move_to(neurons)
            VGroup(*neurons[:len(neurons) // 2]).next_to(
                dots, UP, MED_SMALL_BUFF
            )
            VGroup(*neurons[len(neurons) // 2:]).next_to(
                dots, DOWN, MED_SMALL_BUFF
            )
            layer.dots = dots
            layer.add(dots)
            if self.brace_for_large_layers:
                brace = Brace(layer, LEFT)
                brace_label = brace.get_tex(str(size))
                layer.brace = brace
                layer.brace_label = brace_label
                layer.add(brace, brace_label)

        return layer

    def add_edges(self):
        self.edge_groups = VGroup()
        for l1, l2 in zip(self.layers[:-1], self.layers[1:]):
            edge_group = VGroup()
            for n1, n2 in it.product(l1.neurons, l2.neurons):
                edge = self.get_edge(n1, n2)
                edge_group.add(edge)
                n1.edges_out.add(edge)
                n2.edges_in.add(edge)
            self.edge_groups.add(edge_group)
        self.add_to_back(self.edge_groups)

    def get_edge(self, neuron1, neuron2):
        return Line(
            neuron1.get_center(),
            neuron2.get_center(),
            buff = self.neuron_radius,
            stroke_color = self.edge_color,
            stroke_width = self.edge_stroke_width,
        )

    def get_active_layer(self, layer_index, activation_vector):
        layer = self.layers[layer_index].deepcopy()
        self.activate_layer(layer, activation_vector)
        return layer

    def activate_layer(self, layer, activation_vector):
        n_neurons = len(layer.neurons)
        av = activation_vector
        def arr_to_num(arr):
            return (np.sum(arr > 0.1) / float(len(arr)))**(1./3)

        if len(av) > n_neurons:
            if self.average_shown_activation_of_large_layer:
                indices = np.arange(n_neurons)
                indices *= int(len(av)/n_neurons)
                indices = list(indices)
                indices.append(len(av))
                av = np.array([
                    arr_to_num(av[i1:i2])
                    for i1, i2 in zip(indices[:-1], indices[1:])
                ])
            else:
                av = np.append(
                    av[:n_neurons//2],  # CHANGE: Python 2 integer division used as an index/count -> //.
                    av[-n_neurons//2:],  # CHANGE: Python 2 integer division used as an index/count -> //.
                )
        for activation, neuron in zip(av, layer.neurons):
            neuron.set_fill(
                color = self.neuron_fill_color,
                opacity = activation
            )
        return layer

    def activate_layers(self, input_vector):
        activations = self.neural_network.get_activation_of_all_layers(input_vector)
        for activation, layer in zip(activations, self.layers):
            self.activate_layer(layer, activation)

    def deactivate_layers(self):
        all_neurons = VGroup(*it.chain(*[
            layer.neurons
            for layer in self.layers
        ]))
        all_neurons.set_fill(opacity = 0)
        return self

    def get_edge_propogation_animations(self, index):
        edge_group_copy = self.edge_groups[index].copy()
        edge_group_copy.set_stroke(
            self.edge_propogation_color,
            width = 1.5*self.edge_stroke_width
        )
        return [ShowCreationThenDestruction(
            edge_group_copy, 
            run_time = self.edge_propogation_time,
            lag_ratio = 0.5
        )]

    def add_output_labels(self):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[-1].neurons):
            label = OldTex(str(n))
            label.set_height(0.75*neuron.get_height())
            label.move_to(neuron)
            label.shift(neuron.get_width()*RIGHT)
            self.output_labels.add(label)
        self.add(self.output_labels)


class MNistNetworkMobject(NetworkMobject):
    CONFIG = {
        "neuron_to_neuron_buff" : SMALL_BUFF,
        "layer_to_layer_buff" : 1.5,
        "edge_stroke_width" : 1,
        "include_output_labels" : True,
    }

    def __init__(self, **kwargs):
        network = get_pretrained_network()
        NetworkMobject.__init__(self, network, **kwargs)


class NetworkScene(Scene):
    CONFIG = {
        "layer_sizes" : [8, 6, 6, 4],
        "network_mob_config" : {},
    }
    def setup(self):
        self.add_network()

    def add_network(self):
        self.network = Network(sizes = self.layer_sizes)
        self.network_mob = NetworkMobject(
            self.network,
            **self.network_mob_config
        )
        self.add(self.network_mob)

    def feed_forward(self, input_vector, false_confidence = False, added_anims = None):
        if added_anims is None:
            added_anims = []
        activations = self.network.get_activation_of_all_layers(
            input_vector
        )
        if false_confidence:
            i = np.argmax(activations[-1])
            activations[-1] *= 0
            activations[-1][i] = 1.0
        for i, activation in enumerate(activations):
            self.show_activation_of_layer(i, activation, added_anims)
            added_anims = []

    def show_activation_of_layer(self, layer_index, activation_vector, added_anims = None):
        if added_anims is None:
            added_anims = []
        layer = self.network_mob.layers[layer_index]
        active_layer = self.network_mob.get_active_layer(
            layer_index, activation_vector
        )
        anims = [Transform(layer, active_layer)]
        if layer_index > 0:
            anims += self.network_mob.get_edge_propogation_animations(
                layer_index-1
            )
        anims += added_anims
        self.play(*anims)

    def remove_random_edges(self, prop = 0.9):
        for edge_group in self.network_mob.edge_groups:
            for edge in list(edge_group):
                if np.random.random() < prop:
                    edge_group.remove(edge)


def make_transparent(image_mob):
    alpha_vect = np.array(
        image_mob.pixel_array[:,:,0],
        dtype = 'uint8'
    )
    image_mob.set_color(WHITE)
    image_mob.pixel_array[:,:,3] = alpha_vect
    return image_mob


class PreviewMNistNetwork(NetworkScene):
    CONFIG = {
        "n_examples" : 15,
        "network_mob_config" : {},
    }
    def construct(self):
        self.remove_random_edges(0.7) #Remove?

        training_data, validation_data, test_data = load_data_wrapper()
        for data in test_data[:self.n_examples]:
            self.feed_in_image(data[0])

    def feed_in_image(self, in_vect):
        image = PixelsFromVect(in_vect)
        image.next_to(self.network_mob, LEFT, LARGE_BUFF, UP)
        image.shift_onto_screen()
        image_rect = SurroundingRectangle(image, color = BLUE)
        start_neurons = self.network_mob.layers[0].neurons.copy()
        start_neurons.set_stroke(WHITE, width = 0)
        start_neurons.set_fill(WHITE, 0)

        self.play(FadeIn(image), FadeIn(image_rect))
        self.feed_forward(in_vect, added_anims = [
            self.get_image_to_layer_one_animation(image, start_neurons)
        ])
        n = np.argmax([
            neuron.get_fill_opacity()
            for neuron in self.network_mob.layers[-1].neurons
        ])
        rect = SurroundingRectangle(VGroup(
            self.network_mob.layers[-1].neurons[n],
            self.network_mob.output_labels[n],
        ))
        self.play(ShowCreation(rect))
        self.reset_display(rect, image, image_rect)

    def reset_display(self, answer_rect, image, image_rect):
        self.play(FadeOut(answer_rect))
        self.play(
            FadeOut(image),
            FadeOut(image_rect),
            self.network_mob.deactivate_layers,
        )

    def get_image_to_layer_one_animation(self, image, start_neurons):
        image_mover = VGroup(*[
            pixel.copy()
            for pixel in image
            if pixel.fill_rgb[0] > 0.1
        ])
        return Transform(
            image_mover, start_neurons, 
            remover = True,
            run_time = 1,
        )

    ###

    def add_network(self):
        self.network_mob = MNistNetworkMobject(**self.network_mob_config)
        self.network = self.network_mob.neural_network
        self.add(self.network_mob)


class IntroduceEachLayer(PreviewMNistNetwork):
    CONFIG = {
        "network_mob_config" : {
            "neuron_stroke_color" : WHITE,
            "neuron_stroke_width" : 2,
            "neuron_fill_color" : WHITE,
            "average_shown_activation_of_large_layer" : False,
            "edge_propogation_color" : YELLOW,
            "edge_propogation_time" : 2,
        }
    }
    def construct(self):
        self.setup_network_mob()
        self.break_up_image_as_neurons()
        self.show_activation_of_one_neuron()
        self.transform_into_full_network()
        self.show_output_layer()
        self.show_hidden_layers()
        self.show_propogation()

    def setup_network_mob(self):
        self.remove(self.network_mob)

    def break_up_image_as_neurons(self):
        self.image_map = get_organized_images()
        image = self.image_map[9][0]
        image_mob = PixelsFromVect(image)
        image_mob.set_height(4)
        image_mob.next_to(ORIGIN, LEFT)
        rect = SurroundingRectangle(image_mob, color = BLUE)
        neurons = VGroup()
        for pixel in image_mob:
            pixel.set_fill(WHITE, opacity = pixel.fill_rgb[0])
            neuron = Circle(
                color = WHITE,
                stroke_width = 1,
                radius = pixel.get_width()/2
            )
            neuron.move_to(pixel)
            neuron.set_fill(WHITE, pixel.get_fill_opacity())
            neurons.add(neuron)
        neurons.scale(1.2)
        neurons.space_out_submobjects(1.3)
        neurons.to_edge(DOWN)

        braces = VGroup(*[Brace(neurons, vect) for vect in (LEFT, UP)])
        labels = VGroup(*[
            brace.get_tex("28", buff = SMALL_BUFF) 
            for brace in braces
        ])

        equation = OldTex("28", "\\times", "28", "=", "784")
        equation.next_to(neurons, RIGHT, LARGE_BUFF, UP)

        self.corner_image = MNistMobject(image)
        self.corner_image.to_corner(UP+LEFT)

        self.add(image_mob, rect)
        self.wait()
        self.play(
            ReplacementTransform(image_mob, neurons),
            FadeOut(rect),
            FadeIn(braces),
            FadeIn(labels),
        )
        self.wait()
        self.play(
            ReplacementTransform(labels[0].copy(), equation[0]),
            Write(equation[1]),
            ReplacementTransform(labels[1].copy(), equation[2]),
            Write(equation[3]),
            Write(equation[4]),
        )
        self.wait()

        self.neurons = neurons
        self.braces = braces
        self.brace_labels = labels
        self.num_pixels_equation = equation
        self.image_vect = image

    def show_activation_of_one_neuron(self):
        neurons = self.neurons
        numbers = VGroup()
        example_neuron = None
        example_num = None
        for neuron in neurons:
            o = neuron.get_fill_opacity()
            num = DecimalNumber(o, num_decimal_places = 1)
            num.set_width(0.7*neuron.get_width())
            num.move_to(neuron)
            if o > 0.8:
                num.set_fill(BLACK)
            numbers.add(num)
            if o > 0.25 and o < 0.75 and example_neuron is None:
                example_neuron = neuron
                example_num = num
                example_neuron.save_state()
                example_num.save_state()
        example_neuron.generate_target()
        example_neuron.target.set_height(1.5)
        example_neuron.target.next_to(neurons, RIGHT)
        example_num.target = DecimalNumber(
            example_neuron.get_fill_opacity()
        )
        example_num.target.move_to(example_neuron.target)

        def change_activation(num):
            self.play(
                example_neuron.set_fill, None, num,
                ChangingDecimal(
                    example_num,
                    lambda a : example_neuron.get_fill_opacity(),
                ),
                UpdateFromFunc(
                    example_num,
                    lambda m : m.set_fill(
                        BLACK if example_neuron.get_fill_opacity() > 0.8 else WHITE
                    )
                )
            )

        self.play(LaggedStartMap(FadeIn, numbers))
        self.play(
            MoveToTarget(example_neuron),
            MoveToTarget(example_num)
        )
        self.wait()
        curr_opacity = example_neuron.get_fill_opacity()
        for num in 0.3, 0.01, 1.0, curr_opacity:
            change_activation(num)
            self.wait()

        rect = SurroundingRectangle(example_num, color = YELLOW)
        activation = OldTexText("``Activation''")
        activation.next_to(example_neuron, RIGHT)
        activation.set_color(rect.get_color())
        self.play(ShowCreation(rect))
        self.play(Write(activation, run_time = 1))
        self.wait()
        change_activation(1.0)
        self.wait()
        change_activation(0.2)
        self.wait()

        self.play(
            example_neuron.restore,
            example_num.restore,
            FadeOut(activation),
            FadeOut(rect),
        )
        self.play(FadeOut(numbers))

    def transform_into_full_network(self):
        network_mob = self.network_mob
        neurons = self.neurons
        layer = network_mob.layers[0]
        layer.save_state()
        layer.rotate(np.pi/2)
        layer.center()
        layer.brace_label.rotate(-np.pi/2)
        n = network_mob.max_shown_neurons//2  # CHANGE: Python 2 integer division used as an index/count -> //.

        rows = VGroup(*[
            VGroup(*neurons[28*i:28*(i+1)])
            for i in range(28)
        ])

        self.play(
            FadeOut(self.braces),
            FadeOut(self.brace_labels),
            FadeOut(VGroup(*self.num_pixels_equation[:-1]))
        )

        self.play(rows.space_out_submobjects, 1.2)
        self.play(
            rows.arrange, RIGHT, buff = SMALL_BUFF,
            path_arc = np.pi/2,
            run_time = 2
        )
        self.play(
            ReplacementTransform(
                VGroup(*neurons[:n]), 
                VGroup(*layer.neurons[:n]),
            ),
            ReplacementTransform(
                VGroup(*neurons[n:-n]), 
                layer.dots,
            ),
            ReplacementTransform(
                VGroup(*neurons[-n:]), 
                VGroup(*layer.neurons[-n:]),
            ),
        )
        self.play(
            ReplacementTransform(
                self.num_pixels_equation[-1],
                layer.brace_label
            ),
            FadeIn(layer.brace),
        )
        self.play(layer.restore, FadeIn(self.corner_image))
        self.wait()
        for edge_group, layer in zip(network_mob.edge_groups, network_mob.layers[1:]):
            self.play(
                LaggedStartMap(FadeIn, layer, run_time = 1),
                ShowCreation(edge_group),
            )
        self.wait()

    def show_output_layer(self):
        layer = self.network_mob.layers[-1]
        labels = self.network_mob.output_labels
        rect = SurroundingRectangle(
            VGroup(layer, labels)
        )
        neuron = layer.neurons[-1]
        neuron.set_fill(WHITE, 0)
        label = labels[-1]
        for mob in neuron, label:
            mob.save_state()
            mob.generate_target()
        neuron.target.scale(4)
        neuron.target.shift(1.5*RIGHT)
        label.target.scale(1.5)
        label.target.next_to(neuron.target, RIGHT)

        activation = DecimalNumber(0)
        activation.move_to(neuron.target)

        def change_activation(num):
            self.play(
                neuron.set_fill, None, num,
                ChangingDecimal(
                    activation,
                    lambda a : neuron.get_fill_opacity(),
                ),
                UpdateFromFunc(
                    activation,
                    lambda m : m.set_fill(
                        BLACK if neuron.get_fill_opacity() > 0.8 else WHITE
                    )
                )
            )

        self.play(ShowCreation(rect))
        self.play(LaggedStartMap(FadeIn, labels))
        self.wait()
        self.play(
            MoveToTarget(neuron),
            MoveToTarget(label),
        )
        self.play(FadeIn(activation))
        for num in 0.5, 0.38, 0.97:
            change_activation(num)
            self.wait()
        self.play(
            neuron.restore,
            neuron.set_fill, None, 1,
            label.restore,
            FadeOut(activation),
            FadeOut(rect),
        )
        self.wait()

    def show_hidden_layers(self):
        hidden_layers = VGroup(*self.network_mob.layers[1:3])
        rect = SurroundingRectangle(hidden_layers, color = YELLOW)
        name = OldTexText("``Hidden layers''")
        name.next_to(rect, UP, SMALL_BUFF)
        name.set_color(YELLOW)
        q_marks = VGroup()
        for layer in hidden_layers:
            for neuron in layer.neurons:
                q_mark = OldTexText("?")
                q_mark.set_height(0.8*neuron.get_height())
                q_mark.move_to(neuron)
                q_marks.add(q_mark)
        q_marks.set_color_by_gradient(BLUE, YELLOW)
        q_mark = OldTexText("?").scale(4)
        q_mark.move_to(hidden_layers)
        q_mark.set_color(YELLOW)
        q_marks.add(q_mark)

        self.play(
            ShowCreation(rect),
            Write(name)
        )
        self.wait()
        self.play(Write(q_marks))
        self.wait()
        self.play(
            FadeOut(q_marks),
            Animation(q_marks[-1].copy())
        )

    def show_propogation(self):
        self.revert_to_original_skipping_status()
        self.remove_random_edges(0.7)
        self.feed_forward(self.image_vect)


class BreakUpMacroPatterns(IntroduceEachLayer):
    CONFIG = {
        "camera_config" : {"background_opacity" : 1},
        "prefixes" : [
            "nine", "eight", "four",
            "upper_loop", "right_line",
            "lower_loop", "horizontal_line",
            "upper_left_line"
        ]
    }
    def construct(self):
        self.setup_network_mob()
        self.setup_needed_patterns()
        self.setup_added_patterns()
        self.show_nine()
        self.show_eight()
        self.show_four()
        self.show_second_to_last_layer()
        self.show_upper_loop_activation()
        self.show_what_learning_is_required()

    def setup_needed_patterns(self):
        prefixes = self.prefixes
        vects = [
            np.array(Image.open(
                get_full_raster_image_path("handwritten_" + p),
            ))[:,:,0].flatten()/255.0
            for p in prefixes
        ]
        mobjects = list(map(MNistMobject, vects))
        for mob in mobjects:
            image = mob[1]
            self.make_transparent(image)
        for prefix, mob in zip(prefixes, mobjects):
            setattr(self, prefix, mob)

    def setup_added_patterns(self):
        image_map = get_organized_images()
        two, three, five = mobs = [
            MNistMobject(image_map[n][0])
            for n in (2, 3, 5)
        ]
        self.added_patterns = VGroup()
        for mob in mobs:
            for i, j in it.product([0, 14], [0, 14]):
                pattern = mob.deepcopy()
                pa = pattern[1].pixel_array
                temp = np.array(pa[i:i+14,j:j+14,:], dtype = 'uint8')
                pa[:,:] = 0
                pa[i:i+14,j:j+14,:] = temp
                self.make_transparent(pattern[1])
                pattern[1].set_color(random_bright_color())
                self.added_patterns.add(pattern)
        self.image_map = image_map

    def show_nine(self):
        nine = self.nine
        upper_loop = self.upper_loop
        right_line = self.right_line
        equation = self.get_equation(nine, upper_loop, right_line)
        equation.to_edge(UP)
        equation.shift(LEFT)

        parts = [upper_loop[1], right_line[1]]
        for mob, color in zip(parts, [YELLOW, RED]):
            mob.set_color(color)
            mob.save_state()
            mob.move_to(nine)
        right_line[1].pixel_array[:14,:,3] = 0

        self.play(FadeIn(nine))
        self.wait()
        self.play(*list(map(FadeIn, parts)))
        self.wait()
        self.play(
            Write(equation[1]),
            upper_loop[1].restore,
            FadeIn(upper_loop[0])
        )
        self.wait()
        self.play(
            Write(equation[3]),
            right_line[1].restore,
            FadeIn(right_line[0]),
        )
        self.wait()

        self.nine_equation = equation

    def show_eight(self):
        eight = self.eight
        upper_loop = self.upper_loop.deepcopy()
        lower_loop = self.lower_loop
        lower_loop[1].set_color(GREEN)

        equation = self.get_equation(eight, upper_loop, lower_loop)
        equation.next_to(self.nine_equation, DOWN)

        lower_loop[1].save_state()
        lower_loop[1].move_to(eight[1])

        self.play(
            FadeIn(eight),
            Write(equation[1]),
        )
        self.play(ReplacementTransform(
            self.upper_loop.copy(),
            upper_loop
        ))
        self.wait()
        self.play(FadeIn(lower_loop[1]))
        self.play(
            Write(equation[3]),
            lower_loop[1].restore,
            FadeIn(lower_loop[0]),
        )
        self.wait()

        self.eight_equation = equation

    def show_four(self):
        four = self.four
        upper_left_line = self.upper_left_line
        upper_left_line[1].set_color(BLUE)
        horizontal_line = self.horizontal_line
        horizontal_line[1].set_color(MAROON_B)
        right_line = self.right_line.deepcopy()
        equation = self.get_equation(four, right_line, upper_left_line, horizontal_line)
        equation.next_to(
            self.eight_equation, DOWN, aligned_edge = LEFT
        )

        self.play(
            FadeIn(four),
            Write(equation[1])
        )
        self.play(ReplacementTransform(
            self.right_line.copy(), right_line
        ))
        self.play(LaggedStartMap(
            FadeIn, VGroup(*equation[3:])
        ))
        self.wait(2)

        self.four_equation = equation

    def show_second_to_last_layer(self):
        everything = VGroup(*it.chain(
            self.nine_equation,
            self.eight_equation,
            self.four_equation,
        ))
        patterns = VGroup(
            self.upper_loop,
            self.lower_loop,
            self.right_line,
            self.upper_left_line,
            self.horizontal_line,
            *self.added_patterns[:11]
        )
        for pattern in patterns:
            pattern.add_to_back(
                pattern[1].copy().set_color(BLACK, alpha = 1)
            )
        everything.remove(*patterns)
        network_mob = self.network_mob
        layer = network_mob.layers[-2]
        patterns.generate_target()
        for pattern, neuron in zip(patterns.target, layer.neurons):
            pattern.set_height(neuron.get_height())
            pattern.next_to(neuron, RIGHT, SMALL_BUFF)
        for pattern in patterns[5:]:
            pattern.fade(1)

        self.play(*list(map(FadeOut, everything)))
        self.play(
            FadeIn(
                network_mob,
                lag_ratio = 0.5,
                run_time = 3,
            ),
            MoveToTarget(patterns)
        )
        self.wait(2)

        self.patterns = patterns

    def show_upper_loop_activation(self):
        neuron = self.network_mob.layers[-2].neurons[0]
        words = OldTexText("Upper loop neuron...maybe...")
        words.scale(0.8)
        words.next_to(neuron, UP)
        words.shift(RIGHT)
        rect = SurroundingRectangle(VGroup(
            neuron, self.patterns[0]
        ))
        nine = self.nine
        upper_loop = self.upper_loop.copy()
        upper_loop.remove(upper_loop[0])
        upper_loop.replace(nine)
        nine.add(upper_loop)
        nine.to_corner(UP+LEFT)
        self.remove_random_edges(0.7)
        self.network.get_activation_of_all_layers = lambda v : [
            np.zeros(784),
            sigmoid(6*(np.random.random(16)-0.5)),
            np.array([1, 0, 1] + 13*[0]),
            np.array(9*[0] + [1])
        ]

        self.play(FadeIn(nine))
        self.play(
            ShowCreation(rect),
            Write(words)
        )
        self.add_foreground_mobject(self.patterns)
        self.feed_forward(np.random.random(784))
        self.wait(2)

    def show_what_learning_is_required(self):
        edge_group = self.network_mob.edge_groups[-1].copy()
        edge_group.set_stroke(YELLOW, 4)
        for x in range(3):
            self.play(LaggedStartMap(
                ShowCreationThenDestruction, edge_group,
                run_time = 3
            ))
            self.wait()

    ######

    def get_equation(self, *mobs):
        equation = VGroup(
            mobs[0], OldTex("=").scale(2),
            *list(it.chain(*[
                [m, OldTex("+").scale(2)]
                for m in mobs[1:-1]
            ])) + [mobs[-1]]
        )
        equation.arrange(RIGHT)
        return equation

    def make_transparent(self, image_mob):
        return make_transparent(image_mob)
        alpha_vect = np.array(
            image_mob.pixel_array[:,:,0],
            dtype = 'uint8'
        )
        image_mob.set_color(WHITE)
        image_mob.pixel_array[:,:,3] = alpha_vect
        return image_mob


class BreakUpMicroPatterns(BreakUpMacroPatterns):
    CONFIG = {
        "prefixes" : [
            "loop",
            "loop_edge1",
            "loop_edge2",
            "loop_edge3",
            "loop_edge4",
            "loop_edge5",
            "right_line",
            "right_line_edge1",
            "right_line_edge2",
            "right_line_edge3",
        ]
    }
    def construct(self):
        self.setup_network_mob()
        self.setup_needed_patterns()

        self.break_down_loop()
        self.break_down_long_line()

    def break_down_loop(self):
        loop = self.loop
        loop[0].set_color(WHITE)
        edges = Group(*[
            getattr(self, "loop_edge%d"%d)
            for d in range(1, 6)
        ])
        colors = color_gradient([BLUE, YELLOW, RED], 5)
        for edge, color in zip(edges, colors):
            for mob in edge:
                mob.set_color(color)
        loop.generate_target()
        edges.generate_target()
        for edge in edges:
            edge[0].set_stroke(width = 0)
            edge.save_state()
            edge[1].set_opacity(0)
        equation = self.get_equation(loop.target, *edges.target)
        equation.set_width(FRAME_WIDTH - 1)
        equation.to_edge(UP)
        symbols = VGroup(*equation[1::2])

        randy = Randolph()
        randy.to_corner(DOWN+LEFT)

        self.add(randy)
        self.play(
            FadeIn(loop),
            randy.change, "pondering", loop
        )
        self.play(Blink(randy))
        self.wait()
        self.play(LaggedStartMap(
            ApplyMethod, edges,
            lambda e : (e.restore,),
            run_time = 4
        ))
        self.wait()
        self.play(
            MoveToTarget(loop, run_time = 2),
            MoveToTarget(edges, run_time = 2),
            Write(symbols),
            randy.change, "happy", equation,
        )
        self.wait()

        self.loop_equation = equation
        self.randy = randy

    def break_down_long_line(self):
        randy = self.randy
        line = self.right_line
        line[0].set_color(WHITE)
        edges = Group(*[
            getattr(self, "right_line_edge%d"%d)
            for d in range(1, 4)
        ])
        colors = Color(MAROON_B).range_to(PURPLE, 3)
        for edge, color in zip(edges, colors):
            for mob in edge:
                mob.set_color(color)
        equation = self.get_equation(line, *edges)
        equation.set_height(self.loop_equation.get_height())
        equation.next_to(
            self.loop_equation, DOWN, MED_LARGE_BUFF, LEFT
        )
        image_map = get_organized_images()
        digits = VGroup(*[
            MNistMobject(image_map[n][1])
            for n in (1, 4, 7)
        ])
        digits.arrange(RIGHT)
        digits.next_to(randy, RIGHT)

        self.revert_to_original_skipping_status()
        self.play(
            FadeIn(line),
            randy.change, "hesitant", line
        )
        self.play(Blink(randy))
        self.play(LaggedStartMap(FadeIn, digits))
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, Group(*equation[1:])),
            randy.change, "pondering", equation
        )
        self.wait(3)
