# from src.usecases.task_switch.task_switch_usecase import TaskSwitchUseCase
from src.usecases.operator.frontier_sampling_view import FrontierSamplingDebugView
from src.usecases.operator.mission_view import MissionView
from src.usecases.operator.waypoint_shortcuts_view import WaypointShortcutDebugView
from src.usecases.sar.search_and_rescue_usecase import SearchAndRescueUsecase
from src.usecases.views.debug_map_view import ImageMapDebugView

if __name__ == "__main__":
    # matplotlib.use("Qt5agg")

    """initiliaze view subscribers"""
    MissionView()
    WaypointShortcutDebugView()
    FrontierSamplingDebugView()

    ImageMapDebugView()

    SearchAndRescueUsecase().run()

    # TaskSwitchUseCase().run()

    # benchmark_func()
