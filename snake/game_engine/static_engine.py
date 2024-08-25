from enum import Enum, auto
from typing import Dict

from game_engine.entities import StaticEntity
from game_engine import Level


# Describes an interaction at a specific position that can be calculated in advance
class Interaction(Enum):
    NOTHING = auto()
    WALL = auto()
    HAZARD = auto()
    CHARGE = auto()
    FINISH = auto()


# STATIC - Does not change with electricity
# WALL - WALL when charged, NOTHING when not charged, takes 10 frames to lose the charge
# CHARGE - CHARGE when charged, NOTHING when not charged
# HAZARD - HAZARD when charged, NOTHING when not charged
class InteractionType(Enum):
    STATIC = auto()
    WALL = auto()
    HAZARD = auto()
    CHARGE = auto()


class InteractionGroup():
    def __init__(self, interaction: Interaction, interaction_type: InteractionType):
        self.interaction = interaction
        self.type = interaction_type

        # List of entities that are in this group to update them with electricity when type is CHARGE
        self.entities: list[StaticEntity] = []


class StaticEngine:
    def __init__(self, static: list[StaticEntity]):
        # What group_id is what interaction, 0-4 are reserved for static behavior (always wall, always death...)
        #  groups with id 5+ are initialized when level is loaded, they change based on electricity
        self.group_hash: Dict[int, InteractionGroup] = {
            0: InteractionGroup(Interaction.NOTHING, InteractionType.STATIC),
            1: InteractionGroup(Interaction.WALL, InteractionType.STATIC),
            2: InteractionGroup(Interaction.HAZARD, InteractionType.STATIC),
            3: InteractionGroup(Interaction.FINISH, InteractionType.STATIC),
            4: InteractionGroup(Interaction.CHARGE, InteractionType.STATIC)
        }

        # What group_ids are in what positions
        #  for example position_hash[3, 4] == [2] would indicate that a hazard is in the position (x=3, y=4)
        self.position_hash: Dict[tuple[int, int], list[int]] = {}

        # Preprocess static interactions such as collisions
        # TODO

        # Preprocess electricity
        static = [entity for entity in static if entity.conductive]
        #TODO

    # Get interactions at a specific position (should be O(1) because of the preprocessing)
    def get_interactions(self, x: int, y: int) -> set[Interaction]:
        return set([self.group_hash[group_id].interaction for group_id in self.position_hash[(x, y)]])

    # Call when charge changes at a specific position
    def update_charge(self, x: int, y: int, charge: bool) -> None:
        for group_id in self.position_hash[(x, y)]:
            group = self.group_hash[group_id]
            if group.type == InteractionType.CHARGE:

                group.interaction = Interaction.CHARGE if charge else Interaction.NOTHING
                # Propagates charge to all entities in the group
                for entity in group.entities:
                    entity.charge = charge
