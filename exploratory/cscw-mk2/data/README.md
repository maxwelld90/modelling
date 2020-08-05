# Data Directory (MkII)
Source data and output data lives in here. Everything is anonymised so there's no issue of people complaining here.

* `groups/` contains the group files for the three main conditions (single, with roles and without roles).
* `out/` contains output files. Any file with extension `.lpconfig` is a configuration file you can pass into the log processor. You should be able to obtain the exact same output with that script as is stored in this repository.

You also need the MongoDB instance `searchx-cikm`, which when loaded should weigh in at `0.267GB`. This is not stored in this repository. It's in your Google Drive, David (see `data/cscw/searchx-cikm.zip`)! Import the data with the `mongorestore` command. You should just be able to point to the unzipped directory and all will be well.