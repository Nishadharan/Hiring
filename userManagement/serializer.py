from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import user, UserRoles
from rest_framework.exceptions import AuthenticationFailed
from HiringBackend.util.email import sendMail
from HiringBackend.util.emailHtmlLoader import emailHtmlLoader


class userRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserRoles
        fields='__all__'
        
    
class allUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=user
        fields=['id', 'empId','username', 'roles', 'is_active', 'pause', 'email']
        
class getUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=user
        fields='__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    # roles = userRolesSerializer(many=True)
    roles = serializers.PrimaryKeyRelatedField(queryset=UserRoles.objects.all(), required=True)

    class Meta:
        model = user
        fields = ['email', 'username', 'password','empId','roles']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
    
        if not username.isalnum():
            raise serializers.ValidationError('Username should not contain alpha numeric characters')

        return attrs

    def create(self, validated_data):
        return user.objects.create_user(**validated_data)
    
    
class UpdateallUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    email = serializers.EmailField(required=True)
    roles = serializers.PrimaryKeyRelatedField(queryset=UserRoles.objects.all(), required=True)
    class Meta:
        model = user
        fields = ('username', 'email', 'roles','empId','password', 'pause')


    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.roles=validated_data['roles']
        instance.empId=validated_data['empId']
        instance.set_password(validated_data['password'])
        instance.pause=validated_data['pause']
        instance.save()
        mail=sendMail()
        userpayload=validated_data
        content=emailHtmlLoader.userCreatedMail(userpayload)
        subject='User created'
        receipient=[]
        receipient.append(userpayload.get('email', None))
        mail.sendMailtoReceipients(content, subject, receipient)
        return instance
    
class loginSerializer(serializers.ModelSerializer):
    # email=serializers.EmailField(max_length=255, min_length=5)
    tokens=serializers.SerializerMethodField()
    password=serializers.CharField(max_length=255,min_length=8, write_only=True)
    username=serializers.CharField(max_length=255)
    
    def get_tokens(self, obj):
        users = user.objects.get(username=obj.get('username', ''))

        return {
            'access_token': users.tokens()['access_token'],
            'refresh_token': users.tokens()['refresh_token']
        }        
            
    class Meta:
        model=user
        fields=['username','password','tokens']        
        
    def validate(self, obj):
        name=obj.get('username', '')
        passWord=obj.get('password', '')
        
        user = authenticate(request=self.context.get('request'), username=name, password=passWord)
        
        if not user:
            raise AuthenticationFailed('Invalid Credentials')
            
        if not user.is_active:
            raise AuthenticationFailed('Account not valid, Contact admin')

        # if not user.is_email_verified:
        #     raise AuthenticationFailed('Email not verified')
        
        return {
            'email': user.email,
            'username': user.username,
            'id': user.id,
            'tokens': user.tokens()
        }

class ListOfInterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model=user
        fields=['id', 'username']
        