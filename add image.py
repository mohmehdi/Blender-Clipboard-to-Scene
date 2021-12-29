bl_info = {
    "name": "ClipBoard to Scene",
    "author": "mohmehdi",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > My own addon",
    "description": "adds an image to scene from clipboard",
    "warning": "",
    "wiki_url": "",
    "category": "3D View"}
#------------------------------------------------------------#

import bpy
from PIL import ImageGrab
import os
import shutil

def make_path():
    path = bpy.data.filepath
    path = os.path.dirname(path)
    path = os.path.join( path, bpy.data.filepath.split('\\')[-1:][0].split('.')[0] + " clipboard")
    return path

class CleanImages(bpy.types.Operator):
    bl_idname = "addimage.clean_folder"
    bl_label = "Remove All"
    bl_description = "Deletes all saved files and the folder "
    image_path = ''

    def execute(self, context):
        layout = self.layout
        scene = context.scene
        scene.my_tool.int_value = 0
        
        if not bpy.data.is_saved:
            self.report({'INFO'}, "blend File is not saved" )    
            return {'FINISHED'}
            
        folder = make_path()
        
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)

                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
         
                    self.report({'INFO'}, 'Failed to delete %s. Reason: %s' % (file_path, e))
            
            os.rmdir(folder)
        else:
            self.report({'INFO'}, "Nothing to be cleaned" )               
        return {'FINISHED'}
        

class Add_ClipBoard(bpy.types.Operator):
    bl_idname = "addimage.put_clipboard_to_scene"
    bl_label = "Add Image"
    bl_description = "saves the clipboard image in same directory as blend file and adds it to cursor position in scene"
    image_path = ''
    file_name = "img"
    type = ".jpg"
    
    def make_directory(self,):
        
        self.image_path = make_path()
        is_dir_exists = os.path.exists(self.image_path)
        if not is_dir_exists:
            os.mkdir(self.image_path)        

    def execute(self, context):
        
        if not bpy.data.is_saved:
            self.report({'INFO'}, "you should Save the current blend file first")
            return {'FINISHED'}  
        
                 
        layout = self.layout
        scene = context.scene
        my_prop_tool = scene.my_tool
        index = my_prop_tool.int_value
        scale = my_prop_tool.int_scale

        image = ImageGrab.grabclipboard()
        if image:
            self.make_directory()            
            
            file_name = self.file_name+str(  index  ) +  self.type
            path = os.path.join( self.image_path , file_name )
            
            image = image.convert('RGB')
            image.save(path, 'JPEG')        
            bpy.ops.import_image.to_plane(files=[{"name":file_name, }], directory=self.image_path, align_axis='CAM')
            bpy.context.view_layer.objects.active.scale = (scale, scale, scale)
            
            scene.my_tool.int_value+=1
            
            self.report({'INFO'}, f"added {path}")
        else:
            self.report({'INFO'}, "Clip Board Empty")
        return {'FINISHED'}

class Add_Image_Panel(bpy.types.Panel):
    bl_label = "Add Image Panel"
    bl_category = "Add_Image"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
   
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_prop_tool = scene.my_tool
        
        row = layout.row()
        row.scale_y = 2
        row.operator(Add_ClipBoard.bl_idname,text="Add Clipboard Image",icon="IMAGE_DATA")
        
        row = layout.row()
        row.prop(my_prop_tool,"int_scale")    
        
        row = layout.row()
        
        row.operator(CleanImages.bl_idname,text="Clean",icon="TRASH")
        row.prop(my_prop_tool,"int_value")
        
         
        
class MyProperty(bpy.types.PropertyGroup):
    int_value:bpy.props.IntProperty(name="index",min=0,max=200,default=0)
    int_scale:bpy.props.FloatProperty(name="Scale",min=1.0,max=100,default=1.0)
    


#----------------registration----------------#

classes = (MyProperty,Add_ClipBoard,CleanImages, Add_Image_Panel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
        bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperty)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.my_tool
        
#if __name__ == "__main__":
#     register()