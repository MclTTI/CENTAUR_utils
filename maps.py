import re

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import plotly.express as px
import plotly.graph_objects as go

from grids import fix_coordinates


#############################
# Contour levels and
# color scale definition
#############################

# Precipitation
clevs_prec = {0 : "white",
              0.5 : "cyan",
              2 : "dodgerblue",
              4 : "blue",
              10 : "orchid",
              25 : "magenta",
              50 : "darkorange",
              100 : "red",
              250 : "red"}

# Return period  (RP starts form 1!)
clevs_rp = {1 : "green",
            2 : "lime",
            5 : "yellow",
            10 : "gold",
            20 : "orange",
            50 : "crimson",
            100 : "magenta",
            500 : "darkorchid"}

# Precipitation RP thresholds
# clevs_thresh = {10 : "cyan",
#                 12.5 : "darkturquoise",
#                 15 : "dodgerblue",
#                 17.5 : "blue",
#                 20 : "darkblue",
#                 25 : "blueviolet",
#                 30 : "mediumorchid",
#                 40 : "orchid",
#                 50 : "palevioletred",
#                 75 : "salmon",
#                 100 : "gold",
#                 125 : "yellow",
#                 150 : "orange",
#                 175 : "darkorange",
#                 200 : "orangered",
#                 250 : "red",
#                 300 : "firebrick",
#                 350 : "firebrick"}

clevs_thresh = {10 : "cyan",
                20 : "dodgerblue",
                30 : "blue",
                40 : "blueviolet",
                50 : "mediumorchid",
                60 : "orchid",
                70 : "salmon",
                80 : "gold",
                90 : "yellow",
                100 : "orange",
                200 : "red",
                300 : "firebrick",
                400 : "firebrick"}



def decorate_axes(ax,lons,lats):
    '''
    Crop the given axes to the extent of the field to be plotted on it,
    add administrative boundaries, add geographic features
    and draw gridlines and labels.

            Parameters:
                    
            Returns:
                    
    '''

    ax.set_extent((lons[0],lons[-1],lats[0],lats[-1]),crs=ccrs.PlateCarree())
      
    #ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='black', facecolor='wheat'))
    #ax.patch.set_visible(False)

    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')
    
    ax.add_feature(states_provinces, edgecolor='gray')
    
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAKES)
    ax.add_feature(cfeature.RIVERS)
    #ax.add_feature(cfeature.LAND)
    
    gl=ax.gridlines(draw_labels=True,
                    linestyle='-',linewidth=1,color='gray',alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 16}
    gl.ylabel_style = {'size': 16}

    return ax



def custom_cbar(fig,ax,contour,label=''):

    cbar = fig.colorbar(contour,ax=ax,
                        orientation='horizontal',
                        shrink=0.9,aspect=60,pad=0.075,
                        ticks=None
                        )
    
    cbar.set_label(label=label,
                   size=16, weight='bold',labelpad=15)
    cbar.ax.tick_params(labelsize=16)

    return cbar



def mark_location(ax,lat,lon):
    ax.plot(lon,lat,
            marker='*',markersize=20,markeredgewidth=2.5,
            markeredgecolor='black',markerfacecolor="None",
            transform=ccrs.PlateCarree())
    
    return ax



def plot_prec(p,T,loc,ds_name=''):

    prec = fix_coordinates(p)
    
    # Extract variables
    lons = prec['longitude'].values[:]
    lats = prec['latitude'].values[:]
    pr = prec.sel(time=T).values[:,:]

    TIME_STAMP = pd.to_datetime(str(T.values)).strftime('%a  %d %h %y  %H UTC')
    
    # Make plot
    fig, ax = plt.subplots(subplot_kw={'projection':ccrs.PlateCarree()},figsize=(10,10))

    ax.set_title(f'{ds_name}',loc='left',fontsize=20,weight='bold',pad=2)
    ax.set_title(f'{TIME_STAMP}',loc='right',fontsize=20,weight='bold',pad=2)

    ax = decorate_axes(ax,lons,lats)
    
    cplot_prec = ax.contourf(lons,lats,pr,
                             levels=[float(c) for c in clevs_prec],
                             transform=ccrs.PlateCarree(),
                             #cmap=customColourMap,
                             colors=[clevs_prec[c] for c in clevs_prec.keys()]
                             )
    
    cbar_prec = custom_cbar(fig,ax,cplot_prec,label='Accumulated precipitation (mm/6h)')

    ax = mark_location(ax=ax,lon=loc['lon'],lat=loc['lat'])
        
    return fig

 

