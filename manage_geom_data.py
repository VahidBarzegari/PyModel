
def ele_code_map(*args):
    pass



def manage_geom_data(*args):
	global jnt_data
	global all_jnt_pos
	global all_ele_pos
	global other_jnt_vrts
	global ele_data
	global X
	global Y
	global Z
	global story_jnts
	mem_var_names = ["jntData", "_allJntPos", "eleData", "X", "Y", "Z", "storyJnts"]
	if other_jnt_vrts["pp"]["n"] == None:
		other_jnt_vrts["pp"]["h"] = ["pn","np"]
		other_jnt_vrts["pp"]["v"] = ["np", "pn"]
		other_jnt_vrts["pn"]["h"] = ["pp", "nn"]
		other_jnt_vrts["pn"]["v"] = ["nn", "pp"]
		other_jnt_vrts["np"]["h"] = ["nn", "pp"]
		other_jnt_vrts["np"]["v"] = ["pp", "nn"]
		other_jnt_vrts["nn"]["h"] = ["np", "pn"]
		other_jnt_vrts["nn"]["v"] = ["pn", "np"]

	arg0 =args[0]

	if arg0 == "-initiate":
		#unset member variables if the model has been built in a previous loop iteration
		for var_name in mem_var_names:
			if var_name != None:
				unset = var_name

	if arg0 == "-makeJntList":
		list = ["array", "names", "jntData"]                #problem
		all_jnt_pos = []
		for name in list:									#problem
			pos = name.split("dim")[0]                           #problem
			if all_jnt_pos.find(pos) != -1:
				continue
			all_jnt_pos.append(pos)

		if all_jnt_pos == []:
			raise Exception("manageGeomData is called before computing the jntData array")

		list = ["array", "names", "ele_data"]
		all_ele_pos = []
		for name in list:
			pos = name.split("dim")[0]							#problem
			if  all_ele_pos.find(pos) != -1:
				continue
			all_ele_pos.append(pos)

		if all_ele_pos == []:
			raise Exception("manageGeomData is called before computing the jntData array")
		return

	if arg0 == "-jntExists":
		pos = args[1]
		if all_jnt_pos == None:
			raise Exception("manageGeomData -makeJntList should be called before other options")

		ind = all_jnt_pos.find(pos)
		if ind != -1:
			return 1

		return 0

	if arg0 == "-eleExists":
		pos = args[1]
		ind = all_ele_pos.find(pos)
		if ind != -1:
			return 1

		return 0

	if arg0 == "-getAllJntPos":
		if all_jnt_pos == []:
			raise Exception("manageGeomData is called before computing the jntData array")

		return all_jnt_pos

	if arg0 == "-getMatchingJntDim":
		pos = args[1]
		Dir = args[2]
		vrt = args[3]
		com = args[4]
		other_dir = {}
		other_dir["X"] = "Y"
		other_dir["Y"] = ["X"]
		for d in [Dir ,other_dir[Dir]]:
			for other_vert in other_jnt_vrts[vrt][com]:
				other_name = pos,"dim",d,other_vert,com
				if jnt_data[other_name] != None:
					return jnt_data[other_name]


	if arg0 == "-getEleAlignedJntPos":
		ele_code = args[1]
		ele_pos = args[2]
		ele_aligned_locs = {}
		locs = ele_aligned_locs[ele_code]
		res = []
		ele_internal_nodes = {}
		if ele_internal_nodes[ele_code][ele_pos] !=  None:
			res = ele_internal_nodes[ele_code][ele_pos]

		for loc in locs:
			pos = _pos,loc*                          #problem
			for p in all_jnt_pos:
				if pos == p:                         #problem
					res.append(p)

		return res

	if arg0 == "-getClmnAlignedPos":
		_pos = args[1]
		locs = clmn_aligned_locs						#problem
		res = []
		for loc in locs:
			pos = _pos,loc*
			for p in all_jnt_pos:
				if pos == p:
					res.append(p)

		return res

	if arg0 == "-setEleSection":
		code = ele_code_map(args[1])
		pos = args[2]
		val = args[3]
		ele_data[code][pos]["section"] = val
		if all_ele_pos.find(code) == -1 and all_ele_pos.find(pos) == -1:
			all_ele_pos.append(code)
			all_ele_pos.append(pos)

		return

	if arg0 == "-setEleConfig":
		code = ele_code_map(args[1])
		pos = args[2]
		val = args[3]
		ele_data[code][pos]["config"] = val
		return

	if arg0 == "-setBraceGussDim":
		whr = args[1]
		code = ele_code_map(args[2])
		pos = args[3]
		val = args[4]
		ele_data[code][pos]["GussDim"][whr] = val
		return

	if arg0 == "-setBraceLength":
		whr = args[1]
		code = args[2]
		pos = args[3]
		val = args[4]
		ele_data[code][pos]["Length"][whr] = val
		return

	if arg0 == "-getBraceLength":
		whr = args[1]
		code = args[2]
		pos = args[3]
		return ele_data[code][pos]["Length"][whr]

