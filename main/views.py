from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponseServerError, HttpResponse

from django.views.generic import CreateView

from .tasks import send_verification_email_to_user, send_verification_email_to_verificator, check_tasks

from datetime import datetime

from .forms import TaskModelForm
from .models import Task


class TaskCreateView(CreateView):
    template_name = 'index.html'
    form_class = TaskModelForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.obj = form.save()

        send_verification_email_to_user.apply_async(args=[self.obj.id])

        send_verification_email_to_verificator.apply_async(args=[self.obj.id])

        return super().form_valid(form)

    def form_invalid(self, form):
        form.errors
        print(form.errors)
        return super().form_invalid(form)


def verify_task(request: HttpRequest, id):
    try:
        task = Task.objects.get(id = id)
        if task.deadline > datetime.today().date():
            task.verified = True
            task.save()
            return render(request, 'verification.html', {'task': task, 'message': 'Successfully verified! Thanks!'})
        else:
            return render(request, 'verification.html', {'task': task, 'message': 'Deadline is over. Sorry :('})
    except Exception as e:
        print(e)
        return HttpResponseServerError()
