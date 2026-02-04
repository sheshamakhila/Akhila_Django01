from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, label='Full Name')
    phone = forms.CharField(max_length=15, label="Phone Number")
    email = forms.EmailField(label='Email')
    address = forms.CharField(widget=forms.Textarea, label='Address')
    address_line1 = forms.CharField(max_length=255, label="Address Line 1")
    address_line2 = forms.CharField(max_length=255, label="Address Line 2", required=False)
    landmark = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=50)
    pin_code = forms.CharField(max_length=10)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)

    dob = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    payment_method = forms.ChoiceField(
        choices=[
            ('card', 'Credit/Debit Card'),
            ('paypal', 'PayPal'),
            ('cod', 'Cash on Delivery'),
            ('emi', 'EMI'),
        ],
        widget=forms.RadioSelect
    )

    emi_duration = forms.ChoiceField(
        choices=[
            ('12', '12 Months'),
            ('24', '24 Months'),
        ],
        required=False,
        label="EMI Duration"
    )

    card_number = forms.CharField(label='Card Number', max_length=16, min_length=13, required=False)
    expiry_date = forms.CharField(label='Expiry Date (MM/YY)', max_length=5, required=False)
    cvv = forms.CharField(label='CVV', max_length=4, required=False)
