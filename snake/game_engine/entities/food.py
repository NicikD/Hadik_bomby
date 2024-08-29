from game_engine.entities import StaticEntity


# Food that increases the snakes lenght by 1
class Food(StaticEntity):
    def __init__(self, x, y):
        # Food is not conductive
        super().__init__(x, y, 1, 1, conductive=False, charge=False)

        self.eaten = False

    def draw(self, canvas, offsetx, offsety, block_size) -> None:
        if self.eaten:
            return

        canvas.create_rectangle(offsetx + block_size*(self.x)
                                , offsety + block_size*(self.y)
                                , offsetx + block_size*(self.x + 1)
                                , offsety + block_size*(self.y + 1)
                                , fill="green", outline="")

    # The food is not solid
    def get_collision_coords(self) -> list[tuple[int, int]]:
        return [(self.x, self.y)]

    # The food interacts when the snake eats it
    def get_interact_coords(self) -> list[tuple[int, int]]:
        return [(self.x, self.y)]

    # The food feeds the snake
    def get_interact_type(self) -> StaticEntity.InteractType:
        return StaticEntity.InteractType.FOOD

    # The food does not hurt the snake
    def get_hurt_coords(self) -> list[tuple[int, int]]: return []
    # The food does not conduct electricity
    def get_electricity_coords(self) -> list[tuple[int, int]]: return []
    # The food does not fall because of gravity
    def get_gravity_coords(self) -> list[tuple[int, int]]: return []
