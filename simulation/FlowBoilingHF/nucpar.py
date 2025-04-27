# Nucleation wait time formula calculated from the relationship 
# f  = q/(Nd*E), where:
#
# f  - Bubble frequency
# Nd - Site density, number of sites per m**2
# E  - Heat removed per bubble (4*pi/3)*rho_v*hfg*(Rd**3)
# Rd - Departure radius (capillary_length/2)
# q  - Wall heat flux
#
# See Equation 2 in:
#
# Basu, Nilanjana & Warrier, Gopinath & Dhir, V.K.. (2005).
# Wall Heat Flux Partitioning During Subcooled Flow Boiling: Part 1—Model Development.
# Journal of Heat Transfer-transactions of The Asme - J HEAT TRANSFER. 127. 10.1115/1.1842784.
#
# After non-dimensionalization:
#
# 1/f = (pi*Nd)/6*(rho'*Re*Pr)/(St*Nu_wall)
#
# Using empirical assumptions:
#
# t_growth = (1/4)*(1/f)
# t_wait   = (3/4)*(1/f)

import numpy
import toml

# Load flash.toml to get parameters
params = toml.load("flash.toml")

# Fluid parameters
Re = 1./params["IncompNS"]["ins_invReynolds"]
Pr = params["HeatAD"]["ht_Prandtl"]
St = params["Multiphase"]["mph_Stefan"]
rhoGas = params["Multiphase"]["mph_rhoGas"]

# Heurisitc assignment of site density
maxSiteDensity = 7.5

# Non-dimensional critical heat flux
heatFluxCHF = 60.

# Loop over each heater configuration to
# calculate num sites, and wait time
for key, info in params["Heater"].items():

    # Only do computations if info is of type dictionary.
    # This is where heater configuration is stored
    if type(info) == dict:

        # Read heat flux and compute heat flux ratio to CHF
        heatFlux = info["heatFlux"]
        heatFluxRatio = heatFlux/heatFluxCHF

        # Compute 2D and 3D heater areas
        heaterArea2D = (info["xmax"]-info["xmin"])
        heaterArea3D = heaterArea2D*(info["zmax"]-info["zmin"])

        # Linear scaling for site density to calculate numSites
        siteDensity = heatFluxRatio*maxSiteDensity
        numSites2D = siteDensity*heaterArea2D
        numSites3D = siteDensity*heaterArea3D

        # Calculation of depature, growth, and wait times
        bubbleFrequency = (St*heatFlux)/(numpy.pi/6)/(siteDensity)/(rhoGas*Re*Pr)
        nucWaitTime = (3./4)/bubbleFrequency
        nucGrowthTime = (1./4)/bubbleFrequency

        print(f"Heater.{key}.siteDensity:   {round(siteDensity,1)}")
        print(f"Heater.{key}.heatFluxRatio: {round(heatFluxRatio*100,1)}%")
        print(f"Heater.{key}.nucWaitTime:   {round(nucWaitTime,1)}")
        print(f"Heater.{key}.numSites2D:    {int(numSites2D)}")
        print(f"Heater.{key}.numSites3D:    {int(numSites3D)}")
        print("------------------------------------------------")
