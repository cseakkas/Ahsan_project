from django.shortcuts import redirect
from django.contrib import messages

def employeeLogin(function):
    def wrap(request, *args, **kwargs): 
        if request.session.get('user_id'): 
            return function(request, *args, **kwargs)
        else: 
            messages.add_message(request, messages.INFO,'Please Login First')
            return redirect('/adminlogin')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap