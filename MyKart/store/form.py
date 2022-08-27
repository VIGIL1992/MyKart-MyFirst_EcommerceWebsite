from django import forms
from store.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ 
            'product_name',
            'slug',
            'brand', 
            'category',
            'description', 
            'price', 
            'stock',
            'images',
            'image2',
            'image3',
            'image4',
            
                ]
        prepopulated_fields = {'slug': ('product_name',)}


        widgets = {
            'product_name'  : forms.TextInput(attrs={'class': 'form-control'}),
            'slug'          : forms.TextInput(attrs={'class': 'form-control'}),
            'description'   : forms.Textarea(attrs={'class': 'form-control'}),
            'brand'         : forms.Select(attrs={'class': 'form-control'}),
            'category'      : forms.Select(attrs={'class': 'form-control'}),
            'price'         : forms.NumberInput(attrs={'class': 'form-control'}),
            'stock'         : forms.NumberInput(attrs={'class': 'form-control'}),
            
            'images'        : forms.FileInput(attrs={'class': 'form-control'}),
            'image2'        : forms.FileInput(attrs={'class': 'form-control'}),
            'image3'        : forms.FileInput(attrs={'class': 'form-control'}),
            'image4'        : forms.FileInput(attrs={'class': 'form-control'}),
        }