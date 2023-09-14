import numpy as np
import xarray as xr

def classify_rp(ds,thresholds=[1, 20, 50, 100, 200]):

    print(f'Using return period thresholds {[i for i in thresholds]} years.')

    if 'rp' in list(ds.keys()):
        da = ds['rp']
    else:
        print('Return period DataArray not in dataset, or wrong name.')

    #print(da)

    rp_class = np.digitize(da.fillna(0).load(), thresholds, right=False).astype(np.int8)

    #print(rp_class.min())
    #print(rp_class.max())
    #print(np.count_nonzero(np.isnan(rp_class)))

    # Read time, lon, lat and time_bnds from ds
    TIME = ds.time
    LN = ds.longitude
    LT = ds.latitude
    BNDS = ds.time_bnds

    # Create xarry Dataset and store results
    
    ds = xr.Dataset(
        data_vars={'rp_class' : (['time','latitude','longitude'],
                                 rp_class,
                                 {'long_name' : 'Return period class',
                                  'units' : 'class'}),
                                  #'_FillValue' : np.nan,
                                  #'missing_value' : np.nan}),
                   'time_bnds' : BNDS
                   },
        coords={"time" : TIME,
                "longitude" : LN,
                "latitude" : LT},
                    )
    
    #print(ds)
    
    return ds