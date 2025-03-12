from django.db import models
from account.models import Account
from django.core.validators import FileExtensionValidator

class Company(models.Model):
    # List of popular countries (including Nigeria)
    country_choices = (
        ('NG', 'Nigeria'),
        ('US', 'United States'),
        ('GB', 'United Kingdom'),
        ('CA', 'Canada'),
        ('IN', 'India'),
        ('AU', 'Australia'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('JP', 'Japan'),
        ('CN', 'China'),
        ('BR', 'Brazil'),
        ('ZA', 'South Africa'),
        ('IT', 'Italy'),
        ('ES', 'Spain'),
        ('RU', 'Russia'),
        ('MX', 'Mexico'),
        ('KR', 'South Korea'),
        ('AR', 'Argentina'),
        ('NG', 'Nigeria'),
        # Add more countries as needed
    )

    # List of common industries
    industry_choices = (
        ('tech', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('retail', 'Retail'),
        ('entertainment', 'Entertainment'),
        ('construction', 'Construction'),
        ('manufacturing', 'Manufacturing'),
        ('automotive', 'Automotive'),
        ('transportation', 'Transportation'),
        ('real-estate', 'Real Estate'),
        ('energy', 'Energy'),
        ('hospitality', 'Hospitality'),
        ('agriculture', 'Agriculture'),
        ('media', 'Media'),
        ('telecommunications', 'Telecommunications'),
        ('e-commerce', 'E-commerce'),
        ('food-beverage', 'Food & Beverage'),
        ('tourism', 'Tourism'),
        ('logistics', 'Logistics'),
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=3, choices=country_choices, null=True, blank=True, default='US')
    image = models.ImageField(upload_to="company_image", validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    founded_date = models.DateField(null=True, blank=True)
    industry = models.CharField(max_length=100, choices=industry_choices, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)  # Comprehensive address field
    size = models.CharField(max_length=50, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    can_recruit = models.BooleanField(default=False)

    # Additional fields:
    website_url = models.URLField(max_length=255, null=True, blank=True)  # Website URL
    facebook_link = models.URLField(max_length=255, null=True, blank=True)  # Social media link: Facebook
    twitter_link = models.URLField(max_length=255, null=True, blank=True)   # Social media link: Twitter
    linkedin_link = models.URLField(max_length=255, null=True, blank=True)  # Social media link: LinkedIn
    instagram_link = models.URLField(max_length=255, null=True, blank=True) # Social media link: Instagram
    about = models.TextField(null=True, blank=True)
    mission = models.TextField(null=True, blank=True)
    vision = models.TextField(null=True, blank=True) 

    def __str__(self):
        return self.name if self.name else "Unnamed Company"
