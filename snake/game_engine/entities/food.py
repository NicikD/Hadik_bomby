from game_engine.entities import DynamicEntity


# Food that increases the snakes lenght by 1
class Food(DynamicEntity):
    def __init__(self, blocks):
        # Food is not conductive and does not fall because of gravity
        super().__init__(blocks, conductive=False, charge=False, gravity=False)
        # "blocks" but food is always one block, can be modified but I didnt bother
        assert len(blocks) == 1

    def draw(self, canvas, offsetx, offsety, block_size) -> None:
        x, y = self.blocks[0]

        canvas.create_rectangle(offsetx + block_size*(x)
                                , offsety + block_size*(y)
                                , offsetx + block_size*(x + 1)
                                , offsety + block_size*(y + 1)
                                , fill="green", outline="")

    # The food is not solid
    def get_collision_coords(self) -> list[tuple[int, int]]:
        return []

    # The food does not hurt the snake
    def get_hurt_coords(self) -> list[tuple[int, int]]:
        return []

    # The food does not conduct electricity
    def get_electricity_coords(self) -> list[tuple[int, int]]:
        return []

    # The food interacts when the snake eats it
    def get_interact_coords(self) -> list[tuple[int, int]]:
        return self.blocks

    # The food does not fall because of gravity
    def get_gravity_coords(self) -> list[tuple[int, int]]:
        return []
