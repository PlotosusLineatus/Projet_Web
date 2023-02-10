from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models.functions import Now
from django.http import HttpResponseRedirect

from genomeBact.models import Transcript,Profile, Connexion
from genomeBact.forms import  CreateUserForm, CreateProfileForm, ProfileForm, ModifyUserForm
from genomeBact.decorators import unauthenticated_user, allowed_users, admin_only, unauth_admin


def user_logout(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def user_login(request):

    request.session.clear()
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password') 

        user = authenticate(request, username= username, password= password )

        if user is not None:
            login(request, user)
            Profile.objects.filter(name=username).update(last_connexion = Now())
            Connexion.objects.create(user = user, date=Now())
            return redirect('home')
        else :
            try:
                user = User.objects.get(email=username)
                user = authenticate(request, username= user.username, password= password )
                login(request, user)
                Profile.objects.filter(user=user).update(last_connexion = Now())
                Connexion.objects.create(user = user, date=Now())
                return redirect('home')           
            except User.DoesNotExist:
                messages.info(request, "Username or password is incorrect" )
            

    context = {}
    return render(request, 'genomeBact/login.html', context)

@unauth_admin
def register(request):
    if request.method == 'POST':
        form_user = CreateUserForm(request.POST)  
        form_profile = CreateProfileForm(request.POST)  

        if form_user.is_valid() and form_profile.is_valid():
            user = form_user.cleaned_data
            profile = form_profile.cleaned_data
            
            username = user['username']
            email = user['email']
            
            password = user['password1']

            User.objects.create_user(username=username, email=email, password=password )

            group_name = profile['group']
            group = Group.objects.get(name = group_name)
            user = User.objects.get(username=username)
            user.groups.add(group)
            
            first_name = profile['first_name']
            last_name = profile['last_name']
            phone_number = profile['phone_number']

            Profile.objects.create(user = user, name=username, first_name = first_name, last_name=last_name, phone_number=phone_number,
                                    group = group_name, last_connexion = Now())

            messages.success(request, 'Account was created for ' + username)
            
            if( request.user.is_anonymous ):
                return redirect('login')
            elif(request.user.profile.name == 'Admin' ):
                return redirect('admin')
            else :
                return redirect('login')
    else:
        form_user = CreateUserForm()
        form_profile = CreateProfileForm()

    context = {'form_user':form_user, 'form_profile':form_profile}
    return render(request, 'genomeBact/register.html', context)

@login_required(login_url='login')
def user_detail(request, user_id):
    if(request.user.groups.all()[0].name == 'Admin' or request.user.id == user_id):

        user = User.objects.filter(id=user_id).get()
        profile = Profile.objects.filter(user = user).get()
        user_group = user.profile.group
        username = user.username

        if request.method == 'POST':
            form_profile = ProfileForm(user_group, request.POST) 
            form_user = ModifyUserForm(request.POST)

            if form_profile.is_valid() and form_user.is_valid() :
                if 'Update' in request.POST:
                    user = form_user.cleaned_data
                    profile2 = form_profile.cleaned_data
                    
                    if profile2["group"] == profile.group :
                        profile2["group"] = ""

                    email = user["email"]
                    if(email != ""):
                        User.objects.filter(username=username).update(email=email)

                    phone = profile2["phone_number"]
                    if(phone != ""):
                        Profile.objects.filter(name=username).update(phone_number = phone)
                            
                    last_name = profile2["last_name"]
                    if(last_name != ""):
                        Profile.objects.filter(name=username).update(last_name = last_name)
                    
                    first_name = profile2["first_name"]
                    if(first_name != ""):
                        Profile.objects.filter(name=username).update(first_name = first_name)


                    # changing user role (admin only)
                    if(request.user.groups.all()[0].name == 'Admin'):
                        group_name = profile2["group"]
                        if(group_name != "" and group_name != "Admin"):
                            User.objects.filter(username=username).get().groups.clear()
                            group = Group.objects.get(name = group_name)
                            group.user_set.add(User.objects.filter(username=username).get())
                            Profile.objects.filter(name=username).update(group = group_name)

                    messages.success(request, 'The profile was updated')
                    return HttpResponseRedirect(request.path_info)
                    
                elif 'Update_password' in request.POST:
                    print("èèèèèèè----------------------------------")
                    user = form_user.cleaned_data
                    password1 = user["password1"]
                    password2 = user["password2"]

                    if( password1 == password2 and password1!=""):
                        User.objects.get(username=username).set_password(password1)
                    
                        messages.success(request, 'The password was updated')
                    
                        return HttpResponseRedirect(request.path_info)
                elif 'Delete' in request.POST:
                    user = User.objects.filter(username = username).get()
                    user.delete()

                    if(request.user.profile == "Admin" and request.user.id != user.id):
                        messages.success(request, "The user " + username +" was deleted.")
                        return redirect('admin')
                    else:
                        user_logout(request)
                        return redirect('login')
        else:
            form_profile = ProfileForm(user_group = user_group)
            form_user = ModifyUserForm()

        context = {'profile' : profile, "form_profile":form_profile, "form_user":form_user}
        return render(request, 'genomeBact/user_detail.html', context)
    return redirect('home')

    
@login_required(login_url='login')
@admin_only
def admin_(request):

    if request.method == 'POST':
        if "add_genome" in request.POST:
            return redirect('genome-create')
        elif "add_transcript" in request.POST:
            return redirect('transcript-create')
        elif "add_user" in request.POST:
            return redirect('register')

    nb_val = User.objects.filter(groups__name = "Validator").count()
    nb_annot  = User.objects.filter(groups__name = "Annotator").count()
    nb_read = User.objects.filter(groups__name = "Reader").count()

    all_val = Profile.objects.filter(group = "Validator")
    all_annot = Profile.objects.filter(group = "Annotator")
    all_read = Profile.objects.filter(group = "Reader")

    nb_to_assign = Transcript.objects.filter(status = 'empty').count()
    nb_to_val = Transcript.objects.filter(status = 'annotated').count()
    nb_to_annot = Transcript.objects.filter(status = 'assigned').count()

    context = {"nb_val":nb_val, "nb_annot":nb_annot, "nb_read":nb_read, "all_val":all_val, "all_annot":all_annot, "all_read":all_read,
               "nb_to_assign":nb_to_assign, "nb_to_val":nb_to_val, "nb_to_annot":nb_to_annot }
    return render(request,'genomeBact/admin.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Validator','Annotator'])
