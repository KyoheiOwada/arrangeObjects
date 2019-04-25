import bpy
import numpy as np
import random
import os
from mathutils import Matrix,Euler,Vector
from obj_delete import obj_del


def copy_objects(object_name):
    bpy.data.objects[object_name].select = True
    bpy.context.scene.objects.active = bpy.data.objects[object_name]
    scn = bpy.context.scene
    src_obj = bpy.context.active_object

    bpy.ops.object.select_by_type(type='EMPTY')
    if src_obj is not None:
        new_obj = src_obj.copy()
        new_obj.data = src_obj.data.copy()

        new_obj.animation_data_clear()
        scn.objects.link(new_obj)

        copy_object_name = new_obj.name
        bpy.data.objects[copy_object_name].select = True
        bpy.context.scene.objects.active = bpy.data.objects[copy_object_name]


def make_T(th, p):
    T = Euler(th, "XYZ").to_matrix().to_4x4()
    T.translation = Vector(p)
    return T


def arrangeObjects(amount):
    for number in range(amount):
        obj_del()
        amount_object = np.random.randint(1,5)
        maxvaluex = []
        maxvaluey = []
        object_path = os.environ['HOMEPATH'] + '\\Documents\\objects\\cube.stl'
        bpy.ops.import_mesh.stl(filepath = object_path)
# copy object
        for i in range(amount_object * 2 ):
            copy_objects("Cube")
        objlist = [ob.name for ob in bpy.context.scene.objects]
        objlist.reverse()
        print(objlist)
       
# make max_x cordinate value and max_y cordinate value
        for objname in objlist:    
            deltax = random.uniform(0,0.4)
            deltay = random.uniform(0,0.4)
            
            vertlist = [v.co for v in bpy.data.objects[objname].data.vertices]
            xlist = [vect[0] for vect in vertlist]
            ylist = [vect[1] for vect in vertlist]
            maxvaluex.append(max(xlist)+deltax)
            maxvaluey.append(max(ylist)+deltay)

#movexamount = maxvaluex[0]
        movexamount = 0
        moveyamount = maxvaluey[0]
        

        th = [0,0,0]
        p = [0,0,0]
        T = make_T(th,p)
        i = 0

        movexlist = []
        moveylist = []
        moveyamount = maxvaluey[0] + maxvaluey[1]

        for index,item in enumerate(objlist):
            deltaz = random.uniform(0,-0.5)
            if index > 0:
                if index < len(objlist) / 2:       
        #if np.random.randint(0,2) == 1:
                    movexamount += maxvaluex[index-1] + maxvaluex[index]
                    movexlist.append(movexamount)
                    bpy.context.scene.objects.active = bpy.data.objects[item]
                    T.translation = Vector([movexamount,0,deltaz])
                    bpy.context.active_object.location = T.translation
        
                else:
                #moveyamount = maxvaluey[index-len(objlist)/2-1] + maxvaluey[index-len(objlist)/2]
                    bpy.context.scene.objects.active = bpy.data.objects[item]
                    T.translation = Vector([movexlist[index - len(objlist)] - 0.5,moveyamount + deltay,deltaz])
            #bpy.context.active_object.ratation_mode = "XYZ"
                    bpy.context.active_object.location = T.translation

        export_path = os.environ['HOMEPATH'] + '\\Documents\\objects\\cluster' + str(number) + '.stl'
        bpy.ops.export_mesh.stl(filepath = export_path)
    #obj_del()
    
if __name__ == "__main__":
    arrangeObjects(1)