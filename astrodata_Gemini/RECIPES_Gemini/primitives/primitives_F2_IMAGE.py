from astrodata import AstroData
from astrodata.adutils import gemLog
from astrodata.ConfigSpace import lookup_path
from gempy import geminiTools as gt
from gempy.science import standardization as sdz
from primitives_F2 import F2Primitives

class F2_IMAGEPrimitives(F2Primitives):
    """
    This is the class containing all of the primitives for the F2_IMAGE
    level of the type hierarchy tree. It inherits all the primitives from the
    level above, 'F2Primitives'.
    """
    astrotype = "F2_IMAGE"
    
    def init(self, rc):
        F2Primitives.init(self, rc)
        return rc
