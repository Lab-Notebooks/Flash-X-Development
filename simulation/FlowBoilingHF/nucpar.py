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
maxSiteDensity = 6

# Non-dimensional critical heat flux and heater area
heatFluxCHF = 50
heaterArea = 161.0*1.0

# Linear scaling for heat flux and site density
heatFlux = heatFluxRatio*heatFluxCHF
siteDensity = heatFluxRatio*maxSiteDensity
numSites = siteDensity*heaterArea

# Calculation of depature, growth, and wait times
bubbleFrequency = (St*heatFlux)/(numpy.pi/6)/(siteDensity)/(rhoGas*Re*Pr)
nucWaitTime = (3./4)/bubbleFrequency
nucGrowthTime = (1./4)/bubbleFrequency

print(f"nucWaitTime: {nucWaitTime}")
print(f"numSites : {numSites}")
print(f"heatFlux : {heatFlux}")
