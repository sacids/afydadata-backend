# afydadata-backend

# changes in pyxform/xform2json.py line 387 - 391
# skip raising error for groups without reference and set a random value to ref
ref = "grp_"+str(random.randint(1000,5000))
# raise TypeError(
#    'cannot find "ref" or "nodeset" in {}'.format(repr(obj))
# )