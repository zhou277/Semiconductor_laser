import meep as mp
import numpy as np
import matplotlib.pyplot as plt
from meep.materials import Au,GaAs
import math

###-------------------------Material config--------------------------------------###
def drude_medium(N_cm3, tau_ps, m_eff_ratio, eps_inf)-> mp.Medium:
    # Constants
    e       = 1.602e-19
    eps0    = 8.854e-12
    m_e     = 9.109e-31
    m_eff   = m_eff_ratio * m_e
    c       = 299_792_458.0 * 1e6  # Speed of light in um/s
    N_m3    = N_cm3 * 1e6  # from cm^-3 to m^-3
    omega_p = math.sqrt(N_m3 * e * e / (eps0 * m_eff))  # [rad/s]
    gamma_s = 1.0 / (tau_ps * 1e-12)                     # [1/s]
    omega_meep    = omega_p / (2 * math.pi * c)           # Meep units [1/µm]
    gamma_meep   = gamma_s / (2 * math.pi * c)           # Meep units [1/µm]

    # # Convert units
    # N_m3    = N_cm3 * 1e6  # from cm^-3 to m^-3
    # tau     = tau_ps * 1e-12  # from ps to s

    # # Plasma frequency: ω_p^2 = Ne^2 / (eps0 * m*)
    # omega_p2_SI = N_m3 * e ** 2 / (eps0 * m_eff)  # in rad^2/s^2
    # gamma_SI    = 1 / tau  # in Hz

    # # Convert to Meep units (divide by unit_freq)
    # omega_p2_meep   = omega_p2_SI / (unit_freq ** 2)
    # gamma_meep      = gamma_SI / unit_freq

    # Return Meep medium object
    return mp.Medium(epsilon=eps_inf,E_susceptibilities=[mp.DrudeSusceptibility(frequency=omega_meep, 
                                                                gamma=gamma_meep, 
                                   )])

Au_fun         = drude_medium(N_cm3=5.6e22, tau_ps=0.05,    m_eff_ratio=0.067, eps_inf=1.0 )
GaAs_5e18_fun  = drude_medium(N_cm3=5.0e18, tau_ps=0.1,     m_eff_ratio=0.067, eps_inf=12.9)
GaAs_5e15_fun  = drude_medium(N_cm3=5.0e15, tau_ps=1.0,     m_eff_ratio=0.067, eps_inf=12.9)
GaAs_3e18_fun  = drude_medium(N_cm3=3.0e18, tau_ps=1.0,     m_eff_ratio=0.067, eps_inf=12.9)
GaAs_1e18_fun  = drude_medium(N_cm3=1.0e18, tau_ps=0.1,     m_eff_ratio=0.067, eps_inf=12.9)
GaAs_0_fun  = drude_medium(N_cm3=0, tau_ps=1.0,  m_eff_ratio=0.067, eps_inf=12.9)

# Perfectly Matched Layer if THz , set PML to 1
pml_layers = [mp.PML(1)]
# thickness of different layers（1 μm）
Au_thickness = 0.2
nSI_GaAs_thickness = 0.1
Active_GaAs_thickness = 10
substrate_GaAs_thickness = 50
model = 'MM'  # 'plasmon' or 'MM'

###-------------------------basic config--------------------------------------###
# Set up for source frequency 
c_um_s = 299_792_458.0 * 1e6  # 光速, µm/s
f_Hz = 5e12                   # 5 THz
freq_in_meep = f_Hz / c_um_s          # ≈ 0.016678  (1/µm)，Meep 里的频率
fwidth = 0.002

###--------------------------geometry------------------------------------------###
# define the basic height of layers
def add_layer(thickness, material):
    global x0
    center_x = x0 + 0.5 * thickness
    geometry.append(mp.Block(size=mp.Vector3(thickness,mp.inf,mp.inf),
                             center=mp.Vector3(center_x, 0, 0),
                             material=material))
    x0 += thickness

# Construct layers
geometry = []
if model == 'plasmon':
    "switch to Plasmon structure"
    material_height = Au_thickness + nSI_GaAs_thickness + Active_GaAs_thickness + 2 + substrate_GaAs_thickness
    x0 = -0.5 * (Au_thickness + nSI_GaAs_thickness + Active_GaAs_thickness + 2 + substrate_GaAs_thickness)
    add_layer(substrate_GaAs_thickness, GaAs_1e18_fun)
    add_layer(2,                        GaAs_5e18_fun)
elif model == 'MM':
    "switch to Metal-metal structure"
    material_height = Au_thickness + nSI_GaAs_thickness + Active_GaAs_thickness + nSI_GaAs_thickness + Au_thickness
    x0 = -0.5 * material_height
    add_layer(Au_thickness,             Au_fun)
    add_layer(nSI_GaAs_thickness,       GaAs_3e18_fun)
# other layers
add_layer(Active_GaAs_thickness,    GaAs_5e15_fun)
add_layer(nSI_GaAs_thickness,       GaAs_3e18_fun)
add_layer(Au_thickness,             Au_fun)

###-------------------------source---------------------------###
resolution = 50
sx = material_height
sy = 0
sz = 5
cell = mp.Vector3(sx, sy, sz)

sources = [mp.Source(
                    src=mp.ContinuousSource(frequency=freq_in_meep,fwidth=fwidth),
                    # src=mp.GaussianSource(frequency=freq_in_meep,fwidth=fwidth),
                    amplitude=1,
                    component=mp.Hy,
                    center=mp.Vector3(0,0,-sz/2),      # 放在结构左侧一些
                    size=mp.Vector3(sx, 0, 0)),
                    ]


