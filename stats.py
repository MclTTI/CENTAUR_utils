def min_max_xarray(da):
    if da.long_name:
        lname = da.long_name
    else:
        lname = 'Data array'
    if da.units:
        units = da.units
    else:
        units = ''

    min = da.min().compute()
    max = da.max().compute()

    print(f'{lname} global minimum: {min.values} {units}')
    print(f'{lname} global maximum: {max.values} {units}')

    return