def plot_return_period(return_period,T,loc,ds_name=''):

    rp = fix_coordinates(return_period)

    # Extract variables
    lons = rp['longitude'].values[:]
    lats = rp['latitude'].values[:]
    RP = rp.sel(time=T).values[:,:]

    TIME_STAMP = pd.to_datetime(str(T.values)).strftime('%a  %d %h %y  %H UTC')
    
    # Make plot
    fig, ax = plt.subplots(subplot_kw={'projection':ccrs.PlateCarree()},figsize=(10,10))

    ax.set_title(f'{ds_name}',loc='left',fontsize=20,weight='bold',pad=2)
    ax.set_title(f'{TIME_STAMP}',loc='right',fontsize=20,weight='bold',pad=2)

    ax = decorate_axes(ax,lons,lats)
    
    cplot_rp = ax.contourf(lons,lats,RP,
                           levels=[float(c) for c in clevs_rp],
                           transform=ccrs.PlateCarree(),
                           #cmap=customColourMap,
                           colors=[clevs_rp[c] for c in clevs_rp.keys()]
                           )
    
    cbar = fig.colorbar(cplot_rp,ax=ax,
                        orientation='horizontal',
                        shrink=0.9,aspect=60,pad=0.075,
                        ticks=None
                        )
    
    cbar.set_label(label='Return period (years)',
                   size=16, weight='bold',labelpad=15)
    cbar.ax.tick_params(labelsize=16)

    ax = mark_location(ax=ax,lon=loc['lon'],lat=loc['lat'])
    
    return fig



def plot_prec_rp(p,return_period,T,loc,ds_name=''):

    prec = fix_coordinates(p)
    rp = fix_coordinates(return_period)
    
    #Extract variables
    lons = prec['longitude'].values[:]
    lats = prec['latitude'].values[:]

    lons_rp = rp['longitude'].values[:]
    lats_rp = rp['latitude'].values[:]

    assert np.all(lons == lons_rp)
    assert np.all(lats == lats_rp)

    pr = prec.sel(time=T).values[:,:]
    RP = rp.sel(time=T).values[:,:]

    TIME_STAMP = pd.to_datetime(str(T.values)).strftime('%a  %d %h %y  %H UTC')

    # Make plot
    fig, ax = plt.subplots(1,2,subplot_kw={'projection':ccrs.PlateCarree()},figsize=(18,10))

    fig.text(0.1, 0.925, f'{ds_name}',
             transform=fig.transFigure,ha='left',fontsize=20,weight='bold')
    fig.text(0.9, 0.925, f'{TIME_STAMP}',
             transform=fig.transFigure,ha='right',fontsize=20,weight='bold')
    
    # Plot precipitation
    cplot_prec = ax[0].contourf(lons,lats,pr,
                                levels=[float(c) for c in clevs_prec],
                                transform=ccrs.PlateCarree(),
                                #cmap=customColourMap,
                                colors=[clevs_prec[c] for c in clevs_prec.keys()]
                                )
    
    ax[0] = decorate_axes(ax[0],lons,lats)

    cbar_prec = custom_cbar(fig,ax[0],cplot_prec,label='Accumulated precipitation (mm/6h)')

    ax[0] = mark_location(ax=ax[0],lon=loc['lon'],lat=loc['lat'])

    # Plot return period
    cplot_rp= ax[1].contourf(lons,lats,RP,
                             levels=[float(c) for c in clevs_rp],
                             transform=ccrs.PlateCarree(),
                             #cmap=customColourMap,
                             colors=[clevs_rp[c] for c in clevs_rp.keys()]
                             )
    
    ax[1] = decorate_axes(ax[1],lons,lats)

    cbar_rp = custom_cbar(fig,ax[1],cplot_rp,label='Return period (years)')

    ax[1] = mark_location(ax=ax[1],lon=loc['lon'],lat=loc['lat'])
    
    return fig



