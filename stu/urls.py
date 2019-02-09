from django.urls import path
from stu import views

app_name = 'stu'

urlpatterns = [
    path('classes/', views.classes, name='classes'),
    path('add_class/', views.add_class, name='add_class'),
    path('del_class/', views.del_class, name='del_class'),
    path('edit_class/', views.edit_class, name='edit_class'),

    path('students/', views.students, name='students'),
    path('add_students/', views.add_students, name='add_students'),
    path('del_students/', views.del_students, name='del_students'),
    path('edit_students/', views.edit_students, name='edit_students'),

    path('modal_add_class/', views.modal_add_class, name='modal_add_class'),
    path('modal_edit_class/', views.modal_edit_class, name='modal_edit_class'),
    path('modal_edit_stu/', views.modal_edit_stu, name='modal_edit_stu'),
    path('modal_add_stu/', views.modal_add_stu, name='modal_add_stu'),
    path('modal_add_teacher/', views.modal_add_teacher, name='modal_add_teacher'),
    path('modal_edit_teacher/', views.modal_edit_teacher, name='modal_edit_teacher'),

    path('teachers/', views.teachers, name='teachers'),
    path('del_teacher/', views.del_teacher, name='del_teacher'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('edit_teacher/', views.edit_teacher, name='edit_teacher'),
    path('get_all_class/', views.get_all_class, name='get_all_class'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
]