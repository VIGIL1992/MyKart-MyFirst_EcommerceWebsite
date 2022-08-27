from django import forms
from category.models import Brand, Category 

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = [ 
            'brand_name',          
            'slug',
            'description',
            'brand_logo',
            
        ]
        
        prepopulated_fields = {'slug': ('brand_name',)}
        
             
        
        widgets = {
            'brand_name'    : forms.TextInput(attrs={'class': 'form-control'}),
            'slug'          : forms.TextInput(attrs={'class': 'form-control'}),
            'description'   : forms.Textarea(attrs={'class': 'form-control'}),
            'brand_logo'    : forms.FileInput(attrs={'class': 'form-control'}),
            
        }




class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [ 
            'category_name',          
            'slug',
            'description',
            'cat_image',
            
        ]
        
        prepopulated_fields = {'slug': ('category_name',)}
        
        widgets = {
            'category_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'slug'          : forms.TextInput(attrs={'class': 'form-control'}),
            'description'   : forms.Textarea(attrs={'class': 'form-control'}),
            'cat_image'     : forms.FileInput(attrs={'class': 'form-control'}),
            
        }