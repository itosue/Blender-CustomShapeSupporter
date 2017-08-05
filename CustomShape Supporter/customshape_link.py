import bpy, mathutils

class css_customshape_link(bpy.types.Operator):
	bl_idname = 'pose.css_customshape_link'
	bl_label = "リンク"
	bl_description = "シーン内にないカスタムシェイプ用オブジェクトをリンク"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		try:
			if not context.active_object: return False
			for pose_bone in context.active_object.pose.bones:
				if pose_bone.custom_shape:
					if pose_bone.custom_shape.name not in context.scene.objects.keys(): return True
			return False
		except: return False
		return True
	
	def execute(self, context):
		ob, arm = context.active_object, context.active_object.data
		
		for pose_bone in ob.pose.bones:
			ob_cs = pose_bone.custom_shape
			if not ob_cs: continue
			if ob_cs.name in context.scene.objects.keys(): continue
			
			context.scene.objects.link(ob_cs)
			
			bone = arm.bones[pose_bone.name]
			ob_cs.matrix_world = ob.matrix_world * bone.matrix_local * mathutils.Matrix.Scale((bone.head_local - bone.tail_local).length, 4)
			
			ob_cs.select = False
			ob_cs.show_x_ray = True
		
		return {'FINISHED'}
