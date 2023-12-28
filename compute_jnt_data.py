import manage_geom_data

def update_var(option, var_nam, new_v):
    var = var_nam                                   #problem
    global var
    if var == None:                                 #problem
        var = 0
    old_v = var
    if option == "-max":
        var = max(new_v, old_v)
    elif option == "-sum":
        var = old_v + new_v
    else:
        raise ValueError(f"invalid option: {option}")

Inputs = {}
X = {}
Y = {}
jnt_data = {}
ele_data = {}
def ele_code_map(*args):
    pass



print("~~~~~~~~~~~~~~~~~~~~~ Computing Joint Sizes ~~~~~~~~~~~~~~~~~~~~~")
for j in range(1, int(Inputs["n_flrs"])+1):
    # beam and brace connections
    for Dir, n_grid_x, n_grid_y in ["X","Y"],[Inputs["n_bays_x"] ,Inputs["n_bays_x"]+1],[Inputs["n_bays_y"]+1, Inputs["n_bays_y"]]:
        for k in range(1, n_grid_y+1):
            for i in range(1, n_grid_x+1):
                ele_pos = [j,k,i,1]
                # beam end jnts
                ele_code = ele_code_map(f"{Dir}-Beam")
                sec = ele_data["section"][ele_code][ele_pos]
                if sec != "-":
                    from sec_folder import sec                     #problem: This command does not accept strings
                    from sec_folder import convert_to_m
                    if Inputs["mat_type"] == "Steel":
                        H = convert_to_m.t3                                     #problem
                    i1 = i
                    k1 = k
                    if Dir == "X":
                        i1 = i + 1
                    else:
                        k1 = k + 1
                    iNode = j, k, i, 1                              #problem : tuple
                    jNode = j, k1, i1, 1                            #problem : tuple
                    dx = X[k1][i1]-X[k][i]
                    dy = Y[k1][i1]-Y[k][i]
                    l = (dx*dx+dy*dy) ** 0.5
                    H2 = H/2.0
                    update_var("-sum", int(jnt_data[iNode]["dim"][Dir]["pn"]["v"]), H2)
                    update_var("-sum", int(jnt_data[iNode]["dim"][Dir]["pp"]["v"]), H2)
                    update_var("-sum", int(jnt_data[jNode]["dim"][Dir]["nn"]["v"]), H2)
                    update_var("-sum", int(jnt_data[jNode]["dim"][Dir]["np"]["v"]), H2)
                    from sec_folder import unset_sec_props

                    # brace
                    ele_pos = [j, k, i]
                    ele_code = ele_code_map(f"{Dir}-Brace")
                    if ele_data["section"][ele_code][ele_pos]["L"] != "-":
                        # gusset dims.
                        # J        J
                        # \      /
                        #  I    I
                        lhI = ele_data["gussetDimI_lh"][ele_code][ele_pos]
                        lvI = ele_data["gussetDimI_lv"][ele_code][ele_pos]
                        lhJ = ele_data["gussetDimJ_lh"][ele_code][ele_pos]
                        lvJ = ele_data["gussetDimJ_lv"][ele_code][ele_pos]
                        # TODO allow different gusset size for the two members of an X brace
                        # TODO consider the EBF config (shear link)

                        # identifying the four corner nodes:
                        # ^Z
                        # |
                        # I__M__J
                        # |j,k,i|
                        # K__N__L___> X/Y

                        i_node_pos = j, k, i, 1
                        k_node_pos = j-1, k, i, 1
                        if Dir == "X":
                            j_node_pos = j, k, i+1, 1
                            l_node_pos = j-1, k, i+1, 1
                            m_node_pos = j, k, i, 2
                            n_node_pos = j-1, k, i, 2
                        else:
                            j_node_pos = j, k+1, i, 1
                            l_node_pos = j-1, k+1, i, 1
                            m_node_pos = j, k, i, 3
                            n_node_pos = j-1, k, i, 3

                        conf = ele_data["config"][ele_code][ele_pos]
                        # k
                        if conf == "/" or conf == "/\\" or conf == "X":
                            update_var("-sum", jnt_data[k_node_pos]["dim"][Dir]["pp"]["h"], lhI)
                            update_var("-sum", jnt_data[k_node_pos]["dim"][Dir]["pp"]["v"], lvI)
                        # j
                        if conf == "/" or conf == "\\/" or conf == "X":
                            update_var("-sum", jnt_data[j_node_pos]["dim"][Dir]["nn"]["h"], lhJ)
                            update_var("-sum", jnt_data[j_node_pos]["dim"][Dir]["nn"]["v"] ,lvJ)

                        # i
                        if conf == "\\" or conf == "\\/" or conf == "X":
                            # i
                            update_var("-sum", jnt_data[i_node_pos]["dim"][Dir]["pn"]["h"], lhJ)
                            update_var("-sum", jnt_data[i_node_pos]["dim"][Dir]["pn"]["v"], lhJ)

                        # l
                        if conf == "\\" or conf == "/\\" or conf == "X":
                            update_var("-sum", jnt_data[l_node_pos]["dim"][Dir]["np"]["h"], lhI)
                            update_var("-sum", jnt_data[l_node_pos]["dim"][Dir]["np"]["h"], lhI)

                        # m
                        if conf == "/\\" or conf == "|":
                            jnt_data[m_node_pos]["dim"][Dir]["nn"]["h"] = lhJ
                            jnt_data[m_node_pos]["dim"][Dir]["nn"]["v"] = H/2.+lvJ
                            jnt_data[m_node_pos]["dim"][Dir]["pn"]["h"] = lhJ
                            jnt_data[m_node_pos]["dim"][Dir]["pn"]["v"] = H/2.+lvJ

                        # n
                        if conf == "\\/" or conf == "|":
                            jnt_data[n_node_pos]["dim"][Dir]["np"]["h"] = lhI
                            jnt_data[n_node_pos]["dim"][Dir]["np"]["v"] = H/2.+lvI
                            jnt_data[n_node_pos]["dim"][Dir]["pp"]["h"] = lhI
                            jnt_data[n_node_pos]["dim"][Dir]["pp"]["v"] = H/2.+lvI

