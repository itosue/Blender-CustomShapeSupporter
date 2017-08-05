import bpy
from . import _common

class css_customshape_add(bpy.types.Operator):
	bl_idname = 'pose.css_customshape_add'
	bl_label = "新規作成"
	bl_description = "選択ボーンにテンプレートから選んだカスタムシェイプを割り当て"
	bl_options = {'REGISTER', 'UNDO'}
	
	append_object_name = bpy.props.EnumProperty(items=_common.get_customshape_enum_items(), name="種類")
	
	rename_before = bpy.props.StringProperty(name="前に", default="￥|")
	rename_split = bpy.props.StringProperty(name="接続", default="|")
	rename_after  = bpy.props.StringProperty(name="後に", default="|CS")
	
	@classmethod
	def poll(cls, context):
		try:
			if not context.active_object: return False
			if not len(context.selected_pose_bones): return False
		except: return False
		return True
	
	def draw(self, context):
		self.layout.prop(self, 'append_object_name')
		
		box = self.layout.box()
		column = box.column(align=True)
		column.label(text="新規オブジェクト名", icon='OBJECT_DATA')
		column.prop(self, 'rename_before', icon='BACK')
		column.prop(self, 'rename_split', icon='ARROW_LEFTRIGHT')
		column.prop(self, 'rename_after', icon='FORWARD')
		column.label(text=self.rename_before + context.active_object.name + self.rename_split + context.selected_pose_bones[0].name + self.rename_after)
	
	def execute(self, context):
		ob, arm = context.active_object, context.active_object.data
		
		blend_path = _common.get_append_data_blend_path()
		
		for pose_bone in context.selected_pose_bones:
			
			with context.blend_data.libraries.load(blend_path) as (data_from, data_to):
				data_to.objects = [self.append_object_name]
			new_cs_ob = data_to.objects[0]
			new_cs_ob.name = new_cs_ob.data.name = self.rename_before + context.active_object.name + self.rename_split + pose_bone.name + self.rename_after
			
			pose_bone.custom_shape = new_cs_ob
			
			if new_cs_ob.type == 'MESH':
				if not len(new_cs_ob.data.polygons):
					arm.bones[pose_bone.name].show_wire = True
		
		return {'FINISHED'}
