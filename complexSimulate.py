'''
Function:
    模拟太阳-地球-月亮运动, 复杂版
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animmation
from mpl_toolkits.mplot3d import Axes3D


'''定义一些常量'''
R1 = 10
R2 = 1
W1 = 2 * np.pi
W2 = 24 * np.pi
PHI = 5.145396 * np.pi / 180
earth_radius = 3 * 3
moon_radius = 1 * 3
sun_radius = 9 * 3
x0, y0, z0 = 0, 0, 0
t_range = np.arange(0, 1+0.005, 0.005)


def update(data):
	global earth_track, moon_track_sun, moon_track_earth
	earth_track.set_data([data[0], data[1]])
	earth_track.set_3d_properties(data[2])
	moon_track_sun.set_data([data[3], data[4]])
	moon_track_sun.set_3d_properties(data[5])
	moon_track_earth.set_data([data[6], data[7]])
	moon_track_earth.set_3d_properties(data[8])
	return earth_track, moon_track_sun, moon_track_earth


def init():
	global earth_track, moon_track_sun, moon_track_earth, ax
	global x0, y0, z0
	t = 0
	x1 = x0 + R1 * np.cos(W1 * t)
	y1 = y0 + R1 * np.sin(W1 * t)
	z1 = z0
	x2 = x1 + R2 * np.sin(W2 * t)
	y2 = y1 + R2 * np.cos(W2 * t) / (np.cos(PHI) * (1 + np.tan(PHI) ** 2))
	z2 = z1 + (y2 - y1) * np.tan(PHI)
	earth_track, = ax.plot([x1], [y1], [z1], marker='o', color='blue', markersize=earth_radius)
	moon_track_sun, = ax.plot([x2], [y2], [z2], marker='o', color='orange', markersize=moon_radius)
	all_x2 = x1+R2*np.sin(2*np.pi*t_range)
	all_y2 = y1+R2*np.cos(2*np.pi*t_range)/(np.cos(PHI)*(1+np.tan(PHI)**2))
	all_z2 = (all_y2 - y1) * np.tan(PHI) + z1
	moon_track_earth, = ax.plot(all_x2, all_y2, all_z2, color='lavender')


def genFrames():
	data = []
	for i in range(1, len(t_range)):
		t = t_range[i]
		x1 = x0 + R1 * np.cos(W1 * t)
		y1 = y0 + R1 * np.sin(W1 * t)
		z1 = z0
		x2 = x1 + R2 * np.sin(W2 * t)
		y2 = y1 + R2 * np.cos(W2 * t) / (np.cos(PHI) * (1 + np.tan(PHI) ** 2))
		z2 = z1 + (y2 - y1) * np.tan(PHI)
		all_x2 = x1+R2*np.sin(2*np.pi*t_range)
		all_y2 = y1+R2*np.cos(2*np.pi*t_range)/(np.cos(PHI)*(1+np.tan(PHI)**2))
		all_z2 = (all_y2 - y1) * np.tan(PHI) + z1
		data.append([x1, y1, z1, x2, y2, z2, all_x2, all_y2, all_z2])
	return data


'''模拟运动'''
def simulate():
	# 地球轨道
	x1 = x0 + R1 * np.cos(W1 * t_range)
	y1 = y0 + R1 * np.sin(W1 * t_range)
	z1 = z0 + np.zeros(len(t_range))
	# 月球轨道
	x2 = x1 + R2 * np.sin(W2 * t_range)
	y2 = y1 + R2 * np.cos(W2 * t_range) / (np.cos(PHI) * (1 + np.tan(PHI) ** 2))
	z2 = z1 + (y2 - y1) * np.tan(PHI)
	# 画图
	f = plt.figure(figsize=(8, 8))
	global ax
	ax = f.add_subplot(111, projection='3d')
	ax.set_aspect('equal')
	ax.set_title('Model of Sun-Earth-Moon')
	ax.plot([x0], [y0], [z0], marker='o', color='red', markersize=sun_radius)
	ax.plot(x1, y1, z1, 'wheat')
	ax.plot(x2, y2, z2, 'purple')
	ax.set_xlim([-(R1 + 2), (R1 + 2)])
	ax.set_ylim([-(R1 + 2), (R1 + 2)])
	ax.set_zlim([-5, 5])
	earth_track, = ax.plot([], [], [], marker='o', color='blue', markersize=earth_radius, animated=True)
	moon_track_sun, = ax.plot([], [], [], marker='o', color='orange', markersize=moon_radius, animated=True)
	moon_track_earth, = ax.plot([], [], [], color='lavender', animated=True)
	ani = animmation.FuncAnimation(f, update, frames=genFrames(), init_func=init, interval=20)
	plt.show()



if __name__ == '__main__':
	simulate()