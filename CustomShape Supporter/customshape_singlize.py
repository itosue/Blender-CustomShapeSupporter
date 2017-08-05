import bpy

class css_customshape_singlize(bpy.types.Operator):
	bl_idname = 'pose.css_customshape_singlize'
	bl_label = "シングルユーザー化"
	bl_description = "1つのオブジェクトを複数のカスタムシェイプとして使っていた場合にシングルユーザー化"
	bl_options = {'REGISTER', 'UNDO'}
	
	rename_before = bpy.props.StringProperty(name="前に", default="￥|")
	rename_split = bpy.props.StringProperty(name="接続", default="|")
	rename_after  = bpy.props.StringProperty(name="後に", default="|CS")
	
	@classmethod
	def poll(cls, context):
		try:
			if context.active_object.type != 'ARMATURE': return False
			if not len(context.selected_pose_bones): return False
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
		arm_objects = [o for o in context.blend_data.objects if o.type == 'ARMATURE']
		all_pose_bones = [pb for o in arm_objects for pb in o.pose.bones]
		
		users_dict = {o:0 for o in context.blend_data.objects}
		for pose_bone in all_pose_bones:
			ob_cs = pose_bone.custom_shape
			if not ob_cs: continue
			users_dict[ob_cs] += 1
		
		for pose_bone in context.selected_pose_bones:
			ob_cs = pose_bone.custom_shape
			if not ob_cs: continue
			if users_dict[ob_cs] < 2: continue
			
			new_ob_cs = ob_cs.copy()
			new_me_cs = ob_cs.data.copy()
			new_ob_cs.data = new_me_cs
			
			new_ob_cs.name = new_me_cs.name = self.rename_before + context.active_object.name + self.rename_split + pose_bone.name + self.rename_after
			
			pose_bone.custom_shape = new_ob_cs
		
		return {'FINISHED'}
