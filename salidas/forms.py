from django import forms

from django.forms.models import inlineformset_factory

from salidas.models import FacturaEnc, FacturaDet
from catalogos.models import Producto

class FacturaEncForm(forms.ModelForm):
    fecha_factura = forms.DateInput()

    class Meta:
        model = FacturaEnc
        fields = ['fecha_factura','observacion']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class FacturaDetForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset= Producto.objects.filter(activo=True).
        order_by('descripcion'),
        empty_label="Seleccione Producto"
    )   
    
    class Meta:
        model = FacturaDet
        fields = ['producto', 'cantidad',
                 'precio','total'
                 ]
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        #La variable total no puede ser modificada, solo leida
        self.fields['total'].widget.attrs['readonly']=True 

    def clean_cantidad(self):
        cantidad = self.cleaned_data["cantidad"]
        if not cantidad:
            raise forms.ValidationError("Cantidad Requerida")
        elif cantidad <= 0:
            raise forms.ValidationError("Cantidad Incorrecta")
        return cantidad

    def clean_precio(self):
        precio = self.cleaned_data["precio"]
        if not precio:
            raise forms.ValidationError("Precio Requerido")
        if precio <= 0:
            raise forms.ValidationError("Precio Incorrecto")
        return precio

# inlineformset sirve para para mezclar un formulario que este vinculado entre el encabezado
# y el detalle.
# Pide el modelo padre, luego el modelo que se va a repetir y luego el formulario que queremos 
# reproducir

DetalleFacturaFormSet = inlineformset_factory(FacturaEnc, FacturaDet, 
                        form=FacturaDetForm, extra=3)