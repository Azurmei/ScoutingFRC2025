DATA_LEN = 31

def valid_data_count(data:list) -> bool:
    # checks to make sure the count of data is 28
    return len(data) == DATA_LEN

def check_empty(data:list) -> bool:
    # check if any data fields are empty or null
    for i in data:
        if i == None:
            return False
    return True