from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from catalogos.models import Categoria, SubCategoria, Producto
from catalogos.forms import CategoriaForm, SubCategoriaForm, ProductoForm
from generales.views import SinPrivilegios



class CategoriaView(LoginRequiredMixin, generic.ListView):
    model = Categoria
    template_name = "catalogos/categoria_list.html"
    context_object_name = "obj"
    login_url = 'generales:login'

class CategoriaNew(SuccessMessageMixin, LoginRequiredMixin, SinPrivilegios, 
                   generic.CreateView):
    permission_required = "catalogos.add_categoria"
    model = Categoria
    template_name = "catalogos/categoria_form.html"
    context_object_name = "obj"
    form_class= CategoriaForm
    success_url = reverse_lazy("catalogos:categoria_list")
    success_message="Categoría Creada Satisfactoriamente"

class CategoriaEdit(SuccessMessageMixin, LoginRequiredMixin, SinPrivilegios, generic.UpdateView):
    permission_required = "catalogos.change_categoria"
    model = Categoria
    template_name = "catalogos/categoria_form.html"
    context_object_name = "obj"
    form_class= CategoriaForm
    success_url = reverse_lazy("catalogos:categoria_list")
    success_message = "Categoría Actualizada Satisfactoriamente"


class CategoriaDel(LoginRequiredMixin, SinPrivilegios, generic.DeleteView):
    permission_required = "catalogos.delete_categoria"
    model = Categoria
    template_name = "catalogos/catalogos_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("catalogos:categoria_list")

class SubCategoriaView(LoginRequiredMixin, generic.ListView):
    model = SubCategoria
    template_name = "catalogos/subcategoria_list.html"
    context_object_name = "obj"
    login_url = 'generales:login'

class SubCategoriaNew(SuccessMessageMixin, LoginRequiredMixin, SinPrivilegios, 
                   generic.CreateView):
    permission_required = "catalogos.add_subcategoria"
    model = SubCategoria
    template_name = "catalogos/subcategoria_form.html"
    context_object_name = "obj"
    form_class= SubCategoriaForm
    success_url = reverse_lazy("catalogos:subcategoria_list")
    success_message="Sub Categoría Creada Satisfactoriamente"

class SubCategoriaEdit(SuccessMessageMixin, LoginRequiredMixin, SinPrivilegios, generic.UpdateView):
    permission_required = "catalogos.change_subcategoria"
    model = SubCategoria
    template_name = "catalogos/subcategoria_form.html"
    context_object_name = "obj"
    form_class= SubCategoriaForm
    success_url = reverse_lazy("catalogos:subcategoria_list")
    success_message = "Sub Categoría Actualizada Satisfactoriamente"

class SubCategoriaDel(LoginRequiredMixin, SinPrivilegios, generic.DeleteView):
    permission_required = "catalogos.delete_subcategoria"
    model = SubCategoria
    template_name = "catalogos/catalogos_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("catalogos:subcategoria_list")

class ProductoView(LoginRequiredMixin, generic.ListView):
    model = Producto
    template_name = "catalogos/producto_list.html"
    context_object_name = "obj"
    login_url = 'generales:login'

class ProductoNew(SuccessMessageMixin, LoginRequiredMixin, SinPrivilegios, 
                   generic.CreateView):
    permission_required = "catalogos.producto"
    model = Producto
    template_name = "catalogos/producto_form.html"
    context_object_name = "obj"
    form_class= ProductoForm
    success_url = reverse_lazy("catalogos:producto_list")
    success_message="Producto Creado Satisfactoriamente"

class ProductoEdit(SuccessMessageMixin, LoginRequiredMixin, SinPrivilegios, generic.UpdateView):
    permission_required = "catalogos.change_producto"
    model = Producto
    template_name = "catalogos/producto_form.html"
    context_object_name = "obj"
    form_class= ProductoForm
    success_url = reverse_lazy("catalogos:producto_list")
    success_message = "Producto Modificado Satisfactoriamente"

class ProductoDel(LoginRequiredMixin, SinPrivilegios, generic.DeleteView):
    permission_required = "catalogos.delete_producto"
    model = Producto
    template_name = "catalogos/catalogos_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("catalogos:producto_list")

def categoria_print(self, pk=None):
    import io
    from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter

    # Qué tipo de salida me dará el método
    response  = HttpResponse(content_type='application/pdf')
    buff=io.BytesIO()
    doc=SimpleDocTemplate(buff, 
                          pagesize=letter,
                          rightMargin=40,
                          leftMargin=40,
                          topMargin=60,
                          bottomMargin=18,
                          )

    categorias=[]
    styles=getSampleStyleSheet()
    header=Paragraph("Listado de Categorías", styles['Heading1'])
    categorias.append(header)
    #Tuple con los títulos de una tabla que se creará
    headings=('Id','Descripción','Activo','Creación')
    #Ahora necesitamos los registros que vamos a mostrar
    if not pk:
        #Devolver una lista solamente con 4 propiedades del modelo:
        # id, descripcion, activo y creado
        todascategorias= [(p.id, p.descripcion, p.activo, p.creado)
                   for p in Categoria.objects.all().order_by('pk')
        ]
    else:
        #Filtrar donde id=pk
         todascategorias= [(p.id, p.descripcion, p.activo, p.creado)
                   for p in Categoria.objects.filter(id=pk)
         ]

    t=Table([headings] + todascategorias)
    #Darle colores a la tabla
    t.setStyle(TableStyle(
        [
            ('GRID',(0,0),(3,-1),1, colors.dodgerblue),
            ('LINEBELOW',(0,0),(-1,0),2, colors.darkblue),
            ('BACKGROUND',(0,0),(-1,0), colors.dodgerblue)
        ]
    ))
    # Agregar contenido de tabla a la lista categorias
    categorias.append(t)
    doc.build(categorias)
    #Mandar info a la pantalla
    response.write(buff.getvalue())
    buff.close()
    return response
    









