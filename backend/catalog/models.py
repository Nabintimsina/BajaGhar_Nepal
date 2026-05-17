from django.db import models
from django.core.validators import FileExtensionValidator
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    name_ne = models.CharField(max_length=120, blank=True, default='')
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    description_ne = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Instrument(models.Model):
    name = models.CharField(max_length=150)
    name_ne = models.CharField(max_length=150, blank=True, default='')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='instruments')
    region = models.CharField(max_length=120)
    region_ne = models.CharField(max_length=120, blank=True, default='')
    description = models.TextField()
    description_ne = models.TextField(blank=True, default='')
    history = models.TextField(blank=True)
    history_ne = models.TextField(blank=True, default='')
    materials = models.TextField(blank=True)
    materials_ne = models.TextField(blank=True, default='')
    playing_technique = models.TextField(blank=True)
    playing_technique_ne = models.TextField(blank=True, default='')
    cultural_significance = models.TextField(blank=True)
    cultural_significance_ne = models.TextField(blank=True, default='')
    show_brightness_control = models.BooleanField(default=False)
    primary_image = models.ImageField(upload_to='instruments/images/', blank=True, null=True)
    model_3d = models.FileField(
        upload_to='instruments/media/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['glb', 'gltf', 'bin'],
                message='Upload a valid 3D model file (GLB, GLTF, or BIN)'
            )
        ],
        help_text='Supports: GLB, GLTF, BIN'
    )
    is_featured = models.BooleanField(default=False)
    show_tuner = models.BooleanField(default=False, help_text='Show tuner/practice tool in the frontend instrument page')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Expert(models.Model):
    name = models.CharField(max_length=150)
    name_ne = models.CharField(max_length=150, blank=True, default='')
    expertise = models.CharField(max_length=150)
    expertise_ne = models.CharField(max_length=150, blank=True, default='')
    bio = models.TextField()
    bio_ne = models.TextField(blank=True, default='')
    detailed_bio = models.TextField(blank=True)
    detailed_bio_ne = models.TextField(blank=True, default='')
    contact_email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='experts/photos/', blank=True, null=True)
    achievements = models.JSONField(default=list, blank=True)
    achievements_ne = models.JSONField(default=list, blank=True)
    instruments = models.ManyToManyField(Instrument, related_name='experts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class LearningContent(models.Model):
    title = models.CharField(max_length=200)
    title_ne = models.CharField(max_length=200, blank=True, default='')
    content = models.TextField()
    content_ne = models.TextField(blank=True, default='')
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self) -> str:
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True, db_index=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.subject} - {self.name}"


class Tutorial(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='tutorials')
    title = models.CharField(max_length=200)
    title_ne = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField()
    description_ne = models.TextField(blank=True, default='')
    video_url = models.URLField()
    instructor_name = models.CharField(max_length=150, blank=True, default='')
    instructor_name_ne = models.CharField(max_length=150, blank=True, default='')
    duration = models.CharField(max_length=50, blank=True, default='', help_text="e.g., '12:30'")
    caption_en = models.FileField(
        upload_to='tutorials/captions/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['vtt', 'srt'],
                message='Upload a valid caption file (VTT or SRT format)'
            )
        ],
        help_text='English captions (VTT or SRT format). Optional for YouTube videos.',
    )
    caption_ne = models.FileField(
        upload_to='tutorials/captions/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['vtt', 'srt'],
                message='Upload a valid caption file (VTT or SRT format)'
            )
        ],
        help_text='Nepali captions (VTT or SRT format). Optional for YouTube videos.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.title} - {self.instructor_name}"


class TunerConfiguration(models.Model):
    instrument = models.OneToOneField(Instrument, on_delete=models.CASCADE, related_name='tuner_config')
    tuning_name = models.CharField(max_length=100, default='Standard')
    tuning_name_ne = models.CharField(max_length=100, blank=True, default='')
    notes = models.JSONField(default=list, help_text='List of note names, e.g. ["E2", "A2", "D3", "G3", "B3", "E4"]')
    frequencies = models.JSONField(default=list, help_text="List of frequencies in Hz, e.g. [82.41, 110.00, 146.83, 196.00, 246.94, 329.63]")
    is_default = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', 'tuning_name']

    def __str__(self) -> str:
        return f"{self.instrument.name} - {self.tuning_name}"


class Branding(models.Model):
    name = models.CharField(max_length=120, default=getattr(settings, 'BRANDING_NAME', 'BAJAGHAR'))
    name_ne = models.CharField(max_length=120, blank=True, default='')
    logo = models.FileField(
        upload_to='branding/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'],
                message='Upload a valid image file (JPG, PNG, GIF, WEBP, or SVG)'
            )
        ],
        help_text='Supports: JPG, PNG, GIF, WEBP, SVG'
    )
    logo_alt = models.CharField(max_length=160, blank=True, default=getattr(settings, 'BRANDING_LOGO_ALT', 'BAJAGHAR logo'))
    logo_alt_ne = models.CharField(max_length=160, blank=True, default='')
    contact_email = models.EmailField(
        blank=True,
        default=getattr(settings, 'BRANDING_CONTACT_EMAIL', 'info@bajanepal.com'),
        help_text='Single public email shown in the footer and contact area',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Branding'
        verbose_name_plural = 'Branding'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

