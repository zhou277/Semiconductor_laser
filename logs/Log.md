# Research on aperiodic lattice laser by Meep
## logs
---
### 7.14
- Define the materials in the QCL_Materials.py.  
- The parameters are given by the Chat, based on the Drude model.  
- Try to make the reappearance of 4.5.1 Plasmon waveguide in   
https://dspace.mit.edu/bitstream/handle/1721.1/17012/54455783-MIT.pdf?sequence=2&isAllowed=y
![alt text](image-4.png)   
- The code is in the Reappearance.py, please put the **QCL_materials.py** together to run the script.  
- The structure is as following , the red section is the source.  
 ![alt text](image-2.png)  
- The result is record as following.  
 ![alt text](image-1.png)
- It seems the source can not transport through the materials.
---
### 7.16
- Previous sourcs is setting from the x axis  
- Try source from direction of y axis with the dot source  
- The structure is as following, the red dot is a continuous source with frequency of 3THz.  
 ![alt text](image-5.png)  
- The result is as following.  
![alt text](image-6.png)
---
### 7.18
- Modify the direction from z axis with 3THz and observe the intensity from x axis and result is as follows.  
- Source is setted up as a slab continuous source.  
- The structure is below.  
![alt text](image-8.png)  
- Au thickness is 0.1 um and active region is 10 um.  
- Simulation is run without pml layer in 3D.  
![alt text](image-7.png)  
- The materials is using the parameter in meep.  
---
### 7.23
- Back to the structure of QCL like below.  
![alt text](image-9.png)  
- The grating is the same as below.  
![alt text](image-12.png)  
- sim plot is as below.  
![alt text](image-10.png)  
- The result of ez is like this.  
![alt text](image-11.png)  
- code is in  QCL_Lab_723.py  
---
### 7.24
- Try to reappear the metal-metal waveguide with gold.  
- Set up source as continuous source and will end at 10s.  
- The parameter of material is set as follows, using the drude model.  
~~~python
Au = mp.Medium(
    epsilon=1.0,
    E_susceptibilities=[
        mp.DrudeSusceptibility(
            frequency=5.0,
            gamma=0.5,    
            sigma=1.0)])

# N = 5e18
# n_GaAs = mp.Medium(epsilon=12.25)
n_GaAs = mp.Medium(
    epsilon=10.9,
    E_susceptibilities=[
        mp.DrudeSusceptibility(frequency=0.44, gamma=0.033, sigma=1.0)])


# N = 5e15 低参杂
light_GaAs = mp.Medium(epsilon=12.25)
# light_GaAs = mp.Medium(
#     epsilon=12.25,
#     E_susceptibilities=[
#         mp.DrudeSusceptibility(frequency=0.062, gamma=0.0033, sigma=1.0)])

nplus_GaAs = mp.Medium(
    epsilon=10.9,  
    E_susceptibilities=[
        mp.DrudeSusceptibility(
            frequency=0.1967,   # Plasma resonant frequency
            gamma=0.0333,       # damping constant
            sigma=1.0           # conductivity
        )])
~~~
- Result is as follows.    
![alt text](image-14.png)   
- The frequency of source is set as 5THz.  
- Code is in the **Metal-metal_wg_0724.py**.  
---
### 7.25
- Recalculate the parameter of drude model for there is something wrong in the previous version.
- Code is in the **calculate_drude.py**.
~~~python
# Au = mp.Medium(
#     epsilon=1.0,
#     E_susceptibilities=[
#         mp.DrudeSusceptibility(
#             frequency=5.0,
#             gamma=0.5,    
#             sigma=1.0)])

# N = 5e18 /cm3
# n_GaAs = mp.Medium(epsilon=12.25)
n_GaAs = mp.Medium(
    epsilon=10.9,
    E_susceptibilities=[
        mp.DrudeSusceptibility(frequency=1.62, 
                               gamma=0.033, 
                               sigma=1.0)])


# N = 5e15 /cm3
# light_GaAs = mp.Medium(epsilon=12.25)
light_GaAs = mp.Medium(
    epsilon=12.25,
    E_susceptibilities=[
        mp.DrudeSusceptibility(frequency=0.0513, 
                               gamma=0.0033, 
                               sigma=1.0)])

# N = 1e18 /cm3
nplus_GaAs = mp.Medium(
    epsilon=10.9,  
    E_susceptibilities=[
        mp.DrudeSusceptibility(
            frequency=0.7252,   # Plasma resonant frequency
            gamma=0.0333,       # damping constant
            sigma=1.0           # conductivity
        )
    ]
)
~~~
- Simulation code is in the **MM_wg_modified_0725.py**.
- You can also see the result in **MM_wg_modified_0725.ipynb**.
- Introduction of the code is in the **Intro_MM_0725.md**.
---
### 7.29
- Try the code **holey-wvg-cavity.py**.  
- Modify the parameter to sx = 70 and frequency = 1e12, it will output transmission as 0.
- The structure is using the a periodic sequence.    
- Figure is showing when sx = 60 and material is using the default material(epislon = 13).  
![alt text](image-16.png)  
- The materials is using the default config as blk.  
- Next step will try other kinds of materials.
---
### 7.31
- Cancel the symmetries in simulation lead to no difference.  
- Try using the material set up by ourselves.  
- From the config in the official code **holey-wvg-cavity.py**, I find that the source component should be set up as Ex direction.  
- So that I run the **MM_wg_modified_0725.py** again with new source and the result is below.  
![alt text](image-18.png)
- Compare to the result before, the edge of the material change point is more sharp but there is no decay in the middle of the curve.  
- Try to stimulate the source from 3 directions, and the result of 10 is like below.  
![alt text](image-20.png) ![alt text](image-21.png)![alt text](image-22.png)
---
### 8.01
- Try the waveguide without any holes and material epislon is 13, flux is plot in the figure below.  
![alt text](image-26.png)![alt text](image-19.png)
- The result with air is almost the same.  
![alt text](image-31.png)![alt text](image-32.png)

- As to the mode intensity, the material epislon is 13 and result is like the figure below.  
![alt text](image-33.png)![alt text](image-34.png)![alt text](image-35.png)

- The result with air（epsilon = 1） is almost the same.  
![alt text](image-27.png)![alt text](image-28.png)![alt text](image-29.png)![alt text](image-30.png)
---