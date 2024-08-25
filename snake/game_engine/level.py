from game_engine.entities import DynamicEntity, StaticEntity, Snake


# Holds level metadata and entities
class Level:
    def __init__(self, width, height
                 , snake: Snake
                 , static: list[StaticEntity]
                 , dynamic: list[DynamicEntity]):

        # Level dimensions (level coordinates start at 0 in the top left corner)
        self.width = width
        self.height = height

        # Level entities:
        #  The snake that the player controls
        #  List of static objects (walls, hazards, generators...) for preprocessing and drawing them
        #  List of dynamic objects (boxes, moving hazards...) for interactions and drawing them
        self.snake: Snake = snake
        self.static: list[StaticEntity] = static
        self.dynamic: list[DynamicEntity] = dynamic
