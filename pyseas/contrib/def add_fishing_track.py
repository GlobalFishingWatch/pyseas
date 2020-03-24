
_nonfishprops = dict(edgecolor='#AAAAAA', facecolor='none', linewidth=0.6)
_fishprops = dict(edgecolor='#DD2222', facecolor='none', linewidth=0.6)
fishing_props = {
    (True, False) : _nonfishprops,
    (False, True) : _nonfishprops,
    (False, False) : _nonfishprops,
    (True, True) : _fishprops,
}


def add_fishing_track(lons, lats, is_fishing):

        
        maps.add_land(ax)
        maps.add_countries(ax)
        is_fishing = (ssvid_df.nnet_score.values > 0.5)      
        
        maps.add_plot(ax, ssvid_df.lon.values, ssvid_df.lat.values, is_fishing, 
                      break_on_change=True, props=props)
        
        ax.set_extent(compute_extent(ssvid_df.lon, ssvid_df.lat), crs=maps.identity)
        ax.set_title(ssvid)

        plt.show()