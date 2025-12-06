# Load packages
suppressPackageStartupMessages({
  library(tidyverse)
  library(lubridate)
})

#' Process Cruel Jewel 100 Aid Station Data
#' 
#' This script processes aid station data for the Cruel Jewel 100 race,
#' calculating expected arrival times based on distance and target finish time.
#' 
#' Author: Dan Spakowicz
#' Last modified: 2024

# Constants
RACE_CONSTANTS <- list(
  RACE_START = "2025-05-16 12:00:00",
  TIMEZONE = "EST",
  TARGET_HOURS = 36,
  TIME_OFFSET = 12  # Additional hours offset
)

#' Read and validate race data
#' @param file_path Path to the CSV file
#' @return Validated dataframe
read_race_data <- function(file_path) {
  if (!file.exists(file_path)) {
    stop("Error: Input file not found at ", file_path)
  }
  
  data <- try({
    read_csv(file_path, skip = 2, show_col_types = FALSE)
  })
  
  if (inherits(data, "try-error")) {
    stop("Error reading the CSV file: ", data)
  }
  
  required_cols <- c("Dist.from.Start")
  missing_cols <- setdiff(required_cols, names(data))
  
  if (length(missing_cols) > 0) {
    stop("Missing required columns: ", paste(missing_cols, collapse = ", "))
  }
  
  return(data)
}

#' Calculate race times
#' @param data Input dataframe with distance data
#' @param constants List of race constants
#' @return Dataframe with calculated times
calculate_race_times <- function(data, constants) {
  start_time <- as.POSIXct(
    constants$RACE_START,
    tz = constants$TIMEZONE
  )
  
  finish_time <- start_time + constants$TARGET_HOURS * 60 * 60
  
  data %>%
    mutate(
      # Calculate expected arrival time at each aid station
      Clock.Time = start_time +
        (Dist.from.Start / max(Dist.from.Start)) *
        (finish_time - start_time) +
        (constants$TIME_OFFSET * 60 * 60),
      
      # Calculate elapsed time from start
      Elapsed.Time = difftime(Clock.Time, start_time, units = "secs"),
      
      # Format times for readability
      Elapsed.Time = round(seconds_to_period(as.numeric(Elapsed.Time)), 0),
      Clock.Time = format(Clock.Time, "%H:%M:%S")
    )
}

#' Main execution function
main <- function() {
  # Input and output paths
  input_file <- "data/cruel-jewel100/Cruel-Jewel100_Aid.csv"
  output_file <- "data/cruel-jewel100/Cruel-Jewel100_Aid_edited.csv"
  
  # Process data
  tryCatch({
    # Read data
    cruel_jewel <- read_race_data(input_file)
    
    # Calculate times
    cruel_jewel <- calculate_race_times(cruel_jewel, RACE_CONSTANTS)
    
    # Save results
    write_csv(cruel_jewel, output_file)
    
    message("Processing completed successfully!")
    message("Output saved to: ", output_file)
    
  }, error = function(e) {
    stop("Error in processing: ", e$message)
  })
}

# Execute main function
main()

