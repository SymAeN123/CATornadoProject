# California Tornado Project

## Code Documentation

#### `downloader.py`

This is a file which connects to Amazon's s3 dataset and downloads radar files. It provides one main function, `download_radar_data`. This function accepts four arguments:

1. `site`: A string which reperesents a radar site.

2. `begin`: A naive datetime object in UTC time which represents the start date and time of radar data to get.

3. `end`: A naive datetime object in UTC time which represents the end date and time of radar data to get.

4. `abs_path`: A string which is the absolute pathname to the directory in which to download radar files. If left empty, it will download the files into the cwd.

This file will find the radar file nearest to the `begin` and `end` times and download inclusively all the files between.

#### `case_downloader.py`

This is a wrapper around the `downloader.py` file which has the goal of parsing through a [storm events database](https://www.ncdc.noaa.gov/stormevents/choosedates.jsp?statefips=6,CALIFORNIA) search CSV. It requires a `cases` folder, in which it is capable of creating a new folder for a given case and downloading selected radar sites. It also requires a `spreadsheets` folder where it can read a given CSV. It will display all cases found in the target CSV which do not already have a folder with radar data.