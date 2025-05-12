# Load packages
library(tidyverse)
library(lubridate)

# Read in the data and skip the first 2 rows
cruel_jewel <- read_csv("data/cruel-jewel100/Cruel-Jewel100_Aid.csv", skip = 2)

# Set the start time to noon on Friday, May 16, 2025 on the east coast of the US
start_time <- as.POSIXct("2025-05-16 12:00:00", tz = "EST")

# Finish time is 36 hours later
finish_time <- start_time + 36 * 60 * 60

# Create a sequence of times from start_time to finish_time using the distances in Dist.from.Start
cruel_jewel <- cruel_jewel %>%
  mutate(
    Clock.Time = start_time + (Dist.from.Start / max(Dist.from.Start)) * (finish_time - start_time),
  )

# Calculate the elapsed time 
cruel_jewel <- cruel_jewel %>%
  mutate(
    Elapsed.Time = difftime(Clock.Time, start_time, units = "secs")
  )

# Round Elapsed.Time and convert Clock.Time to H:M:S format 
cruel_jewel <- cruel_jewel %>%
  mutate(
    Elapsed.Time = round(seconds_to_period(as.numeric(Elapsed.Time)), 0),
    Clock.Time = format(Clock.Time, "%H:%M:%S")
  )


write_csv(cruel_jewel, "data/cruel-jewel100/Cruel-Jewel100_Aid_edited.csv")

