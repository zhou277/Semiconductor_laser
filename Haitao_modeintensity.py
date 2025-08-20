# SI-SP (TM) @ 5 THz — forward-only kx projection of the bound mode
# Au  /  AR  /  n+  /  SI-GaAs   —   avoid MPB EigenModeSource (Drude metal not supported)

import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import math, os

mp.verbosity(1)
mp.eps_averaging = True  # subpixel smoothing; suppress interface spiking

# ---------- units ----------
# speed of light in µm/s
c_um_s = 299_792_458.0 * 1e6  # [µm/s]

# ---------- Drude helpers ----------
def drude_from_carriers(n_cm3, tau_ps, m_eff):
    """Return (Meep Drude suscept., omega_p [1/s], gamma_s [1/s])."""
    e, eps0, me = 1.602176634e-19, 8.8541878128e-12, 9.10938356e-31
    n_m3  = n_cm3 * 1e6
    mstar = m_eff * me
    omega_p = math.sqrt(n_m3 * e * e / (eps0 * mstar))  # [rad/s]
    gamma_s = 1.0 / (tau_ps * 1e-12)                     # [1/s]
    freq    = omega_p / (2 * math.pi * c_um_s)           # Meep units [1/µm]
    gamma   = gamma_s / (2 * math.pi * c_um_s)           # Meep units [1/µm]
    susc = mp.DrudeSusceptibility(frequency=freq, gamma=gamma)
    return susc, omega_p, gamma_s

def eps_real_drude(eps_inf, n_cm3, tau_ps, m_eff, f_um_inv):
    """Re{eps(ω)} of Drude at target frequency (for intensity weighting)."""
    e, eps0, me = 1.602176634e-19, 8.8541878128e-12, 9.10938356e-31
    n_m3  = n_cm3 * 1e6
    mstar = m_eff * me
    wp2   = n_m3 * e * e / (eps0 * mstar)               # [rad/s]^2
    w     = 2 * math.pi * c_um_s * f_um_inv             # [rad/s]
    gamma = 1.0 / (tau_ps * 1e-12)                      # [1/s]
    eps   = eps_inf - wp2 / (w * (w + 1j * gamma))
    return float(np.real(eps))

# ---------- geometry Au / AR / n+ / SI-GaAs ----------
t_Au  = 0.20    # µm
t_AR  = 10.0
t_n   = 0.60
t_sub = 50.0

# PML & padding
dpml_x  = 3.0
dpml_y  = 30.0
pad_top = 1.0

# frequency 5 THz
f_thz  = 5.0
lam_um = (c_um_s * 1e-12) / f_thz      # λ = c/f, with f in THz
fcen   = 1.0 / lam_um                  # Meep frequency [1/µm]
fwidth = 0.003                         # narrowband

# resolution & Courant
RES, Cour = 10, 0.30

# materials (per thesis Sec.4.5)
eps_gas = 12.9
m_eff   = 0.067

AR_susc,  _, _ = drude_from_carriers(5e15, 1.0,  m_eff)
nP_susc,  _, _ = drude_from_carriers(3e18, 0.1,  m_eff)

# Gold Drude: ωp ≈ 1.37e16 rad/s, τ ≈ 0.05 ps
omega_p_Au = 1.37e16
tau_Au_ps  = 0.05
gamma_Au_s = 1.0 / (tau_Au_ps * 1e-12)
Au_freq    = omega_p_Au / (2 * math.pi * c_um_s)
Au_gamma   = gamma_Au_s / (2 * math.pi * c_um_s)
Au_susc    = mp.DrudeSusceptibility(frequency=Au_freq, gamma=Au_gamma)

AR_med  = mp.Medium(epsilon=eps_gas, E_susceptibilities=[AR_susc])
nP_med  = mp.Medium(epsilon=eps_gas, E_susceptibilities=[nP_susc])
Sub_med = mp.Medium(epsilon=eps_gas)
Au_med  = mp.Medium(epsilon=1.0,     E_susceptibilities=[Au_susc])