def domain_map(grid,aoi,event):
    
    # Fix grid names if needed
    if 'lat' in grid and 'lon' in grid:
        grid.rename(columns={'lat':'latitude','lon':'longitude'},inplace=True)

    # Grid points
    grid = go.Figure(go.Scattermapbox(
        fill = None,
        hoverinfo = 'skip',
        lon = grid['longitude'],
        lat = grid['latitude'],
        marker = { 'size': 4, 'color': grid["color"] })#, 'symbol': ["cross"] })
        ) 
               
    # Area of interest

    # Coordinates of aoi vertexes
    aoi_lon = [pt[0] for pt in aoi.exterior.coords]
    aoi_lat = [pt[1] for pt in aoi.exterior.coords]
    print(f'AOI longitudes: {aoi_lon}')
    print(f'AOI latitudes: {aoi_lat}')
    
    roi = go.Figure(go.Scattermapbox(
        fill = "toself",
        hoverinfo = 'skip',
        lon = aoi_lon,
        lat = aoi_lat,
        marker = { 'size': 2, 'color': "red" })
        )
               
    fig = go.Figure(data=grid.data + roi.data)

    # Center the map on the event
    
    fig.update_layout(
        autosize=False,
        width=700,
        height=500,
        mapbox = {
            'style': "open-street-map",
            'center': {'lon': event['lon'], 'lat': event['lat'] },
            'zoom': 6},
        showlegend = False,
        margin={"r":25,"t":25,"l":25,"b":25}
        )

    return fig



def plot_threshold(p,loc,ds_name=''):

    prec = fix_coordinates(p)
    
    # Extract variables
    lons = prec['longitude'].values[:]
    lats = prec['latitude'].values[:]
    pr = prec.values[:,:]

    threshold = re.findall(r'\d+',prec.name)[0]
    
    # Make plot
    fig, ax = plt.subplots(subplot_kw={'projection':ccrs.PlateCarree()},figsize=(10,10))

    ax.set_title(f'{ds_name}',loc='left',fontsize=20,weight='bold',pad=2)
    ax.set_title(f'{threshold} years return period',loc='right',fontsize=20,weight='bold',pad=2)
    
    ax = decorate_axes(ax,lons,lats)
    
    cplot_prec = ax.contourf(lons,lats,pr,
                             levels=[float(c) for c in clevs_thresh.keys()],
                             transform=ccrs.PlateCarree(),
                             colors=[clevs_thresh[c] for c in clevs_thresh.keys()]
                             )
    
    cbar = custom_cbar(fig,ax,cplot_prec,label='Accumulated precipitation (mm/6h)')
    
    ax = mark_location(ax=ax,lon=loc['lon'],lat=loc['lat'])
    
    return fig



def plot_min_max_prec(p,ds_name=''):

    prec = fix_coordinates(p)
    
    #Extract variables
    lons = prec['longitude'].values[:]
    lats = prec['latitude'].values[:]

    prec_min = prec.min(dim='time').values[:,:]
    prec_max = prec.max(dim='time').values[:,:]

    # Make plots
    fig, ax = plt.subplots(1,2,subplot_kw={'projection':ccrs.PlateCarree()},figsize=(18,8))

    fig.text(0.1, 0.925, f'{ds_name}',
             transform=fig.transFigure,ha='left',fontsize=20,weight='bold')
    # fig.text(0.9, 0.925, f'',
    #          transform=fig.transFigure,ha='right',fontsize=20,weight='bold')

    # Plot min
    cplot_prec_min = ax[0].contourf(lons,lats,prec_min,
                                    levels=[float(c) for c in clevs_prec],
                                    transform=ccrs.PlateCarree(),
                                    colors=[clevs_prec[c] for c in clevs_prec.keys()]
                                    )
    
    ax[0] = decorate_axes(ax[0],lons,lats)
    cbar_prec = custom_cbar(fig,ax[0],cplot_prec_min,label='Min accumulated precipitation (mm/h)')

    # Plot max
    cplot_prec_max = ax[1].contourf(lons,lats,prec_max,
                                    levels=[float(c) for c in clevs_prec],
                                    transform=ccrs.PlateCarree(),
                                    colors=[clevs_prec[c] for c in clevs_prec.keys()]
                                    )
    
    ax[1] = decorate_axes(ax[1],lons,lats)
    cbar_prec = custom_cbar(fig,ax[1],cplot_prec_max,label='Max accumulated precipitation (mm/h)')
    
    return fig






