import bpy, bmesh, mathutils

class css_customshape_add_from_subselect(bpy.types.Operator):
	bl_idname = 'pose.css_customshape_add_from_subselect'
	bl_label = "サブ選択から作成"
	bl_description = "サブ選択メッシュをカスタムシェイプ用に調整して割り当て"
	bl_options = {'REGISTER', 'UNDO'}
	
	keep_original = bpy.props.BoolProperty(name="オリジナルを保持", default=False)
	
	rename_before = bpy.props.StringProperty(name="前に", default="￥|")
	rename_split = bpy.props.StringProperty(name="接続", default="|")
	rename_after  = bpy.props.StringProperty(name="後に", default="|CS")
	
	def draw(self, context):
		self.layout.prop(self, 'keep_original', icon='UNPINNED')
		
		box = self.layout.box()
		column = box.column(align=True)
		column.label(text="新規オブジェクト名", icon='OBJECT_DATA')
		column.prop(self, 'rename_before', icon='BACK')
		column.prop(self, 'rename_split', icon='ARROW_LEFTRIGHT')
		column.prop(self, 'rename_after', icon='FORWARD')
		column.label(text=self.rename_before + context.active_object.name + self.rename_split + context.active_pose_bone.name + self.rename_after)
	
	def execute(self, context):
		ob, arm = context.active_object, context.active_object.data
		
		original_ob = [o for o in context.selected_objects if o != ob][0]
		original_me = original_ob.data
		
		new_cs_ob = original_ob.copy()
		new_cs_me = original_me.copy()
		new_cs_ob.data = new_cs_me
		
		bone = arm.bones[context.active_pose_bone.name]
		bone_mat = bone.matrix_local * mathutils.Matrix.Scale((bone.head_local - bone.tail_local).length, 4)
		
		bm = bmesh.new()
		bm.from_mesh(new_cs_me)
		for vert in bm.verts: vert.co = (ob.matrix_world * bone_mat).inverted() * new_cs_ob.matrix_world * vert.co
		has_face = bool(len(bm.faces))
		bm.to_mesh(new_cs_me)
		bm.free()
		
		new_cs_ob.name = new_cs_me.name = self.rename_before + context.active_object.name + self.rename_split + context.active_pose_bone.name + self.rename_after
		context.active_pose_bone.custom_shape = new_cs_ob
		if not has_face: bone.show_wire = True
		
		if not self.keep_original:
			context.blend_data.objects.remove(original_ob, do_unlink=True)
			context.blend_data.meshes.remove(original_me, do_unlink=True)
		
		return {'FINISHED'}
