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

import bpy
from PIL import ImageGrab
import os

class Add_ClipBoard(bpy.types.Operator):
    bl_idname = "addimage.put_clipboard_to_scene"
    bl_label = "Add Image"
    image_path = ''
    count = bpy.props.IntProperty(default=0)
    file_name = "img"
    type = ".jpg"
    
    def make_directory(self,):
        path = bpy.data.filepath
        path = os.path.dirname(path)
        path = os.path.join( path , "clipboard")
        self.image_path = path
        is_dir_exists = os.path.exists(path)
        if not is_dir_exists:
            os.mkdir(path)        

    def execute(self, context):
        self.make_directory()
        image = ImageGrab.grabclipboard()
        if image:
            file_name = self.file_name+str(self.count)+self.type
            path = os.path.join( self.image_path , file_name )
            image.save(path, 'JPEG')        
            bpy.ops.import_image.to_plane(files=[{"name":file_name, }], directory=self.image_path, align_axis='Z+')
            self.count+=1
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
        i = 2
        op = layout.operator(Add_ClipBoard.bl_idname,text="Add Clipboard Image")
        op.count = 2
        #layout.prop(i,2)
class MyProperties(bpy.types.PropertyGroup):
    int_value = bpy.props.IntProperty(name="id")
    


classes = (MyProperties,Add_ClipBoard, Add_Image_Panel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
#file_path = "C:\Users\mmafk\Desktop\screenshots\aas.jpg"
#bpy.ops.import_image.to_plane(shader='SHADELESS', files=[{'name':file_path}])