from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Processes a login attempt before registration.
        If a user with such an email exists, associates it with the social account.
        """
        if not sociallogin.is_existing:
            email = sociallogin.account.extra_data.get("email")
            if email:
                try:
                    user = User.objects.get(email=email)
                    sociallogin.connect(request, user)
                except User.DoesNotExist:
                    pass