def workspace(request):
    transcripts_to_annotate = request.user.profile.to_annotate.all()
    #transcripts_to_annotate = request.user.profile.transcript_set.all()
    transcripts_to_assign = Transcript.objects.filter(status = 'empty')
    transcripts_to_validate = Transcript.objects.filter(status = 'annotated', validator = request.user.profile)
    annotators = User.objects.filter(groups__name='Annotator')

    nb_to_assign = Transcript.objects.filter(status = 'empty').count()
    nb_to_val =  Transcript.objects.filter(status = 'annotated', validator = request.user.profile).count()
    nb_to_annot = Transcript.objects.filter(status = 'assigned', annotator = request.user.profile).count()
    nb_send = Transcript.objects.filter(status = 'annotated', annotator =request.user.profile).count()

    if request.method == 'POST':
        annotator_chosen = request.POST.get('annotator')
        transcript_chosen = request.POST.get('transcript_annot')
        
        if( request.user.groups.all()[0].name == 'Validator'):
            ### ASSIGNING A TRANSCRIPT
            if annotator_chosen != None and transcript_chosen!= None:
                    
                #transcript_chosen = Transcript.objects.get(transcript=transcript_chosen)
                
                Transcript.objects.filter(transcript=transcript_chosen).update(annotator = Profile.objects.get(name=annotator_chosen))
                Transcript.objects.filter(transcript=transcript_chosen).update(validator = Profile.objects.get(name=request.user.username))
                Transcript.objects.filter(transcript=transcript_chosen).update(status = 'assigned')
                
                messages.success(request, transcript_chosen +' was assigned for ' + annotator_chosen + ".")

            else:
                messages.info(request, " Please select an Annotator AND a Transcript" )


    context = {'transcripts_to_annotate':transcripts_to_annotate, 'transcripts_to_assign':transcripts_to_assign, 'annotators':annotators,
               'transcripts_to_validate':transcripts_to_validate, "nb_to_assign":nb_to_assign, "nb_to_val":nb_to_val, "nb_to_annot":nb_to_annot, "nb_send":nb_send}
    return render(request,'genomeBact/workspace.html', context)