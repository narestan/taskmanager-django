from django.urls import path
from tasks.views import (
    TaskCreateView, TaskDeleteView, TaskDetailView, CategoryDetailView,
    TaskListView, TaskUpdateView, CategoryListView, CategoryUpdateView, TaskCategoryUpdateView,
    CategoryDeleteView, CategoryCreateView, FollowUpCreateView, FollowUpUpdateView, FollowUpDeleteView, ProjectSearchView

)


app_name = 'tasks'


urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(),
         name='category-detail'),
    path('categories/<int:pk>/update/',
         CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/',
         CategoryDeleteView.as_view(), name='category-delete'),
    path('create-category/', CategoryCreateView.as_view(), name='category-create'),
    path('<int:pk>/followups/create/',
         FollowUpCreateView.as_view(), name='task-followup-create'),
    path('followups/<int:pk>/', FollowUpUpdateView.as_view(),
         name='task-followup-update'),
    path('followups/<int:pk>/delete/',
         FollowUpDeleteView.as_view(), name='task-followup-delete'),
    path('<int:pk>/category/',
         TaskCategoryUpdateView.as_view(), name='task-category-update'),
    path('search/', ProjectSearchView.as_view(), name='project_search'),
]
