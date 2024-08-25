from game_engine.entities import StaticEntity


# Generic solid wall that stops the snake
class Wall(StaticEntity):
    def __init__(self, x, y, width, height):
        # Walls are conductive
        super().__init__(x, y, width, height, conductive=True, charge=False)

    def draw(self, canvas, offsetx, offsety, block_size) -> None:
        color = "gold" if self.charge else "black"

        canvas.create_rectangle(offsetx + block_size*(self.x)
                                , offsety + block_size*(self.y)
                                , offsetx + block_size*(self.x + self.width)
                                , offsety + block_size*(self.y + self.height)
                                , fill=color, outline="")

    # The wall is solid
    def get_collision_coords(self) -> list[tuple[int, int]]:
        collision_coords = []

        for dx in range(self.width):
            collision_coords.append((self.x + dx, self.y))
            collision_coords.append((self.x + dx, self.y + self.height - 1))
        for dy in range(self.height):
            collision_coords.append((self.x, self.y + dy))
            collision_coords.append((self.x + self.width - 1, self.y + dy))

        return collision_coords

    # The wall conducts electricity around it
    def get_electricity_coords(self) -> list[tuple[int, int]]:
        electricity_coords = []

        for dx in range(self.width):
            electricity_coords.append((self.x + dx, self.y - 1))
            electricity_coords.append((self.x + dx, self.y + self.height))
        for dy in range(self.height):
            electricity_coords.append((self.x - 1, self.y + dy))
            electricity_coords.append((self.x + self.width, self.y + dy))

        return electricity_coords

    # The wall does not hurt the snake
    def get_hurt_coords(self) -> list[tuple[int, int]]:
        return []
    # The wall is not interactable
    def get_interact_coords(self) -> list[tuple[int, int]]: return []
    def get_interact_type(self) -> StaticEntity.InteractType: return StaticEntity.InteractType.NONE
