import re
import logging
from django.contrib.auth.models import User, Group
from accounts.models import Profile
from rest_framework import viewsets
from rest_framework import permissions, status, generics
from .serializers import UserSerializer, GroupSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.contrib.auth import authenticate
from src.surveys.utils import calculate_digest


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CurrentUser(APIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return current user.
        """
        user    = User.objects.select_related('profile').filter(pk=request.user.id).values('id','username','first_name','last_name','email','profile__gender','profile__pic','profile__location')
        return Response(user)


#@csrf_exempt
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    

@csrf_exempt  
def login_user(request):
    """User login"""
    code        = request.POST.get('code')
    mobile      = request.POST.get('mobile')
    passwd1     = request.POST.get('password')
    
    response           = {}
    status_code        = 200

    if not code or not mobile or not passwd1:
        #log action
        logging.info("Required parameter missing")

        response['error']        = 'true'
        response['error_msg']    = 'Required parameters are missing'
        status_code              = 203
    else:
        # format mobile number
        username = code[1:] + cast_mobile(mobile)

        #log action
        logging.info("Casting phone and mobile code => " + username)

        # authenticate user
        user = authenticate(request, username=username, password=passwd1)

        if user is not None:
            response['error']    = 'false'
            response['uid']      = user.pk
            response['user']     = {'username':user.username,'first_name':user.first_name,'last_name':user.last_name}
            status_code          = 200

            #log action
            logging.info("User authenticated")
        else:
            response['error']        = 'true'
            response['error_msg']    = 'Invalid username or password'
            status_code              = 203

            #log action
            logging.info("Invalid username and password")
            
    return JsonResponse(response, safe=False, status=status_code)
    
        
@csrf_exempt  
def register_user(request):
    """User registration"""
    code        = request.POST.get('code')
    mobile      = request.POST.get('mobile')
    passwd1     = request.POST.get('password')
    passwd2     = request.POST.get('password_confirm')
    fname       = request.POST.get('first_name')
    lname       = request.POST.get('last_name')

    response           = {}
    status_code        = 200

    # format mobile number
    username = code[1:] + cast_mobile(mobile)

    #log action
    logging.info("Casting phone and mobile code => " + username)

    if passwd1 != passwd2:
        # return password mismatch
        response['error']        = 'true'
        response['error_msg']    = 'Password Mismatch'
        status_code              = 203

        #log action
        logging.info("Password mismatch")
    else:
        try:
            User.objects.get(username = username)
            response['error']        = 'true'
            response['error_msg']    = 'Mobile number already registered'
            status_code              = 203

            #log action
            logging.info("Mobile number already registered")
            
        except User.DoesNotExist:
            new_user = User.objects.create_user(username=username,password=passwd1,first_name=fname,last_name=lname)

            # set digest
            profile         = Profile.objects.get(user=new_user)
            profile.digest  = calculate_digest(new_user.username, passwd1)
            profile.save()

            #log action
            logging.info("Digested password => " + profile.digest)
            
            response['error']    = 'false'
            response['uid']      = new_user.pk
            response['user']     = {'username':new_user.username,'first_name':new_user.first_name,'last_name':new_user.last_name}
            status_code     = 200

            #log action
            logging.info("User registered")
    
    return JsonResponse(response,safe=False, status=status_code)


def cast_mobile(mobile):
    """Cast mobile number"""
    pattern = "^0[6-7]{1}[0-9]{8}$"

    #remove space
    mobile = mobile.replace(' ', '')

    if re.match(pattern, mobile):
      mobile = mobile[1:]
      return mobile
    else:
        return mobile
    