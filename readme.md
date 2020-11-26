# Description

This script recursively travels through the provided path, collects metadata from Thermo Raw files and stores them in SQL database.

This software is using RawFileReader reading tool. Copyright © 2016 by Thermo Fisher Scientific, Inc. All rights reserved

Main (exectuable) script is `Process.py`;  `FileRecord.py` contains classes and functions to work with records (i.e. structured information) of Thero Raw files;
`Method.py` contains function to extract instrument method infromation from Thermo Raw files; `parameter_table.csv` contains a table that can be used to customize
some part of the information to be extracted from Thermo Raw files; `ParameterBuilder.py` is a helper script, that is used to make a draft of `parameter_table.csv`.

## Parameter table format

Parameter table is a regular CSV file with header. Each line corresponds to the piece of information that can be obtained from Raw file. Usually, only the `Active` column has to be edited.

Column description:

* Field - name for the property in FileRecord; the same name will be used as a column in the resulting DB. Has to be unique.

* Location - logical path for the location of the corresponding information in Thermo Raw file. For example, `FileHeader|FileType` means that the value to be obtained is `FileType` property of `FileHeader` structure in Raw file. Danger! Should be edited with care.

* Type - type of the data for the corresponding column in DB. 

* Active - boolean flag, that indicates if this field has to be extracted.

# Usage

    Process.py [subcommand] [Path to process] [Path to SQLite DB file]

Two subcommands are supported:

* `build` create database from scratch
* `update` rescans the path and updates database with the information from the files that are either not present or had error
