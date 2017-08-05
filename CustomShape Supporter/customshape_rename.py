import bpy

class css_customshape_rename(bpy.types.Operator):
	bl_idname = 'pose.css_customshape_rename'
	bl_label = "リネーム"
	bl_description = "カスタムシェイプ用オブジェクトをまとめてリネーム"
	bl_options = {'REGISTER', 'UNDO'}
	
	is_selected_only = bpy.props.BoolProperty(name="選択ボーンのみ", default=False)
	
	rename_before = bpy.props.StringProperty(name="前に", default="￥|")
	rename_split = bpy.props.StringProperty(name="接続", default="|")
	rename_after  = bpy.props.StringProperty(name="後に", default="|CS")
	
	@classmethod
	def poll(cls, context):
		try:
			if context.active_object.type != 'ARMATURE': return False
			context.selected_pose_bones
		except: return False
		return True
	
	def draw(self, context):
		self.layout.prop(self, 'is_selected_only', icon='RESTRICT_SELECT_OFF')
		
		box = self.layout.box()
		column = box.column(align=True)
		column.label(text="新規オブジェクト名", icon='OBJECT_DATA')
		column.prop(self, 'rename_before', icon='BACK')
		column.prop(self, 'rename_split', icon='ARROW_LEFTRIGHT')
		column.prop(self, 'rename_after', icon='FORWARD')
		column.label(text=self.rename_before + context.active_object.name + self.rename_split + "ボーン名" + self.rename_after)
	
	def execute(self, context):
		ob, arm = context.active_object, context.active_object.data
		
		if self.is_selected_only: pose_bones = context.selected_pose_bones[:]
		else: pose_bones = [pb for pb in ob.pose.bones]
		
		for pose_bone in pose_bones:
			if not pose_bone.custom_shape: continue
			new_name = self.rename_before + context.active_object.name + self.rename_split + pose_bone.name + self.rename_after
			if pose_bone.custom_shape.name == new_name: continue
			pose_bone.custom_shape.name = new_name
		
		return {'FINISHED'}
