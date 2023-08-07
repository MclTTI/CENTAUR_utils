import re
from itertools import cycle

import matplotlib.pyplot as plt

from grids import closest_gridpoint_indexes


##################################
# Colors and markers definition
##################################
color_list = ['blue','red','green','black','gold','purple','brown','skyblue','darkorange','pink']
markers = cycle('x.^2p*+')
colors = cycle(color_list)

##################################



def prec_rp_spaghetti_plot(prec,rp,poi,main_loc,event_time,ds_name=''):

    # locate the grid point nearest to main loc
    x, y = closest_gridpoint_indexes(lat=main_loc['lat'],
                                     lon=main_loc['lon'],
                                     ds=prec)
    
    main_ts = prec.isel(longitude=x,latitude=y)
    main_lon = main_ts['longitude'].values
    main_lat = main_ts['latitude'].values

    # make plots
    fig, ax = plt.subplots(2,1,figsize=(14,12))

    fig.text(0.1, 0.925, f'{ds_name}',
             transform=fig.transFigure,ha='left',fontsize=20,weight='bold')
    fig.text(0.9, 0.925, f'Grid points in a radius of 0.2 degree from\n({main_lat:.4f}, {main_lon:.4f})',
             transform=fig.transFigure,ha='right',fontsize=20,weight='bold')
    
    # Vertical line at event time
    ax[0].axvline(event_time, color='red',linewidth=2,linestyle='--')
    ax[1].axvline(event_time, color='red',linewidth=2,linestyle='--')
    
    for _,row in poi.iterrows():
        LN = row['longitude']
        LT = row['latitude']
        #print(f'lat: {LT}, lon: {LN}')

        if (LN == main_lon) and (LT == main_lat):
            lwidth = 2
            cprec = 'navy'
            crp = 'darkorchid'
        else:
            lwidth = 0.75
            cprec = 'deepskyblue'
            crp = 'violet'
    
        # Manual exclusion of flawed grid points
        #if (LT==41.74986002750993 and LN==-0.9501396052110067):
        #    continue
        
        ts_pr6 = prec.sel(longitude=LN,latitude=LT)
        ts_rp = rp.sel(longitude=LN,latitude=LT)
        
        # Filter grid points with a lot of Nan
        null = ts_rp.isnull().values
        if len(null[null==True]) >= len(null)/4:
            print(f'Too many Nan at ({LN},{LT})')
            continue
        
        # Precipitation
        ax[0].plot(ts_pr6['time'],ts_pr6,
                   label=f"{ts_pr6['longitude'].values},{ts_pr6['latitude'].values}",
                   color=cprec,
                   linewidth=lwidth)
        
        #ax[0].set_ylim(bottom=-1)
        ax[0].margins(y=0.05)

        ax[0].set_title('Accumulated precipitation',
                        fontsize=16,fontweight='bold',pad=5,loc='left')

        ax[0].tick_params(axis='x', which='both', labelbottom=False)
        ax[0].xaxis.set_major_locator(plt.MaxNLocator(12))

        ax[0].tick_params(axis='y', which='major', labelsize=16)
        ax[0].set_ylabel('mm/6h',size=16,weight='bold',labelpad=10)

        ax[0].grid(True,axis='both')
        
        # Return period
        ax[1].plot(ts_rp['time'],ts_rp,
                   label=f"{ts_pr6['longitude'].values},{ts_pr6['latitude'].values}",
                   color=crp,
                   linewidth=lwidth)
        
        #ax[1].set_ylim(bottom=0.95)
        ax[1].margins(y=0.05)

        ax[1].set_title('Return period',
                        fontsize=16,fontweight='bold',pad=5,loc='left')

        #xlab = pd.to_datetime(str(ts_rp['time'])).strftime('%d %h %y')    
        #ax[1].set_xticks(ts_rp['time'],labels=xlab)
        
        ax[1].tick_params(axis='x', labelrotation=60, labelsize=14)
        ax[1].xaxis.set_major_locator(plt.MaxNLocator(12))

        ax[1].tick_params(axis='y', which='major', labelsize=16)
        ax[1].set_ylabel('years',size=16,weight='bold',labelpad=10)

        ax[1].grid(True,axis='both')

        # ax[1].legend()

    return fig



def scatter_rp_prec(ds,main_loc,points,ds_name=''):
    
    # locate the grid point nearest to main loc
    x, y = closest_gridpoint_indexes(lat=main_loc['lat'],
                                     lon=main_loc['lon'],
                                     ds=ds)
    
    main_ds = ds.isel(longitude=x,latitude=y)
    main_lon = main_ds['longitude'].values
    main_lat = main_ds['latitude'].values
    
    #Make plot
    fig, ax = plt.subplots(figsize=(12,8))

    fig.text(0.1, 0.925, f'{ds_name}',
             transform=fig.transFigure,ha='left',fontsize=20,weight='bold')
    fig.text(0.9, 0.925, f'Grid points within 0.2 degrees\nfrom({main_lat:.4f}, {main_lon:.4f})',
             transform=fig.transFigure,ha='right',fontsize=16,weight='bold')

    ax.tick_params(axis='x', which='both', labelsize=16)
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax.set_xlabel('Accumulated precipitation [mm/6h]',size=16,weight='bold',labelpad=10)
    
    ax.set_yscale("log")
    ax.tick_params(axis='y', which='both', labelsize=16)
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))
    ax.set_ylabel('Return Period [years]',size=16,weight='bold',labelpad=10)
    
    ax.grid(True,axis='both')

    for idx,_ in points.reset_index().iterrows():
        #print(idx)
        lon = points.iloc[idx].loc['longitude']
        lat = points.iloc[idx].loc['latitude']
        
        COLR = next(colors)

        rp_levs = [rp for rp in ds if rp.startswith('rp')]
        
        for rp in rp_levs:
            years = float(re.findall(r'\d+', rp)[0])
            prec  = ds[f'{rp}'].sel(latitude=lat,longitude=lon).values
            ax.scatter(prec,years,c=COLR,marker='x',s=70)
            
    return fig