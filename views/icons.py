from django.shortcuts import render

from wagtail.admin.views.generic.multiple_upload import AddView as BaseAddView
from wagtail.images import get_image_model
from icons.fields import ALLOWED_EXTENSIONS
from wagtail.images.forms import get_image_form, get_image_multi_form
from wagtail.images.models import UploadedImage
from wagtail.images.permissions import permission_policy

from wagtail.documents import get_document_model
from wagtail.documents.forms import get_document_form, get_document_multi_form
from wagtail.documents.models import UploadedDocument
# from wagtail.documents.permissions import permission_policy
from wagtail.documents.models import UploadedDocument
from icons.models import Icon
from icons.forms import IconForm
from django.views.generic.base import TemplateView
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404


def index(request):

    return render(request, 'icons/icons_page/index.html')




class add(TemplateView):
    template_name = 'icons/icons_page/add.html'

    def post(self, request):
        print(request.POST)
        if request.POST.get('action') == 'upload':
            if not request.FILES:
                return HttpResponseBadRequest("Please upload a file")
            
            # get specified title or file title if specified doesn't exist
            file_title = request.POST.get('title') if request.POST.get('title') else request.FILES['file'].name.rsplit(".", 1)[0]
            form = IconForm({
                'title': file_title,
            },{
                'file': request.FILES['file'],
            })
            print(file_title)
            print(request.FILES['file'])

            if form.is_valid():
                # Save it
                icon = form.save(commit=False)
                icon.uploaded_by_user = self.request.user
                icon.file_size = icon.file.size
                icon.file.seek(0)
                icon.save()
                return JsonResponse({"icon_id":icon.id, "message":"Success"})
            

            return JsonResponse({"message":"Error"})
        elif request.POST.get('action') == 'update':
            return JsonResponse({"message":"Error"})
        elif request.POST.get('action') == 'delete':
            if Icon.objects.filter(id=request.POST.get('icon_id')):
                # delete_icon = Icon.objects.get(id=request.POST.get('icon_id'))
                delete_icon = get_object_or_404(Icon, id=request.POST.get('icon_id'))
                delete_icon.delete()
            return JsonResponse({"message":"Error"})
        else:
            return JsonResponse({"message":"Invalid action"})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = IconForm()

        context.update({
            'form': form,
        })

        return context