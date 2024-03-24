from django import forms

class SignupForm(forms.Form):
    fname = forms.CharField(label='Prenom', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre prénom '}))
    lname = forms.CharField(label='Nom', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre nom'}))
    email = forms.EmailField(label='Adresse email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre email'}))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe'}))
    accept_terms = forms.BooleanField(label="J'accepte les termes et conditions", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'checkbox-signup'}))


class LoginForm(forms.Form):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',"placeholder": "Votre addresse email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder": "Votre mode passe"}))