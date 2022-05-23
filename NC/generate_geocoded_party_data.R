
library(tidyverse)

geocoded_burke_county1 <- read_csv("geocoded_burke_county1.csv")
geocoded_burke_county2 <- read_csv("geocoded_burke_county2.csv")
geocoded_burke_county3 <- read_csv("geocoded_burke_county3.csv")
geocoded_burke_county4 <- read_csv("geocoded_burke_county4.csv")
geocoded_burke_county5 <- read_csv("geocoded_burke_county5.csv")
geocoded_burke_county6 <- read_csv("geocoded_burke_county6.csv")


geocoded_burke_county <- bind_rows(bind_rows(bind_rows(bind_rows(bind_rows(geocoded_burke_county1, geocoded_burke_county2),
               geocoded_burke_county3), geocoded_burke_county4),
               geocoded_burke_county5), geocoded_burke_county6)

raw <- read.table("ncvoter12.txt", header=TRUE) %>%
  select("voter_reg_num", "party_cd")



geocoded_burke_county <- left_join(geocoded_burke_county, raw, by = "voter_reg_num") %>%
  mutate(party_cd=recode(party_cd, 
                        `DEM`= 0,
                        `LIB`= 1,
                        `REP`= 2,
                        `UNA`= 3)) %>%
  select("race_id", "party_cd", "voter_lat", "voter_long", "precinct_id",
         "precinct_lat", "precinct_long", "precinct_abbrv")


write_csv(geocoded_burke_county, "geocoded_burke_county_clean.csv")

