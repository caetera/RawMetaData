# -*- coding: utf-8 -*-
import sys
from os import path, listdir, chdir
from FileRecord import record_from_file, SQLABase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

def recursiveListing(filepath, process_file):
    """
    Recorsively traverse filepath and process each file
    """
    for name in listdir(filepath):
        currentpath = path.join(filepath, name)
        if path.isdir(currentpath):
            print("Entering folder: {}".format(currentpath))
            recursiveListing(currentpath, process_file)
        elif name.lower().endswith("raw"):
            process_file(currentpath)

def process_path(dirpath, outputfile):
    """
    Main function
    """
    if not path.exists(dirpath):
        print("Path does not exist!")
        return 1
    
    if not path.isdir(dirpath):
        print("Path is not folder")
        return 1
    
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

if __name__ == "__main__":
    start = datetime.now()
    process_path(sys.argv[1], sys.argv[2])
    end = datetime.now()
    print("Start: {}; End: {}; Duration: {}".format(start, end, end - start))