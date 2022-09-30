from django import forms
from store.models import Product, ProductGallery

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
       
            
                ]
        prepopulated_fields = {'slug': ('product_name',)}


        widgets = {
            'product_name'  : forms.TextInput(attrs={'class': 'form-control slug-tittle'}),
            'slug'          : forms.TextInput(attrs={'class': 'form-control set-slug'}),
            'description'   : forms.Textarea(attrs={'class': 'form-control'}),
            'brand'         : forms.Select(attrs={'class': 'form-control'}),
            'category'      : forms.Select(attrs={'class': 'form-control'}),
            'price'         : forms.NumberInput(attrs={'class': 'form-control'}),
            'stock'         : forms.NumberInput(attrs={'class': 'form-control'}),
            
            'images'        : forms.FileInput(attrs={'class': 'form-control'}),
            
        }
        
class ProductGalleryForm(forms.ModelForm):
    class Meta:
        model = ProductGallery
        fields = [
            "product",
            "image",
        ]
        widgets = {
            'product':forms.Select(attrs={'class':'form-control'}),
        }