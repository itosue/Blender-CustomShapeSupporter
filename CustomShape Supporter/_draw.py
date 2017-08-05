import bpy

def append(self, context):
	box_main = self.layout.box()
	box_main.label(text="カスタムシェイプ補助", icon='POSE_HLT')
	
	# 一段目
	row = box_main.row(align=True)
	# 新規作成
	row.operator('pose.css_customshape_add', icon='ZOOMIN')
	# サブ選択から作成
	row_local = row.row(align=True)
	row_local.operator('pose.css_customshape_add_from_subselect', icon='OUTLINER_OB_MESH')
	def css_customshape_add_from_subselect_poll(context):
		try:
			if not context.active_pose_bone: return False
			if len(context.selected_objects) != 2: return False
			if [o for o in context.selected_objects if o != context.active_object][0].type != 'MESH': return False
		except: return False
		return True
	row_local.enabled = css_customshape_add_from_subselect_poll(context)
	# ミラーから作成
	row.operator('pose.css_customshape_add_from_mirror', icon='MOD_MIRROR')
	
	# 二段目
	row = box_main.row(align=True)
	# 編集
	row.operator('pose.css_customshape_edit', icon='EDITMODE_HLT')
	# リンク
	row.operator('pose.css_customshape_link', icon='LINKED')
	# リンク解除
	row.operator('pose.css_customshape_unlink', icon='UNLINKED')
	
	# 三段目
	row = box_main.row(align=True)
	# シングルユーザー化
	row_local = row.row(align=True)
	row_local.operator('pose.css_customshape_singlize', icon='COPY_ID')
	def css_customshape_singlize_poll(context):
		try:
			if context.active_object.type != 'ARMATURE': return False
			if not len(context.selected_pose_bones): return False
			
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
				if 2 <= users_dict[ob_cs]: return True
			return False
		except: return False
		return True
	row_local.enabled = css_customshape_singlize_poll(context)
	# リネーム
	row.operator('pose.css_customshape_rename', icon='FILE_REFRESH')
