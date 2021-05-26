from django.db import models

class Repository(models.Model) :
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # repo.introduction_set : repository와 연결되어 있는 자소서를 가져오려고 할 때

    def __str__(self):
        return self.name

class Introduction(models.Model) :
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)  # intro1.repository
    version = models.IntegerField(default=1)
    contents = models.TextField()
    # intro1.comment_set

    def __str__(self):
        return f'{self.version} {self.contents}'

class Comment(models.Model) :
    introduction = models.ForeignKey(Introduction, on_delete=models.CASCADE)  # comment1.introduction
    comment = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment