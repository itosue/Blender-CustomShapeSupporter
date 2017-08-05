import bpy

class css_customshape_unlink(bpy.types.Operator):
	bl_idname = 'pose.css_customshape_unlink'
	bl_label = "リンク解除"
	bl_description = "シーン内のカスタムシェイプ用オブジェクトをリンク解除"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		try:
			if not context.active_object: return False
			for pose_bone in context.active_object.pose.bones:
				if pose_bone.custom_shape:
					if pose_bone.custom_shape.name in context.scene.objects.keys(): return True
			return False
		except: return False
		return True
	
	def execute(self, context):
		ob, arm = context.active_object, context.active_object.data
		
		for pose_bone in ob.pose.bones:
			ob_cs = pose_bone.custom_shape
			if not ob_cs: continue
			if ob_cs.name not in context.scene.objects.keys(): continue
			
			context.scene.objects.unlink(ob_cs)
		
		return {'FINISHED'}
