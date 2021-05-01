import os
import SimpleITK as sitk
import numpy as np

# read 3d image. it works only with tiff/tif
def Read3DImage(image_file_dir):
    
    # get target image list
    file_list = os.listdir(image_file_dir)
    file_list_tiff = [file for file in file_list if file.endswith(".tiff") or file.endswith(".tif")]

    # initialize file reader itk
    file_reader = sitk.ImageFileReader()
    file_reader.SetImageIO('TIFFImageIO')
    
    # set first image
    file_reader.SetFileName(image_file_dir + "\\" +  file_list_tiff[0])
    first_img = file_reader.Execute()
    #img3D = sitk.Image(first_img.GetSize()[0], first_img.GetSize()[1], len(file_list_tiff), sitk.sitkFloat32)
    img3D = sitk.Image(first_img.GetSize()[0], first_img.GetSize()[1], len(file_list_tiff), sitk.sitkUInt16)
    img3D[:, :, 0] = first_img
    
    # read otehr images
    for slice in range(1 , len(file_list_tiff)):
        #print(file_list[slice])
        file_reader.SetFileName(image_file_dir + "\\" +  file_list_tiff[slice])
        current_img = file_reader.Execute()
        img3D[:, :, slice] = current_img
        
    return img3D

# read 3d displacement from image
def Read3DDisplacement(displacement_file_dir):
    
    # get target displacement image list
    file_list = os.listdir(displacement_file_dir)
    file_list_tiff = [file for file in file_list if file.endswith(".tiff") or file.endswith(".tif")]
    
    # sort displacement image list to u,v,w
    file_u=[]
    file_v=[]
    file_w=[]
    for file_name in file_list_tiff:
        if file_name.find("u_") != -1:
            file_u.append(file_name) 
        elif file_name.find("v_") != -1:
            file_v.append(file_name)  
        elif file_name.find("w_") != -1:
            file_w.append(file_name) 
            
    assert len(file_u) == len(file_v) == len(file_w), "input u,v,w files are not mathing"

    # initialize file reader itk
    file_reader = sitk.ImageFileReader()
    file_reader.SetImageIO('TIFFImageIO')
    
    # # read first image
    file_reader.SetFileName(displacement_file_dir + "\\" +  file_list_tiff[0])
    dis_img = file_reader.Execute()
    
    # create displacement array
    # displacement3D = np.zeros((dis_img.GetSize()[0], dis_img.GetSize()[1], len(file_u), 3))
    displacement3D = np.empty((len(file_u), dis_img.GetSize()[1], dis_img.GetSize()[0], 3))
    # read otehr images
    slice = 0
    for w in file_w:
        file_reader.SetFileName(displacement_file_dir + "\\" +  w)
        current_img = file_reader.Execute()
        displacement3D[slice,:,:,2] = -sitk.GetArrayFromImage(current_img)
        slice += 1
    slice = 0
    for v in file_v:
        file_reader.SetFileName(displacement_file_dir + "\\" +  v)
        current_img = file_reader.Execute()
        displacement3D[slice,:,:,1] = -sitk.GetArrayFromImage(current_img)
        slice += 1
    slice = 0
    for u in file_u:
        file_reader.SetFileName(displacement_file_dir + "\\" +  u)
        current_img = file_reader.Execute()
        displacement3D[slice,:,:,0] = -sitk.GetArrayFromImage(current_img)      
        slice += 1
    return displacement3D

#create test image

# #test test test test
# testdp = np.zeros((180,210,210,3))
# for i in range(0,210):
#     testdp[:,i,:,0] = (i-105)/10
    
# testdp = testdp.reshape(-1)
# dpf.SetParameters(testdp)
# test_resample = sitk.Resample(next_img3D, dpf)

# # testdp_restore = -testdp
# # dpf.SetParameters(testdp_restore)
# # test_resample_restored = sitk.Resample(test_resample, dpf)

# # sitk.Show(test_resample)
# # sitk.Show(test_resample_restored)
# # sitk.Show(next_img3D)


# #export image files

# for slice_number in range(0, 180):
#     output_file_name_3D = os.path.join(Path.cwd(), folder_name_output, 
#                                        ('img_from_sikt_' + str('{0:03d}'.format(slice_number)) + '.tiff'))
#     sitk.WriteImage(test_resample[:,:,slice_number], output_file_name_3D)

# #test test test test







