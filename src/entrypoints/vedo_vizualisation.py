import os
import time

import networkx as nx
import vedo
from src.entities.abstract_agent import AbstractAgent
from src.entities.knowledge_roadmap import KnowledgeRoadmap
from src.entities.local_grid import LocalGrid
from src.entrypoints.abstract_vizualisation import AbstractVizualisation
from src.utils.config import Config

# from vedo.pyplot import plot

vedo.settings.allowInteraction = True


class VedoVisualisation(AbstractVizualisation):
    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self.factor = 1 / self.cfg.LG_CELL_SIZE_M
        self.plt = vedo.Plotter(axes=13, sharecam=False, title="Knowledge Roadmap")

        map_pic = vedo.Picture(cfg.FULL_PATH)
        map_pic.x(-cfg.IMG_TOTAL_X_PIX // 2).y(-cfg.IMG_TOTAL_Y_PIX // 2)
        self.plt.show(map_pic, interactive=False)

        logo_path = os.path.join("resource", "KRM.png")
        logo = vedo.load(logo_path)
        self.plt.addIcon(logo, pos=1, size=0.15)

        self.wp_counter = []
        self.ft_counter = []

        time.sleep(0.1)

    def figure_update(
        self, krm: KnowledgeRoadmap, agent: AbstractAgent, lg: LocalGrid
    ) -> None:
        self.viz_all(krm, agent)

    def figure_final_result(
        self, krm: KnowledgeRoadmap, agent: AbstractAgent, lg: LocalGrid
    ) -> None:
        self.figure_update(krm, agent, lg)
        self.plt.show(interactive=True, resetcam=True)

    def viz_all(self, krm, agent):
        actors = []

        positions_of_all_nodes = nx.get_node_attributes(krm.graph, "pos")
        pos_dict = positions_of_all_nodes
        for pos in pos_dict:

            pos_dict[pos] = tuple([self.factor * x for x in pos_dict[pos]])

        ed_ls = list(krm.graph.edges)

        if len(ed_ls) > 1:
            raw_lines = [(pos_dict[x], pos_dict[y]) for x, y in ed_ls]

            raw_edg = vedo.Lines(raw_lines).lw(2)
            actors.append(raw_edg)

        waypoint_nodes = list(
            dict(
                (n, d["type"])
                for n, d in krm.graph.nodes().items()
                if d["type"] == "waypoint"
            ).keys()
        )

        frontier_nodes = list(
            dict(
                (n, d["type"])
                for n, d in krm.graph.nodes().items()
                if d["type"] == "frontier"
            ).keys()
        )

        wps = [pos_dict[wp] for wp in waypoint_nodes]
        self.wp_counter.append(len(wps))
        waypoints = vedo.Points(wps, r=8, c="r")
        actors.append(waypoints)

        fts = [pos_dict[f] for f in frontier_nodes]
        self.ft_counter.append(len(fts))
        frontiers = vedo.Points(fts, r=40, c="g", alpha=0.2)
        actors.append(frontiers)

        agent_pos = [self.factor * agent.pos[0], self.factor * agent.pos[1], 0]
        grid_len = self.factor * self.cfg.LG_LENGTH_IN_M
        local_grid_viz = vedo.Grid(pos=agent_pos, sx=grid_len, sy=grid_len)
        actors.append(local_grid_viz)
        agent_sphere = vedo.Point(agent_pos, r=25, c="b")
        actors.append(agent_sphere)

        self.plt.show(
            actors,
            interactive=False,
            # render=False,
            # sharecam=False,
            resetcam=False,
            # at=0
        )

    # def plot_stats(self):
    #     if len(self.wp_counter) > 1 and len(self.ft_counter) > 1:
    #         self.plt.clear(at=1)
    #         plot_wps = plot(self.wp_counter, "r")
    #         plot_wps.overlayPlot(self.ft_counter, "b")
    #         # plot(self.wp_counter, "r").plot(self.ft_counter, "bo-").show(at=1)
    #         # plot(self.wp_counter, "r").plot(self.ft_counter, "bo-").show()
    #         # plot_fts = plot(self.ft_counter)

    #         # plot_wps.x(0.7 * self.cfg.IMG_TOTAL_X_PIX)
    #         # plot_wps.show()
    #         self.plt.add(plot_wps, at=1, render=False)
