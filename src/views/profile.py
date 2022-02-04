from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin

from src.models.profile import Profile
from src.forms import ProfileForm, UserUpdateForm


class UserProfileUpdate(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            profile = Profile.objects.filter(user=self.request.user)
            p_form = ProfileForm(instance=self.request.user.profile)
            u_form = UserUpdateForm(instance=self.request.user)

            context = {
                'object': profile,
                'p_form': p_form,
                'u_form': u_form
            }
            return render(self.request, 'src/profile.html', context)
        except ObjectDoesNotExist:
            profile = Profile.objects.filter(user=self.request.user)
            p_form = ProfileForm(instance=self.request.user)
            u_form = UserUpdateForm(instance=self.request.user)

            context = {
                'object': profile,
                'p_form': p_form,
                'u_form': u_form
            }
            return render(self.request, 'src/profile.html', context)

    def post(self, *args, **kwargs):
        try:
            u_form = UserUpdateForm(self.request.POST, instance=self.request.user)
            p_form = ProfileForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)

            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()

                messages.info(self.request, "Profile updated successfully.")
                return redirect('src:profile')
        except ObjectDoesNotExist:
            u_form = UserUpdateForm(self.request.POST, instance=self.request.user)
            p_form = ProfileForm(self.request.POST, self.request.FILES, instance=self.request.user)

            if u_form.is_valid() and p_form.is_valid():
                prof = Profile()
                prof.user = self.request.user
                prof.image = p_form.cleaned_data.get('image')
                prof.phone_number = p_form.cleaned_data.get('phone_number')
                prof.country = p_form.cleaned_data.get('country')
                prof.email = u_form.cleaned_data.get('email')
                prof.save()
                p_form.save()
                u_form.save()
                messages.info(self.request, "Profile created successfully.")
                return redirect('src:profile')


def delete_profile(request):
    profile = Profile.objects.filter(user=request.user)
    profile.delete()
    messages.info(request, "Profile deleted successfully.")
    return redirect('src:profile')


def delete_account(request):
    request.user.delete()
    messages.info(request, "Account deleted successfully.")
    return redirect('src:home')
