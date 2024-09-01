import collections

import game_engine
import ai


# Finds a path for the snake with brute force
class FindPathForce:
    def __init__(self, start: tuple[int, int], destination: tuple[int, int], engine: game_engine.StaticEngine
                 , snake_length: int, level_width: int, level_height: int):
        self.start: tuple[int, int] = start
        self.destination: tuple[int, int] = destination

        self.engine: game_engine.StaticEngine = engine

        # To avoid infinite loop of the snake trying to go to impossible coords
        self.width = level_width
        self.height = level_height - snake_length + start[1] - 1
        self.max_y = snake_length + start[1] - 1

        # To avoid pointless pathfinding - the destination should not be farther than this
        self.max_stack_depth = snake_length

        self.move_stack: collections.deque[ai.State] \
            = collections.deque([ai.State(start, None, destination,
                                          engine, self.can_move_up(start[1]),
                                          self.width, self.height, 0, self.max_stack_depth)])

        self.is_finished = False
        # When self.is_finished==True this is True when the destination is found and False when no path was found
        self.found = False

    def get_next_move(self) -> game_engine.Action:
        state = self.move_stack.pop()

        if state.moves and state.depth < self.max_stack_depth:
            # "pops" best move from the list
            new_move = state.moves[0]
            state.moves = state.moves[1:]

            # Returns the parent state to be used later
            self.move_stack.append(state)

            # Appends the new state to the stack (moves to this block)
            self.move_stack.append(ai.State(new_move[0], state.coords, self.destination
                                             , self.engine, self.can_move_up(new_move[0][1])
                                             , self.width, self.height, state.depth + 1, self.max_stack_depth))

            if new_move[0] == self.destination:
                self.is_finished = True
                self.found = True

            return new_move[1]
        else:
            # Did not find a path
            if state.depth == 0:
                self.is_finished = True
                self.found = False
                return game_engine.Action.DO_NOTHING
            # This state did not work out, go back
            return game_engine.Action.UNDO_MOVEMENT

    def can_move_up(self, y):
        return y < self.max_y
