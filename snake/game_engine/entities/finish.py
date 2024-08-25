from game_engine.entities import StaticEntity


# The finish that the player needs to reach, upon interacting advances to the next level
class Finish(StaticEntity):
    def __init__(self, x, y):
        # Finish is not conductive, always 4x3
        super().__init__(x, y, 4, 3, conductive=False, charge=False)

    def draw(self, canvas, offsetx, offsety, block_size) -> None:
        canvas.create_rectangle(offsetx + block_size*(self.x)
                                , offsety + block_size*(self.y)
                                , offsetx + block_size*(self.x + self.width)
                                , offsety + block_size*(self.y + self.height)
                                , fill="black", outline="white")

        #Checkerboard pattern
        for i in range(self.width):
            for j in range(self.height):
                if (i + j) % 2 == 1:
                    color = "white"
                    outline = "black"
                else:
                    color = "black"
                    outline = "white"

                canvas.create_rectangle(offsetx + block_size*(self.x + i) + 1
                                        , offsety + block_size*(self.y + j) + 1
                                        , offsetx + block_size*(self.x + i + 1) - 1
                                        , offsety + block_size*(self.y + j + 1) - 1
                                        , fill=color, outline=outline)



    # The finish is solid
    def get_collision_coords(self) -> list[tuple[int, int]]:
        return [(self.x + dx, self.y + dy)
                for dx in range(self.width)
                for dy in range(self.height)]

    # The finish does not hurt the snake
    def get_hurt_coords(self) -> list[tuple[int, int]]:
        return []

    # The finish does not conduct electricity
    def get_electricity_coords(self) -> list[tuple[int, int]]:
        return []

    # The finish is interactable one block above it
    def get_interact_coords(self) -> list[tuple[int, int]]:
        return [(self.x + dx, self.y - 1) for dx in range(self.width)]