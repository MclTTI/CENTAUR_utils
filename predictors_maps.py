import pandas as pd
from matplotlib import pyplot as plt
import cartopy.crs as ccrs

from maps import decorate_axes, custom_cbar



cfill_cmaps = {'air_pressure_at_mean_sea_level' : 'nipy_spectral',
               'air_temperature' : 'coolwarm',
               'eastward_wind' : 'PiYG_r',
               'geopotential' : 'nipy_spectral',
               'lagrangian_tendency_of_air_pressure' : 'RdBu',
               'northward_wind' : 'PiYG_r',
               'specific_humidity' : 'PuBu',
               }



cline_col = {'air_pressure_at_mean_sea_level' : 'black',
             'air_temperature' : 'crimson',
             'eastward_wind' : 'cornflowerblue',
             'geopotential' : 'black',
             'lagrangian_tendency_of_air_pressure' : 'cornflowerblue',
             'northward_wind' : 'cornflowerblue',
             'geopotential' : 'black',
             'specific_humidity' : 'darkviolet',
             }



def convert_variable(var):

    #print(var.standard_name)
    #print(var.units)
    #print(var)

    if var.standard_name == 'air_pressure_at_mean_sea_level':
        var_out = var/100
        var_name = 'Mean sea level pressure'
        var_units = 'hPa'

    elif var.standard_name == 'air_temperature':
        var_out = var - 273.15
        var_name = 'Temperature'
        var_units = 'C'

    elif var.standard_name == 'eastward_wind':
        var_out = var
        var_name = 'U component of wind'
        var_units = 'm/s'

    elif var.standard_name == 'geopotential':
        var_out = (var / 9.80665)/10
        var_name = 'Geopotential height'
        var_units = 'dam'

    elif var.standard_name == 'lagrangian_tendency_of_air_pressure':
        var_out = var
        var_name = 'Vertical velocity'
        var_units = 'Pa/s'

    elif var.standard_name == 'northward_wind':
        var_out = var
        var_name = 'V component of wind'
        var_units = 'm/s'

    elif var.standard_name == 'specific_humidity':
        var_out = var / 1000
        var_name = 'Specific humidity'
        var_units = 'g/Kg'

    else:
        print('Variable not in list!')
        var_out = var
        var_name = ''
        var_units = ''
    
    return var_out, var_name, var_units



def get_colors(var):
    """
    Get colors for contours
    """

    if hasattr(var,"standard_name"):
        cfill = cfill_cmaps[var.standar_name]
        cline = cline_col[var.standar_name]

    elif hasattr(var,"long_name"):
        cfill = 'viridis'
        cline = 'black'
    else:
        cfill = 'viridis'
        cline = 'black'
    
    return cfill, cline



def convert_get_attr(var):
    """
    Convert the variable as needed
    """

    if hasattr(var,"standard_name"):
        var_out, var_name, var_units = convert_variable(var)

    elif hasattr(var,"long_name"):
        var_out = var
        var_name = var.long_name
        var_units = var.units
    else:
        var_out = var
        var_name = ''
        var_units = ''
    
    return var_out, var_name, var_units



def contour_var(var,T,lev=None,filled=True,ds_name=''):

    # Get time stamp
    TIME_STAMP = pd.to_datetime(str(T.values)).strftime('%a %d %h %y  %H UTC')

    # Extract lat and lon
    lons = var['longitude'].values[:]
    lats = var['latitude'].values[:]

    #Extract variable, convert plev in hPa
    if lev not in [None, 'sfc']:
        LEV = lev*100
        LEV_descr = f'{lev} hPa'
        VAR, var_name, var_units = convert_get_attr(var.sel(time=T,plev=LEV))
    else:
        LEV = 'sfc'
        LEV_descr = LEV
        VAR, var_name, var_units = convert_get_attr(var.sel(time=T))
    
    # Make plot
    fig, ax = plt.subplots(subplot_kw={'projection':ccrs.PlateCarree()},figsize=(8,8))

    ax.text(0,1.01,
            f'Lev = {LEV_descr}',
            fontsize='large',transform=ax.transAxes)

    ax.set_title(f'{TIME_STAMP}',loc='right',fontsize='large',weight='bold',pad=6)


    ax = decorate_axes(ax,lons,lats)

    if filled == True:

        CMAP, _ = get_colors(var)

        ax.text(0,1.05,
            f'{ds_name}',
            fontsize='xx-large',transform=ax.transAxes,weight='bold')
        
        cfplot = ax.contourf(lons,lats,VAR,
                             #levels=[float(c) for c in clevs_prec],
                             alpha=0.7,
                             transform=ccrs.PlateCarree(),
                             cmap=CMAP,
                             #colors=[clevs_prec[c] for c in clevs_prec.keys()]
                             )
        
        cbar = custom_cbar(fig,ax,cfplot,label=f'{var_name} ({var_units})')

    else:

        _, cline_color = get_colors(var)

        ax.text(0,1.07,
            f'{ds_name}',
            fontsize='xx-large',transform=ax.transAxes,weight='bold')
        
        ax.text(0,1.04,
                f'{var_name} ({var_units})',
                fontsize='large',transform=ax.transAxes,weight='bold')
        

        cplot = ax.contour(lons,lats,VAR,
                           levels=12,
                           colors=cline_color,
                           alpha=0.75,
                           linewidths=1,
                           linestyles='dashed',
                           transform=ccrs.PlateCarree(),
                           )
        
        cplot.clabel(fmt='%d')

    return fig


 
 