from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin

from .models import FacturaEnc, FacturaDet
from .forms import FacturaEncForm, FacturaDetForm, DetalleFacturaFormSet
from generales.views import SinPrivilegios


class FacturaList(LoginRequiredMixin, generic.ListView):
    login_url = 'generales:login'
    model=FacturaEnc
    template_name= "salidas/facturas_list.html"
    context_object_name= "facturas"


class FacturaNew(SinPrivilegios, generic.CreateView):
    permission_required='salidas.add_facturaenc'
    model= FacturaEnc
    login_url = 'generales:home'
    template_name = 'salidas/factura_form.html'
    form_class = FacturaEncForm
    success_url = reverse_lazy('salidas:factura_list')

    def get(self, request, *args, **kwargs):
        #Por default, al crear una nueva factura, que el object este vacio, o sea nulo
        self.object = None 
        #Instanciar el formulario que hace la facturacion.Variable que contiene quien es FacturaEncForm
        form_class = self.get_form_class()
        #Formulario que se va a cargar con el contenido de form_class
        form = self.get_form(form_class)
        #Instanciar el formSet
        detalle_factura_formset = DetalleFacturaFormSet()
        #Renderizar formulario del encabezado y del conjunto Formulario
        return self.render_to_response(
            #Para poder enviar un objeto o variable al formulario, o de la vista enviarle algo a la plantilla
            # Todo esto es para indicar que se cargue el formulario vacio
            self.get_context_data(
                #Variable que se inicializa con el contenido del formulario Encabezado
                form=form,
                #Variable que se inicializa con el contenido del detalle facturaFormSet
                detalle_factura=detalle_factura_formset
            )
        )
    
    def post(self, request, *args, **kwargs):
        # Obtener nuevamente las instancia del formulario de facturacion
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #Obtener el conjunto formulario, pero ahora ya con lo que se paso en el Post
        detalle_factura = DetalleFacturaFormSet(request.POST)

        #Metodos para validar el formulario de encabezado y el formulario de detalle:
        # metodo form_valid o metodo form_invalid
        if form.is_valid() and detalle_factura.is_valid():
            return self.form_valid(form,detalle_factura)
        else:
            return self.form_invalid(form, detalle_factura)

#Sobreescribir metodos form_valid y form_invalid para personalizarlos
    def form_valid(self, form, detalle_factura):
        #Guardar el formulario encabezado
        self.object = form.save()
        #Crear instancia del conjunto de formularios que este vinculado con 
        #formulario encabezado, y guardar
        detalle_factura.instance = self.object
        detalle_factura.save()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, detalle_factura):
        #Si hay error, volver a mandar los objetos como estaban antes de intentar 
        # modificarlos
        return self.render_to_response(
            self.get_context_data(
                form=form,
                detalle_factura=detalle_factura
            )
        )


class FacturaEdit(SinPrivilegios, generic.UpdateView):
    permission_required='salidas.change_facturaenc'
    model= FacturaEnc
    login_url = 'generales:home'
    template_name = 'salidas/factura_form.html'
    form_class = FacturaEncForm
    success_url = reverse_lazy('salidas:factura_list')


    def get_success_url(self):
        from django.urls import reverse
        return reverse('salidas:factura_edit',
                       kwargs={'pk' : self.get_object().id})


    def get(self, request, *args, **kwargs):
        #Recargar el formulario como estaba
        self.object = self.get_object()
        #Instanciar el formulario que hace la facturacion.Variable que contiene quien es FacturaEncForm
        form_class = self.get_form_class()
        #Formulario que se va a cargar con el contenido de form_class.Form como una instancia
        #  del formulario
        form = self.get_form(form_class)
        # Filtro de todas las facturas que sean igual al object que se inicializo
        detalles = FacturaDet.objects.filter(factura = self.object).order_by('pk')
        #Crear una lista vacia
        detalles_data=[]
        #Crear un diccionario con los campos de la factura
        for detalle in detalles:
            d = {
                'producto': detalle.producto,
                'cantidad': detalle.cantidad,
                'precio': detalle.precio,
                'total': detalle.total
            }
            #Ingresar el diccionario a la lista, para tener todos los registros de detalle en una lista
            detalles_data.append(d)

        detalle_factura = DetalleFacturaFormSet(initial= detalles_data)
        #Sumarle el numero de campos ingresados en la lista al parametro extra
        detalle_factura.extra += len(detalles_data)
        #Renderizar formulario del encabezado y del conjunto Formulario
        return self.render_to_response(
            #Para poder enviar un objeto o variable al formulario, o de la vista enviarle algo a la plantilla
            # Todo esto es para indicar que se cargue el formulario vacio
            self.get_context_data(
                #Variable que se inicializa con el contenido del formulario Encabezado
                form=form,
                #Variable que se inicializa con el contenido del detalle facturaFormSet
                detalle_factura=detalle_factura
            )
        )
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Obtener nuevamente las instancia del formulario de facturacion
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #Obtener el conjunto formulario, pero ahora ya con lo que se paso en el Post
        detalle_factura = DetalleFacturaFormSet(request.POST)

        #Metodos para validar el formulario de encabezado y el formulario de detalle:
        # metodo form_valid o metodo form_invalid
        if form.is_valid() and detalle_factura.is_valid():
            return self.form_valid(form,detalle_factura)
        else:
            return self.form_invalid(form, detalle_factura)

#Sobreescribir metodos form_valid y form_invalid para personalizarlos
    def form_valid(self, form, detalle_factura):
        #Guardar el formulario encabezado
        self.object = form.save()
        #Crear instancia del conjunto de formularios que este vinculado con 
        #formulario encabezado, y guardar
        detalle_factura.instance = self.object
        #Ir a donde estan los registros anteriores guardados, borrarlos y crear unos nuevos.
        FacturaDet.objects.filter(factura=self.object).delete()
        detalle_factura.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, detalle_factura):
        #Si hay error, volver a mandar los objetos como estaban antes de intentar 
        # modificarlos
        return self.render_to_response(
            self.get_context_data(
                form=form,
                detalle_factura=detalle_factura
            )
        )


class FacturaDel(SinPrivilegios, generic.DeleteView):
  permission_required = 'salidas:delete_facturaenc'
  model = FacturaEnc
  template_name="salidas/factura_del.html"
  context_object_name = 'obj'
  success_url = reverse_lazy("salidas:factura_list")

