import meep as mp
import numpy as np
# from meep.materials import GaAs,Au
import matplotlib.pyplot as plt

# basic setup (1 μm)
resolution = 50
sx = 40
sy = 0
sz = 100
cell = mp.Vector3(sx, sy, sz)
frequency = 1e12

# thickness of different layers（1 μm）
au_thickness = 0.18
ngaas_thickness_1 = 0.08
Active_region_thickness = 0.0113
ngaas_thickness_2 = 0.7
sigaas_thickness = 30

# material definition
# ngaas = mp.Medium(epsilon=12.5)
# si_gaas = mp.Medium(epsilon=12.9)
Active_region = mp.air
# Au = mp.Medium(epsilon=1.0, D_conductivity=1e7)
GaAs_low_doped = mp.Medium(epsilon=12.9, D_conductivity=0)
GaAs_high_doped = mp.Medium(epsilon=5, D_conductivity=100)

geometry = []
# Substrate
geometry.append(mp.Block(
                    material=GaAs_low_doped,
                    size=mp.Vector3(sigaas_thickness,mp.inf,sz),
                    center=mp.Vector3(x = -sx/2 + sigaas_thickness/2)))

geometry.append(mp.Block(
                    material=GaAs_high_doped,
                    size=mp.Vector3(ngaas_thickness_2,mp.inf,sz),
                    center=mp.Vector3(x= -sx/2 + sigaas_thickness + ngaas_thickness_2/2)))

# QCL active region
geometry.append(mp.Block(
                    material=Active_region,
                    size=mp.Vector3(Active_region_thickness,mp.inf,sz),
                    center=mp.Vector3(x= -sx/2 + sigaas_thickness + ngaas_thickness_2 + Active_region_thickness/2)))

# upper layers
x0 = -sx/2 + sigaas_thickness + ngaas_thickness_2 + Active_region_thickness
geometry += [
    mp.Block(material = GaAs_high_doped, 
             size = mp.Vector3(ngaas_thickness_1,mp.inf,sz), 
             center = mp.Vector3(x = x0 + ngaas_thickness_1/2)),
    mp.Block(material = Au,    
             size = mp.Vector3(au_thickness,mp.inf,sz),    
             center = mp.Vector3(x = x0 + ngaas_thickness_1 +  au_thickness/2))]
    
# grating parameters
Λ = 0.5                    
slot_width = 0.1           
slot_depth = au_thickness
slot_spacing = Λ / 2       
pattern_1 = "|-||-|-||||||-|||||-||||-|||-||-||||-|||||||-||-||-|||-||-|-||-|||-||-|-||||||-||-|-|||-||-|||||-|||-||-|"
pattern_2 = "|-||-|||||-||||||-|||-||||-||-||-|||||||||-||-|-||-||-||-|-|||-||-||-|-||||||-||||||||-||-||||||-||||---|"
pattern = pattern_1 + pattern_2

# 起始 z 位置，居中布置
z_start = -len(pattern) * slot_spacing / 2

# 放置高度（x 方向中心）
x_grating = x0 + ngaas_thickness_1 +  au_thickness/2

# 光栅 geometry 列表
grating_geometry = []
for i, symbol in enumerate(pattern):
    if symbol == "|":
        z_pos = z_start + i * slot_spacing
        grating_geometry.append(mp.Block(material=mp.air,
                                         size=mp.Vector3(slot_depth,mp.inf,slot_width),
                                         center=mp.Vector3(x_grating,0,z_pos)))
    else:
        z_pos = z_start + i * slot_spacing * 0.5

geometry += grating_geometry

# Source
sources = [mp.Source(
    src=mp.ContinuousSource(frequency=frequency),  
    component=mp.Ez,
    center=mp.Vector3(0, 0,-sz/2),               
    size=mp.Vector3(10,0,0))]

# Simulation setup
sim = mp.Simulation(
    cell_size=cell,
    resolution=resolution,
    boundary_layers=[mp.PML(0.1)],
    geometry=geometry,
    sources=sources,
    dimensions=2)

sim.plot2D()
sim.run(until = 200)

# 采样 y 方向 Ez 场强
x = np.linspace(-sx/2, sx/2, 1000)
eps_data = np.array([sim.get_epsilon_point(mp.Vector3(xi,0)) for xi in x])
ez_data = np.array([abs(sim.get_field_point(mp.Ez, mp.Vector3(xi))) for xi in x])

# === 画图 === #
fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Distance (um)')
ax1.set_ylabel('Mode Intensity |Ez|', color=color)
ax1.plot(x, ez_data, color=color)  # +10 是对齐示意图坐标
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xlim(-sx/2,sx/2)
ax1.set_ylim(0, np.max(ez_data)*1.2)

ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Re{ε}', color=color)
ax2.plot(x + sx/2, eps_data, color=color, linestyle='--')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(5, 15)

plt.title('Mode Intensity and Epsilon Profile')
plt.show()