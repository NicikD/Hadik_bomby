import game_engine


# Returns all valid reachable positions from a position
def get_reach(current: tuple[int, int], engine: game_engine.StaticEngine
              , lenght: int, level_width: int, level_height: int) -> list[tuple[int, int]]:
    x, y = current
    reach = []

    # If the snake is not on the ground it can not reach anything
    if game_engine.Interaction.WALL not in engine.get_interactions(x, y + 1):
        return reach

    for dx in range(-lenght, lenght + 1):
        for dy in range(-lenght, lenght + 1):
            # The snake cant actually reach here because of how gravity works
            if dx == 0:
                if dy == -lenght \
                        or dy == lenght - 1 \
                        or dy == lenght:
                    continue

            # All positions that are at most distance "length" from the snake head in the taxicab metrix
            #  except ones that would result in the snake falling off because of gravity
            if abs(dx) + abs(dy) < lenght \
                    or ((abs(dx) + abs(dy) == lenght
                         and game_engine.Interaction.WALL in engine.get_interactions(x + dx, y + dy + 1))):
                reach.append((x + dx, y + dy))

    return remove_invalid_neighbors(reach, engine, level_width, level_height)


# Removes destinations where the snake would not be able to reach
def remove_invalid_neighbors(reach: list[tuple[int, int]], engine: game_engine.StaticEngine,
                             width: int, height: int) -> list[tuple[int, int]]:
    return [
        # Check if the position is in the level
        (x, y) for x, y in reach
        if 0 < x < width + 1 and 0 < y < height + 1
        and (game_engine.Interaction.WALL not in engine.get_interactions(x, y)
             or game_engine.Interaction.FOOD in engine.get_interactions(x, y))
            ]
