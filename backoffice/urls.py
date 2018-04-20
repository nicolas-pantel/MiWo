from django.urls import path, include

from rest_framework.documentation import include_docs_urls

from . import views, api_views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('demo', views.DemoView.as_view(), name='demo'),
    path('demo/<channel>', views.DemoServerView.as_view(), name="demo_server"),
    path('campaigns/', views.CampaignsView.as_view(), name="campaigns"),
    path('campaigns/create/', views.CampaignCreateView.as_view(), name="campaign_create"),
    path('campaigns/delete/<int:pk>/', views.CampaignDeleteView.as_view(), name="campaign_delete"),
    path('campaigns/<int:pk>/', views.CampaignUpdateView.as_view(), name="campaign_update"),
    path('products/', views.ProductsView.as_view(), name="products"),
    path('products/create/', views.ProductCreateView.as_view(), name="product_create"),
    path('products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name="product_delete"),
    path('products/<int:pk>/', views.ProductUpdateView.as_view(), name="product_update"),
    path('products/<int:pk>/image/create/', views.ProductImageCreateView.as_view(), name="product_image_create"),
    path(
        'products/<int:product_pk>/image/<int:product_image_pk>/delete/',
        views.product_image_delete_view, name="product_image_delete"),
    path('campaigns/<int:campaign_pk>/publications/', views.PublicationListView.as_view(), name="publications"),
    path(
        'campaigns/<int:campaign_pk>/publications/create/',
        views.PublicationCreateView.as_view(), name="publication_create"),
    path(
        'campaigns/<int:campaign_pk>/publication/<int:pk>/delete',
        views.PublicationDeleteView.as_view(), name="publication_delete"),
    path(
        'campaigns/<int:campaign_pk>/publication/<int:pk>/',
        views.PublicationUpdateView.as_view(), name="publication_update"),
    path('publications/<int:publication_pk>/tagsvideo/', views.TagVideoListView.as_view(), name="tagsvideo"),
    path(
        'publications/<int:publication_pk>/tagsvideo/create/',
        views.TagVideoCreateView.as_view(), name="tagvideo_create"),
    path('publications/tagsvideo/<int:pk>/delete/', views.TagVideoDeleteView.as_view(), name="tagvideo_delete"),

    ### API ###
    path('api/docs/', include_docs_urls(title='Miwo API')),
    path('api/', include('rest_auth.urls')),
    path('api/registration/', include('rest_auth.registration.urls')),
    path('api/influencers/', api_views.InfluencersAPIView.as_view()),
    path('api/influencers/favorites/', api_views.InfluencersFavoritesAPIView.as_view()),
    path('api/influencers/search/<search_text>/', api_views.InfluencersSearchAPIView.as_view()),
    path('api/influencers/<int:influencer_pk>/subscribe/', api_views.InfluencerSubscriptionAPIView.as_view()),
    path('api/influencers/<int:influencer_pk>/publications/', api_views.PublicationsAPIView.as_view()),
    path('api/publications/<int:publication_pk>/tags/', api_views.TagsAPIView.as_view()),
    path('api/publications/<int:publication_pk>/tags/<int:pk>', api_views.TagAPIView.as_view()),
    path('api/tags/favorites', api_views.TagVideoFavoritesListView.as_view()),
    path('api/tags/<int:pk>/favorites/add', api_views.TagVideoFavoriteAddView.as_view()),
]
