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
# 1/f = (Rd*3)*(4*pi*Nd/3)*(rho'*Re*Pr)/(St*Nu_wall)
#
# The non-dimensional value of Rd is calculated using:
#
# Rd = 0.4251*psi*sqrt(2*Bo), where: psi - static contact angle in radians
#
# See Equation 39 in:
#
# Han Chi-Yeh, Peter Griffith,
# The mechanism of heat transfer in nucleate pool boiling—Part I: Bubble initiaton, growth and departure,
# International Journal of Heat and Mass Transfer,
# Volume 8, Issue 6, 1965, Pages 887-904, ISSN 0017-9310,
# https://doi.org/10.1016/0017-9310(65)90073-6
#
# The growth and wait time can be calculated as:
#
# t_growth = (1/4)*(1/f)
# t_wait   = (3/4)*(1/f)
#
# Using empirical assumptions from Equation 44 in:
#
# Xiao, L.; Zhuang, Y.; Wu, X.; Yang, J.; Lu, Y.; Liu, Y.;
# Han, X. A Review of Pool-Boiling Processes Based on Bubble-Dynamics Parameters.
# Appl. Sci. 2023, 13, 12026. https://doi.org/10.3390/app132112026

import numpy
import toml

# Load flash.toml to get parameters
params = toml.load("flash.toml")

# Fluid parameters
Re = 1./params["IncompNS"]["ins_invReynolds"]
Pr = params["HeatAD"]["ht_Prandtl"]
St = params["Multiphase"]["mph_Stefan"]
rhoGas = params["Multiphase"]["mph_rhoGas"]
Bo = params["Multiphase"]["mph_invWeber"]/numpy.sqrt(params["IncompNS"]["ins_gravX"]**2)
psi = (45./180)*numpy.pi

# Heurisitc assignment of site density
maxSiteDensity = 6.

# Non-dimensional critical heat flux
heatFluxCHF = 56.

# Set heat flux ratio and compute heat flux
heatFluxRatio = .2275
heatFlux = heatFluxRatio*heatFluxCHF

# Compute 2D and 3D heater areas
heaterArea2D = (params["Grid"]["xmax"]-params["Grid"]["xmin"])
heaterArea3D = heaterArea2D*(params["Grid"]["zmax"]-params["Grid"]["zmin"])

# Linear scaling for site density to calculate numSites
siteDensity = heatFluxRatio*maxSiteDensity
numSites2D = siteDensity*heaterArea2D
numSites3D = siteDensity*heaterArea3D

# Calculate bubble departure radius
Rd = 0.4251*psi*numpy.sqrt(2*Bo)

# Calculation of depature, growth, and wait times
bubbleFrequency = (St*heatFlux)/(rhoGas*Re*Pr)/(4*siteDensity*numpy.pi/3)/(Rd**3)
nucWaitTime = (3./4)/bubbleFrequency
nucGrowthTime = (1./4)/bubbleFrequency

print(f"siteDensity: {round(siteDensity,1)}")
print(f"heatFlux:    {round(heatFlux,1)}")
print(f"nucWaitTime: {round(nucWaitTime,1)}")
print(f"numSites2D:  {int(numSites2D)}")
print(f"numSites3D:  {int(numSites3D)}")
