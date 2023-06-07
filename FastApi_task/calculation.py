from math import sqrt

def calculate_distance(lat1:float,lon1:float,lat2:float,lon2:float):
    
    x_diffrence_sqr = (lat2-lat1) ** 2
    y_diffrence_sqr = (lon2-lon1) ** 2
    
    distance = sqrt(x_diffrence_sqr + y_diffrence_sqr) 
    
    return distance