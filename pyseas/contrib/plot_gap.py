################################################
### Module for generating gap visualizations ###
### ---------------------------------------- ###
### Author: Jenn Van Osdel                   ###
### Date: 2020-11-06                         ###
################################################

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as mpdates

import pyseas
from pyseas import maps


from pytz import UTC

from cycler import cycler
colors = ["#b2b2b2", "#F59E84", "#CC3A8E", "#99C945", "#DAA51B", "#24796C",
                        "#764E9F", "#CA7400", "#5D69B1", "#BE2045", "#58E8C6", "#A5AA99"]
custom_artist_cycler = cycler(edgecolor=colors, \
                              facecolor=[(0, 0, 0, 0)]*len(colors))


### Transforms hourly data into 
def get_hourly_positions(gap_id, gaps_data, hourly_data):
    gap = gaps_data[gaps_data.gap_id == gap_id].iloc[0]
    query_start = gap.gap_start - pd.to_timedelta(2, unit='d')
    query_end = gap.gap_end + pd.to_timedelta(2, unit='d')

    df = hourly_data[(hourly_data.ssvid == gap.ssvid) \
                   & (hourly_data.gap_id == gap_id)
                   & (hourly_data.date.dt.date >= query_start.date()) \
                   & (hourly_data.date.dt.date <= query_end.date())].copy()
    df.drop(df[(df.date.dt.date == query_start.date()) & (df.hour < query_start.hour)].index, inplace=True)
    df.drop(df[(df.date.dt.date == query_end.date()) & (df.hour > query_end.hour)].index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.sort_values(['date', 'hour'], inplace=True)
    
    return df


##############################################################
### Table creation functions for each supported table type ###
##############################################################

### Creates basic table with only GFW related attributes 
### (no Exact Earth dependencies)
def plot_table_basic(all_gaps, show_all_gaps):
    
    gap_hours = []
    gap_offon_class = []
    gap_implied_speed = []
    gap_reception = []
    for index, gap in all_gaps.iterrows():
        gap_hours.append('%0.2f' % gap.gap_hours)
        gap_offon_class.append('%s/%s' % (gap.off_class, gap.on_class))
        gap_implied_speed.append('%0.2f' % gap.gap_implied_speed_knots)
        gap_reception.append('%0.2f/%0.2f' % (gap.positions_per_day_off, gap.positions_per_day_on))


    # Create the gaps info table.
    cell_text = [gap_hours, gap_offon_class, gap_implied_speed, gap_reception]
    rows =  ['Gap Length (h)', 'Off/On Class', 'Implied Speed (knots)', 'PPD at off/on']
        
    num_gaps = all_gaps.shape[0]
    bbox = ([0.3, 0.3, 0.3, 1] if num_gaps == 1 else ([0.3, 0.3, 0.5, 1.0] if num_gaps < 4 else [0.2, 0.3, 0.8, 1.0]))
    table = plt.table(cellText = cell_text, rowLabels = rows, loc='center', \
              bbox=bbox)
    table.set_fontsize(12)
    
    return table


### Creates table for use with Exact Earth gaps including
### attributes relevant for the gap classification modeling
def plot_table_ee(all_gaps):
    
    ### TABLE ###
    gap_hours = []
    gap_offon_class = []
    gap_implied_speed = []
    gap_reception = []
    gap_ee_pos = []
    gap_ee_pos_invalid = []
    gap_ee_pos_4hr = []
    gap_max_ee_gap = []
    gap_max_gap = []
    model_part1 = []
    model_part2 = []
    for index, gap in all_gaps.iterrows():
        gap_hours.append('%0.2f' % gap.gap_hours)
        gap_offon_class.append('%s/%s' % (gap.off_class, gap.on_class))
        gap_implied_speed.append('%0.2f' % gap.gap_implied_speed_knots)
        gap_reception.append('%0.2f/%0.2f' % (gap.positions_per_day_off, gap.positions_per_day_on))
        gap_ee_pos.append('%d' % gap.ee_positions)
        gap_ee_pos_invalid.append('%d' % gap.ee_positions_invalid)
        gap_ee_pos_4hr.append('%d' % gap.ee_positions_over_4hr)
        gap_max_ee_gap.append('%0.2f' % gap.max_ee_gap)
        gap_max_gap.append('%0.2f' % gap.max_gap)
        model_part1.append('X' if gap.ee_positions_over_4hr == 0 and gap.max_gap >= 12 else '-')
        model_part2.append('X' if gap.max_gap >= 24 and gap.max_gap > 0.5*gap.gap_hours else '-')

    ### TABLE ###
    # Create the gaps info table.
    cell_text = [gap_hours, gap_offon_class, gap_implied_speed, gap_reception, \
                 gap_ee_pos, gap_ee_pos_4hr, gap_max_ee_gap, gap_max_gap, \
                 model_part1, model_part2]
    rows =  ['Gap Length (h)', 'Off/On Class', 'Implied Speed (knots)', 'PPD at off/on', \
             'EE Positions', 'EE Positions - 4hr buffer', \
             'Max EE Gap Length (h)', 'Max Gap Length (h)', \
             'No EE in gap (4hr buffer) & max gap>=12h', 'Max gap>=24h & max gap>0.5*gap hours']
        
    num_gaps = all_gaps.shape[0]
    bbox = ([0.35, -0.6, 0.3, 2.0] if num_gaps == 1 else ([0.3, -0.6, 0.5, 3.0] if num_gaps < 4 else [0.2, -0.6, 0.8, 3.0]))
    table = plt.table(cellText = cell_text, rowLabels = rows, loc='center', \
              bbox=bbox)
    table.set_fontsize(12)
    
    return table


##############################
### MAIN PLOTTING FUNCTION ###
##############################

### Inputs
# gap_id: the gap_id for the gap to plot
# gaps_data: dataframe with all the relevant gap data from either `proj_ais_gaps_catena.raw_gaps_v` 
#     (if using table_type == 'none' or 'basic') or `proj_ais_gaps_catena.raw_gaps_with_ee_stats_v` 
#     (if using table_type == 'ee')
# positions_gfw: AIS positions from `gfw_research.pipe_v` or `gfw_research.pipe_vYYYYMMDD_fishing`
# hourly_data: hourly positions data from `gfw_research_precursors.ais_positions_byssvid_hourly_v`
# positions_ee: Exact Earth positions from `world-fishing-827.ais_exact_earth.XXXX_csv_data_formated_and_partitioned` (where XXXX is 2017, 2018, or 2019)
# (optional - if excluded, cannot use table_type == 'ee')
# performance_data: performance metrics calculated from by the query available in doc/Examples.py (optional - if excluded, metrics will not be included in the visualization)
# show_all_gaps: True if all gaps in the visualized time period should be marked or False if only the gap represented by gap_id should be marked (note: will only include gaps represented in gaps_data)
# table_type: "none", "basic", or "ee" (see doc/Examples.py)
# out_dir: location to save image to (if None, no image will be exported)

### Outputs:
# Figure, (GridSpec axes)

def plot_gap(gap_id, gaps_data, positions_gfw, hourly_data, positions_ee=None, performance_data=None, show_all_gaps=False, table_type="basic", out_dir=None):
    if table_type not in ["none", "basic", "ee"]:
        raise("%s is not a valid model type. Choose from 'none', basic', or 'ee'.")
        
    # Set boolean based on if positions_ee is non-empty.
    has_ee = False
    if positions_ee is not None and positions_ee.shape[0] > 0:
        has_ee = True
    
    # Filter to positions for this gap_id
    # If there are no positions, print an error message
    # This is most likely because the vessel is not in the version of
    # `pipe_vYYYYMMDD_fishing` that is being used.
    df_positions_gfw = positions_gfw[positions_gfw.gap_id == gap_id]
    if df_positions_gfw.empty:
        raise("An image cannot be produced for gap %s because there are no Spire/Orbcomm positions for this dataset. This is usually do to vessels being left out of the `pipe_vYYYYMMDD_fishing` database." % gap_id)
    
    # Get information for this gap and print out ssvid and gap_id
    gap_info = gaps_data[gaps_data.gap_id == gap_id].iloc[0]
    print(gap_info.ssvid)
    print(gap_id)
    
    # If show_all_gaps=True, then get information for ALL gaps from df_gaps between query_start and query_end because there may be more than the one of interest.
    # ELSE, set df_all_gaps to single gap
    # TODO: extend to include gaps that are partially within the query timeframe. Right now they are ignored
    if show_all_gaps:
        df_all_gaps = gaps_data[(gaps_data.ssvid == gap_info.ssvid) \
                              & (gaps_data.gap_start >= df_positions_gfw.timestamp.min()) \
                              & (gaps_data.gap_end <= df_positions_gfw.timestamp.max())].sort_values('gap_start').reset_index(drop=True)
    else:
        df_all_gaps = gaps_data[gaps_data.gap_id == gap_id]

    # If this gap has EE data, merge and sort the GFW and EE positions by timestamp.
    if (has_ee):
        df_positions_ee = positions_ee[(positions_ee.gap_id == gap_id)]
        df_positions_ee = df_positions_ee.assign(receiver_type = 'exactearth')
        df_positions_all = df_positions_gfw[['ssvid', 'timestamp', 'lat', 'lon', 'receiver_type']].append(df_positions_ee[['ssvid', 'timestamp', 'lat', 'lon', 'receiver_type']], ignore_index=True)
        df_positions_all = df_positions_all.sort_values('timestamp').reset_index(drop=True)
    else:
        df_positions_all = df_positions_gfw[['ssvid', 'timestamp', 'lat', 'lon', 'receiver_type']]
        df_positions_all = df_positions_all.sort_values('timestamp').reset_index(drop=True)

        
    with pyseas.context(pyseas.styles.light):
        with pyseas.context({'pyseas.eez.bordercolor' : 'black', \
                             'pyseas.map.trackprops': custom_artist_cycler}):
            gs = gridspec.GridSpec(ncols=1, nrows=3, height_ratios=[4, 2, 1])
            fig = plt.figure(figsize=(8, 12))

            ### STYLING
            start_color_face = "#742980"
            start_color_edge = "#742980"
            gap_map_color = "#3c3c3b"
            gap_fig_color_face = "#e6e7eb"
            gap_fig_color_edge = "#848b9b"
            sat_color = "#e74327"
            ter_color = "#204280"
            ee_color = "#8abbc7"
            
            fig.patch.set_facecolor('white')

            params = {"font.size": 12.0,
                      "legend.fontsize": 12.0,
                      "xtick.labelsize": 12.0,
                      "ytick.labelsize": 12.0,
                      "axes.labelsize": 12.0
                     }
            plt.rcParams.update(params)

            ### Create the main map. Buffer out by 10% (or im_buffer_prop) in each direction.
            extent = [df_positions_all.lon.min(), df_positions_all.lon.max(), \
                      df_positions_all.lat.min(), df_positions_all.lat.max()]
            im_buffer_prop = 0.1 # proportion of lat or lon to use to buffer out the extent
            im_buffer_lon = (extent[1] - extent[0]) * im_buffer_prop
            im_buffer_lat = (extent[3] - extent[2]) * im_buffer_prop
            
            proj_info = maps.find_projection(df_positions_all.lon, df_positions_all.lat)
            maps.create_map(subplot=gs[0], projection=proj_info.projection,
                           extent=[extent[0] - im_buffer_lon, extent[1] + im_buffer_lon, \
                                   extent[2] - im_buffer_lat, extent[3] + im_buffer_lat])
            gl = maps.add_gridlines()
            maps.add_gridlabels(gl)
            maps.add_land()
            maps.add_eezs()

            ### Add the GFW track
            maps.plot(df_positions_all.lon, df_positions_all.lat, color='#b2b2b2', zorder=0)
            
            ### Add the inset where it's working currently
            try:
                inset = maps.add_miniglobe(loc='lower left', offset="outside", central_marker='*', marker_size=9, marker_color='#0c276c')
            except:
                inset = None
    
            ### Plot the starting point.
            plt.gca().scatter(df_positions_all.iloc[0].lon, df_positions_all.iloc[0].lat, transform=maps.identity, color=start_color_face, edgecolor=start_color_edge, ls='-', lw=1, s=180, marker='*', label="Start", zorder=51)

            ### Plot the positions divided up by satellite versus terrestrial.    
            sat_lon, sat_lat = df_positions_all[df_positions_all.receiver_type == "satellite"].lon, df_positions_all[df_positions_all.receiver_type == "satellite"].lat
            terr_lon, terr_lat = df_positions_all[df_positions_all.receiver_type == "terrestrial"].lon, df_positions_all[df_positions_all.receiver_type == "terrestrial"].lat

            plt.gca().scatter(sat_lon, sat_lat, transform=maps.identity, color=sat_color, s=30, label="Satellite", zorder=3)
            plt.gca().scatter(terr_lon, terr_lat, transform=maps.identity, color=ter_color, s=15, label="Terrestrial", zorder=4)

            ### Plot single gap of interest.
            ### NOTE: this currently does not have info for all gaps 
            ### in the time period, only the original one chosen as one of the random 100.
            gap_start_lon, gap_start_lat = gap_info.off_lon, gap_info.off_lat
            gap_end_lon, gap_end_lat = gap_info.on_lon, gap_info.on_lat

            plt.gca().plot([gap_start_lon, gap_end_lon], [gap_start_lat, gap_end_lat], transform=maps.identity, color=gap_map_color, zorder=50)
            plt.gca().scatter(gap_start_lon, gap_start_lat, transform=maps.identity, color=gap_map_color, marker='X', s=90, zorder=50, label="Gap Start")
            plt.gca().scatter(gap_end_lon, gap_end_lat, transform=maps.identity, color=gap_map_color, marker='s', s=50, zorder=50, label="Gap End")

            ### If this track has Exact Earth points, plot them on the map
            if (has_ee):
                plt.gca().scatter(df_positions_ee.lon, df_positions_ee.lat, transform=maps.identity, color=ee_color, marker='^', s=30, label="Exact Earth", zorder=1)

            ### Legend and title
            plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5), facecolor="#f7f7f7", framealpha=1.0)
            
            plot_title = f'''Tracks for vessel {gap_info.ssvid}: \n{gap_info.gap_start:%Y-%m-%d %H:%M:%S} to {gap_info.gap_end:%Y-%m-%d %H:%M:%S}\n{gap_id}'''
            if table_type == 'none':
                plot_title += f'''\n{gap_info.vessel_class} -- {gap_info.flag}'''
            plt.title(plot_title, size=20)


            ### Get hourly positions for GFW and create a timestamp column that combines date and hour.
            df_gap_hourly = get_hourly_positions(gap_id, gaps_data, hourly_data)
            df_gap_hourly = df_gap_hourly.assign(timestamp = pd.to_datetime(df_gap_hourly.date, format='%Y%m%d %H%M%S') + pd.to_timedelta(df_gap_hourly.hour, unit='h'))
            df_gap_hourly.timestamp = df_gap_hourly.timestamp.apply(lambda ts: ts.tz_localize(tz='UTC'))

            ### Graph hourly positions by type
            ax1 = fig.add_subplot(gs[1])
            plt.plot(df_gap_hourly.timestamp, df_gap_hourly.sat_positions, color=sat_color, label="Satellite", zorder=3)
            plt.plot(df_gap_hourly.timestamp, df_gap_hourly.ter_positions, color=ter_color, label="Terrestrial", zorder=2)
            if (has_ee):
                plt.plot(df_gap_hourly.timestamp, df_gap_hourly.ee_positions, color=ee_color, label="Exact Earth", zorder=1)

            ### Highlight the gap to be labeled
            plt.axvspan(gap_info.gap_start, gap_info.gap_end, ls="-", lw=0.7, edgecolor=gap_fig_color_edge, facecolor=gap_fig_color_face, alpha=0.5, zorder=0, label="Gap" if 'Gap' not in plt.gca().get_legend_handles_labels()[1] else '')

            # Add hour markers to x-axis
            hours = mpdates.HourLocator()
            ax1.xaxis.set_minor_locator(hours)
            
            # Add legend and y-axis label
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), facecolor="#f7f7f7", framealpha=1.0)
            plt.ylabel('Positions per hour')

            # Leave extra space between plots for the inset
            plt.subplots_adjust(hspace=0.4)
            
            for index, gap in df_all_gaps.iterrows():
                plt.axvspan(gap.gap_start, gap.gap_end, ls="-", lw=0.7, edgecolor=gap_fig_color_edge, facecolor=gap_fig_color_face, alpha=0.5, zorder=0, label="Gap" if 'Gap' not in plt.gca().get_legend_handles_labels()[1] else '')

            
            ### TABLE ###
            if table_type != 'none':
                
                ax2 = fig.add_subplot(gs[2])

                if table_type == 'basic':
                    plot_table_basic(df_all_gaps, show_all_gaps)
                if table_type == 'ee':
                    plot_table_ee(df_all_gaps)
    
                ax2.axis("off")

            
            ### Add information on satellite class, vessel type, and reception quality
            if table_type != 'none':
                num_gaps = df_all_gaps.shape[0]
                x_offset = (0.7 if num_gaps == 1 else (0.85 if num_gaps < 4 else 1.05))
                x_offset = 1.3 if table_type == 'none' else x_offset
                y_offsets = [0.95, 0.75, 0.55, 0.35, 0.15, -0.05] if table_type == 'none' else [1.2, 1.0, 0.8, 0.6, 0.4, 0.2]
                plt.text(x_offset, y_offsets[0], 'Vessel: %s' % gap_info.vessel_class, transform=plt.gca().transAxes, fontsize='14')
                plt.text(x_offset, y_offsets[1], 'Flag: %s' % gap_info.flag, transform=plt.gca().transAxes, fontsize='14')
                if performance_data is not None:
                    vessel_perf = performance_data[performance_data.ssvid == gap_info.ssvid].iloc[0] 
                    plt.text(x_offset, y_offsets[2], 'Actual Class: %s' % vessel_perf.actual_class, transform=plt.gca().transAxes, fontsize='14')
                    plt.text(x_offset, y_offsets[3], 'Avg Sat. PPD: %0.2f' % vessel_perf.avg_sat_positions_per_day, transform=plt.gca().transAxes, fontsize='14')
                    plt.text(x_offset, y_offsets[4], 'Avg Expected PPD: %0.2f' % vessel_perf.avg_expected_positions_per_day, transform=plt.gca().transAxes, fontsize='14')
                    plt.text(x_offset, y_offsets[5], 'Ratio actual/exp.: %0.2f' % vessel_perf.ratio_actual_to_expected, transform=plt.gca().transAxes, fontsize='14')

            if out_dir:
                plt.savefig(os.path.join(out_dir, 'gap_%s.png' % gap_id), bbox_inches='tight', dpi=150)
                
            plt.show()
            
            return fig, (gs[0], gs[1], gs[2])