# cell size
H_struct = t_Au + t_AR + t_n + t_sub
H_total  = pad_top + H_struct
prop_len = 3.2 * lam_um                   # allow mode to settle
sx = prop_len + 2 * dpml_x
cell = mp.Vector3(sx, H_total + 2 * dpml_y, 0)

# stack top→bottom
geom = []
y = H_total / 2
geom.append(
    mp.Block(mp.Vector3(mp.inf, pad_top, mp.inf),
             center=mp.Vector3(0, y - pad_top/2), material=mp.Medium(epsilon=1.0))
)
y -= pad_top
geom.append(
    mp.Block(mp.Vector3(mp.inf, t_Au, mp.inf),
             center=mp.Vector3(0, y - t_Au/2), material=Au_med)
)
y -= t_Au
geom.append(
    mp.Block(mp.Vector3(mp.inf, t_AR, mp.inf),
             center=mp.Vector3(0, y - t_AR/2), material=AR_med)
)
y -= t_AR
geom.append(
    mp.Block(mp.Vector3(mp.inf, t_n, mp.inf),
             center=mp.Vector3(0, y - t_n/2), material=nP_med)
)
y -= t_n
geom.append(
    mp.Block(mp.Vector3(mp.inf, t_sub, mp.inf),
             center=mp.Vector3(0, y - t_sub/2), material=Sub_med)
)

pml_layers = [mp.PML(dpml_x, mp.X), mp.PML(dpml_y, mp.Y)]

# references
y_intf   = H_total/2 - pad_top - t_Au          # Au/AR interface (top of AR)
y_ar_top = y_intf
y_ar_bot = y_ar_top - t_AR

# ---- source TM (Hz) placed in AR center，尽量少激励辐射态 ----
src_y = 0.5 * (y_ar_top + y_ar_bot)
src_h = min(2.0, 0.4 * t_AR)                    # thin vertical line source
x_src = -0.5 * sx + dpml_x + 1.0
sources = [mp.Source(mp.GaussianSource(frequency=fcen, fwidth=fwidth),
                     component=mp.Hz, center=mp.Vector3(x_src, src_y),
                     size=mp.Vector3(0, src_h, 0))]

sim = mp.Simulation(cell_size=cell, 
                    geometry=geom, 
                    sources=sources,
                    boundary_layers=pml_layers, 
                    resolution=RES, 
                    Courant=Cour)

# ---- wide DFT monitor for good kx resolution (use center window) ----
win_w = 100.0                                  # 60–120 µm works well
x_mon = 0.0
mon_vol = mp.Volume(center=mp.Vector3(x_mon, 0, 0),
                    size=mp.Vector3(win_w, H_total, 0))
mon = sim.add_dft_fields([mp.Ex, mp.Ey, mp.Hz], fcen, 0, 1, where=mon_vol)

# run to steady state
sigma_t = 1.0 / (2.0 * math.pi * fwidth)       # time-domain Gaussian std
t_end   = 6.0 * sigma_t + 600.0                # generous ring-down
sim.run(until=t_end)

# ---------- pull fields ----------
def as_yx(a, Ny_expect):
    # ensure array is (Ny, Nx)
    return a if abs(a.shape[0]-Ny_expect) <= abs(a.shape[1]-Ny_expect) else a.T

Ny_exp = int(round(H_total * RES))
Ex2d = as_yx(np.array(sim.get_dft_array(mon, mp.Ex, 0)), Ny_exp)
Ey2d = as_yx(np.array(sim.get_dft_array(mon, mp.Ey, 0)), Ny_exp)
Hz2d = as_yx(np.array(sim.get_dft_array(mon, mp.Hz, 0)), Ny_exp)

Ny, Nx = Ex2d.shape
y_full = np.linspace(-H_total/2, H_total/2, Ny)
depth  = y_intf - y_full  # depth measured downward from Au/AR interface

