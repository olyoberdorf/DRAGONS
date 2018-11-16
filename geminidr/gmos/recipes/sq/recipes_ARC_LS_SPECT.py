"""
Recipes available to data with tags ['GMOS', 'SPECT', 'LS'].
Default is "reduce".
"""
recipe_tags = set(['GMOS', 'SPECT', 'LS'])

def reduce(p):
    p.prepare()
    p.addDQ()
    p.addVAR(read_noise=True)
    p.overscanCorrect()
    #p.biasCorrect()
    p.ADUToElectrons()
    p.addVAR(poisson_noise=True)
    p.mosaicDetectors(tile=False, tile_all=True)
    p.determineWavelengthSolution()

default = reduce