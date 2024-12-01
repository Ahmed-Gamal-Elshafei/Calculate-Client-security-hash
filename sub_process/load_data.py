from automation.work_items.acme__work_item_read.Acme_WorkItem_ReadTable import AcmeWorkItemReadTable


def load_data_init(driver):
    print(driver.current_url)
    read_table = AcmeWorkItemReadTable(driver)
    table_data = read_table.start()
    print("table_data", table_data)
    write_data_to_xls(table_data)


def write_data_to_xls(table_data):
    # write the data in xlsx.
    import pandas as pd

    df = pd.DataFrame(table_data)
    df.to_excel("../data2.xlsx", index=False)
