import meep as mp
import numpy as np
import matplotlib.pyplot as plt
from QCL_materials import Au,Ti,PdGe,nplus_GaAs,SI_GaAs,AR
# import meep.materials

# thickness of different layers（1 μm）
Au_thickness = 0.18
Ti_thickness = 0.02
PdGe_thickness = 0.1
nplusGaAs_thickness_1 = 0.08
AR_thickness = 11.3
GaAs_thickness_2 = 0.7
SIGaAs_thickness = 10

# basic setup (1 μm)
resolution = 50
sx = 15
sy = 30
sz = 1
cell = mp.Vector3(sx, sy, 0)
# Perfectly Matched Layer
# if THz , set PML to 1
pml_layers = [mp.PML(0.1)]
frequency = 10
observe_range = 0.1


y0 = -0.5 * (Au_thickness + Ti_thickness + PdGe_thickness + nplusGaAs_thickness_1 +
             AR_thickness + GaAs_thickness_2 + SIGaAs_thickness)
geometry = []
def add_layer(thickness, material):
    global y0
    center_y = y0 + 0.5 * thickness
    geometry.append(mp.Block(
        size=mp.Vector3(sx, thickness, sz),
        center=mp.Vector3(0, center_y, 0),
        material=material
    ))
    y0 += thickness

add_layer(SIGaAs_thickness, SI_GaAs)
add_layer(GaAs_thickness_2, nplus_GaAs)
add_layer(AR_thickness, AR)
add_layer(nplusGaAs_thickness_1, nplus_GaAs)
add_layer(PdGe_thickness, PdGe)
add_layer(Ti_thickness, Ti)
add_layer(Au_thickness, Au)

# Source
sources = [mp.Source(
            src=mp.GaussianSource(frequency=frequency, fwidth=1),
            component=mp.Ex,
            center=mp.Vector3(-7.0,0,0),
            size=mp.Vector3(1,sy,0))]


# Simulation setup
sim = mp.Simulation(
    cell_size=cell,
    resolution=resolution,
    boundary_layers=pml_layers,
    geometry=geometry,
    sources=sources,
    dimensions=2
)
sim.plot2D()

# Position of detector
detector_pos = mp.Vector3(7,0,0)       # y0 是波导中轴高度
detector_size = mp.Vector3(1,40,sz)     # 沿 y 方向覆盖整个波导区域
flux_monitor = sim.add_flux(frequency, frequency * observe_range, 100, 
                            mp.FluxRegion(center=detector_pos, size=detector_size))

sim.run(until = 5)