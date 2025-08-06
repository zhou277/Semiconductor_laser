import meep as mp
import math

light_speed = 3e8
meep_trans = 1e-6

###--------------set up by drude model--------------------###
"""refer to the drude model"""
# def cal_omega_p(N,e,epsilon_0,m_star,
#                 light_speed=3e8,meep_trans=1e-6):
#     omega_p = math.sqrt(N * e**2 / (epsilon_0 * m_star))
#     omega_p_meep = omega_p * meep_trans / light_speed
#     return omega_p_meep

# def cal_gamma_meep(gamma,
#                    light_speed=3e8,meep_trans=1e-6):
#     return gamma * meep_trans / light_speed 

# # 1. Calculate the parameter of N=1e18/cm^3
# N = 1e24
# tao = 1e-13
# gamma = 1/tao
# me = 9.109e-31
# m_star = 0.067 * me
# epsilon_0= 8.85e-12
# e = 1.6e-19
# print('n+ substrate GaAs (N = 1 x 10^18 / cm^3)')
# print('     omega = ' + str(cal_omega_p(N=N,e=e,epsilon_0=epsilon_0,m_star=m_star)))
# print('     gamma = '+ str(cal_gamma_meep(gamma=gamma)))

# # 2. Calculate the parameter of N=5e18/cm^3
# N = 5e24
# tao = 1e-13
# gamma = 1/tao
# me = 9.109e-31
# m_star = 0.067 * me
# epsilon_0= 8.85e-12
# e = 1.6e-19
# print('GaAs (N = 5 x 10^18 / cm^3)')
# print('     omega = ' + str(cal_omega_p(N=N,e=e,epsilon_0=epsilon_0,m_star=m_star)))
# print('     gamma = '+ str(cal_gamma_meep(gamma=gamma)))

# # 3. Calculate the parameter of N=5e15/cm^3
# N = 5e21
# tao = 1e-12
# gamma = 1/tao
# me = 9.109e-31
# m_star = 0.067 * me
# epsilon_0= 8.85e-12
# e = 1.6e-19
# print('GaAs (N = 5 x 10^15 / cm^3)')
# print('     omega = ' + str(cal_omega_p(N=N,e=e,epsilon_0=epsilon_0,m_star=m_star)))
# print('     gamma = '+ str(cal_gamma_meep(gamma=gamma)))

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
