import meep as mp
import numpy as np
import matplotlib.pyplot as plt

# --- define parameters ---
cell_x = 16
cell = mp.Vector3(cell_x, 0, 0)

resolution = 50
n_gain = 3.5
n_grating = 3.2
n_bg = 1.0

grating_period = 1
bar_width = 0.5
num_grating = 8

# --- define geometry structure ---
geometry = []

# the gain region
geometry.append(mp.Block(center=mp.Vector3(),
                         size=mp.Vector3(6, mp.inf),
                         material=mp.Medium(index=n_gain)))

# --- periodic grating structure ---
for i in range(num_grating):
    x_pos = i * grating_period
    geometry.append(mp.Block(center=mp.Vector3(x_pos, 0),
                             size=mp.Vector3(bar_width, mp.inf),
                             material=mp.Medium(index=n_grating)))

# --- define a broadband gaussian source ---
sources = [mp.Source(mp.GaussianSource(frequency=3e10, fwidth=0.1),
                     component=mp.Ez,
                     center=mp.Vector3(-6))]

# --- Add a flux monitor to record transmission spectrum ---
tran_fr = mp.FluxRegion(center=mp.Vector3(6))
frequencies = np.linspace(2e10, 4e10, 100)

# --- Set up simulation ---
sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=[mp.PML(1.0)],
    geometry=geometry,
    sources=sources,
    resolution=resolution,
)

tran = sim.add_flux(3e10,1e5,100, tran_fr)
sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ez, mp.Vector3(6), 1e-5))

# --- Extract and plot transmission spectrum ---
flux_vals = mp.get_fluxes(tran)
freqs = mp.get_flux_freqs(tran)

plt.plot(freqs, flux_vals)
plt.xlabel("Frequency (a.u.)")
plt.ylabel("Transmitted Flux")
plt.title("Frequency Response of Grating + Gain Structure")
plt.grid(True)
plt.show()
