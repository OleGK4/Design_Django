from django import forms
from django.contrib.messages import debug
from django.core.exceptions import ValidationError
from django.forms import TextInput

from .models import User, Order
from .models import user_registrated


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput, )
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput,
                                help_text='Повторите тот же самый пароль еще раз')

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch'
            )}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = User
        fields = ('name', 'surname', 'patronymic', 'username', 'email', 'password1', 'password2')


class UpdateOrderForm(forms.ModelForm):
    LOAN_STATUS = (
        ('n', 'Новая'),
        ('a', 'Принято в работу'),
        ('c', 'Выполнено'),
    )
    status = forms.ChoiceField(label='Статус заявки', help_text='Статус', widget=forms.Select, choices=LOAN_STATUS)
    img = forms.ImageField(label='Фото работы', required=False)
    comment = forms.CharField(label='Ваше описание', required=False, help_text='Комментарий')

    def clean(self):
        super().clean()
        print(self.cleaned_data)

        status = self.cleaned_data.get('status')
        comment = self.cleaned_data.get('comment')
        img = self.cleaned_data.get('img')
        if status == 'a' and comment == '':
            errors = {'status': ValidationError(
                'После изменения статуса на принят в работу нужно добавить комментарий'
            )}
            raise ValidationError(errors)
        elif status == 'c' and img is None:
            errors = {'status': ValidationError(
                'После изменения статуса на выполнено нужно добавить фото'
            )}
            raise ValidationError(errors)
        elif status == 'n':
            errors = {'status': ValidationError(
                'Вы не можете изменить статус на новый'
            )}
            raise ValidationError(errors)

    class Meta:
        model = Order
        fields = ('status', 'img', 'comment')
