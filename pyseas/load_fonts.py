from pathlib import Path
from matplotlib import font_manager


data = Path(__file__).parent / "data"

font_dirs = [x for x in (data / "fonts").iterdir() if x.is_dir()]
for font_file in font_manager.findSystemFonts(fontpaths=font_dirs):
    font_manager.fontManager.addfont(font_file)