import bpy

class css_customshape_remove(bpy.types.Operator):
	bl_idname = 'pose.css_customshape_remove'
	bl_label = "削除"
	bl_description = "選択ボーンのカスタムシェイプオブジェクトを削除"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		try:
			if context.active_object.type != 'ARMATURE': return False
			for pose_bone in context.selected_pose_bones:
				if pose_bone.custom_shape: return True
			return False
		except: return False
		return True
	
	def execute(self, context):
		ob, arm = context.active_object, context.active_object.data
		
		for pose_bone in context.selected_pose_bones:
			ob_cs = pose_bone.custom_shape
			if not ob_cs: continue
			me_cs = ob_cs.data
			context.blend_data.objects.remove(ob_cs, do_unlink=True)
			context.blend_data.meshes.remove(me_cs, do_unlink=True)
		
		for area in context.screen.areas: area.tag_redraw()
		return {'FINISHED'}
