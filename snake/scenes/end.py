import time
from scenes import Scene


# Exit message values:
#  1 - Exit application
class End(Scene):
    def __init__(self, canvas):
        super().__init__(canvas)

        # Closes the application after 3 seconds
        self.start_time = time.monotonic()

    def process_frame(self, key_press):
        if time.monotonic() - self.start_time > 3:
            self.is_running = False
            self.exit_message = 1

    def display_frame(self, paddingx, paddingy, screen_size) -> None:
        # GUI made for 508x508 screen originally
        scale = screen_size/508
        font = f"Arial {int(screen_size/30)}"

        self.canvas.delete("all")
        self.canvas.create_text(paddingx + scale*400, paddingy + scale*460, text="Good game", font=font, fill="white")
