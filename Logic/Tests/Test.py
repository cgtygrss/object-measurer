import os
import subprocess
import cv2

# Define the path to the VisualSFM executable
visualsfm_path = 'C:/Users/user/Downloads/VisualSFM_windows_64bit/VisualSFM_windows_64bit/VisualSFM.exe'

# Define the paths to the input images and output directory
input_dir = 'Images/'
output_dir = 'Tests/'

# Define the command to run VisualSFM
command = '{} sfm+pmvs "{}" "{}" -w -1'.format(visualsfm_path, input_dir, output_dir)

# Run VisualSFM using subprocess
subprocess.call(command, shell=True)

# Load the reconstructed 3D model using OpenCV
model_path = os.path.join(output_dir, 'pmvs', 'models', 'option-0000.ply')
model = cv2.ppf_match_3d.readModel(model_path, format='ply')