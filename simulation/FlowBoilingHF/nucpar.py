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
nucSeedRadius = params["Heater"]["htr_nucSeedRadius"]

# Scaling of nucleation site density
maxSiteDensity = 6.

# Non-dimensional critical heat flux
heatFluxCHF = 56.

# Set heat flux ratio and compute heat flux
heatFluxRatio = 0.9628
heatFlux = heatFluxRatio*heatFluxCHF

# Compute 2D and 3D heater areas
heaterArea2D = (params["Grid"]["xmax"]-params["Grid"]["xmin"])
heaterArea3D = heaterArea2D*(params["Grid"]["zmax"]-params["Grid"]["zmin"])

# Linear scaling for site density to calculate numSites
siteDensity2D = heatFluxRatio*maxSiteDensity*(numpy.pi*1e-1/2)*(1e-1/nucSeedRadius)
siteDensity3D = heatFluxRatio*maxSiteDensity*(1e-1/nucSeedRadius)**2

numSites2D = siteDensity2D*heaterArea2D
numSites3D = siteDensity3D*heaterArea3D

# Calculate contact angles
rcdAngle = 45.
advAngle = rcdAngle + heatFluxRatio*75.

# Calculate bubble departure radius
Rd = 0.4251*(rcdAngle*numpy.pi/180.)*numpy.sqrt(2*Bo)

# Calculation of depature, growth, and wait times
bubbleFrequency = (St*heatFlux)/(rhoGas*Re*Pr)/(4*siteDensity3D*numpy.pi/3)/(Rd**3)
nucWaitTime = (3./4)/bubbleFrequency
nucGrowthTime = (1./4)/bubbleFrequency

print(f"siteDensity:   {round(siteDensity3D,1)}")
print(f"heatFlux:      {round(heatFlux,1)}")
print(f"nucWaitTime:   {round(nucWaitTime,1)}")
print(f"nucGrowthTime: {round(nucGrowthTime,1)}")
print(f"numSites2D:    {int(numSites2D)}")
print(f"numSites3D:    {int(numSites3D)}")
print(f"rcdAngle:      {round(rcdAngle,1)}")
print(f"advAngle:      {round(advAngle,1)}")
