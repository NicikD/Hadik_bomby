from enum import Enum, auto
from time import monotonic
from random import choice

from scenes import Scene


# Exit message values:
#  0 - End application
#  1 - End transition
class Transition(Scene):
    class Type(Enum):
        GENERIC_FIRST_HALF = auto()
        GENERIC_SECOND_HALF = auto()
        START_LEVEL_FIRST_HALF = auto()
        START_LEVEL_SECOND_HALF = auto()
        END_APPLICATION = auto()

    # Only pass level_number if type is START_LEVEL
    def __init__(self, canvas, type: "Transition.Type", level_number: int | None = None):
        super().__init__(canvas, True)

        # Ends the transition after 3 seconds if it ends the application
        #  or after the animation is finished if it starts a level
        self.start_time = monotonic()

        self.type = type

        if type is Transition.Type.END_APPLICATION:
            self.text = "Good game " + choice([":3", ":^)", ":P", ":D", "B-)"])
        elif type is Transition.Type.START_LEVEL_FIRST_HALF or type is Transition.Type.START_LEVEL_SECOND_HALF:
            self.text = str(level_number)

        # Does a cool spiral animation
        self.spiral_coords: list[tuple[int, int]] = generate_spiral_coords()
        # -1 because it gets incremented before the first display
        self.spiral_index = -1
        self.animation_finished = False

    def process_frame(self, key_press):
        if (self.animation_finished
                and (self.type == Transition.Type.END_APPLICATION and monotonic() - self.start_time > 3
                     or self.type != Transition.Type.END_APPLICATION)):
            self.is_running = False
            self.exit_message = (0 if self.type is Transition.Type.END_APPLICATION else 1)

        # Progresses the animation
        self.spiral_index += 1
        if self.spiral_index == len(self.spiral_coords):
            self.animation_finished = True

    def display_frame(self, paddingx, paddingy, screen_size) -> None:
        block_size = screen_size/7

        if (self.type is Transition.Type.GENERIC_SECOND_HALF
                or self.type is Transition.Type.START_LEVEL_SECOND_HALF):
            coords = self.spiral_coords[self.spiral_index:]
        else:
            coords = self.spiral_coords[:self.spiral_index]

        for x, y in coords:
            self.canvas.create_rectangle(paddingx + block_size*x,
                                         paddingy + block_size*y,
                                         paddingx + block_size*(x + 1),
                                         paddingy + block_size*(y + 1),
                                         fill="black", outline="black")

        if self.type is Transition.Type.END_APPLICATION:
            # GUI made for 508x508 screen originally
            scale = screen_size / 508
            self.canvas.create_text(paddingx + scale*400,
                                    paddingy + scale*450,
                                    text=self.text,
                                    font=f"Arial {int(screen_size / 30)}", fill="white")
        elif (self.type is Transition.Type.START_LEVEL_FIRST_HALF
                or self.type is Transition.Type.START_LEVEL_SECOND_HALF):
            self.canvas.create_text(paddingx + screen_size / 2,
                                    paddingy + screen_size / 2,
                                    text=self.text,
                                    font=f"Arial {int(screen_size / 2)}", fill="white")


def generate_spiral_coords() -> list[tuple[int, int]]:
    # Initialize the grid and starting point (center of the grid)
    x, y = 3, 3
    dx, dy = 0, -1
    spiral_coords = []

    for _ in range(7*7):
        # Check if the current position is within bounds
        if 0 <= x < 7 and 0 <= y < 7:
            spiral_coords.append((x, y))

        # Rotate when necessary (too lazy to make an algorithm for this)
        if (x, y) in [(3, 2), (4, 2), (4, 4), (2, 4), (2, 1), (5, 1), (5, 5), (1, 5), (1, 0), (6, 0), (6, 6), (0, 6)]:
            dx, dy = -dy, dx

        # Move to the next position
        x, y = x + dx, y + dy

    return spiral_coords
