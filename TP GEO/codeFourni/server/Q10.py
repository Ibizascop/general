#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 14:35:58 2020

@author: grasinaw
"""



if __name__ == '__main__':
    import database
    import sys
    value = sys.argv[1]
    conn = database.init_connection()
    cursor = database.execute_query("SELECT tags->'name', ST_X((ST_DumpPoints(bbox)).geom),ST_Y((ST_DumpPoints(bbox)).geom) \
                                    FROM ways \
                                    WHERE tags->'name' like %s ;",(value,))
    rows = cursor.fetchall()
    for row in rows:
        print(row[0],' ','|',' ',row[1],' ','|',' ',row[2])
    
    
    cursor.close()
    database.close_connection()