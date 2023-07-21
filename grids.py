import numpy as np

def closest_gridpoint_indexes(lat,lon,ds):
    '''
    Returns the indexes of the grid point
    closest to the given location.

            Parameters:
                    lat (float): Latitude of location
                    lon (float): Longitude of location
                    ds (xarray.Dataset): Target dataset 

            Returns:
                    xloc, yloc (numpy.int64, numpy.int64): x and y indexes of the grid point closest to location
    '''
    abslon = np.abs(ds.longitude-lon)
    abslat = np.abs(ds.latitude-lat)
    
    c = np.maximum(abslon, abslat)
    
    ([xloc], [yloc]) = np.where(c == np.min(c))
    
    return xloc, yloc