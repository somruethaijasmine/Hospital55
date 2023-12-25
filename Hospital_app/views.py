from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    return render(request,'base.html')

def index(request):
    drugs = drug.objects.all()
    drug_types = d_type.objects.all()
    context = {"drugs": drugs, "drug_types": drug_types}
    return render(request, 'index.html', context)

@login_required(login_url="/login")
def buy_drug(request):
    if request.method == "POST":
        drug_id = request.POST['drug_name']
        qty = int(request.POST['qty_drug'])
        user = request.user

        try:
            selected_drug = drug.objects.get(drug_id=drug_id)

            if selected_drug.drug_qty >= qty:
                # เบิกยาได้
                selected_drug.drug_qty -= qty
                selected_drug.save()

                # เพิ่มประวัติการเบิกยา
                MedicationHistory.objects.create(
                    drug_name=selected_drug.drug_name,
                    quantity=qty,
                    user=user
                )

                messages.success(request, f'เบิกยา {selected_drug.drug_name} จำนวน {qty} หน่วย เรียบร้อย!')
            else:
                # เบิกยาไม่ได้ เนื่องจากจำนวนยาไม่เพียงพอ
                messages.error(request, 'เบิกยาไม่ได้ จำนวนยาไม่เพียงพอ')
        except drug.DoesNotExist:
            # หากยาที่ต้องการเบิกไม่มีในระบบ
            messages.error(request, 'ยาที่ต้องการเบิกไม่มีในระบบ')

    table = drug.objects.all()
    context = {"drugdata": table}
    return render(request, 'buy_drug.html', context)

@login_required(login_url="/login")
def add_drug(request):
    context = {"drug_type" : d_type.objects.all()}
    if request.method == "POST":
        table = drug()
        table.drug_name = request.POST['drug_name']
        table.drug_type = d_type.objects.get(type_id = request.POST['drug_type'])
        table.drug_qty = request.POST['drug_qty']
        table.drug_exp = request.POST['drug_expired']
        table.save()
        return redirect('/manage_drug')
    return render(request,'add_drug.html',context)

@login_required(login_url="/login")
def add_type(request):
    if request.method == "POST":
        table = d_type()
        table.type_name = request.POST['type_name']
        table.save()
        return redirect('/manage_type')
    return render(request,'add_type.html')

def manage_drug(request):
    show_drug = drug.objects.all()
    context  = {"drug" : show_drug}
    return render(request,'edit_drug.html',context)

def manage_type(request):
    show_type = d_type.objects.all()
    context  = {"type" : show_type}
    return render(request,'manage_type.html',context)

@login_required(login_url="/login")
def delete_drug(request,pk):
    table = drug.objects.get(drug_id=pk)
    table.delete()
    return redirect('/manage_drug')

@login_required(login_url="/login")
def delete_type(request,pk):
    table = d_type.objects.get(type_id=pk)
    table.delete()
    return redirect('/manage_type')

@login_required(login_url="/login")
def edit_drug(request,pk):
    table = drug.objects.get(drug_id=pk)
    table2 = d_type.objects.all()
    context = {"drug_data" : table , "drug_type" : table2}
    if request.method == "POST":
        table.drug_name = request.POST['drug_name']
        table.drug_type = d_type.objects.get(type_id = request.POST['drug_type'])
        table.drug_qty = request.POST['drug_qty']
        table.drug_exp = request.POST['drug_expired'] 
        table.save()
        return redirect('/manage_drug')
    return render(request,'edit_d.html',context)

@login_required(login_url="/login")
def edit_type(request,pk):
    table = d_type.objects.get(type_id=pk)
    context = {"type_data" : table}
    if request.method == "POST":
        table.type_name = request.POST['type_name']
        table.save()
        return redirect('/manage_type')
    return render(request,'edit_t.html',context)

@login_required(login_url="/login")
def increase_drug(request,pk):
    print (pk)
    table = drug.objects.get(drug_id=pk)
    update_qty = table.drug_qty+1
    table.drug_qty = update_qty
    table.save()
    return redirect('/manage_drug') 

@login_required(login_url="/login")
def decrease_drug(request,pk):
    print (pk)
    table = drug.objects.get(drug_id=pk)
    update_qty = table.drug_qty-1
    table.drug_qty = update_qty
    table.save()
    return redirect('/manage_drug') 

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pswd']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'เข้าสู่ระบบสำเร็จ!')
            return redirect('/')
        else:
            messages.error(request, 'เข้าสู่ระบบผิดพลาด. โปรดตรวจสอบข้อมูลของคุณอีกครั้ง.')
            pass
    return render(request, 'login.html')

def logout_view(request):
        logout(request)
        return render(request, 'login.html')
    
from django.contrib.auth.models import User

def addmember(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pswd']
        email = request.POST['email']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        # สร้างผู้ใช้ในฐานข้อมูล
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        messages.success(request, 'สมัครสมาชิกสำเร็จ !')
        return redirect('/')
    
    return render(request, 'addmember.html')

@login_required(login_url="/login")
def edit_profile(request):
    # ดึงข้อมูลผู้ใช้ปัจจุบัน
    user = request.user

    if request.method == "POST":
        # อัปเดตข้อมูลที่ผู้ใช้แก้ไข
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']

        # ถ้ามีการกรอกรหัสผ่านใหม่
        new_password = request.POST['pswd']
        if new_password:
            user.set_password(new_password)

        user.save()
        messages.success(request, 'แก้ไขข้อมูลส่วนตัวสำเร็จ !')
        return redirect('/')

    # ส่งข้อมูลผู้ใช้ไปยังหน้าแก้ไข
    context = {"user_data": user}
    return render(request, 'edit_profile.html', context)

# ประวัติการเบิกยาทั้งหมด
def view_medication_history(request):
    medication_history = MedicationHistory.objects.all()
    context = {"medication_history": medication_history}
    
    if not medication_history:
        context["no_history_message"] = "ยังไม่มีประวัติการเบิกยา"
        
    return render(request, 'medication_history.html', context)

# ประวัติการเบิกยาของคุณ
@login_required(login_url="/login")
def view_own_medication_history(request):
    user = request.user
    medication_history = MedicationHistory.objects.filter(user=user)
    context = {"medication_history": medication_history}
    
    if not medication_history:
        context["no_history_message"] = "ยังไม่มีประวัติการเบิกยา"

    return render(request, 'own_medication_history.html', context)