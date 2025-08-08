import meep as mp
import numpy as np

# basic setup (0.1 μm)
resolution = 100
sx = 70
sy = 35
sz = 12
cell = mp.Vector3(sx, sy, 0)
pml_layers = [mp.PML(1)]

# thickness of different layers（0.1 μm）
au_thickness = 0.018
ti_thickness = 0.002
pdge_thickness = 0.01
ngaas_thickness_1 = 0.008
Ar_thickness = 0.00113

ngaas_thickness_2 = 0.07
sigaas_thickness = 30

# material definition
au = mp.Medium(epsilon=9.5)
ti = mp.Medium(epsilon=6.0)
pdge = mp.Medium(epsilon=10.0)
ngaas = mp.Medium(epsilon=12.5)
Ar = mp.Medium(epsilon=13.0)
si_gaas = mp.Medium(epsilon=12.9,)

geometry = []

# Substrate
geometry.append(mp.Block(
                    material=si_gaas,
                    size=mp.Vector3(sx, sigaas_thickness,sz),
                    center=mp.Vector3(y= -sy/2 + sigaas_thickness/2)))

geometry.append(mp.Block(
                    material=ngaas,
                    size=mp.Vector3(sx, ngaas_thickness_2,sz),
                    center=mp.Vector3(y= -sy/2 + sigaas_thickness + ngaas_thickness_2/2)))

# QCL active region
geometry.append(mp.Block(
                    material=Ar,
                    size=mp.Vector3(sx, Ar_thickness,sz),
                    center=mp.Vector3(y= -sy/2 + sigaas_thickness + ngaas_thickness_2 + Ar_thickness/2)))

# upper layers
y0 = -sy/2 + sigaas_thickness + ngaas_thickness_2 + Ar_thickness
geometry += [
    mp.Block(material = Ar,  
             size = mp.Vector3(sx, Ar_thickness,sz), 
             center = mp.Vector3(y = y0 + Ar_thickness/2)),
    mp.Block(material = ngaas, 
             size = mp.Vector3(sx, ngaas_thickness_1,sz), 
             center = mp.Vector3(y = y0 + Ar_thickness + ngaas_thickness_1/2)),
    mp.Block(material = pdge,    
             size = mp.Vector3(sx, pdge_thickness,sz),    
             center = mp.Vector3(y = y0 + Ar_thickness + ngaas_thickness_1 + pdge_thickness/2)),
    mp.Block(material = ti,    
             size = mp.Vector3(sx, ti_thickness,sz),    
             center = mp.Vector3(y = y0 + Ar_thickness + ngaas_thickness_1 + pdge_thickness + ti_thickness/2)),
    mp.Block(material = au,    
             size = mp.Vector3(sx, au_thickness,sz),    
             center = mp.Vector3(y = y0 + Ar_thickness + ngaas_thickness_1 + pdge_thickness + ti_thickness + au_thickness/2))
]
    
# grating parameters
Λ = 0.5                    # 基本周期（0.1μm）
slot_length = 10
slot_width = 0.1        
slot_depth = 0.5       
slot_spacing = Λ / 2
pattern_1 = "|-||-|-||||||-|||||-||||-|||-||-||||"  # 狭缝排列样式
pattern_2 = "-|||||||-||-||-|||-||-|-||-|||-||-|-||||||-||-|-|||-||-|||||-|||"
pattern_3 = "-||-||-||-|||||-||||||-|||-||||-||-||-|||||||||-||-|-||-||-||-|-|||-||-||-|-||||||-||||||||-||-||||||-||||---|"
pattern = pattern_1 + pattern_2 + pattern_3


x_start = -len(pattern) * slot_spacing / 2
y_grating = y0 + Ar_thickness + ngaas_thickness_1 + pdge_thickness + ti_thickness + au_thickness/2

# grating list
grating_geometry = []

# setup grating list
for i, symbol in enumerate(pattern):
    if symbol == "|":
        x_pos = x_start + i * slot_spacing
        grating_geometry.append(mp.Block(
                                material=mp.air,
                                size=mp.Vector3(slot_width, slot_depth, sz),
                                center=mp.Vector3(x_pos,y_grating,0)
        ))

# add to original layers
geometry += grating_geometry

# Source
sources = [mp.Source(
    src=mp.GaussianSource(frequency=1/0.1, fwidth=0.2),
    component=mp.Ez,
    center=mp.Vector3(0,0,0),
    size=mp.Vector3(0,4.0,0))]

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