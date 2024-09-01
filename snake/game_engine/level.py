import game_engine


# Holds level metadata and entities
class Level:
    def __init__(self, width, height, snake: game_engine.entities.Snake, entities: list[game_engine.entities.Entity]):

        # Level dimensions (level coordinates start at 0 in the top left corner)
        self.width = width
        self.height = height

        # Level entities:
        #  The snake that the player controls
        #  List of static objects (walls, hazards, generators...) for preprocessing and drawing them
        #  List of dynamic objects (boxes, moving hazards...) for interactions and drawing them
        self.snake: game_engine.entities.Snake = snake
        self.static: list[game_engine.entities.StaticEntity] \
            = [entity for entity in entities if isinstance(entity, game_engine.entities.StaticEntity)]
        self.dynamic: list[game_engine.entities.DynamicEntity] \
            = [entity for entity in entities if isinstance(entity, game_engine.entities.DynamicEntity)]
