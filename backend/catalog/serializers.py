from rest_framework import serializers
from .models import Category, Instrument, Expert, LearningContent, Contact, Tutorial, TunerConfiguration, Branding


def get_requested_language(context) -> str:
    request = context.get('request') if isinstance(context, dict) else context
    if request is None:
        return 'en'

    query_params = getattr(request, 'query_params', None) or getattr(request, 'GET', None) or {}
    raw_language = query_params.get('lang') if hasattr(query_params, 'get') else None

    if not raw_language:
        raw_language = getattr(request, 'LANGUAGE_CODE', '') or ''

    if not raw_language and hasattr(request, 'headers'):
        raw_language = request.headers.get('Accept-Language', '').split(',')[0]

    return 'ne' if str(raw_language).lower().startswith('ne') else 'en'


def get_localized_value(instance, field_name: str, language: str, fallback=''):
    if instance is None:
        return fallback

    localized_name = f'{field_name}_ne'
    if language == 'ne':
        localized_value = getattr(instance, localized_name, None)
        if localized_value not in (None, ''):
            return localized_value

    value = getattr(instance, field_name, fallback)
    return fallback if value in (None, '') else value


class LanguageAwareModelSerializer(serializers.ModelSerializer):
    localized_fields: tuple[str, ...] = ()

    def get_language(self) -> str:
        return get_requested_language(self.context)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.get_language() != 'ne':
            return data

        for field_name in self.localized_fields:
            localized_value = getattr(instance, f'{field_name}_ne', None)
            if localized_value not in (None, ''):
                data[field_name] = localized_value

        return data


class CategorySerializer(LanguageAwareModelSerializer):
    localized_fields = ('name', 'description')

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class InstrumentListSerializer(LanguageAwareModelSerializer):
    localized_fields = ('name', 'region', 'description')
    category = serializers.SerializerMethodField()
    image = serializers.ImageField(source='primary_image', allow_null=True, required=False)

    def get_category(self, obj: Instrument) -> str:
        return get_localized_value(obj.category, 'name', self.get_language())

    class Meta:
        model = Instrument
        fields = [
            'id',
            'name',
            'category',
            'region',
            'image',
            'description',
            'show_brightness_control',
            'show_tuner',
            'is_featured',
        ]


class ExpertPreviewSerializer(LanguageAwareModelSerializer):
    localized_fields = ('name', 'expertise')
    photo = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Expert
        fields = ['id', 'name', 'expertise', 'photo']


class InstrumentDetailSerializer(LanguageAwareModelSerializer):
    localized_fields = ('name', 'region', 'description', 'history', 'materials', 'playing_technique', 'cultural_significance')
    category = serializers.SerializerMethodField()
    image = serializers.ImageField(source='primary_image', allow_null=True, required=False)
    model_3d = serializers.SerializerMethodField()
    experts = ExpertPreviewSerializer(many=True, read_only=True)
    tuner_config = serializers.SerializerMethodField()
    tuner_configs = serializers.SerializerMethodField()

    def get_category(self, obj: Instrument) -> str:
        return get_localized_value(obj.category, 'name', self.get_language())

    class Meta:
        model = Instrument
        fields = [
            'id',
            'name',
            'category',
            'region',
            'image',
            'model_3d',
            'description',
            'history',
            'materials',
            'playing_technique',
            'cultural_significance',
            # Nepali-language writable fields
            'name_ne',
            'region_ne',
            'description_ne',
            'history_ne',
            'materials_ne',
            'playing_technique_ne',
            'cultural_significance_ne',
            'show_brightness_control',
            'show_tuner',
            'tuner_config',
            'tuner_configs',
            'experts',
        ]

    def get_model_3d(self, obj: Instrument) -> str | None:
        if not obj.model_3d:
            return None
        request = self.context.get('request')
        url = obj.model_3d.url
        if request is not None:
            return request.build_absolute_uri(url)
        return url

    def get_tuner_config(self, obj: Instrument):
        tuner = obj.tuner_configs.filter(is_default=True).first() or obj.tuner_configs.first()
        if not tuner:
            return None
        return TunerConfigurationSerializer(tuner, context=self.context).data

    def get_tuner_configs(self, obj: Instrument):
        tuners = obj.tuner_configs.all().order_by('-is_default', 'tuning_name')
        return TunerConfigurationSerializer(tuners, many=True, context=self.context).data


