from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Technical_Report, Technical_Specs, General_Specs, Technical_Report_Copy
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import itertools
from django.http import HttpResponse
from .utils import render_to_pdf


def search(request):
    global lookups
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            if query == 'all':
                all = Technical_Report.objects.all()
                return render(request, 'techspecs/search.html', {'all': all})

            else:
                lookups = Q(equipment_name__icontains=query) | Q(technology_level__icontains=query) \
                          | Q(code__icontains=query)
                print(lookups)
                results = Technical_Report.objects.filter(lookups).distinct()

                context = {'results': results,
                           'submitbutton': submitbutton}
                return render(request, 'techspecs/search.html', context)
        else:
            return render(request, 'techspecs/search.html')
    else:
        return render(request, 'techspecs/search.html')


def detail(request, id):
    device = get_object_or_404(Technical_Report, pk=id)
    return render(request, 'techspecs/detail.html', {'device': device})


def add_equipment(request):
    if request.method == 'POST':
        try:
            file = request.FILES['picture']
            fs = FileSystemStorage()
            picture = fs.save(file.name, file)
            name_general_list = request.POST.getlist('gene_name')
            value_general_list = request.POST.getlist('gene_value')
            name_technical_list = request.POST.getlist('tech_name')
            value_technical_list = request.POST.getlist('tech_value')
            equipment = Technical_Report(
                                         technology_level=request.POST.get('technology_level', ''),
                                         facility_level=request.POST.get('facility_level', ''),
                                         modification_date=request.POST.get('modification_date', ''),
                                         addition_date=request.POST.get('addition_date', ''),
                                         code=request.POST.get('code', ''),
                                         version=request.POST.get('report_version', ''),
                                         equipment_name=request.POST.get('equipment_name', ''),
                                         speciality=request.POST.get('speciality', ''),
                                         purpose=request.POST.get('purpose', ''),
                                         picture=picture)

            equipment_copy = Technical_Report_Copy(id=equipment.id,
                                                   technology_level=request.POST.get('technology_level', ''),
                                                   facility_level=request.POST.get('facility_level', ''),
                                                   modification_date=request.POST.get('modification_date', ''),
                                                   addition_date=request.POST.get('addition_date', ''),
                                                   code=request.POST.get('code', ''),
                                                   version=request.POST.get('report_version', ''),
                                                   equipment_name=request.POST.get('equipment_name', ''),
                                                   speciality=request.POST.get('speciality', ''),
                                                   purpose=request.POST.get('purpose', ''),
                                                   picture=picture)

            for gene_item in itertools.zip_longest(name_general_list, value_general_list):
                general_spec = General_Specs(name=gene_item[0], value=gene_item[1])
                general_spec.save()
                general_specss = General_Specs.objects.get(pk=general_spec.id)
                equipment.save()
                equipment_copy.save()
                equipment.general_specs.add(general_specss)
                equipment_copy.general_specs.add(general_specss)
                equipment.save()
                equipment_copy.save()

            for tech_item in itertools.zip_longest(name_technical_list, value_technical_list):
                technical_spec = Technical_Specs(name=tech_item[0], value=tech_item[1])
                technical_spec.save()
                tech_specss = Technical_Specs.objects.get(pk=technical_spec.id)
                equipment.save()
                equipment_copy.save()
                equipment.technical_specs.add(tech_specss)
                equipment_copy.technical_specs.add(tech_specss)
                equipment.save()
                equipment_copy.save()

            messages.success(request, "Added Successfully")
            return redirect('http://127.0.0.1:8000/techspecs/allequipments/')

        except Exception as e:
            print(e)
            messages.success(request, "Check the form again:")
            return render(request, 'techspecs/add_equipment.html')
    else:
        return render(request, 'techspecs/add_equipment.html')


def all_equipments(request):
    all = Technical_Report.objects.all().order_by('version')
    return render(request, 'techspecs/all_equipments.html', {'all': all})


def home(request):
    return render(request, 'techspecs/home.html')


def about(request):
    return render(request, 'techspecs/about.html')


def delete(request, id):
    device = get_object_or_404(Technical_Report, pk=id)
    if request.method == 'POST':
        device.delete()
        return redirect('http://127.0.0.1:8000/techspecs/allequipments/')
    return render(request, 'techspecs/delete.html', {'device': device})


