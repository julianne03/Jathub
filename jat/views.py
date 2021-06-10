from django.db.models import Max
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from jat.models import Repository, Introduction, Comment


class RepositoryListView(generic.ListView) :
    model = Repository


class RepositoryDetailView(generic.DetailView) :
    model = Repository


class RepositoryCreateView(generic.CreateView) :
    model = Repository
    fields = ['name', 'description', 'deadline']  # __all__
    template_name_suffix = '_create'
    success_url = reverse_lazy('jat:repository_list')


class RepositoryUpdateView(generic.UpdateView) :
    model = Repository
    fields = ['name', 'description', 'deadline']  # __all__
    template_name_suffix = '_update'
    success_url = reverse_lazy('jat:repository_list')


class RepositoryDeleteView(generic.DeleteView) :
    model = Repository
    success_url = reverse_lazy('jat:repository_list')


class IntroductionDetailView(generic.DetailView) :
    model = Introduction


class IntroductionCreateView(generic.CreateView) :
    model = Introduction
    fields = ['repository', 'version', 'contents', 'access']  # '__all__'
    template_name_suffix = '_create'  # default : _form
    # success_url = reverse_lazy('jat:repository_detail')  # repositroy_detail은 pk가 필요함
    def get_initial(self):
        repository = get_object_or_404(Repository, pk=self.kwargs['repository_pk'])
        introduction = repository.introduction_set.aggregate(Max('version'))  # 해당 repository의 introduction들 중 최대 버전
        version = introduction['version__max']
        if version == None :  # introduction이 현재 없으면 즉 처음 introduction일 경우, version의 기본값인 1
            version = 1
        else :  # introduction이 있을 경우, version의 현재 최대값에서 +1
            version += 1
        return {'repository': repository, 'version': version }

    def get_success_url(self):
        return reverse_lazy('jat:repository_detail', kwargs={'pk' : self.kwargs['repository_pk']})


class IntroductionUpdateView(generic.UpdateView) :
    model = Introduction
    fields = ['repository', 'version', 'contents', 'access']  # '__all__'
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse_lazy('jat:repository_detail', kwargs={'pk': self.kwargs['repository_pk']})


class IntroductionDeleteView(generic.DeleteView) :
    model = Introduction

    def get_success_url(self):
        return reverse_lazy('jat:repository_detail', kwargs={'pk': self.kwargs['repository_pk']})


class CommentCreateView(generic.CreateView):
    model = Comment
    fields = '__all__'  # ['introduction', 'comment'] => 자동으로 입력되는 필드는 생략함
    template_name_suffix = '_create' # comment_create.html

    def get_initial(self):
        introduction = get_object_or_404(Introduction, pk=self.kwargs['introduction_pk'])
        return {'introduction': introduction}

    def get_success_url(self):  # jat:introduction_detail repository_pk pk
        kwargs = {
            'repository_pk': self.kwargs['repository_pk'],
            'pk': self.kwargs['introduction_pk'],
        }
        return reverse_lazy('jat:introduction_detail', kwargs=kwargs)


class CommentUpdateView(generic.UpdateView):
    model = Comment
    fields = '__all__'  # ['introduction', 'comment'] => 자동으로 입력되는 필드는 생략함
    template_name_suffix = '_update'  # comment_update.html

    def get_success_url(self):  # jat:introduction_detail repository_pk pk
        kwargs = {
            'repository_pk': self.kwargs['repository_pk'],
            'pk': self.kwargs['introduction_pk'],
        }
        return reverse_lazy('jat:introduction_detail', kwargs=kwargs)


class CommentDeleteView(generic.DeleteView):
    model = Comment

    def get_success_url(self):  # jat:introduction_detail repository_pk pk
        kwargs = {
            'repository_pk': self.kwargs['repository_pk'],
            'pk': self.kwargs['introduction_pk'],
        }
        return reverse_lazy('jat:introduction_detail', kwargs=kwargs)
