"""
Created on Sun Apr 24 2022

@author: Debabrata Ghorai, Ph.D.

Closest point extraction between point and line.
"""

import sys

from pathlib import Path
from geobhumi.utils import reading_polyline, dist_calc
from geobhumi.ref_scripts import intersect_point_to_line
from geobhumi.config_entity import PointConfig, PolylineConfig


class FindNearestPoint:
    def __init__(self, pntconfig: PointConfig, plineconfig: PolylineConfig):
        self.pntconfig = pntconfig
        self.plineconfig = plineconfig
        self.point = self.pntconfig.single_point
        self.inline = self.plineconfig.inline

    def find_closest_point(self):
        _, nodes = reading_polyline(self.inline)
        # generate node pairs for close distance calculation
        node_pair = []
        for node in nodes:
            for i in range(len(node)-1):
                node_pair.append((node[i], node[i+1]))
        # near point identification
        min_dist = sys.maxsize  # a number that is bigger than all others
        nearest_pnt = None
        for i in node_pair:
            ln_start = i[0]
            ln_end = i[1]
            intersect_pnt = intersect_point_to_line(
                self.point, ln_start, ln_end)
            cur_dist = dist_calc(self.point, intersect_pnt)
            if cur_dist < min_dist:
                min_dist = cur_dist
                nearest_pnt = intersect_pnt
        return nearest_pnt


def get_nearest_point(point: str, ref_line_file: Path):
    pntconfig = PointConfig(
        single_point=point
    )
    plconfig = PolylineConfig(
        inline=ref_line_file
    )
    obj = FindNearestPoint(pntconfig=pntconfig, plineconfig=plconfig)
    res = obj.find_closest_point()
    return res