class ExpertListSerializer(LanguageAwareModelSerializer):
    localized_fields = ('name', 'expertise', 'bio')
    photo = serializers.ImageField(allow_null=True, required=False)
    instruments = serializers.SerializerMethodField()

    def get_instruments(self, obj: Expert):
        language = self.get_language()
        return [get_localized_value(instrument, 'name', language) for instrument in obj.instruments.all()]

    class Meta:
        model = Expert
        fields = ['id', 'name', 'expertise', 'photo', 'bio', 'instruments']


class InstrumentMiniSerializer(LanguageAwareModelSerializer):
    localized_fields = ('name', 'region')
    category = serializers.SerializerMethodField()
    image = serializers.ImageField(source='primary_image', allow_null=True, required=False)

    def get_category(self, obj: Instrument) -> str:
        return get_localized_value(obj.category, 'name', self.get_language())

    class Meta:
        model = Instrument
        fields = ['id', 'name', 'category', 'region', 'image']


class ExpertDetailSerializer(LanguageAwareModelSerializer):
    localized_fields = ('name', 'expertise', 'bio', 'detailed_bio', 'achievements')
    photo = serializers.ImageField(allow_null=True, required=False)
    instruments = InstrumentMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Expert
        fields = [
            'id',
            'name',
            'expertise',
            'photo',
            'bio',
            'detailed_bio',
            'achievements',
            'contact_email',
            'instruments',
        ]
        extra_kwargs = {
            'contact_email': {'required': False, 'allow_blank': True},
            'detailed_bio': {'required': False, 'allow_blank': True},
            'achievements': {'required': False},
        }


class LearningContentSerializer(LanguageAwareModelSerializer):
    localized_fields = ('title', 'content')

    class Meta:
        model = LearningContent
        fields = ['id', 'title', 'content', 'order']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'subject', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'is_read', 'created_at']


class TutorialSerializer(LanguageAwareModelSerializer):
    localized_fields = ('title', 'description', 'instructor_name')
    caption_en_url = serializers.SerializerMethodField()
    caption_ne_url = serializers.SerializerMethodField()

    def get_caption_en_url(self, obj: Tutorial) -> str | None:
        if not obj.caption_en:
            return None
        request = self.context.get('request')
        url = obj.caption_en.url
        return request.build_absolute_uri(url) if request is not None else url

    def get_caption_ne_url(self, obj: Tutorial) -> str | None:
        if not obj.caption_ne:
            return None
        request = self.context.get('request')
        url = obj.caption_ne.url
        return request.build_absolute_uri(url) if request is not None else url

    class Meta:
        model = Tutorial
        fields = [
            'id',
            'instrument',
            'title',
            'description',
            'video_url',
            'instructor_name',
            'duration',
            'caption_en_url',
            'caption_ne_url',
            'created_at',
        ]
        read_only_fields = ['created_at']
        extra_kwargs = {
            'instructor_name': {'required': False, 'allow_blank': True},
            'duration': {'required': False, 'allow_blank': True},
        }


class TunerConfigurationSerializer(LanguageAwareModelSerializer):
    localized_fields = ('tuning_name', 'instructions')

    class Meta:
        model = TunerConfiguration
        fields = ['id', 'instrument', 'tuning_name', 'instructions', 'notes', 'frequencies', 'is_default', 'created_at', 'updated_at']
        read_only_fields = ['created_at']


class BrandingSerializer(LanguageAwareModelSerializer):
    localized_fields = ('name', 'logo_alt')
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Branding
        fields = ['id', 'name', 'logo', 'logo_url', 'logo_alt', 'contact_email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'logo_url', 'created_at', 'updated_at']

    def get_logo_url(self, obj: Branding) -> str | None:
        if not obj.logo:
            return None

        request = self.context.get('request')
        url = obj.logo.url
        if request is not None:
            return request.build_absolute_uri(url)
        return url
