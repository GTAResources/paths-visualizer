﻿import bpy
import bmesh
from mathutils import Vector

from .ui_constants import *
    
def exportPaths(filepath, ob):
    print("Exporting to: " + filepath)
    print("Exporting Object: " + ob.name)
    file = open(filepath, 'w')
    
    me = ob.data
    
    # Get Bmesh representation
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    
    tagVerts = []
    tagEdges = []
    for i in range(len(bm.verts)):
        tagVerts.append({})
        tagVerts[i]['read'] = False
        tagVerts[i]['group'] = -1
        
    NumGroup = 0
    for i in range(len(bm.edges)):
        tagEdges.append({})
        tagEdges[i]['type'] = "none" # interna/external
        
    for v in bm.verts:
        if tagVerts[v.index]['read']:
            continue
            
        currentIndex = v.index
        internalNodes = []
        g = 0
        while True:
            tagVerts[currentIndex]['group'] = NumGroup
            tagVerts[currentIndex]['read'] = True
            
            internalNodes.append(currentIndex)
            g += 1
            
            if g == 11:
                break
            
            assert len(bm.verts[currentIndex].link_edges) > 0
            
            for link in bm.verts[currentIndex].link_edges:
                
                linkVert = link.verts[0].index
                if linkVert == currentIndex:
                    linkVert = link.verts[1].index
                  
                if (tagVerts[linkVert]['read'] != True and 
                    tagEdges[link.index]['type'] == "none"):
                    currentIndex = linkVert
                    break
        
        NumGroup += 1
        #TEST CODE
        for x in internalNodes:
            print("bm.verts[" + str(x) + "].select = True")
        break
        #END TEST CODE
                    
    bm.to_mesh(me)
    bm.free()
    file.close()
