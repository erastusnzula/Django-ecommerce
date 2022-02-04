from src.models.setting import Setting
from django.views.generic import ListView


class Setting(ListView):
    model = Setting
    template_name = 'src/setting.html'
