# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pandas import read_csv
from os import path
from datetime import datetime
import clr
clr.AddReference(path.abspath("RawFileReader/ThermoFisher.CommonCore.Data.dll"))
from ThermoFisher.CommonCore.Data.Business import RawFileReaderFactory
from Method import methods_from_raw

TypeMapping = {"Integer": Integer,
               "Float": Float,
               "String": String,
               "Text": Text,
               "DateTime": DateTime,
               "Boolean": Boolean}

def load_parameter_table(table_file):
    try:
        table = read_csv(table_file)
    except:
        raise ValueError("Cannot open table file: {}".format(table_file))
    
    return table[table["Active"]].copy()

def create_fields(table):
    """
    Populate fileds of FileRecord class
    """
    param_dict = {"__tablename__": "records",
                  "VDSPath": Column(String, primary_key=True),
                  "VDSFileName": Column(String),
                  "VDSSize": Column(Integer),
                  "VDSCreated": Column(DateTime),
                  "VDSAccessed": Column(DateTime),
                  "VDSModified": Column(DateTime),
                  "Error": Column(Boolean),
                  "ErrorText": Column(String),
                  "NumberOfMethods": Column(Integer),
                  "MethodNames": Column(String),
                  "MethodTexts": Column(Text)}
    
    table.apply(lambda row: param_dict.update(
                            {row["Field"]: 
                                Column(TypeMapping[row["Type"]])}),
                axis=1)
    
    return param_dict

SQLABase = declarative_base()

table = load_parameter_table("parameter_table.csv")

FileRecord = type("FileRecord", (SQLABase,), create_fields(table))

def update_record_from_row(row, record, raw):
    field_name = row["Field"]
    location = row["Location"].split("|")
    if field_name.endswith("Date"):#special case of .NET DateTime objects
        time = raw[location[0]].__getattribute__(location[1]).ToUniversalTime()
        value = datetime(time.Year, time.Month, time.Day, time.Hour, time.Minute,
                         time.Second, time.Millisecond * 1000)
    else:
        value = raw[location[0]].__getattribute__(location[1])
    record.__setattr__(field_name, value)

def make_create_record(table):
    """
    Dynamic method for creating records using a closure
    """
    def create_record(filepath):
        """
        Create inner function
        """
        record = FileRecord()
        
        record.VDSPath = filepath
        record.VDSFileName = path.split(filepath)[1]
        record.VDSSize = path.getsize(filepath)
        record.VDSCreated = datetime.utcfromtimestamp(path.getctime(filepath))
        record.VDSAccessed = datetime.utcfromtimestamp(path.getatime(filepath))
        record.VDSModified = datetime.utcfromtimestamp(path.getmtime(filepath))
        
        try:
            rawFile = RawFileReaderFactory.ReadFile(filepath)
        except:
            record.Error = True
            record.ErrorText = "Cannot open raw file"
            return record
        
        try:
            rawFile.SelectInstrument(0,1)
        except:
            record.Error = True
            record.ErrorText = "Cannot select MS instrument"
            rawFile.Dispose()
            return record
        
        if not rawFile.IsError:
            raw = {}
            raw["InstrumentData"] = rawFile.GetInstrumentData()
            raw["FileHeader"] = rawFile.FileHeader
            raw["SampleInformation"] = rawFile.SampleInformation
            raw["RunHeaderEx"] = rawFile.RunHeaderEx
        
            table.apply(update_record_from_row, axis=1, args=(record, raw))
            
            methods = methods_from_raw(rawFile)
            record.NumberOfMethods = len(methods)
            record.MethodNames = "|".join([method.Name for method in methods])
            record.MethodTexts =\
                "\n\n{0}SPLITTER{0}\n\n".format("#"*10).join([method.Text for method in methods])
            
            record.Error = False
        
            rawFile.Dispose()
            
        else:
            record.Error = True
            record.ErrorText = "Error processing raw file"
            
            rawFile.Dispose()
            
        return record

    return create_record

record_from_file = make_create_record(table)