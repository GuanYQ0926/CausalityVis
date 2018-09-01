import numpy as np
from stl import mesh
import stl
import math
from mpl_toolkits import mplot3d
from matplotlib import pyplot


# divide model
brain_model = mesh.Mesh.from_file('../static/model/brain.stl')
vectors = brain_model.vectors
thres_x = 2.0
model_array = []
for vector in vectors:
    node1, node2, node3 = vector[0], vector[1], vector[2]
    temp1 = (node1[0]-thres_x) * (node2[0]-thres_x)
    temp2 = (node1[0]-thres_x) * (node3[0]-thres_x)
    temp3 = (node2[0]-thres_x) * (node3[0]-thres_x)
    if temp1 < 0 or temp2 < 0 or temp3 < 0:
        continue
    else:
        # if temp1 > 0:
        #     vector[0][0] += 6
        #     vector[1][0] += 6
        #     vector[2][0] += 6
        # elif temp1 < 0:
        #     vector[0][0] -= 6
        #     vector[1][0] -= 6
        #     vector[2][0] -= 6
        # else:
        #     continue
        model_array.append(vector)
model_array = np.array(model_array)
brain_model = mesh.Mesh(np.zeros(model_array.shape[0], dtype=mesh.Mesh.dtype))
brain_model.vectors = model_array
# add slice
data = np.zeros(2, dtype=mesh.Mesh.dtype)
data['vectors'][0] = np.array([[2, 6, -6],
                               [2, 6, 6],
                               [2, -6, 6]])
data['vectors'][1] = np.array([[2, 6, -6],
                               [2, -6, -6],
                               [2, -6, 6]])
slice_model = mesh.Mesh(data.copy())
combined = mesh.Mesh(np.concatenate([brain_model.data]+[slice_model.data]))
combined.save('../static/model/slice_test.stl', mode=stl.Mode.BINARY)
# brain_model.save('../static/model/temp_ascii.stl', mode=stl.Mode.ASCII)
# brain_model.save('../static/model/slice_test.stl', mode=stl.Mode.BINARY)
