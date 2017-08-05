import bpy, mathutils

class css_customshape_edit(bpy.types.Operator):
	bl_idname = 'pose.css_customshape_edit'
	bl_label = "編集"
	bl_description = "カスタムシェイプ用オブジェクトを現在のシーンにリンクして編集モードに移行します"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		try:
			if not context.active_object: return False
			if not context.active_pose_bone: return False
			if not context.active_pose_bone.custom_shape: return False
		except: return False
		return True
	
	def execute(self, context):
		ob, arm = context.active_object, context.active_object.data
		pose_bone = context.active_pose_bone
		ob_cs = pose_bone.custom_shape
		
		bpy.ops.object.mode_set(mode='OBJECT')
		
		if ob_cs.name in context.scene.objects.keys(): context.scene.objects.unlink(ob_cs)
		context.scene.objects.link(ob_cs)
		
		bone = arm.bones[pose_bone.name]
		ob_cs.matrix_world = ob.matrix_world * bone.matrix_local * mathutils.Matrix.Scale((bone.head_local - bone.tail_local).length, 4)
		
		ob.select = False
		ob_cs.select = True
		ob_cs.show_x_ray = True
		context.scene.objects.active = ob_cs
		
		bpy.ops.object.mode_set(mode='EDIT')
		return {'FINISHED'}
