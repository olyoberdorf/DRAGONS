# This module defines a dict containing the coordinates of control pairs
# used to determine the amplitude of fringes in GMOS images. There is one
# entry for each set of CCDs, and the value is a tuple, where each
# item is a pair of tuples with (x,y) coordinates of the peak and trough
# of the fringe pattern. Coordinates are in terms of detector_section().
# The key is the detector_name(), i.e., the actual CCD chip names.
# Try to get 20 pairs across the instrument, covering all 3 CCDs in a
# fairly uniform manner.
control_pairs = {
    # GMOS-N EEV
    "EEV9273-16-03EEV9273-20-04EEV9273-20-03":
        ((( 997, 2724), (1117, 2724)),  # CCD1
         ((1312, 3570), (1309, 3666)),
         ((1480,  936), (1438, 1023)),
         ((1720, 4221), (1837, 4245)),
         ((1816, 1788), (1888, 1848)),
         ((2157,  735), (2250,  696)),  # Now CCD2
         ((2220, 4254), (2340, 4329)),
         ((2646, 1176), (2640, 1092)),
         ((2748, 1944), (2880, 1893)),
         ((2955, 3528), (2925, 3618)),
         ((2970, 3024), (2991, 3129)),
         ((3192, 1389), (3288, 1416)),
         ((3519, 2466), (3546, 2547)),
         ((3840, 3474), (3926, 3536)),
         ((3846, 1362), (3885, 1428)),
         ((3936, 2142), (3963, 2043)),
         ((4511,  462), (4571,  354)),  # Now CCD3
         ((4538, 1185), (4658, 1173)),
         ((4775, 4212), (4688, 4209)),
         ((5186, 2205), (5090, 2292))),
    # GMOS-S EEV
    "EEV2037-06-03EEV8194-19-04EEV8261-07-04":
        (((1500, 3524), (1422, 3470)),  # CCD1
         ((1668, 1364), (1670, 1448)),
         ((1802, 2200), (1852, 2204)),
         ((1856, 3352), (1913, 3336)),
         ((1880, 1344), (1922, 1280)),
         ((2248, 3060), (2282, 3034)),  # Now CCD2
         ((2250, 1398), (2178, 1344)),
         ((2416, 2114), (2448, 2108)),
         ((2584, 4380), (2655, 4377)),
         ((2814, 3134), (2808, 3082)),
         ((3138, 2724), (3148, 2680)),
         ((3342, 1918), (3410, 1922)),
         ((3398,  810), (3451,  806)),
         ((3481, 3346), (3473, 3301)),
         ((3846, 1734), (3904, 1757)),
         ((3918, 2500), (3948, 2504)),
         ((4270,  734), (4332,  776)),  # Now CCD3
         ((4482, 3210), (4464, 3296)),
         ((4678, 2004), (4718, 1996)),
         ((5096, 2168), (5106, 2244))),
    # GMOS-N e2v
    "e2v 10031-23-05,10031-01-03,10031-18-04":
        (((1701,  980), (1765,  968)),  # CCD1
         ((1717, 1384), (1771, 1392)),
         ((1913, 1764), (1893, 1848)),
         ((1945, 3800), (1949, 3708)),
         ((2488, 3048), (2512, 3144)),  # Now CCD2
         ((2508, 3420), (2488, 3332)),
         ((2564, 1844), (2600, 1700)),
         ((2535, 2607), (2499, 2622)),
         ((2572, 2148), (2592, 2285)),
         ((2624,  856), (2882,  836)),
         ((2796, 1350), (2752, 1352)),
         ((2952, 1984), (2892, 1936)),
         ((3186,  346), (3142,  342)),
         ((3540, 3171), (3624, 3183)),
         ((3560, 1636), (3508, 1648)),
         ((3838, 2222), (3878, 2230)),
         ((3792, 4232), (3720, 4196)),
         ((4347, 1248), (4447, 1260)),  # Now CCD3
         ((4471, 2212), (4527, 2206)),
         ((4559, 1970), (4500, 1970))),
    # GMOS-S Hamamatsu
    "BI5-36-4k-2,BI11-33-4k-1,BI12-34-4k-1":
        (((1285, 1766), (1325, 1777)),  # CCD1
         ((1473, 2822), (1517, 2766)),
         ((1519, 1874), (1527, 1814)),
         ((1867, 1970), (1895, 2020)),
         ((1963, 3336), (1973, 3400)),
         ((2527, 3488), (2611, 3448)),  # Now CCD2
         ((2583, 2650), (2587, 2681)),
         ((2668, 3530), (2620, 3454)),
         ((2706, 2212), (2716, 2253)),
         ((2782,  603), (2833,  574)),
         ((2995, 4027), (3031, 4050)),
         ((3024, 1132), (3060, 1134)),
         ((3056, 3638), (2998, 3636)),
         ((3398, 1361), (3473, 1402)),
         ((3535, 2993), (3673, 3006)),
         ((3555,  725), (3574,  765)),
         ((3726, 1580), (3820, 1608)),
         ((3750, 1950), (3750, 2006)),
         ((4462,  947), (4507,  893)),  # Now CCD3
         ((4681, 1448), (4755, 1442))),
    # GMOS-N Hamamatsu
    "BI13-20-4k-1,BI12-09-4k-2,BI13-18-4k-2":
        (((1582, 3800), (1615, 3822)),  # CCD1
         ((1734, 1743), (1759, 1710)),
         ((1938, 1782), (1915, 1770)),
         ((2307, 3711), (2256, 3750)),  # Now CCD2
         ((2321,  681), (2353,  615)),
         ((2334, 3900), (2327, 3891)),
         ((2454, 2139), (2526, 2127)),
         ((2676, 1617), (2682, 1686)),
         ((2955, 2682), (2886, 2691)),
         ((3165, 1560), (3066, 1560)),
         ((3278, 3483), (3294, 3513)),
         ((3366, 2496), (3370, 2436)),
         ((3534, 1572), (3468, 1554)),
         ((3849,  645), (3967,  657)),
         ((3894, 3243), (3948, 3297)),
         ((4050, 1761), (3960, 1776)),
         ((4226, 3258), (4262, 3201)),  # Now CCD3
         ((4382, 1800), (4434, 1782)),
         ((4763, 1578), (4766, 1539)),
         ((4868, 1914), (4928, 1908))),
}