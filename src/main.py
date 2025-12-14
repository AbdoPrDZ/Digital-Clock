import tkinter as tk
import os

from time import strftime
from datetime import datetime
from dotenv import load_dotenv

from utils import asset, register_font, get_font_config, photo_image

class ClockApp(tk.Tk):

  def __init__(self):
    super().__init__()

    self.resizable(False, False)
    masked_color = "#010101"
    self.configure(bg=masked_color)
    self.overrideredirect(True)
    self.wm_attributes("-topmost", True)
    self.wm_attributes("-transparentcolor", masked_color)
    self.wm_attributes("-alpha", 0.95)

    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=0)

    self.frame = tk.Frame(self, bg=masked_color)
    self.frame.grid(row=0, column=0)

    self.time_label = tk.Label(self.frame, text="", font=get_font_config(self.conf.font, self.conf.time_text_size))
    self.time_label.pack()
    self.date_label = tk.Label(self.frame, text="", font=get_font_config(self.conf.font, self.conf.date_text_size))
    self.date_label.pack()

    for widget in [self.time_label, self.date_label]:
      widget.configure(background=masked_color, foreground=self.conf.color, 
                       relief="flat", borderwidth=0, highlightthickness=0)
      widget.bind("<Button-1>", self.on_click)
      widget.bind("<B1-Motion>", self.on_move)
      widget.bind("<Enter>", self.on_hover)
      widget.bind("<Leave>", self.on_leave)

    self.start_x = 0
    self.start_y = 0

    self.exit_timer = None

    self.exit_img = photo_image("exit.png", resize=(24, 24))
    self.exit_button = tk.Button(self, image=self.exit_img, command=self.quit, 
                                width=24, height=24, borderwidth=0, highlightthickness=0,
                                relief="flat")
    self.exit_button.configure(background=masked_color, activebackground=masked_color,
                              bd=0, highlightbackground=masked_color)

    self.update_clock()

    self.place_window()

  def update_clock(self):
    self.time_label.config(text=strftime(self.conf.time_format))
    self.date_label.config(text=strftime(self.conf.date_format))

    if self.exit_timer is not None:
      self.exit_timer -= 1
      if self.exit_timer <= 0:
        self.hide_exit_button()

    now = datetime.now()
    microseconds = now.microsecond
    next_sec_delay = 1000 - (microseconds // 1000)

    self.after(next_sec_delay, self.update_clock)

  def on_click(self, e):
    self.start_x = e.x
    self.start_y = e.y

  def on_move(self, e):
    pointer_x = self.winfo_pointerx()
    pointer_y = self.winfo_pointery()

    new_x = pointer_x - self.start_x
    new_y = pointer_y - self.start_y

    self.geometry(f"+{new_x}+{new_y}")

  def on_hover(self, e):
    self.time_label.config(cursor="fleur")
    self.exit_button.grid(row=0, column=1, padx=5, pady=5, sticky="ne")

    self.update_idletasks()

    self.exit_timer = 3

  def on_leave(self, e):
    self.time_label.config(cursor="")

  def hide_exit_button(self):
    self.exit_button.grid_forget()
    self.exit_timer = None

  def place_window(self):
    self.update_idletasks()
    width = self.winfo_reqwidth()
    x = (self.winfo_screenwidth() // 2) - (width // 2)
    self.geometry(f"+{x}+0")

  @property
  def conf(self):
    class Config:
      def __init__(self):
        self.color = os.environ.get("CLOCK_COLOR", "#00C15D")
        self.font_path = os.environ.get("CLOCK_FONT", asset("DynaPuff.ttf"))
        self.time_text_size = int(os.environ.get("CLOCK_TEXT_SIZE", "30"))
        self.date_text_size = int(os.environ.get("CLOCK_DATE_SIZE", "22"))
        self.time_format = os.environ.get("CLOCK_TIME_FORMAT", "%H:%M:%S")
        self.date_format = os.environ.get("CLOCK_DATE_FORMAT", "%A %Y-%m-%d")

      @property
      def font(self):
        try:
          if os.path.isfile(self.font_path):
            font_family = register_font(self.font_path)
            if font_family:
              return font_family
            else:
              return os.path.splitext(os.path.basename(self.font_path))[0]
        except Exception as e:
          print(f"Error loading font {self.font_path}: {e}")

        return "Helvetica"

    return Config()


if __name__ == "__main__":
  load_dotenv()

  app = ClockApp()
  app.mainloop()
