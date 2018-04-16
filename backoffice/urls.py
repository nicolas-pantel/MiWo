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
    path('api/publications/<int:publication_pk>/tags/<int:tag_pk>', api_views.TagAPIView.as_view()),
]
