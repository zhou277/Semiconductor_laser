import meep as mp
import math

light_speed = 3e8
meep_trans = 1e-6

def cal_omega_p(N,e,epsilon_0,m_star,
                light_speed=3e8,meep_trans=1e-6):
    omega_p = math.sqrt(N * e**2 / (epsilon_0 * m_star))
    omega_p_meep = omega_p * meep_trans / light_speed
    return omega_p_meep

def cal_gamma_meep(gamma,
                   light_speed=3e8,meep_trans=1e-6):
    return gamma * meep_trans / light_speed 

# 1. Calculate the parameter of N=1e18/cm^3
N = 1e24
tao = 1e-13
gamma = 1/tao
me = 9.109e-31
m_star = 0.067 * me
epsilon_0= 8.85e-12
e = 1.6e-19
print('n+ substrate GaAs (N = 1 x 10^18 / cm^3)')
print('     omega = ' + str(cal_omega_p(N=N,e=e,epsilon_0=epsilon_0,m_star=m_star)))
print('     gamma = '+ str(cal_gamma_meep(gamma=gamma)))

# 2. Calculate the parameter of N=5e18/cm^3
N = 5e24
tao = 1e-13
gamma = 1/tao
me = 9.109e-31
m_star = 0.067 * me
epsilon_0= 8.85e-12
e = 1.6e-19
print('GaAs (N = 5 x 10^18 / cm^3)')
print('     omega = ' + str(cal_omega_p(N=N,e=e,epsilon_0=epsilon_0,m_star=m_star)))
print('     gamma = '+ str(cal_gamma_meep(gamma=gamma)))

# 3. Calculate the parameter of N=5e15/cm^3
N = 5e21
tao = 1e-12
gamma = 1/tao
me = 9.109e-31
m_star = 0.067 * me
epsilon_0= 8.85e-12
e = 1.6e-19
print('GaAs (N = 5 x 10^15 / cm^3)')
print('     omega = ' + str(cal_omega_p(N=N,e=e,epsilon_0=epsilon_0,m_star=m_star)))
print('     gamma = '+ str(cal_gamma_meep(gamma=gamma)))

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

    ## GaAs N = 0 or 5e15 cm-3 used in Active Region (highly doped)
GaAs = mp.Medium(
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
