from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Equipment, Technical_Report, Technical_Specs, General_Specs
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from .forms import AddEquipment, AddGeneralSpecs, AddReport, AddTechSpecs
import itertools, datetime


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
                lookups = Q(equipment_name__equipment_name__icontains=query) | Q(technology_level__icontains=query) \
                          | Q(equipment_name__code__icontains=query)
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
            equipment = Equipment(code=request.POST.get('code', ''),
                                  equipment_name=request.POST.get('equipment_name', ''),
                                  speciality=request.POST.get('speciality', ''),
                                  purpose=request.POST.get('purpose', ''),
                                  picture=picture)

            for gene_item in itertools.zip_longest(name_general_list, value_general_list):
                general_spec = General_Specs(name=gene_item[0], value=gene_item[1])
                general_spec.save()
                general_specss = General_Specs.objects.get(pk=general_spec.id)
                equipment.save()
                equipment.general_specs.add(general_specss)

            for tech_item in itertools.zip_longest(name_technical_list, value_technical_list):
                technical_spec = Technical_Specs(name=tech_item[0], value=tech_item[1])
                technical_spec.save()
                tech_specss = Technical_Specs.objects.get(pk=technical_spec.id)
                equipment.save()
                equipment.technical_specs.add(tech_specss)

            report = Technical_Report(report_id=request.POST.get('report_id', ''),
                                      technology_level=request.POST.get('technology_level', ''),
                                      facility_level=request.POST.get('facility_level', ''),
                                      modification_date=request.POST.get('modification_date', ''),
                                      addition_date=request.POST.get('addition_date', ''))

            report.equipment_name = Equipment.objects.get(pk=equipment.code)
            report.save()

            messages.success(request, "Added Successfully")
            return redirect('http://127.0.0.1:8000/techspecs/allequipments/')

        except Exception as e:
            print(e)
            messages.success(request, "Check the form again:")
            return render(request, 'techspecs/add_equipment.html')
    else:
        return render(request, 'techspecs/add_equipment.html')



def all_equipments(request):
    all = Technical_Report.objects.all()
    return render(request, 'techspecs/all_equipments.html', {'all': all})

def test(request, id):
    device = Technical_Report.objects.get(pk=id)
    return render(request, 'techspecs/add_equipment.html', {'device': device})

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


def edit(request, id):
    global picture
    data = Technical_Report.objects.get(pk=id)
    data.equipment_name.general_specs.all().delete()
    data.equipment_name.technical_specs.all().delete()
    device = Technical_Report.objects.get(equipment_name__code=request.POST.get('code', ''))
    if request.method == 'POST':
        try:
            if request.FILES.get('picture') is not None:
                file = request.FILES['picture']
                fs = FileSystemStorage()
                picture = fs.save(file.name, file)
            else:
                picture = None
            if picture is not None:
                device.equipment_name.picture = picture

            device.equipment_name.code = request.POST.get('code')
            device.equipment_name.equipment_name = request.POST.get('equipment_name')
            device.equipment_name.speciality = request.POST.get('speciality')
            device.equipment_name.purpose = request.POST.get('purpose')
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
                device.equipment_name.general_specs.add(general_specss)
            for item in itertools.zip_longest(name_technical_list, value_technical_list):
                technical_spec = Technical_Specs(name=item[0], value=item[1])
                technical_spec.save()
                technical_specss = Technical_Specs.objects.get(pk=technical_spec.id)
                device.equipment_name.technical_specs.add(technical_specss)

            device.save()
            messages.success(request, "Updated Successfully")
            return redirect('http://127.0.0.1:8000/techspecs/update/'+str(device.report_id)+'')
        except Exception as e:
            print(e)
            messages.success(request, "Failed to update")
            return redirect('http://127.0.0.1:8000/techspecs/update/'+str(device.report_id)+'')
    else:
        return render(request, 'techspecs/update.html', {'device': device})
