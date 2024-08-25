from game_engine.entities import DynamicEntity, StaticEntity, Snake


#


#
class EntityGroup:
    def __init__(self, group_id):
        self.id = group_id

        self.charge = False
        self.hazard = False

    def set_charge(self, charge):
        self.charge = charge

    def set_hazard(self, hazard):
        self.hazard = hazard


# Holds information about a level
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
        #  List of static objects (walls, hazards, generators...) just for drawing them
        #  List of dynamic objects (boxes, moving hazards...) for interactions and drawing them
        self.snake: Snake = snake
        self.static: list[StaticEntity] = static
        self.dynamic: list[DynamicEntity] = dynamic



        #  Hashed matrix of static objects to allow O(1) collision detection
        #   static_hash[x, y] returns index of group the block belongs to
        # TODO add strong typing because this is weird
        self.static_hash: dict[tuple[int, int], int] = self.preprocess_static_hash(static, self.groups)

    # TODO add strong typing because this is weird
    def preprocess_static_hash(self) -> dict:
        pass

