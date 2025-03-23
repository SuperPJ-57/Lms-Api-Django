from .repositories import AuthorRepository

class AuthorService:

    def __init__(self):
        self.repo = AuthorRepository()

    def add_author(self, author_data):
        return self.repo.create_author(author_data)
    
    def update_author(self, author_id, updated_data):
        # Fetch existing author details first
        author = self.repo.get_author_by_id(author_id)
        if not author:
            return {"error": "Author not found"}
        
        # Update the author details
        updated_author = self.repo.update_author(author_id, updated_data)
        return updated_author
    
    def get_author_detail(self, author_id):

        author = self.repo.get_author_by_id(author_id)

        if not author:
            return {"error": "Author not found"}
        return author
    
    def delete_author(self, author_id):

        author = self.repo.get_author_by_id(author_id)
        if not author:
            return {"error": "Author not found"}
        
        self.repo.delete_author(author_id)
        return {"message": "Author deleted successfully"}
    
    def list_authors(self, query=None):
        return self.repo.get_all_authors(query)