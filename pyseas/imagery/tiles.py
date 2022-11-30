"""Download tiles from a tile server then merge using gdal

Based on https://github.com/jimutt/tiles-to-tiff but extensively modified
"""
import glob
import logging
import os
import tempfile
import urllib.request
from math import atan, ceil, cos, degrees, floor, log, pi, radians, sinh, tan

from numpy import clip
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly


def latlonzoom_to_xy(lat, lon, z):
    eps = 2 ** -20
    lat = clip(lat, -90 + eps, 90 - eps)
    lon = clip(lon, -180, 180)
    tile_count = pow(2, z)
    x = (lon + 180) / 360
    rads = radians(lat)
    y = (1 - log(tan(rads) + 1 / cos(rads)) / pi) / 2
    return (
        clip(tile_count * x, 0, tile_count - 1),
        clip(tile_count * y, 0, tile_count - 1),
    )


def bbox_and_zoom_to_xy(lon_min, lon_max, lat_min, lat_max, zoom):
    x_min, y_max = latlonzoom_to_xy(lat_min, lon_min, zoom)
    x_max, y_min = latlonzoom_to_xy(lat_max, lon_max, zoom)
    return (floor(x_min), ceil(x_max), floor(y_min), ceil(y_max))


def x_to_lon_edges(x, z):
    tile_count = pow(2, z)
    unit = 360 / tile_count
    lon1 = -180 + x * unit
    lon2 = lon1 + unit
    return (lon1, lon2)


def mercator_y_to_lat(mercator_y):
    return degrees(atan(sinh(mercator_y)))


def y_to_lat_edges(y, zoom):
    tile_count = pow(2, zoom)
    unit = 1 / tile_count
    relative_y1 = y * unit
    relative_y2 = relative_y1 + unit
    lat1 = mercator_y_to_lat(pi * (1 - 2 * relative_y1))
    lat2 = mercator_y_to_lat(pi * (1 - 2 * relative_y2))
    return (lat1, lat2)


def tile_edges(x, y, zoom):
    lat1, lat2 = y_to_lat_edges(y, zoom)
    lon1, lon2 = x_to_lon_edges(x, zoom)
    return [lon1, lat1, lon2, lat2]


def georeference_raster_tile(x, y, zoom, path):
    bounds = tile_edges(x, y, zoom)
    filename, extension = os.path.splitext(path)
    gdal.Translate(filename + ".tiff", path, outputSRS="EPSG:4326", outputBounds=bounds)


def merge_tiles(input_pattern, output_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        vrt_path = temp_dir + "/tiles.vrt"
        gdal.BuildVRT(vrt_path, glob.glob(input_pattern))
        gdal.Translate(output_path, vrt_path)


class TileDownloader:
    """Downloads geographic tiles from a web server

    Args:
        server_url (str): template for server url. The x, y, and z (zoom)
            location should be included in the template using `{x}`, etc.
        headers (list[tuple[str, str]]], optional): headers needed for authentication
        max_tiles (int, optional): If your query would result in more than this
            number of tiles being downloaded, an error is raised.

    """

    def __init__(self, server_url, headers=None, max_tiles=64):
        self.server_url = server_url
        self.headers = headers
        self.max_tiles = max_tiles

    def check_tile_count(self, x_min, x_max, y_min, y_max):
        n_tiles = (x_max - x_min + 1) * (y_max - y_min + 1)
        if n_tiles > self.max_tiles:
            raise ValueError(
                f"requesting {n_tiles}, but max_tiles is {self.max_tiles}. "
                "increase max_tiles if you really want to do this"
            )
        return n_tiles

    def download_tile(self, x, y, zoom, destination):
        url = self.server_url.format(x=x, y=y, z=zoom)
        path = f"{destination}/download_{x}_{y}_{zoom}.png"
        opener = urllib.request.build_opener()
        if self.headers is not None:
            opener.addheaders = self.headers
        urllib.request.install_opener(opener)
        try:
            urllib.request.urlretrieve(url, path)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                # This is expected since not all tiles exist
                return None
            else:
                logging.error(f"failed to download {url} due to HTTPError({err.code})")
                raise
        else:
            return path

    def _compute_extent(self, gdal_img):
        gt = gdal_img.GetGeoTransform()
        proj = gdal_img.GetProjection()
        return (
            gt[0],
            gt[0] + gdal_img.RasterXSize * gt[1],
            gt[3] + gdal_img.RasterYSize * gt[5],
            gt[3],
        )

    def download(self, extent, zoom, path=None):
        x_min, x_max, y_min, y_max = bbox_and_zoom_to_xy(*extent, zoom)
        n_tiles = self.check_tile_count(x_min, x_max, y_min, y_max)

        with tempfile.TemporaryDirectory() as temp_dir:
            logging.info(f"Downloading {n_tiles} tiles")
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    logging.debug(f"downloading: {x},{y}")
                    png_path = self.download_tile(x, y, zoom, temp_dir)
                    if png_path is not None:
                        georeference_raster_tile(x, y, zoom, png_path)
            logging.info("Download complete")

            output_path = f"{temp_dir}/output.tiff" if (path is None) else path
            logging.info(f"Merging tiles to {output_path}")
            merge_tiles(f"{temp_dir}/download_*.tiff", output_path)
            logging.info("Computing extent")
            gdal_img = gdal.Open(output_path, GA_ReadOnly)
            extent = self._compute_extent(gdal_img)

            if path is None:
                data = gdal_img.ReadAsArray().transpose(1, 2, 0)
                return data, extent
            else:
                return extent
