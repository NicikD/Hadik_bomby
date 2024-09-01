import collections


class EatenFood:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# To be able to undo movement, keeps a reference to the entity to move it
class EntityPosition:
    def __init__(self, entity, x, y):
        self.entity = entity

        self.x = x
        self.y = y


class Undo:
    def __init__(self, snake: collections.deque[tuple[int, int]],
                 dynamic_entities: list[EntityPosition], events: list[EatenFood]):
        # Snake is the only entity that can change shape, tracks all separate blocks
        #  for other entities (x, y) is enough
        self.snake = snake
        self.dynamic_entities = dynamic_entities
        self.events = events
