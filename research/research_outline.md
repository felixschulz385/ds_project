---
title: "Data Science Project: Research Outline"
author: Felix Schulz; Marvin Hoberg; Jan Besler
date: 17/10/22
---

# To-Do
- [] Outliers, invalid observations

# Epics
- As a municipality in Germany I want to be able to identify the best strategy for renewable energy adoption based on potential
  - In a dashboard, I want to be able to display a suitability score for solar and wind energy
    - Write download modules for each identified factor

# Factors on the spatial diffusion of wind energy

This sections discusses important model parameters.

### Macro
- Scaling (knowledge, factories, resource mobilization, legitimation) [@bentoSpatialDiffusionFormation2015]

### Micro
#### Positional suitability [@vanhaarenGISbasedWindFarm2011]
- Planning and physical constraints
  - Federal land with specific function (e.g. Bundeswehr grounds, National Parks)
  - Interference zones (e.g. airports, towns, radio masts)
  - Geological restrictions (e.g. soil, slopes, altitude)
- Value
  - Wind resources
    - DWD Try
    - ECMWF (±30kmx30km)
  - Transmission lines
  - Remoteness (distance to infrastructure)
  - Cost of land clearing (previous land cover)
- Secondary factors
  - Birds

#### Economic suitability
- Demand
  - Households/Inhabitants
  - Industry
- Logistics
  - Net centrality (internal/export) using OpenStreetMap net data
- Existing Supply
  - Other facilities

#### Additional ideas
- Political dimension
- Legal Dimension (lawsuits)

# Methodology

## Central ideas
- Placement model with prediction
- Matching model incorporating supply, demand and logistics

## Software
- Raster data: xdarray, rioxdarray
- OSM data: Pyrosm

# Literature