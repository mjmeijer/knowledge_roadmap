from src.config import Scenario, cfg
from src.mission_autonomy.mission_runner import MissionRunner
from src.operator import runner
from src.platform_autonomy.control.real.spot_agent import SpotAgent
from src.platform_autonomy.control.sim.simulated_agent import SimulatedAgent
from src.platform_autonomy.platform_runner import PlatformRunner
from src.shared.prior_knowledge.capabilities import Capabilities

if __name__ == "__main__":
    # matplotlib.use("Qt5agg")

    runner.run()

    # ImageMapDebugView()
    PlatformRunner()

    agent1_capabilities = {Capabilities.CAN_ASSESS}
    if cfg.SCENARIO == Scenario.REAL:
        agents = [SpotAgent(agent1_capabilities)]
    else:
        agents = [
            SimulatedAgent(agent1_capabilities)
        ]  # make the first agent only posses the capabilities
        agents.extend([SimulatedAgent(set(), i) for i in range(1, cfg.NUM_AGENTS)])


    MissionRunner().mission_main_loop(agents)

    # benchmark_func()
