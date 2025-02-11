DATA_LEN = 32

def valid_data_count(data:list) -> bool:
    # checks to make sure the count of data is 32
    return len(data) == DATA_LEN

def check_empty(data:list) -> bool:
    # check if any data fields are empty or null
    for i in data:
        if i == None:
            return False
    return True

def check_duplicate_alliance(data:list) -> bool:
    return len(data) != len(set(data))

def check_pass_flag(flags:list) -> bool:
    for i in flags:
        if i == False:
            return False
    return True