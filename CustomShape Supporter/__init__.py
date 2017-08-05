# アドオンを読み込む時に最初にこのファイルが読み込まれます

# アドオン情報
bl_info = {
	'name' : "CustomShape Supporter",
	'author' : "saidenka",
	'version' : (1, 0),
	'blender' : (2, 7, 8),
	'location' : "ポーズモード > プロパティエリア > ボーンタブ > 表示パネル",
	'description' : "",
	'warning' : "",
	'wiki_url' : "",
	'tracker_url' : "",
	'category' : "Rigging"
}

# サブスクリプト群をインポート
if 'bpy' in locals():
	import imp
	imp.reload(_draw)
	
	imp.reload(customshape_add)
	imp.reload(customshape_add_from_subselect)
	imp.reload(customshape_add_from_mirror)
	imp.reload(customshape_remove)
	
	imp.reload(customshape_edit)
	imp.reload(customshape_link)
	imp.reload(customshape_unlink)
	
	imp.reload(customshape_singlize)
	imp.reload(customshape_rename)
else:
	from . import _draw
	
	from . import customshape_add
	from . import customshape_add_from_subselect
	from . import customshape_add_from_mirror
	from . import customshape_remove
	
	from . import customshape_edit
	from . import customshape_link
	from . import customshape_unlink
	
	from . import customshape_singlize
	from . import customshape_rename

# この位置でbpyインポート (重要)
import bpy

# プラグインをインストールしたときの処理
def register():
	bpy.utils.register_module(__name__)
	bpy.types.BONE_PT_display.append(_draw.append)

# プラグインをアンインストールしたときの処理
def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.BONE_PT_display.remove(_draw.append)

# 最初に実行される
if __name__ == '__main__': register()
