import tkinter.font as tkFont
from PIL import Image, ImageTk
import ctypes
from ctypes import wintypes
import os

def asset(name: str) -> str:
  """
  Get the absolute path to an asset file in the assets directory.
  
  This function constructs the full path to an asset file located in the
  ../assets directory relative to the current file's location.

  Args:
      name (str): The filename of the asset (e.g., "icon.png", "font.ttf")

  Returns:
      str: The absolute path to the asset file

  Raises:
      FileNotFoundError: If the asset file does not exist

  Example:
      >>> font_path = asset("DynaPuff.ttf")
      >>> icon_path = asset("exit.png")
  """

  path = os.path.join(os.path.dirname(__file__), "../assets", name)

  if not os.path.exists(path):
    raise FileNotFoundError(f"Asset not found: {path}")

  return path

def register_font(font_path: str) -> str:
  """
  Register a font file with Windows and return the font family name.

  This function uses the Windows GDI32 API to temporarily register a TrueType
  font file (.ttf) with the system, making it available for use in the application.
  The font is registered privately (FR_PRIVATE flag) so it's only available to
  this application instance.

  Args:
      font_path (str): The absolute path to the font file (.ttf)

  Returns:
      str or None: The font family name extracted from the filename if successful,
                   None if registration failed

  Raises:
      Exception: If there's an error during font registration

  Example:
      >>> font_name = register_font(r"C:\path\to\DynaPuff.ttf")
      >>> print(font_name)  # "DynaPuff"
      
  Note:
      - Only works on Windows systems
      - Font is registered temporarily and removed when app closes
      - Requires ctypes and wintypes modules
  """
  try:
    # Load the font file temporarily
    gdi32 = ctypes.WinDLL('gdi32')
    AddFontResourceEx = gdi32.AddFontResourceExW
    AddFontResourceEx.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.LPVOID]
    AddFontResourceEx.restype = ctypes.c_int

    # Add the font resource
    result = AddFontResourceEx(font_path, 0x10, 0)  # FR_PRIVATE flag

    if result > 0:
      # Extract font family name from filename
      font_name = os.path.splitext(os.path.basename(font_path))[0]
      return font_name
    else:
      print(f"Failed to register font: {font_path}")
      return None

  except Exception as e:
    print(f"Error registering font {font_path}: {e}")
    return None

def get_font_config(family: str, size: int, **kwargs) -> tkFont.Font:
  """
  Create and return a configured tkinter Font object.

  This function creates a tkinter Font object with the specified family and size,
  with optional additional font attributes. If the font creation fails (e.g.,
  font family not found), it falls back to a safe Helvetica font.

  Args:
      family (str): The font family name (e.g., "DynaPuff", "Arial")
      size (int): The font size in points
      **kwargs: Additional font attributes such as:
                - weight: "normal" or "bold"
                - slant: "roman" or "italic"
                - underline: True or False
                - overstrike: True or False

  Returns:
      tkFont.Font: A configured Font object ready for use in tkinter widgets

  Example:
      >>> font = get_font_config("DynaPuff", 24, weight="bold")
      >>> label = tk.Label(root, text="Clock", font=font)
      
  Note:
      - Always returns a valid Font object (fallback to Helvetica if needed)
      - Font family must be registered with the system before use
  """

  try:
    custom_font = tkFont.Font(family=family, size=size, **kwargs)
    return custom_font
  except Exception as e:
    print(f"Error creating font {family}: {e}")
    return tkFont.Font(family="Helvetica", size=size, **kwargs)

def photo_image(name: str, resize: tuple | None = None, **kwargs) -> ImageTk.PhotoImage:
  """
  Load and optionally resize an image asset for use in tkinter.
  
  This function loads an image from the assets directory and converts it to
  a format suitable for tkinter widgets (PhotoImage). Optionally resizes the
  image to specified dimensions using PIL/Pillow.

  Args:
      name (str): The filename of the image asset (e.g., "exit.png", "icon.jpg")
      resize (tuple[int, int] or None): Target dimensions as (width, height).
                                       If None, original size is preserved.
      **kwargs: Additional arguments passed to ImageTk.PhotoImage constructor

  Returns:
      ImageTk.PhotoImage: A PhotoImage object ready for use in tkinter widgets

  Example:
      >>> # Load original size
      >>> icon = photo_image("exit.png")

      >>> # Load and resize to 24x24 pixels
      >>> small_icon = photo_image("exit.png", resize=(24, 24))

      >>> # Use in a button
      >>> button = tk.Button(root, image=small_icon)

  Note:
      - Supports all image formats supported by PIL/Pillow
      - Returns ready-to-use PhotoImage for immediate tkinter widget assignment
      - Keep a reference to the returned PhotoImage to prevent garbage collection
  """
  if resize:
    img = Image.open(asset(name))
    img = img.resize(resize)
    return ImageTk.PhotoImage(img, **kwargs)
  return ImageTk.PhotoImage(file=asset(name), **kwargs)