# x coords across the DFT window
x0 = x_mon - win_w/2
x1 = x_mon + win_w/2
dx = (x1 - x0) / Nx
xs = x0 + np.arange(Nx) * dx

# ---------- find +kx of bound mode using Hz spectrum ----------
k0    = 2 * math.pi / lam_um
k_sub = k0 * math.sqrt(eps_gas)

# rows within AR + n+ + small margin
mask_y = (depth >= 0.0) & (depth <= (t_AR + t_n + 2.0))
Hz_rows = Hz2d[mask_y, :]

win = np.kaiser(Nx, beta=10.0)
Spec = np.fft.fft(Hz_rows * win[None, :], axis=1)
kx_all = 2 * math.pi * np.fft.fftfreq(Nx, d=dx)  # [rad/µm]
P_full = np.mean(np.abs(Spec)**2, axis=0)

# pick strongest positive kx with kx > k_sub (guided / bound)
mask_bnd = kx_all > k_sub
if np.any(mask_bnd):
    cand_idx = np.where(mask_bnd)[0]
    idx = cand_idx[int(np.argmax(P_full[mask_bnd]))]
else:
    # fallback: strongest positive kx
    idx = int(np.argmax(P_full[kx_all > 0]))

kx_sel = float(kx_all[idx])

# ---------- forward-only coherent projection ----------
phase_fwd = np.exp(-1j * kx_sel * xs) * win
norm = np.sum(win)

Ex_mode = (Ex2d @ phase_fwd) / norm
Ey_mode = (Ey2d @ phase_fwd) / norm

# ---------- intensity with Re{eps} * |E|^2 ----------
eps_AR  = eps_real_drude(eps_gas, 5e15, 1.0,  m_eff, fcen)
eps_n   = eps_real_drude(eps_gas, 3e18, 0.1,  m_eff, fcen)
eps_sub = eps_gas

eps_line = np.empty(Ny)
for i, yy in enumerate(y_full):
    if (yy <= y_intf) and (yy > y_intf - t_AR):
        eps_line[i] = eps_AR
    elif (yy <= y_intf - t_AR) and (yy > y_intf - t_AR - t_n):
        eps_line[i] = eps_n
    else:
        eps_line[i] = eps_sub

Iline = eps_line * (np.abs(Ex_mode)**2 + np.abs(Ey_mode)**2)

# only keep below the Au/semiconductor interface
mask  = (depth >= 0) & (depth <= (t_AR + t_n + t_sub))
depth = depth[mask]
Iline = Iline[mask]

# normalize like the thesis figure; ignore first 0.5 µm under Au
norm_mask = depth >= 0.5
peak = float(np.max(Iline[norm_mask])) if np.any(norm_mask) else float(np.max(Iline))
Iline = (Iline / peak) * 100.0

# ---------- plot ----------
os.makedirs('results', exist_ok=True)
plt.figure(figsize=(7.2, 4.3))
plt.plot(depth, Iline, lw=2, label='forward-projected  εr·|E|²')
for yy in [t_AR, t_AR + t_n]:
    plt.axvline(yy, ls='--', lw=.9)
plt.xlim(0, depth.max() if depth.size else 1)
plt.ylim(0, 105)
plt.xlabel('Distance from Au/semiconductor interface  (µm)')
plt.ylabel('Mode intensity (a.u.)  ~  Re{ε(ω)}|E|²')
neff = abs(kx_sel) / k0
plt.title('SI-SP (TM)  Mode intensity at 5 THz  —  Au / AR / n⁺ / SI-GaAs')
plt.legend(title=f'n_eff ≈ {neff:.3f}', loc='upper right', fontsize=9)
plt.tight_layout()
plt.savefig('results/SISP_5THz_profile_kxproj_forward.png', dpi=300)

print(f'Selected kx = {kx_sel:.4f} rad/µm  (n_eff ≈ {neff:.4f});  k0*n_sub = {k_sub:.4f}')
print('Saved results/SISP_5THz_profile_kxproj_forward.png')
