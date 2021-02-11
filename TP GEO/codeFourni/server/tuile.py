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

def routes(min_lon,max_lon,min_lat,max_lat,width,height,name):
    conn = database.init_connection()
    cursor = database.execute_query("SELECT tags->'name',id,ST_X((ST_DumpPoints(ST_Transform(linestring,3857))).geom),ST_Y((ST_DumpPoints(ST_Transform(linestring,3857))).geom) \
                                    FROM ways \
                                    WHERE tags ? 'highway' AND ST_Contains(ST_MakeEnvelope(%s,%s,%s,%s,3857),ST_Transform(linestring,3857)) \
                                    GROUP BY id \
                                    ;",min_lon,min_lat,max_lon,max_lat)
                                    
    rows = cursor.fetchall()
    image = drawer.Image(width,height)
    for i in range(1,len(rows)):
        #On présuppose que la taille des tuiles sera 256*256
        lo1 = (rows[i-1][2]-min_lon)/43.48
        lo2 = (rows[i][2]-min_lon)/43.48
        la1 = abs(((rows[i-1][3]-min_lat)/61.65)-256)
        la2 = abs(((rows[i][3]-min_lat)/61.65)-256)
        if rows[i][1] == rows[i-1][1]:
            image.draw_line(lo1,la1,lo2,la2,(0,0,0,255))
    
    image.save(name)
    cursor.close()
    database.close_connection()
    
def batiments(min_lon,max_lon,min_lat,max_lat,width,height,name):
    conn = database.init_connection()
    cursor = database.execute_query("SELECT tags ->'name', id, ST_X((ST_DumpPoints(ST_Transform(bbox,3857))).geom) , ST_Y((ST_DumpPoints(ST_Transform(bbox,3857))).geom) \
                                    FROM ways \
                                    WHERE tags ? 'amenity' \
                                    AND ST_Contains(ST_MakeEnvelope(%s,%s,%s,%s,3857),ST_Transform(bbox,3857)) \
                                    GROUP BY id \
                                    ;",min_lon,min_lat,max_lon,max_lat)
                             
    rows = cursor.fetchall()
    image = drawer.Image(width,height)
    for i in range(1,len(rows)):
        #On présuppose que la taille des tuiles sera 256*256
        lo1 = ((rows[i-1][2]-5.7)-min_lon)/43.48
        lo2 = ((rows[i][2]-5.7)-min_lon)/43.48
        la1 = abs(((rows[i-1][3]-min_lat)/61.65)-256)
        la2 = abs(((rows[i][3]-min_lat)/61.65)-256)
        if rows[i][1] == rows[i-1][1]:
            image.draw_line(lo1,la1,lo2,la2,(0,0,0,255))
    
    image.save(name)
    cursor.close()
    database.close_connection()
