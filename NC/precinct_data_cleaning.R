library(tidyverse)
library(eiCompare)
library(stringr)
library(tidyverse)
library(tigris)
library(tidyr)
library(foreach)
library(parallel)
library(doParallel)
library(data.table)
library(plyr)
library(censusxy)
library(sf)
library(leaflet)
library(readxl)

# GEOCODE PRECINT
precinct_dataset <- read_excel("precinct_info.xlsx")

# convert dataframe into a tibble
precinct_dataset <- as_tibble(precinct_dataset)

# Perform geocoding
precinct_geocoded <- run_geocoder(
  voter_file = precinct_dataset,
  geocoder = "census",
  parallel = TRUE,
  voter_id = "precinct_abbrv",
  street = "p_street_address",
  city = "p_city",
  state = "p_state",
  zipcode = "p_zipcode",
  country = "US",
  census_return = "locations",
  census_benchmark = "Public_AR_Current",
  census_output = "simple",
  census_class = "sf",
  census_vintage = 4,
  opencage_key = NULL
)


precinct_geocoded <- precinct_geocoded %>%
  mutate(precinct_lat = unlist(map(precinct_geocoded$geometry,2)),
         precinct_long = unlist(map(precinct_geocoded$geometry,1)))

write_csv(precinct_geocoded, "precinct_dataset_lat_long.csv"