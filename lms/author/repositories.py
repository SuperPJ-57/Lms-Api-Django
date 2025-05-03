from .models import Author
from django.db.models import Q
class AuthorRepository:

    def create_author(self, author_data):
        return Author.objects.create(**author_data)
    
    def get_author_by_id(self,author_id):
        author = Author.objects.filter(author_id = author_id, is_deleted = False).first()
        return author

    def get_all_authors(self, query=None):
        authors = Author.objects.filter(is_deleted=False).order_by('author_id')
        if query:
            authors = authors.filter(Q(name__icontains=query) )
        return authors

    def update_author(self,author_id,updated_data):
        author = Author.objects.filter(author_id=author_id,is_deleted=False).first()
        if not author:
            return None
        
        for key,value in updated_data.items():
            setattr(author,key,value)

        author.save()


        return author
    
    def delete_author(self,author_id):
        author = Author.objects.filter(author_id=author_id,is_deleted=False).first()

        if not author:
            return None

        author.is_deleted = True

        author.save()

        return author 



    

