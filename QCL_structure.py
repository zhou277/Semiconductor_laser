import meep as mp
import numpy as np

# 各层厚度（单位：μm）
resolution = 50
sx = 7000
sy = 350
sz = 120
cell = mp.Vector3(0, sy, sz)
pml_layers = [mp.PML(0.1)]

# 各层厚度（单位：μm）
au_thickness = 0.18
ti_thickness = 0.02
pdge_thickness = 0.1
ngaas_thickness_1 = 0.08
Ar_thickness = 0.0113

ngaas_thickness_2 = 0.7
sigaas_thickness = 300

# 材料定义（近似 ε = n^2）
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
                    size=mp.Vector3(mp.inf, sigaas_thickness,sz),
                    center=mp.Vector3(y= -sy/2 + sigaas_thickness/2)))

geometry.append(mp.Block(
                    material=ngaas,
                    size=mp.Vector3(mp.inf, ngaas_thickness_2,sz),
                    center=mp.Vector3(y= -sy/2 + sigaas_thickness/2 + ngaas_thickness_2/2)))

# QCL active region
geometry.append(mp.Block(
                    material=Ar,
                    size=mp.Vector3(mp.inf, Ar_thickness,sz),
                    center=mp.Vector3(y= -sy/2 + sigaas_thickness/2 + ngaas_thickness_2/2 + Ar_thickness/2)))

# 上层金属叠层
y0 = -sy/2 + sigaas_thickness/2 + ngaas_thickness_2/2 + Ar_thickness/2
geometry += [
    mp.Block(material = Ar,  
             size = mp.Vector3(mp.inf, Ar_thickness,sz), 
             center = mp.Vector3(y=y0 + Ar_thickness/2)),
    mp.Block(material = ngaas, 
             size = mp.Vector3(mp.inf, ngaas_thickness_1,sz), 
             center = mp.Vector3(y=y0 + Ar_thickness + ngaas_thickness_1/2)),
    mp.Block(material = pdge,    
             size = mp.Vector3(mp.inf, pdge_thickness,sz),    
             center = mp.Vector3(y=y0 + Ar_thickness + ngaas_thickness_1/2 + pdge_thickness/2)),
    mp.Block(material = ti,    
             size = mp.Vector3(mp.inf, ti_thickness,sz),    
             center = mp.Vector3(y=y0 + Ar_thickness + ngaas_thickness_1/2 + pdge_thickness/2 + ti_thickness/2)),
    mp.Block(material = au,    
             size = mp.Vector3(mp.inf, au_thickness,sz),    
             center = mp.Vector3(y=y0 + Ar_thickness + ngaas_thickness_1/2 + pdge_thickness/2 + ti_thickness/2 + au_thickness/2))
]
    
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


sim.plot2D(output_plane=mp.Volume(center=mp.Vector3(0,0,0), 
                                  size=mp.Vector3(0, y=sim.cell_size.y, z=sim.cell_size.z)))