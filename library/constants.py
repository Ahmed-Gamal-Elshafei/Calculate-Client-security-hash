from asyncio import timeout
from enum import Enum
import pandas as pd


# using in initialization app
# read xlsx file to get the data constants values.
# def read_constants_values(file_path):
#     df = pd.read_excel(file_path)
#     return df
#
# df = read_constants_values("../data/Config.xlsx")
# print(df["Key"][0], df["Value"][0], df["Type"][0])
#
# class ConfigEnum(Enum):
#     pass
#
# # Populate the Enum with data from the DataFrame
# for i, row in df.iterrows():
#     # Use row['Key'] as the attribute name, and (Value, Type) as its value tuple
#     setattr(ConfigEnum, row['Key'], (row['Value'], row['Type']))
# # Test output
# print(ConfigEnum.TimeOutS[0], ConfigEnum.TimeOutS[1])  # Output: (10.0, 'int')
# print(ConfigEnum.TimeOutM[0], ConfigEnum.TimeOutM[1])  # Output: (20.0, 'int')



# class Timeout(Enum):
#     SHORT = (df["Value"][0],df["Type"][0])  # seconds
#     MEDIUM = (df["Value"][1],df["Type"][1])  # seconds
#     LONG = (df["Value"][2],df["Type"][2])  # seconds
# print(x.MEDIUM.value[0]) 20
# print(x.MEDIUM.value[1]) int

class Timeout(Enum):
    SHORT = 5  # seconds
    MEDIUM = 10
    LONG = 30



# class Delay(Enum):
#     SHORT = (df["Value"][3],df["Type"][3])  # seconds
#     MEDIUM = (df["Value"][4],df["Type"][4])  # seconds
#     LONG = (df["Value"][5],df["Type"][5])  # seconds
# print(x.MEDIUM.value[0]) 20
# print(x.MEDIUM.value[1]) int


class Delay(Enum):
    SHORT = 5  # seconds
    MEDIUM = 10
    LONG = 30

class ClickType(Enum):

    DOUBLE = "double"
    SINGLE = "single"


class ClickButton(Enum):
    LEFT = "left"
    RIGHT = "right"




