# Descriptor Index Rules
# (1) file must beging with "calculatorIndex." and end in ".py"
# (2) the dictionary set must be named "calculatorIndex"
# (3) both the key and value should be strings
# (4) the key is an AstroDataType, the value is the name of the object
#       to use as the calculator for that type
# (5) the value should have the form <module name>.<calculator class name>
# (6) the "descriptors" subdirectory and all subdirectories of it are added to import path
# (7) when the calculator is needed the Descriptor system execs "import <module name>"
#       and gets the object by "eval <module name>.<calculator class name>"
# (8) indexes may not conflict in the type names, but otherwise can be distributed
#       however one likes in the directory structure. Also, multiple calculators
#       can be defined in the same module... i.e. we could have a single giant
#       index and single giant calculator .py file, but that would be a mess.

calculatorIndex = {
    "FLAMINGOS2_RAW":"FLAMINGOS2_RAWDescriptor.FLAMINGOS2_RAWDescriptorCalc()",
    "GMOS_RAW":"GMOS_RAWDescriptor.GMOS_RAWDescriptorCalc()",
    "GNIRS_RAW":"GNIRS_RAWDescriptor.GNIRS_RAWDescriptorCalc()",
    "MICHELLE_RAW":"MICHELLE_RAWDescriptor.MICHELLE_RAWDescriptorCalc()",
    "NICI_RAW":"NICI_RAWDescriptor.NICI_RAWDescriptorCalc()",
    "NIFS_RAW":"NIFS_RAWDescriptor.NIFS_RAWDescriptorCalc()",
    "NIRI_RAW":"NIRI_RAWDescriptor.NIRI_RAWDescriptorCalc()",
    "TRECS_RAW":"TRECS_RAWDescriptor.TRECS_RAWDescriptorCalc()",
    }
