# ==============================================================================
# Scene:      BayesianNetworkPreview
# Source:     videos/_2018/eop/bayes.py (lines 1143-1239)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BayesianNetworkPreview.py BayesianNetworkPreview -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - node.children/node.parents renamed to bn_children/bn_parents (GL Mobject.parents is an internal list)
# ==============================================================================

from manim_imports_ext import *

class BayesianNetworkPreview(Scene):
    def construct(self):
        self.add_network()
        self.show_propogation(self.network.nodes[0])
        self.show_propogation(self.network.nodes[-1])

    def add_network(self):
        radius = MED_SMALL_BUFF
        node = Circle(color = WHITE, radius = radius)
        node.shift(2*DOWN)
        nodes = VGroup(*[
            node.copy().shift(x*RIGHT + y*UP)
            for x, y in [
                (-1, 0),  
                (1, 0),
                (-2, 2),
                (0, 2),
                (2, 2),
                (-2, 4),
                (0, 4),
            ]
        ])
        for node in nodes:
            # CHANGE: renamed node.children/node.parents to bn_children/bn_parents: GL Mobject already uses .parents (a list) internally
            node.bn_children = VGroup()
            node.bn_parents = VGroup()
            node.outgoing_edges = VGroup()
        edge_index_pairs = [
            (2, 0),
            (3, 0),
            (3, 1),
            (4, 1),
            (5, 2),
            (6, 3),
        ]
        edges = VGroup()
        for i1, i2 in edge_index_pairs:
            n1, n2 = nodes[i1], nodes[i2]
            edge = Arrow(
                n1.get_center(), 
                n2.get_center(),
                buff = radius,
                color = WHITE,
            )
            n1.outgoing_edges.add(edge)
            edges.add(edge)
            n1.bn_children.add(n2)
            n2.bn_parents.add(n1)

        network = VGroup(nodes, edges)
        network.nodes = nodes
        network.edges = edges
        self.add(network)
        self.network = network

    def show_propogation(self, node):
        self.set_network_fills()
        all_ghosts = VGroup()
        curr_nodes = [node]
        covered_nodes = set()
        self.play(GrowFromCenter(node.fill))
        self.remove(node.fill)
        while curr_nodes:
            next_nodes = set([])
            anims = []
            for node in curr_nodes:
                node.ghost = node.fill.copy().fade()
                self.add(node.ghost)
                all_ghosts.add(node.ghost)
                connected_nodes = [n for n in it.chain(node.bn_children, node.bn_parents) if n not in covered_nodes]
                for next_node in connected_nodes:
                    if next_node in covered_nodes:
                        continue
                    next_nodes.add(next_node)
                    anims.append(Transform(
                        node.fill.copy(), next_node.fill,
                        remover = True
                    ))
                if len(connected_nodes) == 0:
                    anims.append(FadeOut(node.fill))
            if anims:
                self.play(*anims)
            covered_nodes.update(curr_nodes)
            curr_nodes = list(next_nodes)
        self.wait()
        self.play(FadeOut(all_ghosts))


    def set_network_fills(self):
        for node in self.network.nodes:
            node.fill = self.get_fill(node)


    def get_fill(self, node):
        fill = node.copy()
        fill.set_fill(YELLOW, 1)
        fill.set_stroke(width = 0)
        return fill
