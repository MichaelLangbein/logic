#%%
import numpy as np
import matplotlib.pyplot as plt
import rasterio as rio
import rasterio.features as riof
import rasterio.transform  as riot
from pyproj.transformer import Transformer
from pystac_client import Client
import os
import requests as req
from urllib.parse import urlparse
import json


#%% part -1: bbox
bbox = [
    11.213092803955078,
    48.06580565720895,
    11.300640106201172,
    48.09161057547795
]

#%% Part 0: directories
thisDir = os.getcwd()
assetDir = os.path.join(thisDir, 'assets')
osmDir = os.path.join(assetDir, 'osm')
s2Dir = os.path.join(assetDir, 's2')
os.makedirs(osmDir, exist_ok=True)
os.makedirs(s2Dir, exist_ok=True)


#%% Part 1: download S2 data

def downloadAndSaveS2(saveToDirPath, bbox, maxNrScenes=1, maxCloudCover=10, bands=None):
    catalog = Client.open("https://earth-search.aws.element84.com/v0")

    searchResults = catalog.search(
        collections=['sentinel-s2-l2a-cogs'],
        bbox=bbox,
        max_items=maxNrScenes,
        query={
            "eo:cloud_cover": { "lt": maxCloudCover },
            "sentinel:valid_cloud_cover": { "eq": True }  # we want to have the cloud mask in there, too.
        },
    )

    def shouldDownload(key, val):
        if not val.href.endswith('tif'):
            return False
        if bands is not None and key not in bands:
            return False
        return True

    def rioSaveTif(targetFilePath, data, crs, transform, noDataVal):
        h, w = data.shape
        options = {
            'driver': 'GTiff',
            'compress': 'lzw',
            'width': w,
            'height': h,
            'count': 1,
            'dtype': data.dtype,
            'crs': crs,
            'transform': transform,
            'nodata': noDataVal
        }
        with rio.open(targetFilePath, 'w', **options) as dst:
            dst.write(data, 1)

    #  downloading only bbox-subset
    fullData = {}
    for item in searchResults.get_items():
        itemData = {}
        for key, val in item.assets.items():
            if shouldDownload(key, val):
                with rio.open(val.href) as fh:
                    coordTransformer = Transformer.from_crs('EPSG:4326', fh.crs)
                    coordUpperLeft = coordTransformer.transform(bbox[3], bbox[0])
                    coordLowerRight = coordTransformer.transform(bbox[1], bbox[2])
                    pixelUpperLeft = fh.index( coordUpperLeft[0],  coordUpperLeft[1] )
                    pixelLowerRight = fh.index( coordLowerRight[0],  coordLowerRight[1] )
                    # make http range request only for bytes in window
                    window = rio.windows.Window.from_slices(
                        ( pixelUpperLeft[0],  pixelLowerRight[0] ),
                        ( pixelUpperLeft[1],  pixelLowerRight[1] )
                    )
                    print(f"Downloading {key} data ...")
                    subset = fh.read(1, window=window)
                    itemData[key] = subset

                url = urlparse(val.href)
                fileName = os.path.basename(url.path)
                targetDir = os.path.join(saveToDirPath, item.id)
                os.makedirs(targetDir, exist_ok=True)
                fullFilePath = os.path.join(targetDir, fileName)
                rioSaveTif(fullFilePath, subset, fh.crs, fh.transform, fh.nodata)

        fullData[item.id] = itemData
    return fullData


s2Data = downloadAndSaveS2(s2Dir, bbox, 1, 5, ["visual"])

# %% Part 2: download OSM data
# Tested with http://overpass-turbo.eu/#

def nodeToPoint(node):
    coordinates = [node["lon"], node["lat"]]
    properties = {key: val for key, val in node.items() if key not in ["type", "lon", "lat"]}
    point =  {
        "type": "Feature",
        "geometry" : {
            "type": "Point",
            "coordinates": coordinates,
            },
        "properties" : properties,
    }
    return point

def nodeToPoly(node):
    coordinates = [[[e["lon"], e["lat"]] for e in node["geometry"]]]
    properties = node["tags"]
    properties["id"] = node["id"]
    return {
        "type": "Feature",
        "geometry" : {
            "type": "Polygon",
            "coordinates": coordinates,
            },
        "properties" : properties,
    }

def osmToGeojson(data, saveFreeNodes=False):
    elements = data["elements"]

    ways =  [e for e in elements if e["type"] == "way"]
    polygons = [nodeToPoly(n) for n in ways]
    features = polygons

    if saveFreeNodes:
        nodes = [e for e in elements if e["type"] == "node"]
        freeNodes = []
        for node in nodes:
            isFreeNode = True
            for way in ways:
                if node["id"] in way["nodes"]:
                    isFreeNode = False
                    break
            if isFreeNode:
                freeNodes.append(node)
        freePoints = [nodeToPoint(n) for n in freeNodes]
        features += freePoints

    json = {
        "type": "FeatureCollection",
        "features": features
    }
    return json

