import bpy, re
from . import _common

class css_customshape_add_from_mirror(bpy.types.Operator):
	bl_idname = 'pose.css_customshape_add_from_mirror'
	bl_label = "ミラーから作成"
	bl_description = "左右対称のボーンにすでにカスタムシェイプがあれば左右反転して割り当て"
	bl_options = {'REGISTER', 'UNDO'}
	
	rename_before = bpy.props.StringProperty(name="前に", default="￥|")
	rename_split = bpy.props.StringProperty(name="接続", default="|")
	rename_after  = bpy.props.StringProperty(name="後に", default="|CS")
	
	@classmethod
	def poll(cls, context):
		try:
			for pose_bone in context.selected_pose_bones:
				mirror_name = _common.get_mirror_name(pose_bone.name)
				if pose_bone.name == mirror_name: continue
				if mirror_name not in context.active_object.pose.bones.keys(): continue
				if context.active_object.pose.bones[mirror_name].custom_shape: break
			else: return False
		except: return False
		return True
	
	def draw(self, context):
		box = self.layout.box()
		column = box.column(align=True)
		column.label(text="新規オブジェクト名", icon='OBJECT_DATA')
		column.prop(self, 'rename_before', icon='BACK')
		column.prop(self, 'rename_split', icon='ARROW_LEFTRIGHT')
		column.prop(self, 'rename_after', icon='FORWARD')
		column.label(text=self.rename_before + context.active_object.name + self.rename_split + context.selected_pose_bones[0].name + self.rename_after)
	
	def execute(self, context):
		ob, arm = context.active_object, context.active_object.data
		for pose_bone in context.selected_pose_bones:
			mirror_name = _common.get_mirror_name(pose_bone.name)
			if pose_bone.name == mirror_name: continue
			if mirror_name not in ob.pose.bones.keys(): continue
			
			mirror_pose_bone = ob.pose.bones[mirror_name]
			if not mirror_pose_bone.custom_shape: continue
			if mirror_pose_bone.custom_shape.type != 'MESH': continue
			
			new_cs_ob = mirror_pose_bone.custom_shape.copy()
			new_cs_me = mirror_pose_bone.custom_shape.data.copy()
			new_cs_ob.data = new_cs_me
			name = self.rename_before + context.active_object.name + self.rename_split + pose_bone.name + self.rename_after
			new_cs_ob.name = new_cs_me.name = name
			
			for v in new_cs_me.vertices: v.co.x = -v.co.x
			
			pose_bone.custom_shape = new_cs_ob
			arm.bones[pose_bone.name].show_wire = arm.bones[mirror_pose_bone.name].show_wire
		
		return {'FINISHED'}