def data_to_update(request, id):
    device = Technical_Report.objects.get(pk=id)
    return render(request, 'techspecs/update.html', {'device': device})


def edit(request, id, version):
    global picture
    data = Technical_Report.objects.get(pk=id)
    dev_copy = Technical_Report_Copy.objects.get(pk=id)
    device_copy = Technical_Report_Copy()
    device_copy.id = data.id
    device_copy.version = data.version
    device_copy.picture = data.picture
    device_copy.code = data.code
    device_copy.equipment_name = data.equipment_name
    device_copy.speciality = data.speciality
    device_copy.purpose = data.purpose
    device_copy.technology_level = data.technology_level
    device_copy.facility_level = data.facility_level
    device_copy.addition_date = data.addition_date
    device_copy.modification_date = data.modification_date
    dev_copy.general_specs.all().delete()
    dev_copy.technical_specs.all().delete()
    gene = data.general_specs.all()
    tech = data.technical_specs.all()
    for item in gene:
        general_spec = General_Specs(name=item.name, value=item.value)
        general_spec.save()
        device_copy.save()
        general_specss = General_Specs.objects.get(pk=general_spec.id)
        device_copy.general_specs.add(general_specss)
    for item in tech:
        technical_spec = Technical_Specs(name=item.name, value=item.value)
        technical_spec.save()
        device_copy.save()
        technical_specss = Technical_Specs.objects.get(pk=technical_spec.id)
        device_copy.technical_specs.add(technical_specss)

    device_copy.save()

    data.general_specs.all().delete()
    data.technical_specs.all().delete()
    device = Technical_Report.objects.get(pk=id)
    if request.method == 'POST':
        try:
            if request.FILES.get('picture') is not None:
                file = request.FILES['picture']
                fs = FileSystemStorage()
                picture = fs.save(file.name, file)
                print(file.name)
                device.picture = picture
            else:
                picture = None

            device.version = version + 1
            device.code = request.POST.get('code')
            device.equipment_name = request.POST.get('equipment_name')
            device.speciality = request.POST.get('speciality')
            device.purpose = request.POST.get('purpose')
            device.technology_level = request.POST.get('technology_level')
            device.facility_level = request.POST.get('facility_level')
            device.addition_date = request.POST.get('addition_date')
            device.modification_date = request.POST.get('modification_date')
            name_general_list = request.POST.getlist('gene_name')
            value_general_list = request.POST.getlist('gene_value')
            name_technical_list = request.POST.getlist('tech_name')
            value_technical_list = request.POST.getlist('tech_value')
            for item in itertools.zip_longest(name_general_list, value_general_list):
                general_spec = General_Specs(name=item[0], value=item[1])
                general_spec.save()
                general_specss = General_Specs.objects.get(pk=general_spec.id)
                device.general_specs.add(general_specss)

            for item in itertools.zip_longest(name_technical_list, value_technical_list):
                technical_spec = Technical_Specs(name=item[0], value=item[1])
                technical_spec.save()
                technical_specss = Technical_Specs.objects.get(pk=technical_spec.id)
                device.technical_specs.add(technical_specss)

            device.save()

            messages.success(request, "Updated Successfully")
            return redirect('http://127.0.0.1:8000/techspecs/allequipments/')
        except Exception as e:
            print(e)
            messages.success(request, "Failed to update")
            return redirect('http://127.0.0.1:8000/techspecs/update/' + str(device.id) + '')
    else:
        return render(request, 'techspecs/update.html', {'device': device})


def archive(request, id):
    device = get_object_or_404(Technical_Report, pk=id)
    return redirect('http://127.0.0.1:8000/techspecs/compare/' + str(device.id) + '')


def archive_view(request, id):
    new_device = Technical_Report.objects.get(pk=id)
    device = Technical_Report_Copy.objects.get(pk=id)
    return render(request, 'techspecs/compare.html', {'new_device': new_device, 'device': device})


def gen_pdf(request, id):
    device = get_object_or_404(Technical_Report, pk=id)
    pdf = render_to_pdf('techspecs/pdf_template.html', {'device': device})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "%s.pdf" %(device.equipment_name)
        content = "inline; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
