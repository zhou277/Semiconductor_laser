import meep as mp
import math

light_speed = 3e8
meep_trans = 1e-6

Au = mp.Medium(
    epsilon=1.0,
    E_susceptibilities=[
        mp.DrudeSusceptibility(frequency=0.44, gamma=0.033, sigma=1.0)])

# Material in waveguide experiments
    ## GaAs N = 5e18 cm-3 used in the middle layer between Au and Active Region (n-Si doping)
nSI_GaAs = mp.Medium(
    epsilon=10.9,
    E_susceptibilities=[
        mp.DrudeSusceptibility(frequency=1.62, 
                               gamma=0.033, 
                               sigma=1.0)])
    ## GaAs N = 0 or 5e15 cm-3 used in Active Region
GaAs_active = mp.Medium(
    epsilon=12.25,
    E_susceptibilities=[
        mp.DrudeSusceptibility(frequency=0.0513, 
                               gamma=0.0033, 
                               sigma=1.0)])
    ## substrate GaAs N = 1~2e18 cm-3 used in substrate 
substrate_GaAs = mp.Medium(
    epsilon=10.9,
    E_susceptibilities=[
        mp.DrudeSusceptibility(frequency=0.7252,   
                               gamma=0.0333,       
                               sigma=1.0)])


###--------------Another way of setting up the material by Drude--------------###
"""refer to the official document,using the meep unit"""
def drude_medium(N_cm3, tau_ps, m_eff_ratio, eps_inf)-> mp.Medium:
    # Constants
    e = 1.602e-19
    eps0 = 8.854e-12
    m_e = 9.109e-31
    m_eff = m_eff_ratio * m_e
    a = 1e-6  # um
    c = 3e8
    unit_freq = c / a

    # Convert units
    N = N_cm3 * 1e6  # from cm^-3 to m^-3
    tau = tau_ps * 1e-12  # from ps to s

    # Plasma frequency: ω_p^2 = Ne^2 / (eps0 * m*)
    omega_p2_SI = N * e ** 2 / (eps0 * m_eff)  # in rad^2/s^2
    gamma_SI = 1 / tau  # in Hz

    # Convert to Meep units (divide by unit_freq)
    omega_p2_meep = omega_p2_SI / (unit_freq ** 2)
    gamma_meep = gamma_SI / unit_freq

    # Return Meep medium object
    return mp.Medium(
        epsilon=eps_inf,
        E_susceptibilities=[
            mp.DrudeSusceptibility(frequency=0, gamma=gamma_meep, sigma=omega_p2_meep)
        ])

material_au = drude_medium(N_cm3=5.6e22, tau_ps=0.05, m_eff_ratio=1.0, eps_inf=1.0)
material_gaas_doped = drude_medium(N_cm3=5e18, tau_ps=0.1, m_eff_ratio=0.067, eps_inf=12.9)
material_gaas_lightly_doped = drude_medium(N_cm3=5e15, tau_ps=1.0, m_eff_ratio=0.067, eps_inf=12.9)
material_gaas_substrate = drude_medium(N_cm3=1e18, tau_ps=0.1, m_eff_ratio=0.067, eps_inf=12.9)

###--------------Do not use the Drude model to identify the material--------------###
# Au
Au_XD = mp.Medium(index=2.21)
## GaAs N = 5e18 cm-3 used in the middle layer between Au and Active Region (n-Si doping)
GaAs_High_XD = mp.Medium(index=4.55)
## GaAs N = 0 or 5e15 cm-3 used in Active Region
GaAs_Act_XD = mp.Medium(index=3.45)
