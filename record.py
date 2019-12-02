import pyrealsense2 as rs
import numpy as np
import cv2

CLIP_UPBOUND_METER = 0.5 # upper bound of clipping distance (m)
CLIP_LWBOUND_METER = 0.3 # lower bound of clipping distance (m)

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)
config.enable_record_to_file('./records/201912012154.bag')

# Start streaming and get profile
profile = pipeline.start(config)

# Get depth sensor config and calculate boundaries for clipping
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale() # Note: scale is set 0.0001m (i.e. 1mm) by default
upper_bound_depth = CLIP_UPBOUND_METER / depth_scale
lower_bound_depth = CLIP_LWBOUND_METER / depth_scale

align_to = rs.stream.color
align = rs.align(align_to)

try:
	while True:
		frames = pipeline.wait_for_frames()
		aligned_frames = align.process(frames)
		color_frame = aligned_frames.get_color_frame()
		depth_frame = aligned_frames.get_depth_frame()
		
		if not depth_frame or not color_frame:
			continue

		color_image = np.asanyarray(color_frame.get_data())
		depth_image = np.asanyarray(depth_frame.get_data())

		upper_clipped_image = np.where((depth_image <= upper_bound_depth), depth_image, upper_bound_depth)
		clipped_image = np.where((upper_clipped_image >= lower_bound_depth), upper_clipped_image, lower_bound_depth)

		alpha = float(255) / (float(CLIP_UPBOUND_METER - CLIP_LWBOUND_METER) / depth_scale)
		print("alpha", alpha, "lower_bound_depth:", lower_bound_depth, "upper_bound_depth:", upper_bound_depth)
		depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(clipped_image - lower_bound_depth, alpha = alpha), cv2.COLORMAP_JET)
		images = np.hstack((color_image, depth_colormap))
		
		# Show images
		cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
		cv2.imshow('RealSense', images)
		cv2.waitKey(1)

finally:
	# Stop streaming

	pipeline.stop()