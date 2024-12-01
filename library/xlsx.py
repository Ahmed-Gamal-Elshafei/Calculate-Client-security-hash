from win32com.client.gencache import EnsureDispatch
import os
import pandas as pd

#need to install openpyxl pywin32 pandas 

# Function to read a password-protected Excel file
def read_xlsx(file_path, sheet_name, password=None):
    try:
        if password:
            excel = EnsureDispatch("Excel.Application")
            # Open the workbook with password
            wb = excel.Workbooks.Open(file_path, False, False, None, password)
            sheet = wb.Sheets(sheet_name)
            # Make the sheet invisible
            excel.Visible = False

            # Extracting data from the opened sheet
            data = sheet.UsedRange.Value
            wb.Close()
            excel.Quit()

            # Convert data to DataFrame
            headers = data[0]
            rows = data[1:]
            print(data)
            df = pd.DataFrame(rows, columns=headers)

            return df
        else:
            # If no password, read using pandas directly
            return pd.read_excel(file_path, sheet_name=sheet_name)

    except Exception as e:
        return f"Error reading file: {e}"


def set_workbook_password(file_path, password):
    excel = EnsureDispatch("Excel.Application")
    # Set the display alerts to False
    excel.DisplayAlerts = False
    # Open the workbook
    wb = excel.Workbooks.Open(file_path)
    # Make the sheet invisible
    wb.Visible = False
    wb.SaveAs(file_path, Password=password)
    wb.Close()
    excel.Quit()


def write_xlsx(file_path, sheet_name, df, password=None):
    try:
        _path = r"D:\Work\Selenium\Project" + "/" + file_path
        if is_file_exist(file_path):
            write_df_to_xlsx(file_path, df, sheet_name)
        else:
            df.to_excel(file_path, sheet_name=sheet_name)

        if password:
            set_workbook_password(_path, password)

        print("path is ", _path)
        return "File written successfully", _path
    except Exception as e:
        return f"Error writing file: {e}", None


def write_df_to_xlsx(file_path, df, sheet_name):
    with pd.ExcelWriter(
        file_path, engine="openpyxl", mode="a" if is_file_exist(file_path) else "w"
    ) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)


def is_file_exist(file_path):
    return os.path.exists(file_path)






# data = {"key": ["A", "B", "C"], "value": ["D", "E", "F"]}
# converted_data = pd.DataFrame(data)
# print(converted_data)


# # Example usage
# _, _path = write_xlsx("example.xlsx", "Sheet1", converted_data, "password")

# # _path=r"D:\Work\Selenium\Project\example.xlsx"
# df = read_xlsx(
#     file_path=_path,
#     sheet_name="Sheet1",
#     password="password",
# )
# print(df)
