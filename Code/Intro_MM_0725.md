📄 Simulation Report: THz Wave Propagation in Multi-Layer GaAs/Au Structure using Meep  
---
✅ Objective  
To simulate the electromagnetic wave propagation through a layered structure consisting of  

- Gold (Au)  
- Heavily doped GaAs (n-GaAs)  
- Lightly doped GaAs (light-GaAs)  

To evaluate the mode intensity profile (|Ez|²) and the corresponding dielectric profile (Re{ε}) across the structure under a 5 THz excitation. 

---
🛠️ Simulation Setup  
- Software: Meep (Python API)  
    - Resolution: 50 pixels/μm  
    - Simulation dimensions: Initially defined as 2D, but the structure is essentially 1D (along x-axis).  
    - Cell size:  
        - x: 13 μm (covers all layers)  
        - y: 0 μm (ignored in 1D setup)  
        - z: 5 μm (used for vertical injection, may be irrelevant in 1D)  

---
🧱 Materials  
- Au (Gold)  
    - Imported from meep.materials.Au (preset frequency-dependent model).  
- n-GaAs (Heavily Doped)  
     - Modeled using a Drude dispersion:  
     - ε∞ = 10.9  
     - Plasma frequency = 1.62  
     - γ = 0.033  
     - σ = 1.0  
- Light-GaAs (Lightly Doped)  
     - Modeled using a Drude dispersion:   
     - ε∞ = 12.25  
     - Plasma frequency = 0.0513  
     - γ = 0.0033  
     - σ = 1.0  
- (Optional) n⁺-GaAs  
     - Defined but not used in current geometry.

---

🧱 Layered Geometry Configuration  
The structure is built symmetrically from left to right:  
 - Au layer: 1 μm  
 - n-GaAs: 0.1 μm  
 - light-GaAs: 10 μm  
 - n-GaAs: 0.1 μm  
 - Au layer: 1 μm  

Geometry is defined using mp.Block objects and dynamically constructed via add_layer() function.

---

🔊 Source Configuration
Source Type: Continuous wave (ContinuousSource)  
 - Central Frequency: 5 THz  
 - Bandwidth (fwidth): 0.5 THz  
 - Injection Direction: Along z (but simulation is 1D in x — needs adjustment)  
 - Component: Ez (out-of-plane electric field)

---

📈 Observation and Output  
Simulation runs iteratively in time steps: i = 10, 20, ..., 90 fs.  
- At each step:  
    - Extracts Ez field profile squared (|Ez|² / 2, i.e., time-averaged intensity).  
    - Extracts permittivity profile ε(x) using get_epsilon_point. 

---

📊 Visualization  
A plot is generated at each step:  
- Left Y-axis: Mode Intensity |Ez| (blue curve)  
- Right Y-axis: Re{ε} (green dashed curve)  
- X-axis: Distance (μm) along the propagation axis  