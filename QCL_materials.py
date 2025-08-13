import meep as mp
import math

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
    N_m3 = N_cm3 * 1e6  # from cm^-3 to m^-3
    tau = tau_ps * 1e-12  # from ps to s

    # Plasma frequency: ω_p^2 = Ne^2 / (eps0 * m*)
    omega_p2_SI = N_m3 * e ** 2 / (eps0 * m_eff)  # in rad^2/s^2
    gamma_SI = 1 / tau  # in Hz

    # Convert to Meep units (divide by unit_freq)
    omega_p2_meep = omega_p2_SI / (unit_freq ** 2)
    gamma_meep = gamma_SI / unit_freq

    # Return Meep medium object
    return mp.Medium(epsilon=eps_inf,
                    E_susceptibilities=[mp.DrudeSusceptibility(frequency=0, 
                                                                gamma=gamma_meep, 
                                                                sigma=omega_p2_meep
                                   )])

Au_fun         = drude_medium(N_cm3=5.6e22, tau_ps=0.05, m_eff_ratio=1.0,   eps_inf=1.0 )
GaAs_5e18_fun  = drude_medium(N_cm3=5.0e18, tau_ps=0.1,  m_eff_ratio=0.067, eps_inf=12.9)
GaAs_5e15_fun  = drude_medium(N_cm3=5.0e15, tau_ps=1.0,  m_eff_ratio=0.067, eps_inf=12.9)
GaAs_1e18_fun  = drude_medium(N_cm3=1.0e18, tau_ps=0.1,  m_eff_ratio=0.067, eps_inf=12.9)
GaAs_0_fun  = drude_medium(N_cm3=0, tau_ps=1.0,  m_eff_ratio=0.067, eps_inf=12.9)


"""Using the approximated parameter model"""
# Au
Au_XD = mp.Medium(index=2.21)
## GaAs N = 5e18 cm-3 used in the middle layer between Au and Active Region (n-Si doping)
GaAs_High_XD = mp.Medium(index=4.55)
## GaAs N = 0 or 5e15 cm-3 used in Active Region
GaAs_Act_XD = mp.Medium(index=3.45)

"""Using the complex conductivity"""
def transfer_to_meep_frequency(frequency:int)->int:
    um = 1e-6
    c = 3e8 
    frequency_in_meep = frequency * um / c
    return frequency_in_meep

# Electronically tunable aperiodic distributed feedback terahertz lasers
# material in the above artical
# the details are in the Fig 1 part c and d
# c is a standard SI-SP waveguide at 2.85THz and d is same structure after the removal of the metal overlayers
# This material is used to plot the mode intensity
freq_in_meep = transfer_to_meep_frequency(2.85e12)

QCL_neff_c = mp.Medium(epsilon=3.647, D_conductivity=2*math.pi*freq_in_meep*0.007/3.647)
QCL_neff_d = mp.Medium(epsilon=3.308, D_conductivity=2*math.pi*freq_in_meep*0.217/3.308)
