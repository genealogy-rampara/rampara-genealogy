from django.urls import path
from . import views
urlpatterns = [
    path('', views.render_tree_view, name='tree_view'),
    path('note/', views.note, name='note'),
    path('get_tree_data/', views.get_tree_data, name='get_tree_data'),
    path('person/<int:person_id>/', views.person_detail, name='person_detail'),
    path('d3-collapsible-tree/', views.d3_collapsible_tree, name='d3_collapsible_tree'),
    path('create_person/', views.create_person, name='create_person'),    
    # path('build_tree/', views.build_tree, name='build_tree'),    
    path('import_data_from_csv/', views.import_data_from_csv, name='import_data_from_csv'),  
    path('generate_tree_data/', views.generate_tree_data, name='generate_tree_data'),
    path('search/', views.search_person, name='search_person'),
]
