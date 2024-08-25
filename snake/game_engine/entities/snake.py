from collections import deque
from game_engine.entities import DynamicEntity


# The snake that the player controls
class Snake(DynamicEntity):
    def __init__(self, blocks):
        # The snake is conductive and has gravity
        super().__init__(blocks, conductive=True, charge=False, gravity=True)

        # The snake is saved as a deque instead of a list (overrides DynamicEntity behavior)
        self.blocks = deque()
        self.blocks.extend(blocks)

    def draw(self, canvas, offsetx, offsety, block_size) -> None:
        if self.charge:
            color_head = "DarkGoldenrod3"
            color_body = "DarkGoldenrod1"
            color_tail = "DarkGoldenrod2"
        else:
            color_head = "RoyalBlue4"
            color_body = "RoyalBlue1"
            color_tail = "RoyalBlue3"

        for i, (x, y) in enumerate(self.blocks):
            # First and last blocks are different shades
            if i == 0:
                color = color_head
            elif i + 1 == len(self.blocks):
                color = color_tail
            else:
                color = color_body

            canvas.create_rectangle(offsetx + block_size*(x)
                                    , offsety + block_size*(y)
                                    , offsetx + block_size*(x + 1)
                                    , offsety + block_size*(y + 1)
                                    , fill=color, outline="")

    # The snake is solid
    def get_collision_coords(self) -> list[tuple[int, int]]:
        return list(self.blocks)

    # The snake does not hurt itself :D
    def get_hurt_coords(self) -> list[tuple[int, int]]:
        return []

    # The snake conducts electricity around itself
    def get_electricity_coords(self) -> list[tuple[int, int]]:
        electricity_coords = []

        for block in self.blocks:
            electricity_coords.append((block[0] - 1, block[1]))
            electricity_coords.append((block[0] + 1, block[1]))
            electricity_coords.append((block[0], block[1] - 1))
            electricity_coords.append((block[0], block[1] + 1))

    # The snake does not interact with itself :D
    def get_interact_coords(self) -> list[tuple[int, int]]:
        return []

    # There needs to be a solid entity one block below the snake
    def get_gravity_coords(self) -> list[tuple[int, int]]:
        return [(x, y + 1) for x, y in self.blocks]
