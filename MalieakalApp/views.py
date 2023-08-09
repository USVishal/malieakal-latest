from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import uuid
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import update_session_auth_hash
from .forms import *
import random
import string
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime,date, timedelta
# import pywhatkit
######################################################################### <<<<<<<<<< LANDING MODULE >>>>>>>>>>>>>>

def ind(request):
    item_det = item.objects.all().order_by('-buying_count')[:10]

    return render(request, 'index.html',{"item_det":item_det})
def index(request):
    all_images = bannerads.objects.all().last()
    cat_images = category.objects.all()
    item_det = item.objects.all().order_by('-buying_count')[:10]
    offer = offer_zone.objects.all().order_by('-id')[:5]
    return render(request, 'index/index.html',{'image': all_images,'cat':cat_images,"offer":offer,"item_det":item_det})

def index_search_feature(request):
        
        if request.method == 'POST':
            # Retrieve the search query entered by the user
            search_query = request.POST['search_query']
            # Filter your model by the search query
            items = item.objects.filter(name__contains=search_query)
            return render(request, 'index/index_all_item.html', { 'items':items})
        else:
            return redirect('index')

def user_type(request):
  
    return render(request, 'index/user_type.html')

def login_main(request):
    if request.method == 'POST':
        username  = request.POST['username']
        password = request.POST['password']
        print(username)
        user = authenticate(username=username, password=password)
        
        try:
            if User_Registration.objects.filter(username=request.POST['username'], password=request.POST['password'],role="user1").exists():

                member = User_Registration.objects.get(username=request.POST['username'],password=request.POST['password'])
                
                request.session['userid'] = member.id
                if Profile_User.objects.filter(user_id=member.id).exists():
                    return redirect('staff_home')
                else:
                    return redirect('profile_staff_creation')
                
                
            elif User_Registration.objects.filter(username=request.POST['username'], password=request.POST['password'],role="user2").exists():
                member = User_Registration.objects.get(username=request.POST['username'],password=request.POST['password'])
                request.session['userid'] = member.id
                if Profile_User.objects.filter(user_id=member.id).exists():
                    return redirect('home')
                else:
                    return redirect('profile_user_creation')

            elif user.is_superuser:
                    request.session['userid'] = request.user.id
                    return redirect('admin_home')
            else:
                messages.error(request, 'Invalid username or password')
        except:
            messages.error(request, 'Invalid username or password')
    return render(request,'index/login.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if  User_Registration.objects.filter(email=email).exists():
            user =  User_Registration.objects.get(email=email)

        

            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string('index/forget-password/reset_password_email.html',{
                'user':user,
                'domain' :current_site,
                'user_id' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            }) 

            to_email = email
            send_email = EmailMessage(mail_subject,message,to = [to_email])
            send_email.send()

            messages.success(request,"Password reset email has been sent your email address.")
            return redirect('login_main')
        else:
            messages.error(request,"This account does not exists !")
            return redirect('forgotPassword')
    return render(request,'index/forget-password/forgotPassword.html')


def resetpassword_validate(request,uidb64,token):
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user =  User_Registration._default_manager.get(pk=user_id)  
    except(TypeError,ValueError,OverflowError, User_Registration.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['user_id'] = user_id 
        messages.success(request,"Please reset your password.")
        return redirect('resetPassword')
    else:
        messages.error(request,"The link has been expired !")
        return redirect('login_main')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('user_id') 
            user =  User_Registration.objects.get(pk=uid)
            user.password = password
            user.save()
            messages.success(request,"Password reset successfull.")
            return redirect('login_main')

        else:
            messages.error(request,"Password do not match")
            return redirect('resetPassword')
    else:
        return render(request,'index/forget-password/resetPassword.html')

def logout(request):
    if 'userid' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')

############################################################# <<<<<<<<<< ADMIN MODULE >>>>>>>>>>>
def admin_home(request): 
    items = item.objects.all()
    return render(request, 'admin/admin_home.html',{'items':items})

def staff_management(request):
    return render(request, 'admin/staff_management.html')

def edit_staff(request,id):

    if request.method == "POST":
        form = User_Registration.objects.get(id=id)

        form.name = request.POST.get('name',None)
        form.lastname = request.POST.get('lastname',None)
        form.nickname = request.POST.get('nickname',None)
        form.gender = request.POST.get('gender',None)
        form.date_of_birth = request.POST.get('date_of_birth',None)
        form.phone_number = request.POST.get('phone_number',None)
        form.email = request.POST.get('email',None)
       
        form.username = request.POST.get('username',None)
        form.password = request.POST.get('password',None)
        form.save()
   
        
        return redirect ("staff_list")
    return redirect ("staff_list")

def delete_staff(request,id):
    form = User_Registration.objects.get(id=id)
    form.delete()
    return redirect ("staff_list")

def upload_images(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            banner_image = bannerads(
                banner_image1=form.cleaned_data['image_1'],
                banner_title1=form.cleaned_data['label_1'],
                banner_image2=form.cleaned_data['image_2'],
                banner_title2=form.cleaned_data['label_2'],
                banner_image3=form.cleaned_data['image_3'],
                banner_title3=form.cleaned_data['label_3'],
                banner_image4=form.cleaned_data['image_4'],
                banner_title4=form.cleaned_data['label_4'],
                banner_image5=form.cleaned_data['image_5'],
                banner_title5=form.cleaned_data['label_5'],
            )
            banner_image.save()

            messages.success(request, 'Images and labels have been uploaded successfully!')
            return redirect('upload_images')  # Redirect to the same page to clear the form

    else:
        form = ImageForm()
    return render(request, 'admin/bannerimg.html', {'form': form})


def admin_add_item(request):

    item_categories = category.objects.all()
    under_choices = (
    ("Home Appliance", "Home Appliance"),
    ("Electronics", "Electronics"),
    ("Furniture", "Furniture"),
    )
    if request.method == 'POST':
        form_data = request.POST.dict()

        title = form_data.get('title', None)
        price = form_data.get('price', None)

        
        offer_percentage = form_data.get('offer_percentage', None)
        offer_prices = form_data.get('offer_price', None)
        image = request.FILES.get('image', None)
        category_id = form_data.get('categories', None)
        under_category = form_data.get('under_category', None)
        title_description = form_data.get('title_description', None)
        description = form_data.get('description', None)

        categorys = get_object_or_404(category, pk=category_id)
      

        new_item = item(
            category = categorys,
            name = title,
            price = price,
            buying_count = 0,
            offer = offer_percentage,
            offer_price=offer_prices,
            image = image,
            under_category = under_category,
            title_description = title_description,
            description = description
        )
        new_item.save()
        return redirect('admin_home')
    context={
        'item_categories':item_categories,
        'under_choices':under_choices,
    }

    return render(request,'admin/ad_add_item.html',context)


def admin_edit_item(request, item_id):
    item_instance = get_object_or_404(item, pk=item_id)
    item_categories = category.objects.all()
    under_choices = (
        ("Home Appliance", "Home Appliance"),
        ("Electronics", "Electronics"),
        ("Furniture", "Furniture"),
    )

    context = {
        'item_instance': item_instance,
        'item_categories': item_categories,
        'under_choices': under_choices,
    }
    if request.method == 'POST':
        form_data = request.POST.dict()
        item_instance.name = form_data.get('title', '')
        item_instance.price = form_data.get('price', '')
        item_instance.offer = form_data.get('offer_percentage', '')
        item_instance.offer_price = form_data.get('offer_price', '')
        
        item_instance.image = request.FILES.get('image', item_instance.image)
        category_id = form_data.get('categories', None)
        if category_id:
            category_instance = get_object_or_404(category, pk=category_id)
            item_instance.category = category_instance
        item_instance.under_category = form_data.get('under_category', '')
        item_instance.title_description = form_data.get('title_description', '')
        item_instance.description = form_data.get('description', '')

        item_instance.save()
        return redirect('admin_home')

    return render(request, 'admin/admin_edit_item.html', context)

    

def admin_delete_item(request,id):
    d1=item.objects.get(id=id)
    d1.delete()
    return redirect('/admin_home/')


def admin_itemlist(request):
    items = item.objects.all()
    return render(request, 'admin/admin_itemlist.html',{'items':items})

# #######################admin add staff #####################
def add_staff(request):
    if request.method == "POST":
        username = request.POST.get('username',None)
        email = request.POST.get('',None)
        if User_Registration.objects.filter(email=email).exists():
            messages.error(request,"Email already Exist")
            return redirect ("add_staff")
        else:
            if User_Registration.objects.filter(username=username).exists():
                messages.error(request,"Username already Exist")
                return redirect ("add_staff")
            else:
                form = User_Registration()

                form.name = request.POST.get('name',None)
                form.lastname = request.POST.get('lastname',None)
                form.nickname = request.POST.get('nickname',None)
                form.gender = request.POST.get('gender',None)
                form.date_of_birth = request.POST.get('date_of_birth',None)
                form.phone_number = request.POST.get('phone_number',None)
                form.email = request.POST.get('email',None)
                form.role = "user1"
                form.username = request.POST.get('username',None)
                form.password = request.POST.get('password',None)
                form.save()
   
        
        return redirect ("staff_list")
    return render(request, "admin/admin_addstaff.html")







def admin_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name', None)
        image = request.FILES.get('category_image')
       

        categorys = category(
            category_name = category_name,
            image = image,
        )
        categorys.save()
        return redirect('admin_home')

    return render(request,'admin/admin_category.html')

def new_form(request):
        
        if request.method == 'POST':
            image = request.FILES.get('image')
            title = request.POST["title"]
           
            price = request.POST["price"]
            offer = request.POST["offer_percentage"]
            offer_price =  request.POST["offer_price"]
            offer_zone_instance = offer_zone(
                image = image,
                title = title ,
              
                price = price ,
                offer = offer ,
                offer_price=offer_price,
            )
            offer_zone_instance.save()
            return redirect('admin_home')

        return render(request,'admin/admin_offer.html')
############################################################# <<<<<<<<<< STAFF MODULE >>>>>>>>>>>>>>
def staff_base(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    lk=category.objects.get(id=1)
 
    context={
        'user':usr,
        "lk":lk
    }
    return render(request, 'staff/staff_base.html',context)

def staff_home(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    items = item.objects.all()
    banner= bannerads.objects.all().last()
    return render(request, 'staff/staff_home.html',{'items':items,'user':usr,'banner':banner})

def new_module(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    item_categories = category.objects.all()
    under_choices = (
    ("Home Appliance", "Home Appliance"),
    ("Electronics", "Electronics"),
    ("Furniture", "Furniture"),
    )
    if request.method == 'POST':
        form_data = request.POST.dict()

        title = form_data.get('title', None)
        price = form_data.get('price', None)

        
        offer_percentage = form_data.get('offer_percentage', None)
        offer_prices = form_data.get('offer_price', None)
        image = request.FILES.get('image', None)
        category_id = form_data.get('categories', None)
        under_category = form_data.get('under_category', None)
        title_description = form_data.get('title_description', None)
        description = form_data.get('description', None)

        categorys = get_object_or_404(category, pk=category_id)
      

        new_item = item(
            category = categorys,
            name = title,
            price = price,
            buying_count = 0,
            offer = offer_percentage,
            offer_price=offer_prices,
            image = image,
            under_category = under_category,
            title_description = title_description,
            description = description
        )
        new_item.save()
        return redirect('staff_home')
    context={
        'item_categories':item_categories,
        'under_choices':under_choices,
        'user':usr,
    }

    return render(request,'staff/new_item_add.html',context,)
#  ###############staff item list##################
def staff_itemlist(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    item_categories = category.objects.all()
    under_choices = (
    ("Home Appliance", "Home Appliance"),
    ("Electronics", "Electronics"),
    ("Furniture", "Furniture"),
    )
    items = item.objects.all()
    return render(request, 'staff/staff_itemlist.html',{'items':items,'item_categories':item_categories,
        'under_choices':under_choices,'user':usr})
# ##############################staff item edit###########################
def staff_itemedit(request, item_id):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)

    item_instance = get_object_or_404(item, pk=item_id)
    item_categories = category.objects.all()
    under_choices = (
        ("Home Appliance", "Home Appliance"),
        ("Electronics", "Electronics"),
        ("Furniture", "Furniture"),
    )

    context = {
        'item_instance': item_instance,
        'item_categories': item_categories,
        'under_choices': under_choices,
    }
    if request.method == 'POST':
        form_data = request.POST.dict()
        item_instance.name = form_data.get('title', '')
        item_instance.price = form_data.get('price', '')
        item_instance.offer = form_data.get('offer_percentage', '')
        item_instance.offer_price = form_data.get('offer_price', '')
        
        if request.POST.get('image',None) == "":
            item_instance.image = item_instance.image
        else:
            item_instance.image=request.FILES.get('image',None)

        category_id = form_data.get('categories', None)
        if category_id:
            category_instance = get_object_or_404(category, pk=category_id)
            item_instance.category = category_instance
        item_instance.under_category = form_data.get('under_category', '')
        item_instance.title_description = form_data.get('title_description', '')
        item_instance.description = form_data.get('description', '')

        item_instance.save()
        return redirect('staff_itemlist')

    return render(request, 'staff/staff_itemlist.html', context,{'user':usr})

# ##############################staff item delete###########################
def staff_itemdelete(request,item_id):
    d1=item.objects.get(id=item_id)
    d1.delete()
    return redirect('staff_itemlist')


    

# ######################admin staff list####################
def staff_list_view(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    staff_members = User_Registration.objects.filter(role='user1')
    return render(request, 'staff/admin_offerlist.html', {'staff_members': staff_members,'user':usr})
# ##################offer add#############
def staff_new_offer(request):
        ids=request.session['userid']
        usr=Profile_User.objects.get(user=ids)
        if request.method == 'POST':
            image = request.FILES.get('image')
            title = request.POST["title"]
            
            price = request.POST["price"]
            offer = request.POST["offer_percentage"]
            offer_price =  request.POST["offer_price"]
            offer_zone_instance = offer_zone(
                image = image,
                title = title ,
                
                price = price ,
                offer = offer ,
                offer_price=offer_price,
            )
            offer_zone_instance.save()
            return redirect('staff_home')

        return render(request,'staff/staff_offer.html',{'user':usr})
# ########################staff offer list###############
def staffofferlist(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)

    offerlist = offer_zone.objects.all()
    return render(request, 'staff/staff_offerlist.html', {'offerlist': offerlist,'user':usr})
# ############################staff offer edit ###############
def edit_offer(request,id):

    if request.method == "POST":
        form = offer_zone.objects.get(id=id)
        if request.POST.get('image',None)=="":
            form.image = form.image
        else:
            form.image = request.FILES.get('image',None)
        form.title = request.POST.get('title',None)
        form.description = request.POST.get('description',None)
        form.price = request.POST.get('price',None)
        form.offer = request.POST.get('offer',None)
        form.offer_rice = request.POST.get('offer_price',None)
        
        form.save()       
        return redirect ("staffofferlist")
    return redirect ("staffofferlist")


########################## staff offer delete###############
def delete_offer(request,id):
    form = offer_zone.objects.get(id=id)
    form.delete()
    return redirect ("staffofferlist")

# ################staff Cateory #######################
def staff_categorylist(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    cat = category.objects.all()
    return render(request, 'staff/staff_categlist.html',{'cat':cat,'user':usr})
# ################staff Cateory edit #######################
def edit_staffcateg(request,id):
     if request.method == 'POST':
        cat=category.objects.get(id=id)
        
        cat.category_name = request.POST.get('category_name',None)
        if request.POST.get('category_image',None) == "":
            cat.image=cat.image
        else:
            cat.image = request.FILES.get('category_image',None)
       
        cat.save()
        return redirect('staff_home')

     return redirect('staff_categorylist(')
# ################staff Cateory Delete #######################
def delete_staffcateg(request,id):
    form = category.objects.get(id=id)
    form.delete()
    return redirect ("staff_categorylist")


# <<<<<<<<<< for Editing item >>>>>>>>>>>>>>


#################################
def delete_item(request,id):
    d1=item.objects.get(id=id)
    d1.delete()
    return redirect('/staff_home/')

def profile_staff_creation(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    if request.method =="POST":
        
        firstname = request.POST.get('firstname',None)
        lastname = request.POST.get('lastname',None)
        phonenumber = request.POST.get('phonenumber',None)
        email = request.POST.get('email',None)
        gender = request.POST.get('gender',None)
        address = request.POST.get('address',None)
        date_of_birth= request.POST.get('date_of_birth',None)
        pro_pics = request.FILES.get('propic',None)
        secondnumb = request.POST.get('secondnumb',None)
        profile_artist = Profile_User(
            firstname=firstname,
            lastname=lastname,
            phonenumber=phonenumber,
            email=email,
            gender=gender,
            date_of_birth=date_of_birth,
            address=address,
            pro_pic=pro_pics,
            user=usr,
            secondnumber=secondnumb
        )
        profile_artist.save()


        return redirect('staff_home')
    context={
        'user':usr
    }
    return render(request,'index/index_staff/profile_staff_creation.html', context)




def staff_upload_images(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            banner_image = bannerads(
                banner_image1=form.cleaned_data['image_1'],
                banner_title1=form.cleaned_data['label_1'],
                banner_image2=form.cleaned_data['image_2'],
                banner_title2=form.cleaned_data['label_2'],
                banner_image3=form.cleaned_data['image_3'],
                banner_title3=form.cleaned_data['label_3'],
                banner_image4=form.cleaned_data['image_4'],
                banner_title4=form.cleaned_data['label_4'],
                banner_image5=form.cleaned_data['image_5'],
                banner_title5=form.cleaned_data['label_5'],
            )
            banner_image.save()

            messages.success(request, 'Images and labels have been uploaded successfully!')
            return redirect('staff_upload_images')  # Redirect to the same page to clear the form

    else:
        form = ImageForm()
    return render(request, 'admin/staff_bannerimg.html', {'form': form})
# #################### staff edit banner################
def edit_banner(request,id):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    banner = bannerads.objects.get(id=id)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        print(request.POST.get('image_1',None))
        banner_image = bannerads.objects.get(id=id)
        if request.POST.get('image_1',None) == "":
            banner_image.banner_image1==banner_image.banner_image1
        else:
            banner_image.banner_image1=request.FILES.get('image_1',None)
        banner_image.banner_title1=request.POST.get('label_1',None)
        if request.POST.get('image_2',None) == "":
            banner_image.banner_image2==banner_image.banner_image2
        else:
            banner_image.banner_image2=request.FILES.get('image_2',None)
        
        banner_image.banner_title2=request.POST.get('label_2',None)
        if request.POST.get('image_3',None) == "":
            banner_image.banner_image3==banner_image.banner_image3
        else:
            banner_image.banner_image3=request.FILES.get('image_3',None)
       
        banner_image.banner_title3=request.POST.get('label_3',None)
        if request.POST.get('image_4',None) == "":
            banner_image.banner_image4==banner_image.banner_image4
        else:
            banner_image.banner_image4=request.FILES.get('image_4',None)

        banner_image.banner_title4=request.POST.get('label_4',None)
        if request.POST.get('image_5',None) == "":
            banner_image.banner_image5==banner_image.banner_image5
        else:
            banner_image.banner_image5=request.FILES.get('image_5',None)

        banner_image.banner_title5=request.POST.get('label_5',None)
        
        banner_image.save()

        return redirect('staff_home')  # Redirect to the same page to clear the form

    
    return render(request, 'staff/staff_editbanner.html', {'banner': banner,'user':usr})
##################################################
def staff_category(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    if request.method == 'POST':
        category_name = request.POST.get('category_name', None)
        image = request.FILES.get('category_image')
       

        categorys = category(
            category_name = category_name,
            image = image,
        )
        categorys.save()
        return redirect('staff_home')

    return render(request,'staff/staff_category.html',{'user':usr})

# ##############sraff order##################
def staff_view_order(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    chk=checkout.objects.all().order_by("-id")
    chk_item=checkout_item.objects.all().order_by("-id")
    context={
        "chk":chk,
        "chk_item":chk_item,
        'user':usr,

    }
    return render(request,'staff/staff_vieworders.html',context)

def staff_delete_check(request,id):
        chk=checkout.objects.get(id=id)
        chk_item=checkout_item.objects.filter(checkout_id=id)
        chk_item.delete()
        chk.delete()
        return redirect('staff_view_order')
# ############staff user management######################
def staff_user_list_view(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)

    staff_members = User_Registration.objects.filter(role='user2')
    print(staff_members.values())
    return render(request, 'staff/staff_userview.html', {'staff_members': staff_members,'user':usr})

def staff_edit_user(request,id):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)

    if request.method == "POST":
        form = User_Registration.objects.get(id=id)

        form.name = request.POST.get('name',None)
        form.lastname = request.POST.get('lastname',None)
        form.nickname = request.POST.get('nickname',None)
        form.gender = request.POST.get('gender',None)
        form.date_of_birth = request.POST.get('date_of_birth',None)
        form.phone_number = request.POST.get('phone_number',None)
        form.email = request.POST.get('email',None)
       
        form.username = request.POST.get('username',None)
        form.password = request.POST.get('password',None)
        form.save()
   
        
        return redirect ("staff_user_list_view")
    return redirect ("staff_user_list_view")

def staff_delete_user(request,id):
    form = User_Registration.objects.get(id=id)
    pro= Profile_User.objects.get(user_id=id)
    form.delete()
    pro.delete()
    return redirect ("staff_user_list_view")


#######################################logout################### <<<<<<<<<< USER MODULE >>>>>>>>>>>>>>>>

def base_sub(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    lk=category.objects.get(id=1)
    crt_cnt=cart.objects.filter(user=ids).count()
 
    context={
        'user':usr,
        "lk":lk,
        "crt_cnt":2
    }
    return render(request, 'user/base_sub.html',context)

def user_base(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    lk=category.objects.get(id=1)
    crt_cnt=cart.objects.filter(user=ids).count()
 
    context={
        'user':usr,
        "lk":lk,
        "crt_cnt":crt_cnt
    }
    return render(request, 'user/user_base.html',context)



def user_registration(request):

    if request.method =='POST':
        form = User_RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User_Registration.objects.filter(email=email).exists():
                messages.error(request, 'Email Id already exists')
                return redirect('user_registration')
            else:
                user_model=form.save()
            user_id = user_model.pk
            return redirect('index_user_confirmation',user_id=user_id)
    else:
        form = User_RegistrationForm()
        form.initial['role'] = 'user2'
    return render(request,'index/index_user/index_user_registraion.html',{'form':form})


def index_user_confirmation(request,user_id):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            print("success")
            if User_Registration.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('index_user_confirmation', user_id=user_id)
            else:
                artist_object = get_object_or_404(User_Registration, pk=user_id)
                artist_object.username=username
                artist_object.password = password
                artist_object.save()
                messages.success(request, 'Thank you for registering with us.')
                return redirect('login_main')
        else:
            messages.error(request, ' Password and Confirm Password are not matching. Please verify it.')
            return redirect('index_user_confirmation', user_id=user_id)

    return render(request,'index/index_user/index_user_confirmation.html',{'user_id':user_id})

def profile_user_creation(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    if request.method =="POST":
        
        firstname = request.POST.get('firstname',None)
        lastname = request.POST.get('lastname',None)
        phonenumber = request.POST.get('phonenumber',None)
        email = request.POST.get('email',None)
        gender = request.POST.get('gender',None)
        address = request.POST.get('address',None)
        date_of_birth= request.POST.get('date_of_birth',None)
        pro_pics = request.FILES.get('propic',None)
        secondnumb = request.POST.get('secondnumb',None)
        profile_artist = Profile_User(
            firstname=firstname,
            lastname=lastname,
            phonenumber=phonenumber,
            email=email,
            gender=gender,
            date_of_birth=date_of_birth,
            address=address,
            pro_pic=pro_pics,
            user=usr,
            secondnumber=secondnumb
        )
        profile_artist.save()


        return redirect('home')
    context={
        'user':usr
    }
    return render(request,'index/index_user/profile_user_creation.html', context)


def home(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    crt_cnt=cart.objects.filter(user=ids).count()
    cat1="Home Appliance"
    cat2="Electronics"
    cat3="Furniture"
    all_images = bannerads.objects.all().last()
    cat_images = category.objects.all()
    item_det = item.objects.all().order_by('-buying_count')[:10]
    offer = offer_zone.objects.all().order_by('-id')[:5]
    
    return render(request, 'user/home.html', {'image': all_images,'cat':cat_images,'user':usr,"cat1":cat1,"cat2":cat2,"cat3":cat3,"item_det":item_det,'offer':offer,"crt_cnt":crt_cnt})


def search_feature(request):
    
        ids=request.session['userid']
        usr=Profile_User.objects.get(user=ids)
        crt_cnt=cart.objects.filter(user=ids).count()
        
        if request.method == 'POST':
            # Retrieve the search query entered by the user
            search_query = request.POST['search_query']
            # Filter your model by the search query
            items = item.objects.filter(name__contains=search_query)
            return render(request, 'user/all_item.html', {'user':usr,"crt_cnt":crt_cnt, 'items':items})
        else:
            return redirect('home')
            
            
def user_home(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    context={
        'user':usr
    }
    return render(request, 'user/user_home.html',context)

def category_items(request, categorys):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    crt_cnt=cart.objects.filter(user=ids).count()
    items=item.objects.filter(category_id=categorys)
    cat=category.objects.get(id=categorys)
    context={
        'user':usr,
        "items":items,
        "cat":cat,
        "crt_cnt":crt_cnt
        
    }
    return render(request, 'user/category_items.html',context)

def under_items(request, category):

    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    crt_cnt=cart.objects.filter(user=ids).count()
    if category=="home_applience":
        items=item.objects.filter(under_category="Home Appliance")
    elif category=="electronics":
        items=item.objects.filter(under_category="Electronics")
    elif category=="furniture":
        items=item.objects.filter(under_category="Furniture")
    else:
        items=item.objects.all()
    

    context={
        'user':usr,
        "items":items,
        "category":category,
        "crt_cnt":crt_cnt
    }
    return render(request, 'user/uder_items.html',context)

def under_category_items_add_cart(request, id, categorys):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    
    items=item.objects.get(id=id)
    cat=category.objects.get(id=categorys)
    if cart.objects.filter(user=usr,item=items).exists():
        messages.error(request, 'This item is already in cart')
        items=item.objects.filter(category_id=categorys)
        usrd=Profile_User.objects.get(user=ids)
        context={
        'user':usrd,
        "items":items
        }
   
    else:
        crt=cart()
        crt.user=usr
        crt.item=items
        crt.save()
        messages.error(request, 'This item is add to cart')
        items=item.objects.filter(category_id=categorys)
        usrd=Profile_User.objects.get(user=ids)
        context={
            'user':usrd,
            "items":items
        }
    return redirect("cart_checkout")

def all_items(request):

    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    crt_cnt=cart.objects.filter(user=ids).count()
    
    items=item.objects.all()

    context={
        'user':usr,
        "items":items,
        "crt_cnt":crt_cnt
 
    }
    return render(request, 'user/all_item.html',context)

def all_items_add_cart(request, id, category):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    
    items=item.objects.get(id=id)

    if cart.objects.filter(user=usr,item=items).exists():
        messages.error(request, 'This item is already in cart')
        items=item.objects.filter(category_id=category)
        usrd=Profile_User.objects.get(user=ids)
        context={
        'user':usrd,
        "items":items
        }
   
    else:
        crt=cart()
        crt.user=usr
        crt.item=items
        crt.save()
        messages.error(request, 'This item is add to cart')
        items=item.objects.filter(category_id=category)
        usrd=Profile_User.objects.get(user=ids)
        context={
            'user':usrd,
            "items":items
        }
    return redirect("cart_checkout")

def add_cart(request, id, category):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    
    items=item.objects.get(id=id)
  
    if cart.objects.filter(user=usr,item=items).exists():
        messages.error(request, 'This item is already in cart')
        items=item.objects.filter(category_id=category)
        usrd=Profile_User.objects.get(user=ids)
        context={
        'user':usrd,
        "items":items
        }
   
    else:
        crt=cart()
        crt.user=usr
        crt.item=items
        crt.save()
        messages.error(request, 'This item is add to cart')
        items=item.objects.filter(category_id=category)
        usrd=Profile_User.objects.get(user=ids)
        context={
            'user':usrd,
            "items":items
        }
    return redirect("cart_checkout")
    
def cart_view(request):
   
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    carts=cart.objects.filter(user=ids)
  
    context={
        "cart":carts,
        'user':usr,
        
    }
    return render(request, 'user/cart_display.html',context)

def product_view(request, item_id):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    crt_cnt=cart.objects.filter(user=ids).count()
    try:
        item_instance = item.objects.get(id=item_id)
        oprice = item_instance.price

        if item_instance.offer:
            off = item_instance.offer
            rp = oprice - (oprice * (off / 100))
        else:
            rp = oprice

        return render(request, 'user/productview.html', {'item': item_instance, 'rp': rp,'user':usr,"crt_cnt":crt_cnt})

    except item.DoesNotExist:
        # Handle the case where the item does not exist
        return HttpResponse("Item not found", status=404)

def add_cart_pr_view(request, id, category):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    
    items=item.objects.get(id=id)

    if cart.objects.filter(user=usr,item=items).exists():
        messages.error(request, 'This item is already in cart')
        items=item.objects.filter(category_id=category)
        usrd=Profile_User.objects.get(user=ids)
        
   
    else:
        crt=cart()
        crt.user=usr
        crt.item=items
        crt.save()
        messages.error(request, 'This item is add to cart')
        items=item.objects.filter(category_id=category)
        usrd=Profile_User.objects.get(user=ids)
        
    return redirect("cart_checkout")

def cart_checkout(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    carts=cart.objects.filter(user=ids)
    crt_cnt=cart.objects.filter(user=ids).count()
  
    context={
        "cart":carts,
        'user':usr,
        "crt_cnt":crt_cnt
        
    }
    return render(request, 'user/cart_checkout.html',context)
    
# send reciept
def send_receipt(request):
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    pro=Profile_User.objects.get(user=ids)
    if request.method =="POST":
        total_amount = request.POST.get('total_amount')
       
        item_id =request.POST.getlist('item_id[]') 
        qty =request.POST.getlist('qty[]') 

        if len(item_id)==len(qty):
            mapped2 = zip(item_id,qty)
            mapped2=list(mapped2)
         
            for ele in mapped2:
                itm=item.objects.get(id=ele[0])
                itm.buying_count=int(itm.buying_count+1)
                itm.save()
                # created = checkout.objects.create(user=usr,item=itm,qty=ele[1],item_total=int(ele[1])*int(itm.price),item_name=itm.name,item_price=itm.price,date=date.today())

        chk_item=checkout.objects.filter(date=date.today()).order_by('-id')[:len(item_id)]
      
        lst=""
        for i in chk_item:
            rcp="\n\nItem : "+str(i.item_name)+'\nAmount : '+str(i.item_price)+' * '+str(i.qty)+' = '+str(i.item_total)
            lst+=rcp
     
        tot="\n\nTotal Amount : "+str(total_amount)
        
        message = 'Greetings from Malieakal\n\nReciept,\n\nName :'+str(usr.name)+str(usr.lastname)+'\nAddress :'+str(pro.address)+'\n\n'+str(lst)+str(tot)
      
        # pywhatkit.sendwhatmsg_instantly(
        #     phone_no="+918848937577", 
        #     message=""+str(message),
        # )
     
        messages.error(request, 'Purchase Success Full')
        
        for i in item_id:
            ckt=cart.objects.get(user=usr,item_id=i).delete()
        
          
    
        return redirect("cart_checkout")
    return redirect("cart_checkout")

def delete_cart(request,id):
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    ckt=cart.objects.get(user=usr,id=id).delete()
    return redirect("cart_checkout")


def edit_banner(request,id):
    banner = bannerads.objects.get(id=id)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        print(request.POST.get('image_1',None))
        banner_image = bannerads.objects.get(id=id)
        if request.POST.get('image_1',None) == "":
            banner_image.banner_image1==banner_image.banner_image1
        else:
            banner_image.banner_image1=request.FILES.get('image_1',None)
        banner_image.banner_title1=request.POST.get('label_1',None)
        if request.POST.get('image_2',None) == "":
            banner_image.banner_image2==banner_image.banner_image2
        else:
            banner_image.banner_image2=request.FILES.get('image_2',None)
        
        banner_image.banner_title2=request.POST.get('label_2',None)
        if request.POST.get('image_3',None) == "":
            banner_image.banner_image3==banner_image.banner_image3
        else:
            banner_image.banner_image3=request.FILES.get('image_3',None)
       
        banner_image.banner_title3=request.POST.get('label_3',None)
        if request.POST.get('image_4',None) == "":
            banner_image.banner_image4==banner_image.banner_image4
        else:
            banner_image.banner_image4=request.FILES.get('image_4',None)

        banner_image.banner_title4=request.POST.get('label_4',None)
        if request.POST.get('image_5',None) == "":
            banner_image.banner_image5==banner_image.banner_image5
        else:
            banner_image.banner_image5=request.FILES.get('image_5',None)

        banner_image.banner_title5=request.POST.get('label_5',None)
        
        banner_image.save()

        return redirect('staff_home')  # Redirect to the same page to clear the form

    
    return render(request, 'staff/staff_editbanner.html', {'banner': banner})
  