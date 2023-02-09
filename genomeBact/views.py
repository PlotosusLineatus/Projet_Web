from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models.functions import Now
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
import csv


from Bio import SeqIO
from io import StringIO

from .models import Genome,Transcript,Profile, Connexion
from .forms import GenomeForm, TranscriptForm, UploadFileForm, CreateUserForm, AnnotForm, ProfileForm, ModifyUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only

from scripts.utils import get_max_length

def user_logout(request):
    logout(request)
    print("logouuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuut")
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
                username = User.objects.get(email=username)
                user = authenticate(request, username= username.username, password= password )
                login(request, user)
                Profile.objects.filter(email=username).update(last_connexion = Now())
                Connexion.objects.create(user = user, date=Now())
                return redirect('home')           
            except User.DoesNotExist:
                messages.info(request, "Username or password is incorrect" )
            

    context = {}
    return render(request, 'genomeBact/login.html', context)

#@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)  
        if form.is_valid():
            user = form.save()

            group_name = request.POST.get('group')
            group = Group.objects.get(name = group_name)
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            
            Profile.objects.create(user = user, name=user.username, group = group_name, last_connexion = Now())

            messages.success(request, 'Account was created for ' + username)
            
            #if( request.user.groups.all()[0].name == None):
            return redirect('admin')
            #else :
            return redirect('login')
        else:
            messages.error(request, form.errors)
    else:
        form = CreateUserForm()

    context = {'form':form}
    return render(request, 'genomeBact/register.html', context)

@login_required(login_url='login')
def user_detail(request, user_id):

    user = User.objects.filter(id=user_id).get()
    profile = Profile.objects.filter(user = user).get()
    '''
    if( request.user.groups.all()[0].name == 'Admin'):
    '''
    username = user.username
    #user = User.objects.get(username = 'r')
    if request.method == 'POST':
        form_profile = ProfileForm(request.POST)  
        form_user = ModifyUserForm(request.POST)

        if form_profile.is_valid() and form_user.is_valid() :
            if 'Update' in request.POST:
                user = form_user.cleaned_data
                profile2 = form_profile.cleaned_data
                
                if profile2["group"] == profile.group :
                    profile2["group"] = ""

                ## test if there's some changes or none
                x = list(user.values())
                y = list(profile2.values())
                if ( [x[0]]*len(x) != x and [y[0]]*len(y) != y):
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

                    group_name = profile2["group"]
                    if(group_name != "" and group_name != "Admin"):
                        group = Group.objects.get(name = group_name)
                        group.user_set.add(User.objects.filter(username=username).get())
                        Profile.objects.filter(name=username).update(group = group_name)

                    messages.success(request, 'The profile was updated')
                
                    return HttpResponseRedirect(request.path_info)
                
            elif 'Update_password' in request.POST:

                user = form_user.cleaned_data
                password1 = user["password1"]
                password2 = user["password2"]

                if( password1 == password2 and password1!=""):
                    User.objects.get(username=username).set_password(password1)
                
                    messages.success(request, 'The password was updated')
                
                    return HttpResponseRedirect(request.path_info)
                    return redirect('admin')
            elif 'Delete' in request.POST:
                user = User.objects.filter(username = username).get()
                user.delete()

                #if(request.user.profile == "Admin" and request.user.id != user.id)
                if(request.user.id != user.id) :
                    messages.success(request, "The user " + username +" was deleted.")
                    return redirect('admin')
                else:
                    user_logout(request)
                    return redirect('login')
    else:
        form_profile = ProfileForm()
        form_user = ModifyUserForm()

    context = {'profile' : profile, "form_profile":form_profile, "form_user":form_user}
    return render(request, 'genomeBact/user_detail.html', context)

@login_required(login_url='login')
def home(request):

    # Does user submit anything ?
    if request.method == "POST":    
      
        # User submits but don't fill any research field
        if request.POST.keys() is not None:

            # Genome or transcript ?
            query_type = request.POST.get("query_type")
            request.session["query_type"] = query_type

            if query_type == "Genome":

                request.session["accession"] = request.POST.get("accession", "")
                request.session["specie"] = request.POST.get("specie", "")
                request.session["max"] = request.POST.get("max_length")
                request.session["min"] = request.POST.get("min_length")

                if request.POST.get("sub_nt"):

                    # Minimum substring length to search
                    if len(request.POST.get("sub_nt")) < 3:

                        request.session["sub_nt"] = ""
                    
                    else:

                        request.session["sub_nt"] = request.POST.get("sub_nt")
                else:

                    request.session["sub_nt"] = ""

                return redirect("results")

            if query_type == "Transcript":

                accession= request.POST.get("accession", "")
                specie = request.POST.get("specie", "")

                default_max = get_max_length()
                max_ = request.POST.get("max_length", default_max)
                min_ = request.POST.get("min_length", 0)

                if request.POST.get("sub_nt"):

                    # Minimum substring length to search
                    if len(request.POST.get("sub_nt")) < 3:

                        sub_nt = ""
                    
                    else:

                        sub_nt = request.POST.get("sub_nt")
                else:

                    sub_nt = ""


                if request.POST.get("sub_pep"):

                    # Minimum substring length to search
                    if len(request.POST.get("sub_pep")) < 3:

                        sub_pep = ""
                    
                    else:

                        sub_pep = request.POST.get("sub_pep")
                else:

                    sub_pep = ""

                if ( not request.POST.get("specie") ) or request.POST.get("specie") == "":

                    query_max = Q(length__gte = min_)
                    query_min = Q(length__lte = max_)
                    query_access = Q(chromosome__contains = accession)
                    query_sub_nt = Q(seq_nt__contains = sub_nt)
                    query_sub_pep = Q(seq_cds__contains = sub_pep)
                    query_specie = Q(specie__contains = specie)

                    Transcripts = Transcript.objects.filter(query_max & query_min & query_access & query_sub_nt & query_sub_pep)

                    # Pour plus tard : transcripts = Transcript.objects.filter(chromosome__in = genomes)
                    # retourne les trancripts des ( )


                return render(request, "genomeBact/transcript_list.html",{'genome': genome, 'transcript': transcript})

    # Return empty research fields to results/ if user don't submit button
    request.session["accession"] = ""
    request.session["specie"] = ""
    request.session["max"] = ""
    request.session["min"] = ""
    request.session["substring"] = ""
    request.session["query_type"] = ""

    return render(request,'genomeBact/home.html')

