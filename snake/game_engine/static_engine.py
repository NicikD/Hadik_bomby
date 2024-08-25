from enum import Enum, auto
from collections import defaultdict
from typing import Dict

from utils import get_connected_conductive_groups
from game_engine.entities import StaticEntity, Food, Finish


# Describes an interaction at a specific position that can be calculated in advance
#  these values are reserved for the group_hash
class Interaction(Enum):
    # Nothing gets set to interactions that change with electricity when they are not charged
    NOTHING = 0
    WALL = 1
    HAZARD = 2
    CHARGE = 3
    FINISH = 4
    FOOD = 5


# STATIC - Does not change with electricity
# WALL - WALL when charged, NOTHING when not charged, takes 10 frames to lose the charge
# CHARGE - CHARGE when charged, NOTHING when not charged
# HAZARD - HAZARD when charged, NOTHING when not charged
class InteractionType(Enum):
    STATIC = auto()
    WALL = auto()
    HAZARD = auto()
    CHARGE = auto()


class InteractionGroup:
    def __init__(self, interaction: Interaction, interaction_type: InteractionType):
        self.interaction = interaction
        self.type = interaction_type

        # List of entities that are in this group to update them
        self.entities: list[StaticEntity] = []


class StaticEngine:
    def __init__(self, static: list[StaticEntity]):
        # What group_id is what interaction, 0-9 are reserved for static behavior (always wall, always death...)
        #  groups with id 10+ are initialized when level is loaded, they change behavior based on electricity
        #  should crash when group_id that does not exist is queried
        self._group_hash: Dict[int, InteractionGroup] = {
            Interaction.WALL.value: InteractionGroup(Interaction.WALL, InteractionType.STATIC),
            Interaction.HAZARD.value: InteractionGroup(Interaction.HAZARD, InteractionType.STATIC),
            Interaction.CHARGE.value: InteractionGroup(Interaction.CHARGE, InteractionType.STATIC),
            Interaction.FINISH.value: InteractionGroup(Interaction.FINISH, InteractionType.STATIC),
            Interaction.FOOD.value: InteractionGroup(Interaction.FOOD, InteractionType.STATIC)
        }
        self.next_group_id = 10

        # What group_ids are in what positions
        #  for example position_hash[3, 4] == [2] would indicate that a hazard is in the position (x=3, y=4)
        #  should return empty list when position without any interaction is queried
        self._position_hash: Dict[tuple[int, int], list[int]] = defaultdict(list)

        # Preprocess static interactions
        collision_positions: set[tuple[int, int]] = set()
        hazard_positions: set[tuple[int, int]] = set()
        charge_positions: set[tuple[int, int]] = set()
        finish_positions: set[tuple[int, int]] = set()

        for entity in static:
            collision_positions.update(entity.get_collision_coords())
            hazard_positions.update(entity.get_hurt_coords())

            if entity.charge:
                charge_positions.update(entity.get_electricity_coords())

            if entity.get_interact_type() == StaticEntity.InteractType.FOOD:
                # Saves a reference to the food, so it can be removed when eaten
                food = InteractionGroup(Interaction.FOOD, InteractionType.STATIC)
                food.entities = entity
                self._group_hash[self.next_group_id] = food
                self._position_hash[entity.x, entity.y].append(self.next_group_id)
                self.next_group_id += 1
            elif entity.get_interact_type() == StaticEntity.InteractType.FINISH:
                finish_positions.update(entity.get_interact_coords())

        for x, y in collision_positions:
            self._position_hash[(x, y)].append(Interaction.WALL.value)
        for x, y in hazard_positions:
            self._position_hash[(x, y)].append(Interaction.HAZARD.value)
        for x, y in charge_positions:
            self._position_hash[(x, y)].append(Interaction.CHARGE.value)
        for x, y in finish_positions:
            self._position_hash[(x, y)].append(Interaction.FINISH.value)

        # Preprocess electricity
        for connected_entities in get_connected_conductive_groups(static):
            # Group entities that share the same charge and create interactions groups for them
            group = InteractionGroup(Interaction.CHARGE, InteractionType.CHARGE)
            group.entities = connected_entities

            # Gets all positions that the group occupies and adds the group_id to them
            group_positions: set[tuple[int, int]] = set()
            for entity in connected_entities:
                for x, y in entity.get_electricity_coords():
                    group_positions.add((x, y))

            # Updates the hashes
            self._group_hash[self.next_group_id] = group
            for x, y in group_positions:
                self._position_hash[(x, y)].append(self.next_group_id)
            self.next_group_id += 1

    # Get interactions at a specific position
    def get_interactions(self, x: int, y: int) -> set[Interaction]:
        return set([self._group_hash[group_id].interaction for group_id in self._position_hash[(x, y)]])

    # Call when charge changes at a specific position
    def update_charge(self, x: int, y: int, charge: bool) -> None:
        for group_id in self._position_hash[(x, y)]:
            group = self._group_hash[group_id]
            if group.type == InteractionType.CHARGE:

                group.interaction = Interaction.CHARGE if charge else Interaction.NOTHING
                # Propagates charge to all entities in the group
                for entity in group.entities:
                    entity.charge = charge

    # Call when food is eaten at a specific position
    def update_eaten_food(self, x: int, y: int) -> None:
        for group_id in self._position_hash[(x, y)]:
            group = self._group_hash[group_id]

            if group.interaction == Interaction.FOOD:
                group.entities.eaten = True
                self._position_hash[(x, y)].remove(group_id)
