import pandas as pd

from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature



#############################
# Contour levels and
# color scale definition
#############################

# Precipitation
clevs_prec = [0,0.5,2,4,10,25,50,100,250]
colors_prec = ["white","cyan","dodgerblue","blue", "orchid", "magenta", "darkorange","red","red"]

# Return period  (RP starts form 1!)
clevs_rp = [0,1,2,5,10,20,100]
colors_rp = ["white","green","yellow","orange","red","magenta"]



def decorate_axes(ax,lons,lats):
    '''
    Crop the given axes to the extent of the field to be plotted on it,
    add administrative boundaries, add geographic features
    and draw gridlines and labels.

            Parameters:
                    
            Returns:
                    
    '''

    ax.set_extent((lons[0],lons[-1],lats[0],lats[-1]))
    
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



def plot_prec(prec,T,loc,ds_name=''):

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
                             levels=clevs_prec,
                             transform=ccrs.PlateCarree(),
                             #cmap=customColourMap,
                             colors=colors_prec
                             )
    
    cbar = fig.colorbar(cplot_prec,ax=ax,
                        orientation='horizontal',
                        shrink=0.9,aspect=60,pad=0.075,
                        ticks=None
                        )
    
    cbar.set_label(label='Accumulated precipitation (mm/6h)',
                   size=16, weight='bold',labelpad=15)
    cbar.ax.tick_params(labelsize=16)

    ax.plot(loc['lon'],loc['lat'],
            marker='*',markersize=20,markeredgewidth=2.5,
            markeredgecolor='black',markerfacecolor="None",
            transform=ccrs.PlateCarree())
    
    return fig















