import common

class Sample:
	def __init__(self, thickness, density, compound, chi):
		'''' Sample with thickness in cm, density in g/cm^3 
		     compound as a string and sample angle chi in degrees '''
		self.thickness = thickness
		self.density = density
		self.stoichiometry = common.strtoz(compound)
		self.chi = chi
