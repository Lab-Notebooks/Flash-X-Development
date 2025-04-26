# Nucleation wait time formula calculated from the relationship t = Nd*E/q, where:
# Nd - Site density - number of sites per m**2
# E - Heat removed per bubble (4*pi/3)*hfg*(Rd**3), Rd is departure radius
# q - Wall heat flux
#
# After non-dimensionalization. The formula for twait comes out as:
#
# t = (pi*Nd)/6 * (rho'*Re*Pr)/(St*Nu_wall)

import numpy

heatFluxRatioCHF = 0.2
siteDensity = heatFluxRatioCHF*3.2
heaterArea = 161.
Re = 238
Pr = 8.4
St = 0.5
heatFlux = heatFluxRatioCHF*50
rhoGas = 0.0083

nucWaitTime = (numpy.pi / 6) * (siteDensity) * (rhoGas * Re * Pr) / (St * heatFlux)

print(f"nucWaitTime: {nucWaitTime}")
print(f"numSites : {siteDensity*heaterArea}")
print(f"heatFlux : {heatFlux}")
