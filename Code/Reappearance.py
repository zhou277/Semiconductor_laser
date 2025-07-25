import meep as mp
import numpy as np
import matplotlib.pyplot as plt
from QCL_materials import Au,GaAs

# thickness of different layers（1 μm）
Au_thickness = 0.1
GaAs_thickness_1 = 10
GaAs_thickness_2 = 0.1

# basic setup (1 μm)
resolution = 50
sx = 15
sy = 11
sz = 1
cell = mp.Vector3(sx, sy, 0)
# Perfectly Matched Layer if THz , set PML to 1
pml_layers = [mp.PML(0.1)]

# Set up for source frequency 
frequency = 3e10 # 3THz

# Set up for detector 's observe range
observe_range = 0.1

# define the basic height of layers
y0 = -0.5 * (Au_thickness + GaAs_thickness_2 + GaAs_thickness_1 + GaAs_thickness_2 + Au_thickness)

# Construct layers
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

add_layer(Au_thickness, Au)
add_layer(GaAs_thickness_2, GaAs)
add_layer(GaAs_thickness_1,GaAs)
add_layer(GaAs_thickness_2, GaAs)
add_layer(Au_thickness, Au)

# Source
sources = [mp.Source(
            src=mp.GaussianSource(frequency=frequency, fwidth=1),
            component=mp.Ex,
            center=mp.Vector3(-sx/2,0,0),
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

# Plot the structure
sim.plot2D()

# Set up the flux monitor 
flux_monitor = sim.add_flux(frequency, frequency * observe_range, 100, 
                            mp.FluxRegion(center=mp.Vector3(7,0,0), 
                                          size=mp.Vector3(0,30,1))
                                          )

# Run the simulation
sim.run(until = 50)


# Plot the figure of frequency and flux intensity
frequencies = mp.get_flux_freqs(flux_monitor)
flux_data = mp.get_fluxes(flux_monitor)
plt.figure(figsize=(8, 4))
plt.plot(frequencies, flux_data, marker='o', color='blue', label='Spectral Flux')
plt.xlabel('Frequency (1/μm)', fontsize=12)
plt.ylabel('Flux Intensity (a.u.)', fontsize=12)
plt.title('Spectral Response at Detector', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

# Plot the figure of field point of Ex along the y-axis
y_vals = np.linspace(-sy/2, sy/2, 500)
ex_vals = []

for y in y_vals:
    pt = mp.Vector3(0, y)  # x=0, y=varies
    ex_vals.append(sim.get_field_point(mp.Ex, pt))

plt.figure(figsize=(6,4))
plt.plot(y_vals, ex_vals, label='Ex along y-axis at x=0', color='blue')
plt.xlabel("y (μm)")
plt.ylabel("Ex Field")
plt.title("Field Distribution Along y-axis")
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

# Plot Mode Intensity
ex_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ex)
center_x_index = ex_data.shape[0] // 2
field_line = np.abs(ex_data[center_x_index, :])**2  # Ex 场强平方 -> 模强度
fig, ax1 = plt.subplots(figsize=(8, 4))
x = np.linspace(-2, 12, len(field_line))
ax1.plot(x, field_line, 'b-', label='Mode Intensity')
ax1.set_xlabel('Distance (μm)')
ax1.set_ylabel('Mode Intensity (a.u.)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Plot Re(ε) on secondary axis
ax2 = ax1.twinx()
epsilon_profile = np.where((x > 0) & (x < 10), 12, 1)
ax2.plot(x, epsilon_profile, 'g--', label='Re(ε)')
ax2.set_ylabel('Re(ε)', color='g')
ax2.tick_params(axis='y', labelcolor='g')

plt.title('Mode Intensity and Dielectric Profile')
plt.show()