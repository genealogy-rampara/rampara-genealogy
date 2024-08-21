from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.render_tree_view, name='tree_view'),
    path('mobile_template/', views.mobile_template, name='mobile_template'),
    path('v2_mobile_template/', views.v2_mobile_template, name='v2_mobile_template'),
    path('note/', views.note, name='note'),
    path('person/<int:person_id>/', views.person_detail, name='person_detail'),
    path('d3-collapsible-tree/', views.d3_collapsible_tree, name='d3_collapsible_tree'),
    path('import_data_from_csv/', views.import_data_from_csv, name='import_data_from_csv'),  
    path('generate_tree_data/', views.generate_tree_data, name='generate_tree_data'),
    path('search/', views.search_person, name='search_person'),
    path('tree_including_daughter/', views.tree_with_female, name='tree_with_female'),
    path('login/', views.login, name='login'),
    path('save-person-data/', views.save_person_data, name='save_person_data'),
    # path('success/', views.success, name='success'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)