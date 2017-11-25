from models.models import PostModel

from models.base_manager import SNBaseManager


class PostManager(SNBaseManager):
    def __init__(self):
        class_model = PostModel
        super(PostManager, self).__init__(class_model)

    def save_post(self,form, user):
        self.object.title = form.get('title', '')
        self.object.photos = form.get('photos', '')
        self.object.text = form.get('text', '')
        self.object.user = user.object
        self.save()

    def get_posts(self,user):
        return self.select().And([('user','=',user.object.id)]).run()

