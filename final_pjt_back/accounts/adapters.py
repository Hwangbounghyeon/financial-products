from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.nick_name = form.cleaned_data.get('nick_name')
        user.financial_products = form.cleaned_data.get('financial_products')
        user.age = form.cleaned_data.get('age')
        user.money = form.cleaned_data.get('money')
        user.salary = form.cleaned_data.get('salary')
        user.profile_image = form.cleaned_data.get('profile_image')
        user.save()
        return user