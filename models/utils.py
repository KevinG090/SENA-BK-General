

class UtilsModel:
    def __init__(self) -> None:
        pass
    
    def next_page_exist(self,count,limit,offset):
        num_pages = int(count / limit)
        if count % limit != 0:
            num_pages += 1
        current_page = offset // limit + 1
        return current_page < num_pages