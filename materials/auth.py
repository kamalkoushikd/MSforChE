from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import ValidationError

class RestrictGoogleDomainAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email
        allowed_domain = "iith.ac.in"

        # ✅ Allow subdomains (e.g., @dept.iith.ac.in)
        if not email.endswith(f".{allowed_domain}") and not email.endswith(f"@{allowed_domain}"):
            raise ValidationError("Only emails from iith.ac.in and its subdomains are allowed!")