def downloadAndSaveOSM(saveToDirPath, bbox, getBuildings=True, getTrees=True, getWater=True):
    overpass_url = "http://overpass-api.de/api/interpreter"

    stringifiedBbox = f"{bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]}"

    buildingQuery = f"""
        [out:json];     /* output in json format */
        way[building]( {stringifiedBbox} );
        (._;>;);        /* get the nodes that make up the ways  */
        out geom;
    """

    treesQuery = f"""
        [out:json];
        (
            way[landuse=forest]( {stringifiedBbox} );
            way[landuse=meadow]( {stringifiedBbox} );
            way[landuse=orchard]( {stringifiedBbox} );
        );              /* union of the above statements */
        (._;>;);
        out geom;
    """

    waterQuery = f"""
        [out:json];
        way[natural=water]( {stringifiedBbox} );
        (._;>;);
        out geom;
    """

    roadQuery = f"""
        [out:json];
        way[highway]( {stringifiedBbox} );
        (._;>;);
        out geom;
    """

    fullData = {}

    if getBuildings:
        response = req.get(overpass_url, params={'data': buildingQuery})
        data = response.json()
        geojson = osmToGeojson(data)
        filePath = os.path.join(saveToDirPath, 'buildings.geo.json')
        with open(filePath, 'w') as fh:
            json.dump(geojson, fh, indent=4)
        fullData["buildings"] = geojson

    if getTrees:
        response = req.get(overpass_url, params={'data': treesQuery})
        data = response.json()
        geojson = osmToGeojson(data)
        filePath = os.path.join(saveToDirPath, 'trees.geo.json')
        with open(filePath, 'w') as fh:
            json.dump(geojson, fh, indent=4)
        fullData["trees"] = geojson

    if getWater:
        response = req.get(overpass_url, params={'data': waterQuery})
        data = response.json()
        geojson = osmToGeojson(data)
        filePath = os.path.join(saveToDirPath, 'water.geo.json')
        with open(filePath, 'w') as fh:
            json.dump(geojson, fh, indent=4)
        fullData["water"] = geojson

    return fullData


osmData = downloadAndSaveOSM(osmDir, bbox)

# %%

def rasterizeGeojson(geojson, bbox, imgShape):
    """
    | a  b  c |    | scale  rot  transX |
    | d  e  f | =  | rot   scale transY |
    | 0  0  1 |    |  0      0     1    |

    Transformation
        from pixel coordinates of source
        to the coordinate system of the input shapes.
    See the transform property of dataset objects.
    """

    imgH, imgW = imgShape

    lonMin, latMin, lonMax, latMax = bbox
    scaleX = (lonMax - lonMin) / imgW
    transX = lonMin
    scaleY = -(latMax - latMin) / imgH
    transY = latMax

    # tMatrix = np.array([
    #     [scaleX, 0, transX],
    #     [0, scaleY, transY],
    #     [0, 0, 1]
    # ])
    # lon_tl, lat_tl, _ = tMatrix @ np.array([0, 0, 1])
    # lon_br, lat_br, _ = tMatrix @ np.array([imgH, imgW, 1])
    # assert(lon_tl == lonMin)
    # assert(lat_tl == latMax)
    # assert(lon_br == lonMax)
    # assert(lat_br == latMin)

    transform = riot.Affine(
        a=scaleX,  b=0,  c=transX,
        d=0,   e=scaleY,  f=transY
    )
    rasterized = riof.rasterize(
        [(f["geometry"], 1) for f in geojson["features"]],
        (imgH, imgW),
        all_touched=True,
        transform=transform
    )
    return rasterized

waterRasterized = rasterizeGeojson(osmData["water"], bbox, s2Data["S2B_32UPU_20230210_0_L2A"]["visual"].shape)
buildingsRasterized = rasterizeGeojson(osmData["buildings"], bbox, s2Data["S2B_32UPU_20230210_0_L2A"]["visual"].shape)
treesRasterized = rasterizeGeojson(osmData["trees"], bbox, s2Data["S2B_32UPU_20230210_0_L2A"]["visual"].shape)

# %%
fig, axes = plt.subplots(2, 1)
axes[0].imshow(s2Data["S2B_32UPU_20230210_0_L2A"]["visual"])
axes[1].imshow(treesRasterized + 2 * buildingsRasterized + 4 * waterRasterized)
# %%

