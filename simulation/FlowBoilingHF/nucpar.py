# Nucleation wait time formula calculated from the relationship t_d = Nd*E/q, where:
# t_d - Bubble departure time
# Nd - Site density - number of sites per m**2
# E - Heat removed per bubble (4*pi/3)*hfg*(Rd**3), Rd is departure radius
# q - Wall heat flux
#
# After non-dimensionalization. The formula for twait comes out as:
#
# t_d = (pi*Nd)/6 * (rho'*Re*Pr)/(St*Nu_wall)
#
# t_growth = 3*t_d/4
# t_wait = t_d - t_growth = t_d/4

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
nucDepartureTime = (numpy.pi/6)*(siteDensity)*(rhoGas*Re*Pr)/(St*heatFlux)
nucGrowthTime = (3./4) * nucDepartureTime
nucWaitTime = nucDepartureTime - nucGrowthTime

print(f"nucWaitTime: {nucWaitTime}")
print(f"numSites : {numSites}")
print(f"heatFlux : {heatFlux}")
