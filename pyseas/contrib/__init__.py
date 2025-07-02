from .plot_tracks import track_state_panel
from .plot_tracks import multi_track_panel
from .plot_tracks import find_projection

def _reload():
    """Reload modules during development

    Note: Not 100% reliable!
    """
    from importlib import reload
    from . import plot_tracks
    from pyseas import contrib

    reload(plot_tracks)
    reload(contrib)
