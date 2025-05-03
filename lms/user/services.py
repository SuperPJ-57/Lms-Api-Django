from .repositories import UserRepository
from .serializers import LoginSerializer

class UserService:
    def __init__(self):
        self.repo = UserRepository()
        
    def register_user(self, data):
        user = self.repo.create_user(data)
        return user
    
    

    def login(self, data):
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['user_name']
            password = serializer.validated_data['password']
            user = self.repo.authenticate_user(username, password)
            if not user:
                return {"error": "user not found"}
            return user
        
    def get_user(self, username):
        user = self.repo.get_user(username)
        return user
    
    def get_all_users(self):
        users = self.repo.get_all_users()
        return users