def download_csv(request, transcripts = None, genomes = None):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transcripts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Accession', 'Sequence'])

    if transcripts:

        for transcript in transcripts:
            writer.writerow([transcript.transcript, transcript.seq_cds])

        return response

    elif genomes:

        for genome in genomes:

            writer.writerow([genome.chromosome, genome.sequence])
        return response


@login_required(login_url='login')
def results(request):
    '''
    # If user don't search anything from home page, return full list of genomes
    if 'user_input' in request.session:
        user_input = request.session['user_input'] 
        del request.session['user_input'] 
        # Sinon, on utilise l'input de l'user pour filtrer les génomes sur leur num d'accession
        genome = Genome.objects.filter(chromosome__contains = user_input)
        return render(request, 'genomeBact/results.html',{'genome': genome}) 
    '''

    
    # Delete session without deleting user current logs
    keys = ["accession","specie","sub_nt","sub_pep", "max","min", "query_type"]
    keys = [key for key in keys if key in request.session.keys() ]

    
    accession = request.session["accession"] 
    specie = request.session["specie"]
    substring = request.session["substring"]
    substring = substring.upper() # Just in case

    # For some reason request.session doesn't store request.POST.get(name, default_integer) default output as integer but rather as ''
    max_ = request.session["max"]
    if max_ == '':
        max_ = get_max_length()
    min_ = request.session["min"]
    if min_ == '':
        min_ = 0

    query_max = Q(length__gte = min_)
    query_min = Q(length__lte = max_)
    query_access = Q(chromosome__contains = accession)
    query_sub = Q(sequence__contains = substring)
    query_specie = Q(specie__contains = specie)

    genomes = Genome.objects.filter(query_max & query_min & query_access & query_sub & query_specie)

    #for key in keys:
    #    del request.session[key]

        
    if request.method == 'POST':


        if not genomes:

            return render(request, '404.html', status=404)

        else:

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="models.csv"'

            writer = csv.writer(response)
            writer.writerow(['Number', 'Text'])

        
            for genome in genomes:
                writer.writerow([genome.chromosome, genome.specie])

            return response
        
    return render(request,'genomeBact/results.html', {'genomes': genomes}) 


       
@login_required(login_url='login')
def genome_detail(request, specie):
    genome = Genome.objects.get(specie=specie)
    transcripts = Transcript.objects.filter(chromosome = genome.chromosome)

    sequence = genome.sequence

    return render(request,'genomeBact/genome_detail.html',{'genome': genome, 'transcripts' : transcripts})
    
@login_required(login_url='login')
def transcript_list(request, specie):


    
    genome = Genome.objects.get(specie=specie)
    transcripts = Transcript.objects.filter(chromosome = genome.chromosome)

    return render(request, 'genomeBact/transcript_list.html',{'genome': genome, 'transcripts': transcripts})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Validateur'])
def transcript_create(request, specie):
    genome = Genome.objects.get(specie=specie)

    if request.method == 'POST':
        form = TranscriptForm(request.POST)  
        if form.is_valid():
            form.instance.chromosome = genome
            form.save()
            #return redirect('transcript-list', genome.specie)
            return redirect('genome-detail', genome.specie)
    else:
        form = TranscriptForm()

    return render(request,'genomeBact/transcript_create.html',{'form': form, 'genome' : genome}) 

