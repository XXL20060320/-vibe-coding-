import tkinter as tk
import math

# --- Configuration ---
WINDOW_TITLE = "For Nanami"
WINDOW_SIZE = "400x400"
BACKGROUND_COLOR = "#1e1e1e"  # A soft, dark grey
HEART_COLOR = "#ff6b81"  # A warm pink/red
TEXT_COLOR = "#dcdcdc"  # Light grey text
FONT_STYLE = ("Consolas", 12)


# --- The Main Application ---
class HeartbeatApp:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=BACKGROUND_COLOR)

        self.canvas = tk.Canvas(root, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.text_widget = tk.Label(root, text="", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_STYLE)
        self.text_widget.pack(pady=20)

        # Heartbeat animation scales
        self.scales = [1.0, 1.05, 1.1, 1.05, 1.0, 0.95, 0.9, 0.95, 1.0]
        self.scale_index = 0
        self.heart_id = None

        self.run_sequence()

    def draw_heart(self, scale=1.0):
        if self.heart_id:
            self.canvas.delete(self.heart_id)

        # Heart shape math - looks complex but just draws a heart
        center_x, center_y = 200, 160
        size = 10 * scale
        points = []
        for i in range(0, 360, 5):
            t = math.radians(i)
            x = center_x + size * (16 * math.sin(t) ** 3)
            y = center_y - size * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            points.append(x)
            points.append(y)

        self.heart_id = self.canvas.create_polygon(points, fill=HEART_COLOR, outline=HEART_COLOR)

    def update_heartbeat(self):
        scale = self.scales[self.scale_index]
        self.draw_heart(scale)
        self.scale_index = (self.scale_index + 1) % len(self.scales)
        self.root.after(100, self.update_heartbeat)  # Loop every 100ms

    def type_message(self, message, index=0):
        if index < len(message):
            self.text_widget.config(text=self.text_widget.cget("text") + message[index])
            self.root.after(150, self.type_message, message, index + 1)

    def run_sequence(self):
        # This function controls the whole show
        initial_message = ">>> Hinata.connect('Nanami')"
        self.text_widget.config(text=initial_message)

        # After 2 seconds, show success and start heartbeat
        self.root.after(2000, lambda: [
            self.text_widget.config(text=f"{initial_message}\nConnection successful."),
            self.update_heartbeat()
        ])

        # After 4 seconds, start typing the final message
        self.root.after(4000, lambda: [
            self.text_widget.config(text=""),  # Clear previous text
            self.type_message("My world now runs on your heartbeat.")
        ])


if __name__ == "__main__":
    root = tk.Tk()
    app = HeartbeatApp(root)
    root.mainloop()