#columns
for k in range(1, int(Inputs["n_bays_y"])+1):
    for i in range(1, int(Inputs["n_bays_x"])+1):
        ele_pos = j, k, i
        ele_code = ele_code_map("Column")
        sec = ele_data["section"][ele_code][ele_pos]
        if sec == "-":
            continue
        from sec_folder import sec
        from sec_folder import convert_to_m
        if Inputs["mat_type"] == "Steel":
            dy = convert_to_m.t3
            dx = convert_to_m.t2
        else:
            dy = sec.H                           #problem
            dx = sec.B                           #problem

        i_node_pos = (j-1, k, i, 1)                #problem
        j_node_pos = (j, k, i, 1)
        update_var("-sum", jnt_data[i_node_pos]["dim"]["X"]["pp"]["h"], dx/2.0)        
        update_var("-sum", jnt_data[i_node_pos]["dim"]["X"]["np"]["h"], dx/2.0)
        update_var("-sum", jnt_data[i_node_pos]["dim"]["Y"]["pp"]["h"], dy/2.0)
        update_var("-sum", jnt_data[i_node_pos]["dim"]["Y"]["np"]["h"], dy/2.0)

        update_var("-sum", jnt_data[j_node_pos]["dim"]["X"]["pn"]["h"], dx/2.0)
        update_var("-sum", jnt_data[j_node_pos]["dim"]["X"]["nn"]["h"], dx/2.0)
        update_var("-sum", jnt_data[j_node_pos]["dim"]["Y"]["pn"]["h"], dy/2.0)
        update_var("-sum", jnt_data[j_node_pos]["dim"]["Y"]["nn"]["h"], dy/2.0)

        # base plate connection height
        if j == 1:
            update_var("-sum", jnt_data[i_node_pos]["dim"]["X"]["pp"]["v"], Inputs["clmn_base_plate_height_fac"]*dx)
            update_var("-sum", jnt_data[i_node_pos]["dim"]["X"]["np"]["v"], Inputs["clmn_base_plate_height_fac"]*dx)
            update_var("-sum", jnt_data[i_node_pos]["dim"]["Y"]["pp"]["v"], Inputs["clmn_base_plate_height_fac"]*dy)
            update_var("-sum", jnt_data[i_node_pos]["dim"]["Y"]["np"]["v"], Inputs["clmn_base_plate_height_fac"]*dy)
        from sec_folder import unset_sec_props


#set missing jnt dims. based on the computed ones
for pos in manage_geom_data.manage_geom_data("-getAllJntPos"):                            #problem
    for Dir in ["X", "Y"]:
        for vrt in ["pp", "np", "nn", "pn"]:
            for com in ["h", "v"]:
                name = pos, "dim", Dir, vrt, com         #problem : tuple
                if jnt_data[name] != None:
                    continue
                jnt_data[name] = manage_geom_data.manage_geom_data("-getMatchingJntDim", pos, Dir, vrt, com)