import shapely.geometry as sgeom
from shapely.prepared import prep
import cartopy.crs    

def _rings_to_multi_polygon(self, rings, is_ccw):
        exterior_rings = []
        interior_rings = []
        for ring in rings:
            if ring.is_ccw != is_ccw:
                interior_rings.append(ring)
            else:
                exterior_rings.append(ring)

        polygon_bits = []

        # Turn all the exterior rings into polygon definitions,
        # "slurping up" any interior rings they contain.
        for exterior_ring in exterior_rings:
            polygon = sgeom.Polygon(exterior_ring)
            prep_polygon = prep(polygon)
            holes = []
            for interior_ring in interior_rings[:]:
                if prep_polygon.contains(interior_ring):
                    holes.append(interior_ring)
                    interior_rings.remove(interior_ring)
                elif polygon.crosses(interior_ring):
                    # Likely that we have an invalid geometry such as
                    # that from #509 or #537.
                    holes.append(interior_ring)
                    interior_rings.remove(interior_ring)
            polygon_bits.append((exterior_ring.coords,
                                 [ring.coords for ring in holes]))

        # Ignore leftover rings rather than trying to fix them

        if polygon_bits:
            multi_poly = sgeom.MultiPolygon(polygon_bits)
        else:
            multi_poly = sgeom.MultiPolygon()
        return multi_poly

def monkey_patch_cartopy():
    cartopy.crs.Projection._rings_to_multi_polygon = _rings_to_multi_polygon
