# Nucleation wait time formula calculated from the relationship 
# f  = q/(Nd*E), where:
#
# f  - Bubble frequency
# Nd - Site density, number of sites per m**2
# E  - Heat removed per bubble (4*pi/3)*hfg*(Rd**3), Rd is departure radius (lo/2)
# q  - Wall heat flux
#
# After non-dimensionalization:
#
# 1/f = (pi*Nd)/6 * (rho'*Re*Pr)/(St*Nu_wall)
#
# t_growth = (3/4)*(1/f)
# t_wait = 1/f - (3/4)*(1/f)

import numpy
import toml

# Heat flux ratio for each configuration
heatFluxRatio = 0.2

# Load flash.toml to get parameters
params = toml.load("flash.toml")

# Fluid parameters
Re = 1./params["IncompNS"]["ins_invReynolds"]
Pr = params["HeatAD"]["ht_Prandtl"]
St = params["Multiphase"]["mph_Stefan"]
rhoGas = params["Multiphase"]["mph_rhoGas"]

# Heurisitc assignment of site density
maxSiteDensity = 10

# Non-dimensional critical heat flux and heater area
heatFluxCHF = 50
heaterArea = 161.0*1.0

# Linear scaling for heat flux and site density
heatFlux = heatFluxRatio*heatFluxCHF
siteDensity = heatFluxRatio*maxSiteDensity
numSites = siteDensity*heaterArea

# Calculation of depature, growth, and wait times
bubbleFrequency = (St*heatFlux)/(numpy.pi/6)/(siteDensity)/(rhoGas*Re*Pr)
nucGrowthTime = (3./4)/bubbleFrequency
nucWaitTime = (1./4)/bubbleFrequency

print(f"nucWaitTime: {nucWaitTime}")
print(f"numSites : {numSites}")
print(f"heatFlux : {heatFlux}")
