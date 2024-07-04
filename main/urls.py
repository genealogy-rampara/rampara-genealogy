from django.urls import path
from . import views, utils
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
urlpatterns = [
    # path('',views.LoginUserView, name='login'),
    # path('signup/',views.RegisterUserView, name='signup'),
    # path('logout/',views.logout_view, name='logout'),
    # path("changepass/",views.changepass,name="changepass"),
    # path("otp/",views.otp, name="otp"),
    # path('forgotpass/',views.forgotpass,name='forgotpass'),
    # path('contactus/', views.contactus_view, name='contactus'),
    path('', views.render_tree_view, name='tree_view'),
    path('get_tree_data/', views.get_tree_data, name='get_tree_data'),
    path('person/<int:person_id>/', views.person_detail, name='person_detail'),
    path('d3-collapsible-tree/', views.d3_collapsible_tree, name='d3_collapsible_tree'),
    path('child/<int:child_id>/', views.child_detail, name='child_detail'),  # URL pattern for child detail
    path('create_person/', views.create_person, name='create_person'),  
    # path('create_spouse/', views.create_spouse, name='create_spouse'),  
    # path('create_family/', views.create_family, name='create_family'),  
    # path('update_person/<int:person_id>/', views.update_person, name='update_person'),    
    # path('update_spouse/<int:spouse_id>/', views.update_spouse, name='update_spouse'),
    # path('update_family/<int:family_id>/', views.update_family, name='update_family'),  
    # path('delete_person/<int:person_id>/', views.delete_person, name='delete_person'),  
    # path('delete_spouse/<int:spouse_id>/', views.delete_spouse, name='delete_spouse'),  
    # path('delete_family/<int:family_id>/', views.delete_family, name='delete_family'),  
    # path('generate_tree_data_from_csv/', utils.generate_tree_data_from_csv, name='generate_tree_data_from_csv'),  
    path('import_data_from_csv/', views.import_data_from_csv, name='import_data_from_csv'),  
    path('save-person-details/', views.save_person_details, name='save_person_details'),
    path('generate_tree_data/', views.generate_tree_data, name='generate_tree_data'),
    # path('build_tree/', views.build_tree, name='build_tree'),
    
]
