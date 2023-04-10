from .models import UserAccount
from .forms import UserAccountForm, EditUserAccountForm, LoginForm
from django.views.generic import CreateView, UpdateView, FormView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class AddUserAccount(CreateView):
    model = UserAccount
    template_name = 'account/userAccount-add.html'
    form_class = UserAccountForm
    success_url = reverse_lazy('ArticleList')

    def get_form_kwargs(self):
        kwargs = super(AddUserAccount, self).get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs





class EditUserAccount(LoginRequiredMixin, UpdateView):
    model = UserAccount
    template_name = 'account/userAccount-edit.html'
    form_class = EditUserAccountForm
    success_url = reverse_lazy('ArticleList')

    def get_form_kwargs(self):
        kwargs = super(EditUserAccount, self).get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs






class Login(FormView):
    form_class = LoginForm
    template_name = 'account/userAccount-login.html'
    success_url = reverse_lazy('ArticleList')

    def form_valid(self, form):

        email = form.cleaned_data.get('email')
        passsword = form.cleaned_data.get('password')

        try:
            user = UserAccount.objects.get(emali__iexact = email)
        except UserAccount.DoesNotExist:
            form.add_error('email', "حسابی با این ایمیل وجود ندارد.")
        else:
            user = authenticate(self.request, email=email, passsword=passsword)
            if user is None:
                form.add_error('password', "رمز وارد شده نادرست است.")
            else:
                login(self.request, user)
            
        return super().form_valid(form)





class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'account/userAccount-logout.html'
    next_page = reverse_lazy('ArticleList')