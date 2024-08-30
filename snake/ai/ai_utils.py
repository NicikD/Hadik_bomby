from game_engine import Interaction, StaticEngine


# Returns all reachable positions from a position
def get_reach(current: tuple[int, int], engine: StaticEngine, lenght: int) -> list[tuple[int, int]]:
    x, y = current
    reach = []

    # If the snake is not on the ground it can not reach anything
    if Interaction.WALL not in engine.get_interactions(x, y + 1):
        return reach

    for dx in range(-lenght, lenght + 1):
        for dy in range(-lenght, lenght + 1):
            # The snake cant actually reach here
            if dx == 0:
                if dy == -lenght \
                        or dy == lenght - 1 \
                        or dy == lenght:
                    continue

            # All positions that are distance "length" from the snake head in the taxicab metrix
            #  except ones that would result in the snake falling off because of gravity
            if abs(dx) + abs(dy) < lenght \
                or (abs(dx) + abs(dy) == lenght and Interaction.WALL in engine.get_interactions(x + dx, y + dy + 1)):
                reach.append((x + dx, y + dy))

    return reach


# Removes destinations where the snake would not be able to reach
def remove_invalid_neighbors(reach: list[tuple[int, int]], engine: StaticEngine,
                             width: int, height: int) -> list[tuple[int, int]]:
    return [
        (x, y) for x, y in reach
        if 0 < x < width + 1 and 0 < y < height + 1
        and (Interaction.WALL not in engine.get_interactions(x, y) or Interaction.FOOD in engine.get_interactions(x, y))
            ]
