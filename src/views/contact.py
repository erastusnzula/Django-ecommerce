from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from src.forms import ContactForm
from src.models.contact import Contact


class ContactAdmin(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        """Display contact form and sent information."""
        contact = Contact.objects.filter(user=self.request.user).order_by('date_created')
        email = self.request.user.email
        form = ContactForm()
        context = {
            'object': contact,
            'form': form,
            'email': email,
        }

        return render(self.request, 'src/contact.html', context)

    def post(self, *args, **kwargs):
        """Accept user input data from contact form."""
        error = None
        form = ContactForm(self.request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            contact = Contact()
            contact.user = self.request.user
            contact.email = self.request.user.email
            contact.message = message
            if "fuck" in contact.message.lower():
                error = "fuck"
                form = ContactForm(data=self.request.POST)

                context = {
                    'error': error,
                    'form': form
                }
                messages.warning(self.request, "Message not sent, please edit and try again.")
                return render(self.request, 'src/contact.html', context)

            contact.save()
            messages.success(self.request, "Message send successfully.")
            return redirect('src:contact-confirm')


class ContactConfirmation(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'src/contact_confirmation.html')
