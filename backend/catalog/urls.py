from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    CategoryViewSet,
    InstrumentViewSet,
    ExpertViewSet,
    LearningContentViewSet,
    ContactViewSet,
    TutorialViewSet,
    TunerConfigurationViewSet,
    BrandingView,
)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('instruments', InstrumentViewSet)
router.register('experts', ExpertViewSet)
router.register('learning', LearningContentViewSet)
router.register('contact', ContactViewSet)
router.register('tutorials', TutorialViewSet)
router.register('tuner-configurations', TunerConfigurationViewSet)

urlpatterns = router.urls + [
    path('branding/', BrandingView.as_view()),
]
