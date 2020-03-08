"""GFW Colormaps

Official GFW Colormaps
----------------------
reception
fishing
presence


Unofficial GFW Colormaps
------------------------

Colormaps made by Juan Carlos:

unofficial.jc_presence
unofficial.jc_reception
unofficial.jc_linearorange
unofficial.jc_linearblue
unofficial.jc_linearpink
"""
from matplotlib import colors


def _tuple2cmap(name, color_seq):
    '''
    '''
    c = color_seq

    color_ramp = [ [c[i], int(100*(i/(len(c)-1))), int(100*i/(len(c)-1)) ] for i in range(len(c))]
    tm = 100.0 #this is just to scale the the following... this makes the colormap
    cdict = { 'red':tuple(   (color[2]/tm, int(color[0][1:3],16)/256.0, int(color[0][1:3],16)/256.0) 
                                  for color in color_ramp ),
              'green':tuple( (color[2]/tm, int(color[0][3:5],16)/256.0, int(color[0][3:5],16)/256.0) 
                                  for color in color_ramp ),
              'blue':tuple(  (color[2]/tm, int(color[0][5:7],16)/256.0, int(color[0][5:7],16)/256.0) 
                                  for color in color_ramp )}#,

    cmap = colors.LinearSegmentedColormap(name, cdict, 256)
    cmap.set_bad(alpha = 0.0)
    return cmap


reception = _tuple2cmap('reception', ('#ff4573', '#7b2e8d', '#093b76', '#0c276c')) 
fishing = _tuple2cmap('fishing', ('#0c276c', '#3b9088', '#eeff00', '#ffffff')) 
presence = _tuple2cmap('presence', ('#0c276c', '#114685','#00ffc3','#ffffff'))

class _Unofficial(object):
  jc_presence  = _tuple2cmap('jc_presence', ('#3359A8', '#16A3A4', '#00FFC3', '#ffffff'))
  jc_reception = _tuple2cmap('jc_reception', ('#5E0C20', '#2927A8', '#41FFA7', '#ffffff'))
  jc_linearorange = _tuple2cmap('jc_linearorange', ('#0C276C', '#824158', '#FF9500', '#ffffff'))
  jc_linearblue = _tuple2cmap('jc_linearblue', ('#0C276C', '#1D5780', '#00FFC3', '#ffffff'))
  jc_linearpink = _tuple2cmap('jc_linearpink', ('#0C276C', '#4E289B', '#F74559', '#ffffff'))

unofficial = _Unofficial()
