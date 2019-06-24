#Aquí se declaran todos los formularios que va a buscar Python. La plantilla solamente muestra la información de
#las tablas, por lo que aquí recogerá Django la información para que sea mostrada mediante las plantillas

from django import forms

from catalogos.models import Categoria, SubCategoria, Producto

class CategoriaForm(forms.ModelForm):
    class Meta:
        model=Categoria
        fields = ['descripcion','activo']
        labels = {'descripcion': "Descripción de la categoría",
                  "activo":"Estado"
                 }
        widget ={'descripcion':forms.TextInput()}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class SubCategoriaForm(forms.ModelForm):
    # Esta porción de código se encarga de que no se muestren las categorías
    # con estado inactivo entre las opciones disponibles cuando se crea una 
    # subcategoría. Además, ordena las categorías disponibles en orden
    # alfabético

    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(activo=True).
                 order_by('descripcion')
    )
    # Fin del código que filtra y ordena las categorías para las subcategorías

    class Meta:
        model=SubCategoria
        fields = ['categoria','descripcion','activo']
        labels = {
            'categoria':'Categoria',
            'descripcion': "Descripción de la Sub categoría",
            'activo':"Estado"
                 }
        widget ={'descripcion':forms.TextInput()}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        # Mensaje default previo a seleccionar categoría en el
        # formulario de agregar o editar subcategoría    
        self.fields['categoria'].empty_label="Seleccione Categoría" 


class ProductoForm(forms.ModelForm):
    subcategoria = forms.ModelChoiceField(
        queryset=SubCategoria.objects.filter(activo=True).
                 order_by('categoria__descripcion','descripcion'),
                 empty_label="Seleccione Sub Categoría"
    )
    class Meta:
        model=Producto
        fields = '__all__'
       
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

