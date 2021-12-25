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

class Add_ClipBoard(bpy.types.Operator):
    bl_idname = "addimage.put_clipboard_to_scene"
    bl_label = "Add Image"

    def execute(self, context):
        
        file_path = "C:\Users\mmafk\Desktop\screenshots\aas.jpg"
        bpy.ops.import_image.to_plane(shader='SHADELESS', files=[{'name':file_path}])
        self.report({'INFO'}, f"added {self.bl_idname}")
        
        return {'FINISHED'}

class Add_Image_Panel(bpy.types.Panel):
    bl_label = "add_image_panel"
    bl_category = "Add_Image"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.operator(Add_ClipBoard.bl_idname)

classes = (Add_ClipBoard, Add_Image_Panel)


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