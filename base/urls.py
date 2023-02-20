from django.urls import path
from .views import MemberList, MemberDetail, MemberCreate, MemberEdit, DeleteView


urlpatterns = [


    path('', MemberList.as_view(), name='members'),
    path('member/<int:pk>/', MemberDetail.as_view(), name='member'),
    path('member-create/', MemberCreate.as_view(), name='member-create'),
    path('member-edit/<int:pk>/', MemberEdit.as_view(), name='member-edit'),
    path('member-delete/<int:pk>/', DeleteView.as_view(), name='member-delete'),
]
