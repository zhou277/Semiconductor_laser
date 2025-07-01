import meep as mp
import numpy as np
import matplotlib.pyplot as plt

resolution = 50
sx = 12
sy = 5
cell = mp.Vector3(sx, sy, 0) # 2D structure
pml_layers = [mp.PML(1.0)] # set up perfectly match layer

# set up each layers width (μm)
padge_thickness = 0.08
ngaas_thickness = 0.1
ti_thickness = 0.02
au_thickness = 0.18
core_thickness = 2.5
substrate_thickness = 1.0

# define material with epsilon
si_gaas = mp.Medium(epsilon=12.9)
qcl_core = mp.Medium(epsilon=13.0)
ngaas = mp.Medium(epsilon=12.5)
pdge = mp.Medium(epsilon=10.0)
ti = mp.Medium(epsilon=6.0)
au = mp.Medium(epsilon=9.5)

geometry = []

# Substrate
geometry.append(mp.Block(
    material=si_gaas,
    size=mp.Vector3(mp.inf, substrate_thickness),
    center=mp.Vector3(y=-sy/2 + substrate_thickness/2)
))

# QCL active region
geometry.append(mp.Block(
    material=qcl_core,
    size=mp.Vector3(mp.inf, core_thickness),
    center=mp.Vector3(y=-sy/2 + substrate_thickness + core_thickness/2)
))

# upper layer
y0 = -sy/2 + substrate_thickness + core_thickness
geometry += [
    mp.Block(material = pdge, size = mp.Vector3(mp.inf, padge_thickness), center = mp.Vector3(y=y0 + padge_thickness/2)),
    mp.Block(material = ngaas, size = mp.Vector3(mp.inf, ngaas_thickness), center = mp.Vector3(y=y0 + padge_thickness + ngaas_thickness/2)),
    mp.Block(material = ti, size = mp.Vector3(mp.inf, ti_thickness), center = mp.Vector3(y=y0 + padge_thickness + ngaas_thickness + ti_thickness/2)),
    mp.Block(material = au, size = mp.Vector3(mp.inf, au_thickness), center = mp.Vector3(y=y0 + padge_thickness + ngaas_thickness + ti_thickness + au_thickness/2))
]

# Source
sources = [mp.Source(
    src=mp.GaussianSource(frequency=1/0.1, fwidth=0.2),
    component=mp.Ez,
    center=mp.Vector3(-3, -sy/2 + 0.5),
    size=mp.Vector3(0, 1.0)
)]

tran_fr = mp.FluxRegion(center=mp.Vector3(6))
frequencies = np.linspace(10,10,100)

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

# tran = sim.add_flux(10,10,100,tran_fr)
# sim.run(until=50)

# # --- Extract and plot transmission spectrum ---
# flux_vals = mp.get_fluxes(tran)
# freqs = mp.get_flux_freqs(tran)

# plt.plot(freqs, flux_vals)
# plt.xlabel("Frequency (a.u.)")
# plt.ylabel("Transmitted Flux")
# plt.title("Frequency Response of Grating + Gain Structure")
# plt.grid(True)
# plt.show()