###----------------------simulation setup------------------###
# basic setup (1 μm)
def plot_Ex(sim:mp.simulation):
    """sample Ex on x axis in the simulation"""
    x = np.linspace(-sx/2, sx/2, 1000)
    eps_data = np.array([sim.get_epsilon_point(mp.Vector3(xi,0,0)) for xi in x])
    ex_data = np.array([abs(sim.get_field_point(mp.Ex, mp.Vector3(xi))**2) for xi in x])
    ey_data = np.array([abs(sim.get_field_point(mp.Ey, mp.Vector3(xi))**2) for xi in x])
    ez_data = np.array([abs(sim.get_field_point(mp.Ez, mp.Vector3(xi))**2) for xi in x])


    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Distance (um) along x')
    ax1.set_ylabel('Mode Intensity |Ex|', color=color)
    ax1.plot(x, ex_data, color=color)
    ax1.tick_params(axis='x', labelcolor=color)
    ax1.set_xlim(-sx/2-1,sx/2+1)
    ax1.set_ylim(0, np.max(ex_data)*1.2)

    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Re{ε}', color=color)
    ax2.plot(x, eps_data, color=color, linestyle='--')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(5, 15)

    plt.title('Mode Intensity and Epsilon Profile')
    plt.show()
    
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Distance (um) along x')
    ax1.set_ylabel('Mode Intensity |Ey|', color=color)
    ax1.plot(x, ey_data, color=color)
    ax1.tick_params(axis='x', labelcolor=color)
    ax1.set_xlim(-sx/2-1,sx/2+1)
    ax1.set_ylim(0, np.max(ey_data)*1.2)

    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Re{ε}', color=color)
    ax2.plot(x, eps_data, color=color, linestyle='--')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(5, 15)

    plt.title('Mode Intensity and Epsilon Profile')
    plt.show()
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Distance (um) along x')
    ax1.set_ylabel('Mode Intensity |Ez|', color=color)
    ax1.plot(x, ez_data, color=color)
    ax1.tick_params(axis='x', labelcolor=color)
    ax1.set_xlim(-sx/2-1,sx/2+1)
    ax1.set_ylim(0, np.max(ez_data)*1.2)

    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Re{ε}', color=color)
    ax2.plot(x, eps_data, color=color, linestyle='--')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(5, 15)

    plt.title('Mode Intensity and Epsilon Profile')
    plt.show()


dpml = 1
sim = mp.Simulation(
    cell_size=cell,
    resolution=resolution,
    # boundary_layers=[mp.PML(dpml, direction=mp.X),
                    #  mp.PML(dpml, direction=mp.Z)],
    geometry=geometry,
    sources=sources,
    dimensions=2)


# sim.run(until=10)
# plot_Ex(sim)

# for i in range (0,10,1):
#     sim.run(until=i)
#     plot_Ex(sim)
dft_fields = sim.add_dft_fields([mp.Ex, mp.Ey, mp.Ez],
                                 freq_in_meep, 0, 1,
                                 where=mp.Volume(center=mp.Vector3(0,0,0),
                                                 size=mp.Vector3(sx,0,sz))) 

sim.plot2D(eps_parameters={'colorbar':True},  # 显示介电常数的 colorbar},
           colorbar_parameters={
               "label": "Ez field",           # 设置colorbar标题
               "orientation": "vertical",     # 垂直显示
               "position": "right",           # 放在图的右侧
               "size": "5%",                  # colorbar的宽度
               "pad": "2%",                   # colorbar和图之间的距离
               "format": "{x:.2e}"            # 科学计数法显示刻度
           },
           labels=True)

sigma_t = 1.0 / (2.0 * math.pi * fwidth)
t_end   = 6.0 * sigma_t + 600.0
sim.run(until=t_end)


# ---------- 取 DFT 场并画沿 x ----------
Ez = sim.get_dft_array(dft_fields, mp.Ez, 0)
Ex = sim.get_dft_array(dft_fields, mp.Ex, 0)
Ey = sim.get_dft_array(dft_fields, mp.Ey, 0)
Ez = np.squeeze(Ez)               # (Nx, Ny, Nz) -> (Nx,)
# Ex = np.squeeze(Ex)
I = np.abs(Ez)**2
# I = np.abs(Ex)**2
plt.figure()
x_coords = np.linspace(-cell.x/2, cell.x/2, I.shape[0])

fig, ax1 = plt.subplots()
color = 'tab:blue'
ax1.set_xlabel('Distance (um) along y')
ax1.set_ylabel('Mode Intensity |Ez|', color=color)
ax1.plot(x_coords, I, lw=2, label='forward-projected |Ez|² (x–z, normalized)')
ax1.tick_params(axis='x', labelcolor=color)
ax1.set_xlim(-sx/2-1,sx/2+1)
ax1.set_ylim(0, np.max(I)*1.2)

eps_data = np.array([sim.get_epsilon_point(mp.Vector3(xi,0,0)) for xi in x_coords])
ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Re{ε}', color=color)
ax2.plot(x_coords, eps_data, color=color, linestyle='--')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(5, 15)

plt.title(f"Mode intensity at f={freq_in_meep:.5f} (Meep units)")
plt.show()

plt.savefig('results/mode_profile_forward_xy.png', dpi=300)