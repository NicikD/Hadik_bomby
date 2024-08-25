from collections import deque
from game_engine.entities import StaticEntity


# Groups static entities that share charge (are connected to each other by at least one side)
#  used in the static engine to preprocess electricity interactions
def get_connected_conductive_groups(entities: list[StaticEntity]):
    # Only conductive entities are considered
    entities = [entity for entity in entities if entity.conductive]

    groups: list[list[StaticEntity]] = []

    while entities:
        # Group of entities that are connected
        connected: list[StaticEntity] = []
        # Stack of entities not checked yet
        not_checked: deque[StaticEntity] = deque([entities.pop()])

        while not_checked:
            current = not_checked.pop()

            for entity in pop_connected_entities(current, entities):
                not_checked.append(entity)

            connected.append(current)

        groups.append(connected)

    return groups


# Get connected groups is recursive, this is just a single iteration
def pop_connected_entities(current: StaticEntity, entities: list[StaticEntity]):
    connected: list[StaticEntity] = []
    current_reach = set(current.get_electricity_coords())

    for entity in entities:
        # The entities are connected
        if current_reach.intersection(set(entity.get_collision_coords())):
            connected.append(entity)

    # To not lose the reference
    entities[:] = [entity for entity in entities if entity not in connected]
    return connected
