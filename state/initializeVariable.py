from state.StateMachine import State


class InitializeVariable(State):
    """State to initialize shared variables in the context."""

    def execute(self, context):
        """Initialize shared variables."""
        try:
            static_variable = StaticVariable()
            print("Executing InitializeVariable State...")
            context.variables["bot_id"] = 0
            context.variables["dict_bool"] = static_variable.dict_bool
            context.variables["credentials"] = static_variable.decrypted_credentials
            context.variables["dict_int"] = static_variable.dict_int
            context.variables["dict_string"] = static_variable.dict_string
        except Exception as e:
            print(f"Error in InitializeVariable.execute: {e}")
            context.terminate = True  # Terminate the state machine on error

    def next_state(self, context):
        """Move to the InitializeApp state."""
        from state.initializeApp import InitializeApp
        return InitializeApp()


import pandas as pd
from reusables.aes_handler import AESHandler


class StaticVariable:
    _initialized = False
    dict_int = None
    dict_string = None
    dict_bool = None
    decrypted_credentials = None

    def __init__(self):
        self.initialize_variable()

    @classmethod
    def initialize_variable(cls):
        if not cls._initialized:
            """Static method to initialize variables and return shared dictionaries."""
            raw_data = cls._read_variables_from_xlsx()
            cls.dict_int, cls.dict_string, cls.dict_bool, dict_credentials = cls._initialize_variables_from_xlsx(
                raw_data
            )
            cls.decrypted_credentials = cls._decrypt_credentials(dict_credentials)
            cls._initialized = True

    @staticmethod
    def _read_variables_from_xlsx(file_path="../data/Config.xlsx"):
        """Reads data from an Excel file."""
        excel_data = pd.ExcelFile(file_path)
        return {sheet: excel_data.parse(sheet) for sheet in excel_data.sheet_names}

    @staticmethod
    def _check_for_duplicates(data, sheet_name):
        """Checks for duplicate variable names in the specified sheet."""
        if sheet_name in data:
            variable_names = data[sheet_name]["VariableName"]
            duplicates = variable_names[variable_names.duplicated()].unique()
            if len(duplicates) > 0:
                duplicate_names = ", ".join(duplicates)
                raise ValueError(
                    f"Please modify the xlsx file to remove the duplicate(s) of: {duplicate_names}"
                )

    @classmethod
    def _initialize_variables_from_xlsx(cls, data):
        """Processes Excel data into structured dictionaries."""
        dict_int, dict_string, dict_bool, dict_credentials = {}, {}, {}, {}

        # Check for duplicates in each relevant sheet
        if "Constants" in data:
            cls._check_for_duplicates(data, "Constants")
            for _, row in data["Constants"].iterrows():
                variable_name, value, var_type = row["VariableName"], row["Value"], row["Type"]
                if "int" in var_type:
                    dict_int[variable_name] = {"value": value, "type": var_type}
                elif "str" in var_type:
                    dict_string[variable_name] = {"value": value, "type": var_type}
                elif "bool" in var_type:
                    dict_bool[variable_name] = {"value": value, "type": var_type}

        if "Cred" in data:
            cls._check_for_duplicates(data, "Cred")
            for _, row in data["Cred"].iterrows():
                variable, username, password = row["VariableName"], row["Username"], row["Password"]
                dict_credentials[variable] = {"username": username, "password": password}

        return dict_int, dict_string, dict_bool, dict_credentials

    @staticmethod
    def _decrypt_credentials(credentials):
        """Decrypts credentials using AESHandler."""
        key = b"put your key that you use to encrypt here"
        iv = b'put your iv that you use to encrypt here'
        aes = AESHandler(key=key, iv=iv)
        return {
            key: {k: aes.decrypt(v).decode("utf-8") for k, v in values.items()}
            for key, values in credentials.items()
        }
