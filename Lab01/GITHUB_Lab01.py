# OA3801 (Comp Methods II)
# Naval Postgraduate School
# This simple module includes a class representation of a Coordinate,
# along with a few support functions.

import math
import datetime

class Coordinate:
    '''A simple class to represent lat/lon values.'''
    
    def __init__(self,lat,lon):
        self.lat = float(lat)  # make sure it's a float
        self.lon = float(lon)  
        
    # Follows the specification described in the Aviation Formulary v1.46
    # by Ed Williams (originally at http://williams.best.vwh.net/avform.htm)
    def calc_dist(self, other):
        lat1 = deg2rad(self.lat)
        lon1 = deg2rad(self.lon)
        lat2 = deg2rad(other.lat)
        lon2 = deg2rad(other.lon)
        
        # there are two implementations of this function.
        # implementation #1:
        #dist_rad = math.acos(math.sin(lat1) * math.sin(lat2) 
        #                   + math.cos(lat1) * math.cos(lat2) * math.cos(lon1-lon2))

        # implementation #2: (less subject to numerical error for short distances)
        dist_rad=2*math.asin(math.sqrt((math.sin((lat1-lat2)/2))**2 +
                   math.cos(lat1)*math.cos(lat2)*(math.sin((lon1-lon2)/2))**2))

        return rad2nm(dist_rad)
    

    def __str__(self):
        return "(%f,%f)" % (self.lat,self.lon)
    
    def __repr__(self):
        return "Coodinate(%f,%f)" % (self.lat,self.lon)        

# end of class Coordinate


# The following functions are of general use.

def dms_to_decimal(degrees,minutes,seconds):
    '''Convertes coordinates in dms to decimals.'''
    return degrees + minutes/60 + seconds/3600

def deg2rad(degrees):
    '''Converts degrees (in decimal) to radians.'''
    return (math.pi/180)*degrees

def rad2nm(radians):
    '''Converts a distance in radians to a distance in nautical miles.'''
    return ((180*60)/math.pi)*radians

       

class Vessel:
    '''Simple representation of a Vessel for use with AIS data.'''

    def __init__(self,MMSI,vessel_name=None,vessel_type=None,length=0):
        self.MMSI=MMSI  # assumed to be unique and permanent
        self.name = vessel_name
        self.type = vessel_type
        self.length = length
        self.track = dict() #the track is a dictionary with 'time' keys and (lat,long) tuples
        self.call_signs = set() # an empty set (could be many call_signs)

    #add a new location to the track dict 
    def add_to_track(self,time,lat,lon,call_sign=None):
        '''Adds a new time/location to the track.
           'time' is assumed to be a string in the form '%Y-%m-%d %H:%M:%S'
           'lat','lon' are assumed to be compatible with Coordinate objects.
        '''
        timestamp = datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
        self.track[timestamp]=Coordinate(lat,lon)

        # because call_signs can change, add a new one if found
        if call_sign:
            self.call_signs.add(call_sign)


    def initial_position(self):
        time_series = sorted(self.track)
        # returns a tuple of (timestamp, Coordinate position)
        return time_series[0], self.track[time_series[0]]
    

    def final_position(self):
        time_series = sorted(self.track)
        # returns a tuple of (timestamp, Coordinate position)
        return time_series[-1], self.track[time_series[-1]]        
    

    def total_track_distance(self):
        time_series = sorted(self.track)
        i = 0
        j = 1
        total_distance = 0.0
        # print('attempt 5')
        
        while j < len(time_series):
            # print('attempt 1')
            total_distance += self.track[time_series[j]].calc_dist(self.track[time_series[i]])
            j+=1
            i+=1
        return total_distance 
    
        '''return the total distance traveled in the track'''

    def last_known_position(self,request_time):
        

        '''find most recent position (and time), prior to and following a given datetime object'''
        # returns a tuple of (timestamp, Coordinate position)  
        
        # we require that the request_time be a datetime object
        assert isinstance(request_time,datetime.datetime)
        time_series = sorted(self.track) # sorted dictionary made up of 'time' for keys and values thst are (lat,long) tuples.
        
        # print("request_time=", request_time, ", time_series[0]=", time_series[0])
        if request_time < time_series[0]:
            return (None,None)

        elif request_time > time_series[-1]:
            return (time_series[-1], self.track[time_series[-1]])

        else:           
            time_to_be_returned = time_series[0]
            for time_key in time_series:
                if time_key <= request_time: # This conditional will help me check each time in my list and compare it to the requested time. 
                    time_to_be_returned = time_key
                else:
                    break
            return (time_to_be_returned, self.track[time_to_be_returned])


       

        ### YOUR CODE GOES HERE: FOLLOW THE STEPS BELOW ###

        # step 1: create a time series of sorted datetime objects to be searched
        #   ( hint: look at initial_position() and final_position() )

        
        # step 2: find the most recent announced position prior to the given request_time
        # note  : if request_time is before first announced position, then return (None,None);
        #         otherwise, return a tuple of (timestamp, position) corresponding to 
        #         the most recent announced position prior the given request_time;




    def __str__(self):
        retval = self.MMSI
        if self.name:
            retval += '(' + self.name
            if self.type:
                retval += ',type=' + str(self.type)
            else:
                retval += ',type=None' 
                
            if self.length:
                retval += ',length=' + str(self.length)
                
            if len(self.call_signs) > 0:
                retval += ',call_signs=' + str(self.call_signs)
            retval += ')'
        return retval

# end of class Vessel


