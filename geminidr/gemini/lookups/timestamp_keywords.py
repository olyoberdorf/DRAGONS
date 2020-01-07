timestamp_keys = {
    # Dictionary key is the name of the user level function (in alphabetical
    # order)
    # Dictionary value is the timestamp keyword that should be used when
    # writing a timestamp keyword to the header once the user level function
    # has completed
    "add": "ADD",
    "addDQ": "ADDDQ",
    "addIllumMaskToDQ": "ADILLMSK",
    "addMDF": "ADDMDF",
    "addObjectMaskToDQ": "ADOBJMSK",
    "addReferenceCatalog": "ADDRECAT",
    "addVAR": "ADDVAR",
    "ADUToElectrons": "ADUTOELE",
    "resampleToCommonFrame": "ALIGN",
    "applyDQPlane": "APLDQPLN",
    "applyQECorrection": "QECORR",
    "associateSky": "ASSOCSKY",
    "attachWavelengthSolution": "ATTWVSOL",
    "biasCorrect": "BIASCORR",
    "calculateSensitivity": "SENSFUNC",
    "correctBackgroundToReference": "CORRBG",
    "adjustWCSToReference": "CORRWCS",
    "cutFootprints": "CUTSFP",
    "darkCorrect" : "DARKCORR",
    "detectSources": "DETECSRC",
    "appwave": "APPWAVE",
    "determineDistortion": "FITCOORD",
    "determineWavelengthSolution": "WAVECAL",
    "determineAstrometricSolution": "ASTRMTRY",
    "dilateObjectMask": "DLOBJMSK",
    "distortionCorrect": "TRANSFRM",
    "divide": "DIVIDE",
    "extract1DSpectra": "EXTRACT",
    "findAcquisitionSlits": "FINDACQS",
    "findSourceApertures": "FINDAPER",
    "flatCorrect": "FLATCORR",
    "fluxCalibrate": "FLUXCAL",
    "fringeCorrect": "FRNGCORR",
    "linearizeSpectra": "LINEARZE",
    "makeBPM": "BPMASK",
    "makeFlat": "MAKEFLAT",
    "makeFringeFrame": "FRINGE",
    "makeIRAFCompatible": "IRAFCOMP",
    "measureBG": "MEASREBG",
    "measureIQ": "MEASREIQ",
    "measureCC": "MEASRECC",
    "mosaicDetectors": "MOSAIC",
    "multiply": "MULTIPLY",
    "nonlinearityCorrect": "LINCORR",
    "normalizeFlat": "NORMLIZE",
    "prepare": "PREPARE",
    "rejectCosmicRays": "REJECTCR",
    "removePatternNoise": "RMPTNNSE",
    "resampleToLinearCoords": "LINCOORD",
    "wcalResampleToLinearCoords": "LINCOORD",
    "scaleByExposureTime": "EXPSCALE",
    "scaleByIntensity": "SCALEINT",
    "separateSky": "SEPSKY",
    "skyCorrectFromSlit": "SKYCORR",
    "skyCorrectNodAndShuffle": "SKYCORR",
    "stackFrames": "STACKFRM",
    "stackSkyFrames": "STACKSKY",
    "standardizeObservatoryHeaders": "SDZHDRSG",
    "standardizeInstrumentHeaders": "SDZHDRSI",
    "standardizeStructure": "SDZSTRUC",
    "subtract": "SUBTRACT",
    "subtractOverscan": "SUBOVER",
    "subtractSky": "SUBSKY",
    "subtractSkyBackground": "SUBSKYBG",
    "thresholdFlatfield": "TRHFLAT",
    "tileArrays": "TILEARRY",
    "trimOverscan": "TRIMOVER",
    "traceFootprints": "TRACEFP",
    "validateData": "VALDATA",
    }
