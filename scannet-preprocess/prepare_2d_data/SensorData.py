
import os, struct
import numpy as np
import zlib
import imageio
import cv2
#定义两个字典常量用于存储颜色和深度数据的压缩类型
COMPRESSION_TYPE_COLOR = {-1:'unknown', 0:'raw', 1:'png', 2:'jpeg'}
COMPRESSION_TYPE_DEPTH = {-1:'unknown', 0:'raw_ushort', 1:'zlib_ushort', 2:'occi_ushort'}

class RGBDFrame():

  def load(self, file_handle):
    '''
    从给定的文件句柄中加载帧数据。在这个方法中，首先从文件中读取相机到世界坐标系的变换矩阵、颜色和深度图像的时间戳、
    颜色和深度图像的大小(字节数),然后分别读取颜色和深度图像的数据,并存储在color_data和depth_data属性中
    '''
    self.camera_to_world = np.asarray(struct.unpack('f'*16, file_handle.read(16*4)), dtype=np.float32).reshape(4, 4)
    self.timestamp_color = struct.unpack('Q', file_handle.read(8))[0]
    self.timestamp_depth = struct.unpack('Q', file_handle.read(8))[0]
    self.color_size_bytes = struct.unpack('Q', file_handle.read(8))[0]
    self.depth_size_bytes = struct.unpack('Q', file_handle.read(8))[0]
    self.color_data = b''.join(struct.unpack('c'*self.color_size_bytes, file_handle.read(self.color_size_bytes)))
    self.depth_data = b''.join(struct.unpack('c'*self.depth_size_bytes, file_handle.read(self.depth_size_bytes)))


  def decompress_depth(self, compression_type):
    '''
    对深度图像进行解压缩,根据给定的压缩类型选择相应的解压缩方法。目前仅支持zlib_ushort类型的解压缩
    '''
    if compression_type == 'zlib_ushort':
       return self.decompress_depth_zlib()
    else:
       raise


  def decompress_depth_zlib(self):
    '''
    使用zlib库对深度数据进行解压缩
    '''
    return zlib.decompress(self.depth_data)


  def decompress_color(self, compression_type):
    '''
    对颜色图像进行解压缩，根据给定的压缩类型选择相应的解压缩方法。目前仅支持jpeg类型的解压缩
    '''
    if compression_type == 'jpeg':
       return self.decompress_color_jpeg()
    else:
       raise


  def decompress_color_jpeg(self):
    '''
    使用imageio库读取JPEG格式的颜色数据
    '''
    return imageio.imread(self.color_data)


class SensorData:

  def __init__(self, filename):
    self.version = 4
    self.load(filename)


  def load(self, filename):
    with open(filename, 'rb') as f:
      version = struct.unpack('I', f.read(4))[0]
      assert self.version == version
      strlen = struct.unpack('Q', f.read(8))[0]
      self.sensor_name = b''.join(struct.unpack('c'*strlen, f.read(strlen)))
      self.intrinsic_color = np.asarray(struct.unpack('f'*16, f.read(16*4)), dtype=np.float32).reshape(4, 4)
      self.extrinsic_color = np.asarray(struct.unpack('f'*16, f.read(16*4)), dtype=np.float32).reshape(4, 4)
      self.intrinsic_depth = np.asarray(struct.unpack('f'*16, f.read(16*4)), dtype=np.float32).reshape(4, 4)
      self.extrinsic_depth = np.asarray(struct.unpack('f'*16, f.read(16*4)), dtype=np.float32).reshape(4, 4)
      self.color_compression_type = COMPRESSION_TYPE_COLOR[struct.unpack('i', f.read(4))[0]]
      self.depth_compression_type = COMPRESSION_TYPE_DEPTH[struct.unpack('i', f.read(4))[0]]
      self.color_width = struct.unpack('I', f.read(4))[0]
      self.color_height =  struct.unpack('I', f.read(4))[0]
      self.depth_width = struct.unpack('I', f.read(4))[0]
      self.depth_height =  struct.unpack('I', f.read(4))[0]
      self.depth_shift =  struct.unpack('f', f.read(4))[0]
      num_frames =  struct.unpack('Q', f.read(8))[0]
      self.frames = []
      for i in range(num_frames):
        frame = RGBDFrame()
        frame.load(f)
        self.frames.append(frame)


  def export_depth_images(self, output_path, image_size=None, frame_skip=1):
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    # print 'exporting', len(self.frames)//frame_skip, ' depth frames to', output_path
    for f in range(0, len(self.frames), frame_skip):
      depth_data = self.frames[f].decompress_depth(self.depth_compression_type)
      depth = np.fromstring(depth_data, dtype=np.uint16).reshape(self.depth_height, self.depth_width)
      if image_size is not None:
        depth = cv2.resize(depth, (image_size[1], image_size[0]), interpolation=cv2.INTER_NEAREST)
      imageio.imwrite(os.path.join(output_path, str(f) + '.png'), depth)


  def export_color_images(self, output_path, image_size=None, frame_skip=1):
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    # print 'exporting', len(self.frames)//frame_skip, 'color frames to', output_path
    for f in range(0, len(self.frames), frame_skip):
      color = self.frames[f].decompress_color(self.color_compression_type)
      if image_size is not None:
        color = cv2.resize(color, (image_size[1], image_size[0]), interpolation=cv2.INTER_NEAREST)
      imageio.imwrite(os.path.join(output_path, str(f) + '.jpg'), color)


  def save_mat_to_file(self, matrix, filename):
    with open(filename, 'w') as f:
      for line in matrix:
        np.savetxt(f, line[np.newaxis], fmt='%f')


  def export_poses(self, output_path, frame_skip=1):
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    # print 'exporting', len(self.frames)//frame_skip, 'camera poses to', output_path
    for f in range(0, len(self.frames), frame_skip):
      self.save_mat_to_file(self.frames[f].camera_to_world, os.path.join(output_path, str(f) + '.txt'))


  def export_intrinsics(self, output_path):
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    # print 'exporting camera intrinsics to', output_path
    self.save_mat_to_file(self.intrinsic_color, os.path.join(output_path, 'intrinsic_color.txt'))
    self.save_mat_to_file(self.extrinsic_color, os.path.join(output_path, 'extrinsic_color.txt'))
    self.save_mat_to_file(self.intrinsic_depth, os.path.join(output_path, 'intrinsic_depth.txt'))
    self.save_mat_to_file(self.extrinsic_depth, os.path.join(output_path, 'extrinsic_depth.txt'))