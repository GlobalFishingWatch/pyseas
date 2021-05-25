from .plot_tracks import track_state_panel
from .plot_tracks import multi_track_panel
from .plot_tracks import find_projection

def _reload():
    """Reload modules during development

    Note: Not 100% reliable!
    """
    import imp
    from . import plot_tracks
    from pyseas import contrib

    imp.reload(plot_tracks)
    imp.reload(contrib)