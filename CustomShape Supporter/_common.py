import bpy, os, re

def get_append_data_blend_path():
	return os.path.join(os.path.dirname(__file__), "_append_data.blend")

def get_customshape_enum_items():
	items = [
		('CustomShape.Stick', "棒", "", 'IPO_LINEAR'),
		('CustomShape.Arrow', "矢印", "", 'FORWARD'),
		]
	for i, item in enumerate(items): items[i] = tuple(list(item) + [i + 1])
	return items

def get_mirror_name(name):
	base_name = name
	
	number = ""
	pattern = r'\.\d{3,}$'
	match = re.search(pattern, base_name)
	if match:
		number = match.group()
		base_name = re.sub(pattern, "", base_name)
	
	direction = ""
	pattern = r'[\._][lrLR]$'
	match = re.search(pattern, base_name)
	if match:
		direction = match.group()
		base_name = re.sub(pattern, "", base_name)
		
		if   direction[-1] == 'l': direction = direction[:-1] + 'r'
		elif direction[-1] == 'r': direction = direction[:-1] + 'l'
		elif direction[-1] == 'L': direction = direction[:-1] + 'R'
		elif direction[-1] == 'R': direction = direction[:-1] + 'L'
	
	return base_name + direction + number
