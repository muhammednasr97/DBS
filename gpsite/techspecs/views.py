from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Equipment, Technical_Report, Technical_Specs, General_Specs
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from .forms import AddEquipment, AddGeneralSpecs, AddReport, AddTechSpecs


def index(request):
    global lookups
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            if query == 'all':
                all = Technical_Report.objects.all()
                return render(request, 'techspecs/index.html', {'all': all})

            else:
                lookups = Q(equipment_name__equipment_name__icontains=query) | Q(technology_level__icontains=query) \
                          | Q(equipment_name__code__icontains=query)
                print(lookups)
                results = Technical_Report.objects.filter(lookups).distinct()

                context = {'results': results,
                           'submitbutton': submitbutton}
                return render(request, 'techspecs/index.html', context)
        else:
            return render(request, 'techspecs/index.html')
    else:
        return render(request, 'techspecs/index.html')


def detail(request, id):
    device = get_object_or_404(Technical_Report, pk=id)
    return render(request, 'techspecs/detail.html', {'device': device})


def add_equipment(request):
    if request.method == 'POST':
        file = request.FILES['picture']
        fs = FileSystemStorage()
        profile_img = fs.save(file.name, file)
        try:
            #general_specs = Technical_Report.objects.get(equipment_name=request.POST.get('gene_name', ''))
            # technical_specs = Technical_Specs.objects.get(name=request.POST.get('technical_specs', ''))
            equipment = Equipment(code=request.POST.get('code', ''),
                                  equipment_name=request.POST.get('equipment_name', ''),
                                  speciality=request.POST.get('speciality', ''),
                                  purpose=request.POST.get('purpose', ''),
                                  picture=profile_img, general_specs=request.POST.get('gene_name', ''))
            equipment.save()

            name_general_list = request.POST.getlist('name')
            value_general_list = request.POST.getlist('value')
            for name in name_general_list:
                general_specs_name = General_Specs(name=name)
                general_specs_name.save()
            for value in value_general_list:
                general_specs_name = General_Specs(value=value)
                general_specs_name.save()

            messages.success(request, "Added Successfully")
            return render(request, 'techspecs/add_equipment.html')
        except Exception as e:
            print(e)
            messages.error(request, "Failed to Add Equipment")
            return render(request, 'techspecs/add_equipment.html')
    else:
        return render(request, 'techspecs/add_equipment.html')


def data(request):
    data = General_Specs.objects.all()
    return render(request, 'techspecs/add_equipment.html', {'data': data})


def all_equipment(request):
    all = Equipment.objects.all()
    return render(request, 'techspecs/all_equipments.html', {'all': all})


def add_report(request):
    if request:
        data = Equipment.objects.all()
        return render(request, 'techspecs/add_report.html', {'data': data})
    if request.method == 'POST':
        form = AddReport(request.POST or None)
        if form.is_valid():
            form.save()
        return render(request, 'techspecs/all_equipments.html')
    else:
        return render(request, 'techspecs/add_equipment.html')


def add_tech_specs(request):
    if request.method == 'POST':
        form = AddTechSpecs(request.POST or None)
        if form.is_valid():
            form.save()
        return render(request, 'techspecs/add_tech_specs.html')
    else:
        return render(request, 'techspecs/add_tech_specs.html')


def add_general_specs(request):
    if request.method == 'POST':
        form = AddGeneralSpecs(request.POST or None)
        if form.is_valid():
            form.save()
            return render(request, 'techspecs/add_general_specs.html')
    else:
        return render(request, 'techspecs/add_general_specs.html')


def test(request):
    return render(request, 'techspecs/JS.html')
