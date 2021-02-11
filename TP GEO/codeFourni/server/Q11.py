#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 16:06:24 2020

@author: grasinaw
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 14:35:58 2020

@author: grasinaw
"""

import database
import sys
import drawer

def routes(min_lon,max_lon,min_lat,max_lat,width,height,):
    conn = database.init_connection()
    cursor = database.execute_query("SELECT tags->'name',id,ST_X((ST_DumpPoints(linestring)).geom),ST_Y((ST_DumpPoints(linestring)).geom) \
                                    FROM ways \
                                    WHERE tags ? 'highway' AND ST_Contains(ST_MakeEnvelope(%s,%s,%s,%s,4326),linestring) \
                                    GROUP BY id \
                                    ;",min_lon,min_lat,max_lon,max_lat)
                                    
    rows = cursor.fetchall()
    image = drawer.Image(width,height)
    for i in range(1,len(rows)):
        #Mise à l'échelle des coordonnées 
        lo1 = (rows[i-1][2]-min_lon)*width*10
        lo2 = (rows[i][2]-min_lon)*width*10
        la1 = abs(((rows[i-1][3]-min_lat)*height*10)-height)
        la2 = abs(((rows[i][3]-min_lat)*height*10)-height)
        if rows[i][1] == rows[i-1][1]:
            image.draw_line(lo1,la1,lo2,la2,(0,0,0,255))
    
    image.save("Q11")
    cursor.close()
    database.close_connection()
    
if __name__ == '__main__':    
    
    min_lon = float(sys.argv[1])
    max_lon = float(sys.argv[2])
    min_lat = float(sys.argv[3])
    max_lat = float(sys.argv[4])
    width = int(sys.argv[5])
    height = int(sys.argv[6])

    routes(min_lon, max_lon, min_lat, max_lat, width, height)