from abc import ABC, abstractmethod
from tkinter import Canvas


class Entity(ABC):
    @abstractmethod
    def __init__(self, conductive: bool, charge: bool):

        # Whether the entity conducts electricity
        self.conductive = conductive
        # Whether the entity is charged with electricity
        self.charge = charge

    @abstractmethod
    # Draw the entity on the canvas
    def draw(self, canvas: Canvas, paddingx, paddingy, block_size) -> None: pass

    # get_xyz_coords functions returns a tuple of (x, y) coords where the entity will interact with other entities
    #  in dynamic entities these are called every frame
    #  in static entities these are called at the beginning of the level

    @abstractmethod
    # In these coords moving entities can not go
    def get_collision_coords(self) -> list[tuple[int, int]]: pass

    @abstractmethod
    # In these coords the entity will cut the snake
    def get_hurt_coords(self) -> list[tuple[int, int]]: pass

    @abstractmethod
    # In these coords the entity will emit electricity
    def get_electricity_coords(self) -> list[tuple[int, int]]: pass

    @abstractmethod
    # In these coords the entity will interact with the snake
    def get_interact_coords(self) -> list[tuple[int, int]]: pass


# Simple rectangle shape
# Does not change position, gets hashed at beginning of level to allow O(1) interaction detection
class StaticEntity(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, conductive: bool, charge: bool):
        super().__init__(conductive, charge)

        # Position in the grid (top left corner)
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height

    def draw(self, canvas: Canvas, paddingx, paddingy, block_size) -> None: pass
    def get_collision_coords(self) -> list[tuple[int, int]]: pass
    def get_hurt_coords(self) -> list[tuple[int, int]]: pass
    def get_electricity_coords(self) -> list[tuple[int, int]]: pass
    def get_interact_coords(self) -> list[tuple[int, int]]: pass


# Made of 1x1 blocks, can have any shape
# Can change position so interactions get checked every frame manually
class DynamicEntity(Entity):
    @abstractmethod
    def __init__(self, blocks: list[tuple[int, int]], conductive, charge, gravity):
        super().__init__(conductive, charge)

        # Whether the entity is affected by gravity
        self.gravity = gravity

        # List of blocks the entity is made of
        self.blocks: list[tuple[int, int]] = blocks

    @abstractmethod
    def draw(self, canvas: Canvas, paddingx, paddingy, block_size) -> None: pass
    @abstractmethod
    def get_collision_coords(self) -> list[tuple[int, int]]: pass
    @abstractmethod
    def get_hurt_coords(self) -> list[tuple[int, int]]: pass
    @abstractmethod
    def get_electricity_coords(self) -> list[tuple[int, int]]: pass
    @abstractmethod
    def get_interact_coords(self) -> list[tuple[int, int]]: pass

    @abstractmethod
    # In these coords the entity will require at least one collision to not fall because of gravity
    def get_gravity_coords(self) -> list[tuple[int, int]]: pass
