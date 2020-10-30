#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from os import path, listdir, chdir
from FileRecord import record_from_file, SQLABase, FileRecord
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

def recursiveListing(filepath, process_file):
    """
    Recorsively walk filepath and apply process_file function to all RAW files
    """
    for name in listdir(filepath):
        currentpath = path.join(filepath, name)
        if path.isdir(currentpath):
            print("Entering folder: {}".format(currentpath))
            recursiveListing(currentpath, process_file)
        elif name.lower().endswith("raw"):
            process_file(currentpath)

def build_path(dirpath, outputfile):
    """
    Build function
    """
    #some checks
    if not path.exists(dirpath):
        print("Path does not exist!")
        return 1
    
    if not path.isdir(dirpath):
        print("Path is not folder")
        return 1
    
    #for now SQLite
    try:
        output = create_engine("sqlite:///{}".format(outputfile))
    except:
        print("Cannot create output file")
        return 1
    
    SQLABase.metadata.create_all(output)
    
    session = sessionmaker(bind=output)()
    
    def record_wrapper(filename):
        record = record_from_file(filename)
        session.add(record)
        session.commit()
    
    chdir(dirpath)
    recursiveListing(".", record_wrapper)

def update_path(dirpath, outputfile):
    """
    Update function
    """
    #some checks
    if not path.exists(dirpath):
        print("Path does not exist!")
        return 1
    
    if not path.isdir(dirpath):
        print("Path is not folder")
        return 1
    
    #for now SQLite
    try:
        output = create_engine("sqlite:///{}".format(outputfile))
    except:
        print("Cannot open output file")
        return 1
    
    session = sessionmaker(bind=output)()
    
    #create filelist of known files
    known_files = set([record.VDSPath for record in 
                   session.query(FileRecord.VDSPath).filter(FileRecord.Error != True)])
    error_files = set([record.VDSPath for record in 
                   session.query(FileRecord.VDSPath).filter(FileRecord.Error == True)])
     
    def record_wrapper(filename):
        if not filename in known_files:
            record = record_from_file(filename)
            if filename in error_files:
                print("{} is error".format(filename))
                session.query(FileRecord).filter(FileRecord.VDSPath == filename).delete()
            else:
                print("{} is new".format(filename))
                
            session.add(record)
            session.commit()
        
        else:
            print("{} is known".format(filename))
    
    chdir(dirpath)
    recursiveListing(".", record_wrapper)


if __name__ == "__main__":
    if len(sys.argv) > 3:
        start = datetime.now()
        if sys.argv[1].lower() == "build":
            build_path(sys.argv[2], sys.argv[3])
        elif sys.argv[1].lower() == "update":
            update_path(sys.argv[2], sys.argv[3])
        else:
            print("Unknown subcommand: {}".format(sys.argv[1]))
        end = datetime.now()
        print("Start: {}; End: {}; Duration: {}".format(start, end, end - start))
    else:
        print("Usage: Process.py [subcommand] [Path to process] [SQLite database file]")