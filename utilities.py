def get_fixed_length_str(text:str,length:int):
    numOfSpaceToBeAppended=length-len(text)
    return text+get_repeated_str_by_length(numOfSpaceToBeAppended)

def get_repeated_str_by_length(length,str=" "):
    result=""
    for i in range(0,length):
        result+=str
    return result