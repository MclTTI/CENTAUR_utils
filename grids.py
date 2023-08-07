import numpy as np
import geopandas as gpd

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
    if 'lon' in ds.coords and 'lat' in ds.coords:
        ds = ds.rename({'lon' : 'longitude', 'lat' : 'latitude'})
    
    abslon = np.abs(ds.longitude-lon)
    abslat = np.abs(ds.latitude-lat)
    
    c = np.maximum(abslon, abslat)
    
    ([xloc], [yloc]) = np.where(c == np.min(c))
    
    return xloc, yloc



def in_circle(dataarray,center,radius=0.2):

    p = gpd.points_from_xy([center['lon']],
                           [center['lat']],
                           crs="EPSG:4326")
    
    q = p.buffer(radius)

    # Convert datarray to GeoDataFrame
    df = dataarray.to_dataframe()
    
    lats = df.index.get_level_values('latitude')
    lons = df.index.get_level_values('longitude')
    
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(lons,lats),crs="EPSG:4326")
    gdf.reset_index(inplace=True)

    # Locate and return points within buffer
    gdf['in_buffer'] = gdf['geometry'].within(q[0])
    return gdf.loc[gdf['in_buffer']==True]

