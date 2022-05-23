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

precinct_geocoded <- read_csv("precinct_dataset_lat_long.csv")

raw <- read.table("ncvoter12.txt", header=TRUE) %>%
  filter(voter_status_reason_desc != "DECEASED") %>%
  filter(voter_status_desc == "ACTIVE") %>%
  select(voter_reg_num, race_code, precinct_abbrv,precinct_desc, res_street_address, res_city_desc, state_cd, zip_code) %>%
  #left_join(precinct_dataset,by="precinct_abbrv", all = TRUE, copy = TRUE) %>%
  mutate(race_id=recode(race_code, 
                        `A`= 0,
                        `B`= 1,
                        `I`= 2,
                        `M`= 3,
                        `O`= 4,
                        `U`= 5,
                        `W`= 6))


raw_full <- merge(raw, precinct_geocoded, by = "precinct_abbrv")

# race code
g <- ggplot(raw, aes(race_code)) 
g + geom_bar()


# precincts
g <- ggplot(raw, aes(precinct_abbrv)) 
g + geom_bar()

mini_raw = head(raw)

# Perform geocoding
geocoded_data <- run_geocoder(
  voter_file = raw_full[50001:51328,],
  geocoder = "census",
  parallel = TRUE,
  voter_id = "voter_reg_num",
  street = "res_street_address",
  city = "res_city_desc",
  state = "state_cd",
  zipcode = "zip_code",
  country = "US",
  census_return = "locations",
  census_benchmark = "Public_AR_Current",
  census_output = "simple",
  census_class = "sf",
  census_vintage = 4,
  opencage_key = NULL
)


geocoded_data <- geocoded_data %>%
       mutate(voter_lat = unlist(map(geocoded_data$geometry,2)),
                           voter_long = unlist(map(geocoded_data$geometry,1)))


write_csv(geocoded_data, "geocoded_burke_county.csv")