@login_required(login_url='login')
def transcript_detail(request, specie, transcript):

    genome = Genome.objects.get(specie=specie)
    cds = Transcript.objects.get(transcript=transcript)

    if request.method == 'POST':
        form = AnnotForm(request.POST)  

        if 'Validate' in request.POST:
            Transcript.objects.filter(transcript=transcript).update(status = 'validated', status_date = Now(), annotator=None)
            messages.success(request, 'Annotations were validated.')
            return HttpResponseRedirect(request.path_info)
        elif 'to_validate' in request.POST:
            Transcript.objects.filter(transcript=transcript).update(status = 'annotated', status_date = Now())
            messages.success(request, 'Annotations were send for validation.')
            return HttpResponseRedirect(request.path_info)
        elif 'reject_validation' in request.POST:
            Transcript.objects.filter(transcript=transcript).update(status = 'assigned', status_date = Now())
            messages.success(request, 'Annotations were send back to '+ cds.annotator.name )
            return HttpResponseRedirect(request.path_info)
        elif form.is_valid():
            annotations = form.save(commit=False)
            gene = annotations.gene
            gene_biotype = annotations.gene_biotype
            transcript_biotype = annotations.transcript_biotype
            gene_symbol = annotations.gene_symbol
            description = annotations.description

            Transcript.objects.filter(transcript=transcript).update(gene = gene, gene_biotype=gene_biotype, transcript_biotype=transcript_biotype, gene_symbol=gene_symbol, description=description, status_date = Now())
            
            messages.success(request, 'Annotations were saved.')
            
            return HttpResponseRedirect(request.path_info)
    else:
        form = AnnotForm()

    context = {'genome':genome,'transcript': cds, 'form':form}
    return render(request, 'genomeBact/transcript_detail.html', context)
    
@login_required(login_url='login')
def transcript_annot(request, transcript):
    transcript = Transcript.objects.get(transcript=transcript)

    return render(request,'genomeBact/transcript_annot.html',{'transcript': transcript})

@login_required(login_url='login')
@admin_only
def admin(request):
    if request.method == 'POST':
        return redirect('register')

    nb_val = User.objects.filter(groups__name = "Validateur").count()
    nb_annot  = User.objects.filter(groups__name = "Annotateur").count()
    nb_read = User.objects.filter(groups__name = "Lecteur").count()

    all_val = Profile.objects.filter(group = "Validateur")
    all_annot = Profile.objects.filter(group = "Annotateur")
    all_read = Profile.objects.filter(group = "Lecteur")

    nb_to_assign = Transcript.objects.filter(status = 'empty').count()
    nb_to_val = Transcript.objects.filter(status = 'annotated').count()
    nb_to_annot = Transcript.objects.filter(status = 'assigned').count()

    context = {"nb_val":nb_val, "nb_annot":nb_annot, "nb_read":nb_read, "all_val":all_val, "all_annot":all_annot, "all_read":all_read,
               "nb_to_assign":nb_to_assign, "nb_to_val":nb_to_val, "nb_to_annot":nb_to_annot }
    return render(request,'genomeBact/admin.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Validateur','Annotateur'])
def workspace(request):
    transcripts_to_annotate = request.user.profile.to_annotate.all()
    #transcripts_to_annotate = request.user.profile.transcript_set.all()
    transcripts_to_assign = Transcript.objects.filter(status = 'empty')
    transcripts_to_validate = Transcript.objects.filter(status = 'annotated', validator = request.user.profile)
    annotators = User.objects.filter(groups__name='Annotateur')

    nb_to_assign = Transcript.objects.filter(status = 'empty').count()
    nb_to_val =  Transcript.objects.filter(status = 'annotated', validator = request.user.profile).count()
    nb_to_annot = request.user.profile.to_annotate.count()
    nb_send = '?'
    #nb_send = Transcript.objects.filter(status = 'empty').count()

    if request.method == 'POST':
        annotator_chosen = request.POST.get('annotator')
        transcript_chosen = request.POST.get('transcript_annot')
        
        if( request.user.groups.all()[0].name == 'Validateur'):
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

@login_required(login_url='login')
def validator(request):
    
    return render(request,'genomeBact/validator.html')

@login_required(login_url='login')
def assign_transcript(request):
    
    return render(request,'genomeBact/assign_transcript.html')

@login_required(login_url='login')
def transcript_list_state(request):
    
    return render(request,'genomeBact/transcript_list_state.html')

@login_required(login_url='login')
def transcript_to_validate(request):
    
    return render(request,'genomeBact/transcript_to_validate.html')

@login_required(login_url='login')
def annotator(request):
    
    return render(request,'genomeBact/annotator.html')

@login_required(login_url='login')
def transcript_to_annot(request):
    
    return render(request,'genomeBact/transcript_to_annot.html')


### NOT CURRENTLY WORKING NEED TO ADD GENOME FOR WHICH TRANSCRIPTS ARE UPLOADED ###
@login_required(login_url='login')
@admin_only
def transcript_upload(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() :
            
            file = request.FILES['file'] # Returns HttpRequest object

            # Convert byte to text mode for BioPython SeqIO
            stringio = StringIO(file.read().decode("utf-8")) 
            for record in SeqIO.parse(stringio, 'fasta'):
                t = Transcript(sequence = record.description)
                t.save()
            
     
        return HttpResponse(" Chargement réussi ! ")
    else:
        form = UploadFileForm()

    return render(request, 'polls/transcript_upload.html', {'form': form})