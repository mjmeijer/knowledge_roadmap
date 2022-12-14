from abc import ABC, abstractmethod

from src.platform_autonomy.control.abstract_agent import AbstractAgent
from src.shared.situational_graph import SituationalGraph
from src.shared.task import Task


class MissionInitializer(ABC):
    @abstractmethod
    def initialize_mission(self, agents: list[AbstractAgent], tosg: SituationalGraph):
        pass
