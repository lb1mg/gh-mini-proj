
from app.managers.request_manager import RequestManager

class BitbucketManager:
    
    def __init__(self) -> None:
        self.req_manager = RequestManager()
        raise NotImplementedError