import open3d as o3d
# visualization of point clouds.
pcd = o3d.io.read_point_cloud('/home/ztl/deeplearning/sam3d/SegmentAnything3D/data/{pwd}/scans/scene0568_00/scene0568_00_vh_clean_2.ply')
o3d.visualization.draw_geometries([pcd])

#scene0000_00_ensemble
#scene0000_00_group

python sam3d.py --rgb_path data/scannetv2_images/scene0568_00 --data_path data/dataset/val/scene0568_00.pth --save_path data/savepcd --save_2dmask_path data/savesam --sam_checkpoint_path sam_vit_h_4b8939.pth 
