# value of each land cover category
landcover_default_cat = {
    "Shrub land": 20,
    "Herbaceous vegetation": 30,
    "Agricultural land": 40,
    "Urban / built up": 50,
    "Bare / sparse vegetation": 60,
    "Snow and ice": 70,
    "Herbaceous wetland": 90,
    "Moss and lichen": 100,
}

land_use_criterias = {
    k: {"tooltip": 2, "layer": "land_cover", "header": "land_use", "content": "BINARY"}
    for k in landcover_default_cat
}

# list of the available constraints types. They will be used in the criterias names
criteria_types = {
    "land_use": "Land use constraints",
    "bio": "Biophysical constraints",
    "socio_eco": "Socio-economic constraints",
    "forest": "Forest change",
}

# list of the available constraint criteria
# the "header" describe the category of the concstraint
# the "layer" describe the layer to use
# the "content" how it should be used
# None for binary inputs
# dict for dropdown
# integer for the max of a range input
# the number of the "tooltip" text:
# 0: less than
# 1: more than
# 2 binary
criterias = {
    **land_use_criterias,
    "Annual rainfall": {
        "tooltip": 3,
        "layer": "annual_rainfall",
        "header": "bio",
        "content": "RANGE",
    },
    "Baseline water stress": {
        "tooltip": 3,
        "layer": "water_stress",
        "header": "bio",
        "content": "RANGE",
    },
    "Elevation": {
        "tooltip": 3,
        "layer": "elevation",
        "header": "bio",
        "content": "RANGE",
    },
    "Slope": {"tooltip": 3, "layer": "slope", "header": "bio", "content": "RANGE"},
    "Accessibility to cities": {
        "tooltip": 3,
        "layer": "city_access",
        "header": "socio_eco",
        "content": "RANGE",
    },
    "Population density": {
        "tooltip": 3,
        "layer": "population_density",
        "header": "socio_eco",
        "content": "RANGE",
    },
    "Protected areas": {
        "tooltip": 2,
        "layer": "protected_areas",
        "header": "socio_eco",
        "content": "BINARY",
    },
    "Property rights protection": {
        "tooltip": 3,
        "layer": "property_rights",
        "header": "socio_eco",
        "content": "RANGE",
    },
    "Deforestation rate": {
        "tooltip": 3,
        "layer": "deforestation_rate",
        "header": "forest",
        "content": "RANGE",
    },
    "Climate risk": {
        "tooltip": 3,
        "layer": "climate_risk",
        "header": "forest",
        "content": "RANGE",
    },
    "Natural regeneration variability": {
        "tooltip": 3,
        "layer": "natural_regeneration",
        "header": "forest",
        "content": "RANGE",
    },
    "Declining population": {
        "tooltip": 2,
        "layer": "declining_population",
        "header": "socio_eco",
        "content": "BINARY",
    },
}
