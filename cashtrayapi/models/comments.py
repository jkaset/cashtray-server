from django.db import models

class Comment(models.Model):
    recipient = models.ForeignKey("Nonsmoker", on_delete=models.CASCADE)
    commenter = models.ForeignKey("Nonsmoker", related_name='user_commenting', on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_on = models.DateField()

    @property
    def my_comment(self):
        return self.__my_comment

    @my_comment.setter
    def my_comment(self, value):
        self.__my_comment = value