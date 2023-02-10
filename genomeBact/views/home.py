
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):


    '''
    Main page of the website. User can search instances of Genome or Transcript based on queries.
    
    '''
    # Does user submit anything ?
    if request.method == "POST":    
      
        # User submits and fill any research field
        if request.POST.keys() is not None:

            # Genome or transcript ?
            query_type = request.POST.get("query_type")
            request.session["query_type"] = query_type

            request.session["accession"] = request.POST.get("accession", "")
            request.session["specie"] = request.POST.get("specie", "")
            request.session["max"] = request.POST.get("max_length")
            request.session["min"] = request.POST.get("min_length")
            request.session["start"] = request.POST.get("start")
            request.session["stop"] = request.POST.get("stop")


            # Que des brin sens autorisés dans la DB
            if request.session["start"] > request.session["stop"]:

                return render(request, 'genomeBact/strand_error.html')

            if request.POST.get("sub_nt"):

                # Minimum substring length to search
                if len(request.POST.get("sub_nt")) < 3:

                    request.session["sub_nt"] = ""
                
                else:

                    request.session["sub_nt"] = request.POST.get("sub_nt")
            else:

                request.session["sub_nt"] = ""

            if request.POST.get("sub_pep"):

                # Minimum substring length to search
                if len(request.POST.get("sub_pep")) < 3:

                    request.session["sub_pep"] = ""
                
                else:

                    request.session["sub_pep"] = request.POST.get("sub_pep")
            else:

                request.session["sub_pep"]  = ""

            return redirect("results")

        # User submits button but does not enter query specification
        else:

            request.session["accession"] = ""
            request.session["specie"] = ""
            request.session["max"] = ""
            request.session["min"] = ""
            request.session["sub_nt"] = ""
            request.session["sub_pep"] = ""
            request.session["query_type"] = ""
            request.session["start"] = ""
            request.session["stop"] = ""
    else:

        # Return empty research fields to results/ if user don't submit button
        request.session["accession"] = ""
        request.session["specie"] = ""
        request.session["max"] = ""
        request.session["min"] = ""
        request.session["sub_nt"] = ""
        request.session["sub_pep"] = ""
        request.session["query_type"] = ""
        request.session["start"] = ""
        request.session["stop"] = ""


    return render(request,'genomeBact/home.html')
