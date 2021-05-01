import SimpleITK as sitk
import SImpleITK_myutil as itkmu
import numpy as np
from pathlib import Path
import os

input_file_name = "recon_proj_0019_swipeNum_13.00_binning_2X2"
output_file_name = "recon_proj_0019_swipeNum_12.00_binning_2X2"

folder_name_prev = "Data\\" + input_file_name
# folder_name_prev = "Data\\" + input_file_name + "\\AF"
folder_name_next = "Data\\" + output_file_name
folder_name_displacement = "Data\\" + output_file_name + "\\export.0000"

output_path = "Data\\" + output_file_name + "\\AF"
file_name = output_file_name

z_makeup_front = 8
z_makeup_back = 8

z_scale = 1.

#read prev image
image_file_dir = str(Path.cwd()) + "\\" + folder_name_prev
prev_img3D = itkmu.Read3DImage(image_file_dir)

#read next image
image_file_dir = str(Path.cwd()) + "\\" + folder_name_next
next_img3D = itkmu.Read3DImage(image_file_dir)

#define Displacement field
dpf = sitk.DisplacementFieldTransform(3)
field_size = list(next_img3D.GetSize())
field_origin = [0., 0., 0.]  
field_spacing = [1., 1., 1.]   
field_direction = [1., 0., 0., 0., 1., 0., 0., 0., 1.]
dpf.SetFixedParameters(field_size + field_origin + field_spacing + field_direction)
dpf.SetInterpolator(sitk.sitkLinear)

#set displacement and apply to displacement field
image_file_dir = str(Path.cwd()) + "\\" + folder_name_displacement
dp = itkmu.Read3DDisplacement(image_file_dir)

#scale z direction
if abs(z_scale - 1.) > 0.001:
    dp[:, :, :, 2] = dp[:, :, :, 2] / z_scale

dp_shape = np.shape(dp) #numpy니까 앞에 (z, y, z , dis) -> dis는 x, y, z

z_makeup_array_front = np.zeros((z_makeup_front, dp_shape[1], dp_shape[2], dp_shape[3]))
z_makeup_array_back = np.zeros((z_makeup_back, dp_shape[1], dp_shape[2], dp_shape[3]))

dp = np.concatenate([z_makeup_array_front, dp], axis=0)
dp = np.concatenate([dp, z_makeup_array_back], axis=0)

#reshape displacements for resampling
dp = dp.reshape(-1)
dpf.SetParameters(dp)

#resample image with displacement field
AF_image = sitk.Resample(prev_img3D, dpf)

#show result
sitk.Show(prev_img3D, title="prev_img3D")
sitk.Show(next_img3D, title="next_img3D")
sitk.Show(AF_image, title="AF_image")

#save the reult
stack_size = AF_image.GetSize()[2]
for slice_number in range(0, stack_size):
    output_file_name_3D = os.path.join(Path.cwd(), output_path, (file_name + '_' + str('{0:03d}'.format(slice_number)) + ".tiff"))
    sitk.WriteImage(AF_image[:, :, slice_number], output_file_name_3D)






