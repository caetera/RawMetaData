# -*- coding: utf-8 -*-
import pandas as pd

fields = {"InstrumentData":
         ["AxisLabelX", "AxisLabelY", "ChannelLables", "Flags", "HardwareVersion",
          "Model", "Name", "SerialNumber", "SoftwareVersion", "Units"],
         "FileHeader":
         ["CreationDate", "FileDescription", "FileType", "ModifiedDate",
          "NumberOfTimesCalibrated", "NumberOfTimesModified", "Revision", 
          "WhoCreatedId", "WhoCreatedLogon", "WhoModifiedId", "WhoModifiedLogon"],
         "SampleInformation":
         ["SampleVolume", "SampleType", "ProcessingMethodFile", "Path", "RowNumber",
          "IstdAmount", "CalibrationFile", "RawFileName", "InstrumentMethodFile",
          "CalibrationLevel", "BarcodeStatus", "Barcode", "InjectionVolume",
          "Vial", "SampleName", "SampleId", "Comment", "SampleWeight", "UserText"],
         "RunHeaderEx":
         ["SpectraCount", "FirstSpectrum", "LastSpectrum", "StartTime", "EndTime", "LowMass",
          "HighMass", "Comment1", "Comment2", "MaxIntensity", "FilterMassPrecision",
          "MassResolution", "MaxIntegratedIntenisty"]}

field_names = []
field_positions = []
for key, value in fields.items():
    field_names.extend(value)
    field_positions.extend(["{}|{}".format(key, element) for element in value])


parameter_table = pd.DataFrame({"Field": field_names,
                                "Location": field_positions})
                               

parameter_table["Type"] = "String"
parameter_table["Active"] = True

parameter_table.to_csv("parameter_table.csv", index=False)