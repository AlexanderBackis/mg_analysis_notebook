#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
energy_calculation.py: Tools to calculate energy.
"""

import numpy as np
from mg.helper_functions.mapping import create_mapping

# =============================================================================
#                                 CALCULATE ENERGY
# =============================================================================

def get_energies(df, distance_offset=0):
    """
    Calculates the energy transfer of a data set.

    Args:
        df (DataFrame): Clustered events

    Returns:
        DeltaE (float): Energy transfer in meV
    """
    # Declare necessary constants, neutron mass in [kg]
    origin_voxel = [1, 88, 40]
    NEUTRON_MASS = 1.674927351e-27
    JOULE_TO_meV = 6.24150913e18 * 1000
    time_offset = 0.6e-3
    period_time = (1/14)
    # Get chopper-to-detector distance for each voxel
    distance_mapping = get_distances(origin_voxel, distance_offset)
    # Extract necessary values from dataframe
    wChs = df.wch
    gChs = df.gch
    buses = df.bus
    ToF = (df.tof * 62.5e-9 + time_offset) % period_time
    d = distance_mapping[buses, gChs, wChs]
    # Calculate energy Ef of detected neutron
    energy = ((NEUTRON_MASS/2) * ((d/ToF) ** 2)) * JOULE_TO_meV

    #indices = (energy > 10.6) & (energy < 10.8)
    #print(max(ToF[indices]*1e6))
    #print(min(ToF[indices]*1e6))
    return energy.values



# =============================================================================
#                           VOXEL DISTANCES 3D MATRIX
# =============================================================================

def get_distances(origin_voxel, distance_offset):
    """
    Calculates the distances to each of the voxels from the sample.

    Returns:
        distances (numpy array): 3D matrix where the axises are bus, gCh and wCh.
                                 The elements are the distances in m from the
                                 sample position.
    """
    mapping = create_mapping(origin_voxel, distance_offset)
    distances = np.zeros((3, 120, 80), dtype='float')
    for bus in range(0, 3):
        for gCh in range(80, 120):
            for wCh in range(0, 80):
                coordinate = mapping[bus, gCh, wCh]
                x = coordinate['x']
                y = coordinate['y']
                z = coordinate['z']
                distances[bus, gCh, wCh] = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    return distances
