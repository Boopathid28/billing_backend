class ResponseMessages:
    def login(self, text):
        msg = text + ' successfully!'
        return msg
    
    def retrieve(self, text):
        msg = text + ' retrieved successfully!'
        return msg
    
    def create(self, text):
        msg = text + ' created successfully!'
        return msg

    def not_create(self, text):
        msg = text + ' is not created!'
        return msg
    
    def update(self, text):
        msg = text + ' updated successfully!'
        return msg
    
    def not_update(self, text):
        msg = text + ' is not updated!'
        return msg
    
    def delete(self, text):
        msg = text + ' deleted successfully!'
        return msg
    
    def related_item(self, text):
        msg = text + ' the related items!'
        return msg
    
    def not_exists(self, text):
        msg = text + ' does not exists!'
        return msg
    
    def already_exists(self, text):
        msg = text + ' already exists!'
        return msg
    
    def in_valid(self, text):
        msg = text + ' is invalid!'
        return msg
    
    def in_valid_fields(self):
        msg = 'Invalid Field values!'
        return msg
    
    def change(self, text):
        msg = text + ' changed successfully!'
        return msg
    
    def something_else(self):
        msg = 'Something went wrong!'
        return msg
    
    def sent_msg(self, text):
        msg = text + ' sented successfully!'
        return msg
    
    def permission(self, text):
        msg = "Don't have a permission to update the " + text
        return msg
    
    def activate(self, text):
        msg = "Activate the " + text
        return msg
    
    def missing_fields(self, text):
        msg = "Please Enter the " + text
        return msg