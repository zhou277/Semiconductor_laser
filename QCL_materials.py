import meep as mp

Au = mp.Medium(
    epsilon=1,  # epsilon_infty
    E_susceptibilities=[
        mp.DrudeSusceptibility(
            frequency=1.37,  # omega_p
            gamma=0.0106,    # gamma
            sigma=1.0        # MEEP内部等效，取值=1即可
        )
    ]
)

Ti = mp.Medium(
    epsilon=1.0,
    D_conductivity=27.1
)

PdGe = mp.Medium(
    epsilon=1.0,
    D_conductivity=5.0  # 比钛弱，但仍是吸收型
)

nplus_GaAs = mp.Medium(
    epsilon=12.9,  # 高频ε
    E_susceptibilities=[
        mp.DrudeSusceptibility(
            frequency=0.0063,  # ωp，归一化 μm⁻¹
            gamma=0.01,        # γ，归一化 μm⁻¹
            sigma=1.0          # Meep 内部写1即可
        )
    ]
)

SI_GaAs = mp.Medium(
    epsilon=12.9
)

AR = mp.Medium(epsilon=1.45**2)

GaAs = mp.Medium(epsilon=12.9)