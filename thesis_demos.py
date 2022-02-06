import matplotlib.pyplot as plt
import os
from PIL import Image

from knowledge_roadmap.entities.agent import Agent
from knowledge_roadmap.data_providers.manual_graph_world import *
from knowledge_roadmap.entrypoints.GUI import GUI
from knowledge_roadmap.usecases.exploration_usecase import ExplorationUsecase
from knowledge_roadmap.data_providers.local_grid_adapter import LocalGridAdapter
from knowledge_roadmap.entities.knowledge_roadmap import KnowledgeRoadmap
from knowledge_roadmap.entities.local_grid import LocalGrid
from config import Configuration

import matplotlib

matplotlib.use("Tkagg")

############################################################################################
# DEMONSTRATIONS
############################################################################################

def exploration_with_sampling_viz(plotting="none") -> bool:
    # this is the prior image of the villa we can include for visualization purposes
    # It is different from the map we use to emulate the local grid.
    cfg = Configuration()
    step = 0


    upside_down_map_img = Image.open(cfg.full_path)
    map_img = img_axes2world_axes(upside_down_map_img)
    world = ManualGraphWorld()
    gui = GUI(
        map_img=map_img,
        origin_x_offset=cfg.total_map_len_m_x / 2,
        origin_y_offset=cfg.total_map_len_m_y / 2,
    )

    # gui.preview_graph_world(world)
    agent = Agent(debug=False, start_pos=cfg.agent_start_pos)
    krm = KnowledgeRoadmap(start_pos=agent.pos)

    debug_container = {
        "world": world,
        "agent": agent,
        "gui": gui,
    }

    lga = LocalGridAdapter(
        img_length_in_m=cfg.total_map_len_m,
        mode="spoof",
        num_cells=cfg.lg_num_cells,
        cell_size_m=cfg.lg_cell_size_m,
        debug_container=debug_container,
    )

    exploration_use_case = ExplorationUsecase(
        agent,
        debug=False,
        len_of_map=cfg.total_map_len_m,
        lg_num_cells=cfg.lg_num_cells,
        lg_length_scale=cfg.lg_length_in_m / 2,
    )

    exploration_completed = False
    while agent.no_more_frontiers == False:

        local_grid_img = lga.get_local_grid(mode="spoof")

        lg = LocalGrid(
            world_pos=agent.pos,
            data=local_grid_img,
            length_in_m=cfg.lg_length_in_m,
            cell_size_in_m=cfg.lg_cell_size_m,
        )

        exploration_completed = exploration_use_case.run_exploration_step(
            agent, krm, lg
        )
        if exploration_completed:
            continue
        if plotting == "all" or plotting == "intermediate only":
            close_nodes = krm.get_nodes_of_type_in_margin(
                lg.world_pos, cfg.lg_length_in_m / 2, "waypoint"
            )
            points = [krm.get_node_data_by_idx(node)["pos"] for node in close_nodes]
            if points:
                gui.viz_collision_line_to_points_in_world_coord(points, lg)
            gui.viz_krm(krm)
            gui.draw_agent(agent.pos, rec_len=cfg.lg_length_in_m)
            gui.plot_unzoomed_world_coord(lg)
            plt.pause(0.001)

        print(f"step= {step}")
        step += 1
    if plotting == "result only" or plotting == "all":
        plt.figure(1)
        gui.viz_krm(krm)
        gui.draw_agent(agent.pos, rec_len=cfg.lg_length_in_m)

        plt.pause(0.001)
        plt.ioff()
        plt.show()
        return exploration_completed



if __name__ == "__main__":

    # exploration_with_sampling_viz("result only")
    # exploration_with_sampling_viz("none")
    exploration_with_sampling_viz("all")


