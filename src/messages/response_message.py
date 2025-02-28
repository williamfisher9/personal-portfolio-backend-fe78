
class ResponseMessage:
    def __init__(self, message, status):
        self.message = message
        self.status = status

    def create_response_message(self):
        return {"message": self.message, "status": self.status}, self.status