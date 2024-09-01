import collections
import copy

import game_engine

FREEZE_FRAMES = 8


class Engine:
    def __init__(self, level: game_engine.Level):
        self.level: game_engine.Level = level

        self.static_engine = game_engine.StaticEngine(level.static)

        # Falling takes a bit longer than normal movement (not for the first frame), just for visual effect
        self.snake_is_falling = False
        self.first_frame_falling = False
        self.falling_frame_countdown = FREEZE_FRAMES

        # When the snake reaches the finish line it does a short animation before setting self.level_finished = True
        self.level_finish_animation = False
        self.level_finish_frame_countdown = FREEZE_FRAMES

        self.level_finished = False

        # When this is true no movement will happen, not even automatic like gravity
        self.movement_stopped = False

        # If movement happened last frame
        self.movement_happened = False
        self.last_movement: game_engine.Action = game_engine.Action.DO_NOTHING

        # Keeps track of all movement that happened to be able to unto it
        self.current_frame_undo = None
        self.undo_stack: collections.deque[game_engine.Undo] = collections.deque()

    def process_frame(self, action: game_engine.Action) -> None:
        # Stops all movement even automatic like gravity
        if action is game_engine.Action.STOP_MOVEMENT or self.movement_stopped \
                and action is game_engine.Action.DO_NOTHING:
            self.movement_stopped = True
            return
        self.movement_stopped = (action is game_engine.Action.UNDO_MOVEMENT)

        # Undoes last frame of movement
        if action is game_engine.Action.UNDO_MOVEMENT:
            if self.undo_stack:
                undo = self.undo_stack.pop()

                before = self.level.snake.blocks[0]
                self.level.snake.blocks = undo.snake
                after = self.level.snake.blocks[0]

                for movement in undo.dynamic_entities:
                    movement.entity.x = movement.x
                    movement.entity.y = movement.y

                for event in undo.events:
                    if isinstance(event, game_engine.EatenFood):
                        self.static_engine.update_eaten_food(event.x, event.y, False)

                self.movement_happened = True
                self.last_movement = calculate_last_movement(before, after)
            return

        # Does nothing while falling
        if self.snake_is_falling:
            if not self.first_frame_falling:
                self.falling_frame_countdown -= 1
                if self.falling_frame_countdown == 0:
                    self.falling_frame_countdown = FREEZE_FRAMES
                else:
                    return

        # Does nothing while doing the level finish animation
        if self.level_finish_animation:
            self.level_finish_frame_countdown -= 1
            if self.level_finish_frame_countdown == 0:
                self.level_finish_frame_countdown = FREEZE_FRAMES
                # Removes blocks from the snake until it dissapears
                if self.level.snake.blocks:
                    self.level.snake.blocks.pop()
                else:
                    self.level_finished = True

            return

        # "Physics" processing
        self.movement_happened = False
        self.last_movement = game_engine.Action.DO_NOTHING

        # Saves entity positions to append them to the undo stack if movement happens
        snake_pos = copy.deepcopy(self.level.snake.blocks)
        entity_pos = [game_engine.EntityPosition(entity, entity.x, entity.y) for entity in self.level.dynamic]
        self.current_frame_undo = game_engine.Undo(snake_pos, entity_pos, [])

        # self.process_automatic_movement()
        if not self.snake_is_falling:
            self.process_player_movement(action)
        self.process_gravity()
        # TODO elektrika
        # TODO self.process_hazards()
        # TODO process interakcie return

        # Keeps track of all movement that happened to be able to unto it
        if self.movement_happened and action is not game_engine.Action.UNDO_MOVEMENT:
            self.undo_stack.append(self.current_frame_undo)

    def process_player_movement(self, action: game_engine.Action):
        if action is game_engine.Action.DO_NOTHING:
            return

        eat_food = False

        dx, dy = 0, 0
        if action == game_engine.Action.MOVE_LEFT:
            dx = -1
        elif action == game_engine.Action.MOVE_RIGHT:
            dx = 1
        elif action == game_engine.Action.MOVE_UP:
            dy = -1
        elif action == game_engine.Action.MOVE_DOWN:
            dy = 1

        # (x, y) of where the snake tries to move to
        first_block = self.level.snake.blocks[0]
        x, y = first_block[0] + dx, first_block[1] + dy

        # If movement is within the level
        if 0 < x < self.level.width + 1 and 0 < y < self.level.height + 1:

            static_interactions = self.static_engine.get_interactions(x, y)
            if game_engine.Interaction.FOOD in static_interactions:
                self.static_engine.update_eaten_food(x, y, True)
                self.current_frame_undo.events.append(game_engine.EatenFood(x, y))
                eat_food = True
            elif game_engine.Interaction.FINISH in static_interactions:
                self.level_finish_animation = True
            elif game_engine.Interaction.WALL in static_interactions:
                # Cannot move there
                return

            # Check if the snake tries to move in its own body
            block_at_position = None
            for i, (block) in enumerate(self.level.snake.blocks):
                if (x, y) == block:
                    block_at_position = i

            # If the snake tries to move to a new position delete its tail (if not eating food)
            if block_at_position is None and not eat_food:
                self.level.snake.blocks.pop()
            # If the snake tries to move in its own body moves block order
            elif block_at_position is not None:
                del self.level.snake.blocks[block_at_position]
            self.level.snake.blocks.appendleft((x, y))

            self.movement_happened = True
            self.last_movement = action
            return True

    def process_gravity(self):
        interactions = [self.static_engine.get_interactions(x, y) for x, y in self.level.snake.get_gravity_coords()]

        # If the snake is not on the ground it will fall
        if not any(game_engine.Interaction.WALL in interaction for interaction in interactions):

            # If the snake falls on the finish line it ends the level
            if any(game_engine.Interaction.FINISH in interaction for interaction in interactions):
                self.level_finish_animation = True

            self.level.snake = game_engine.entities.Snake([(x, y + 1) for x, y in self.level.snake.blocks])

            if self.snake_is_falling:
                self.first_frame_falling = False
            else:
                self.snake_is_falling = True
                self.first_frame_falling = True

            self.movement_happened = True
            self.last_movement = game_engine.Action.MOVE_DOWN
            return True
        else:
            self.snake_is_falling = False


def calculate_last_movement(before, after):
    if before[1] > after[1]:
        return game_engine.Action.MOVE_UP
    elif before[1] < after[1]:
        return game_engine.Action.MOVE_DOWN
    elif before[0] > after[0]:
        return game_engine.Action.MOVE_LEFT
    elif before[0] < after[0]:
        return game_engine.Action.MOVE_RIGHT
    # Should never happen
    else:
        return game_engine.Action.DO_NOTHING
