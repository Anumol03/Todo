from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from crm.models import Employee
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework import permissions,authentication
class EmployeesSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Employee

        fields="__all__"
# Create your views here.
class EmployeeView(ViewSet):
    # localhost:8000/api/employee
    # method-get
    def list(self,request,*args,**kwargs):
        qs=Employee.objects.all()
        if "department" in request.query_params:
            dept=request.query_params.get("department")
            qs=qs.filter(department=dept)
        if "salary" in request.query_params:
            sal=request.query_params.get("salary")
            qs=qs.filter(salary=sal)
        if "salary_gt" in request.query_params:
            sal=request.query_param.get("salary")
            qs=qs.filter(salary__gte=sal)
        serializer=EmployeesSerializer(qs,many=True)
        return Response(data=serializer.data)
    # localhost:8000/api/employee/
    # method-post
    def create(self,request,*args,**kwargs):
        serializer=EmployeesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    # localhost:8000/api/employee/<int:pk>/
    # method-get
    def retrieve(self,request,*args,**kwargs):
       id=kwargs.get("pk")
       qs=Employee.objects.get(id=id)
       serializers=EmployeesSerializer(qs)
       return Response(data=serializers.data)
    # localhost:8000/api/employee/<int:pk>/
    # method-put
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp_obj=Employee.objects.get(id=id)
        serializer=EmployeesSerializer(instance=emp_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # localhost:8000/api/employee/<int:pk>/
    # method-delete
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            Employee.objects.get(id=id).delete()
            return Response(data="deleted")
        except Exception:
            return Response(data="no matching record found")
    @action(methods=["get"],detail=False)
    def departments(self,request,*args,**kwargs):
        qs=Employee.objects.all().values_list("department",flat=True).distinct()
        return Response(data=qs)

class EmployeeViewSetView(ModelViewSet):
    serializer_class=EmployeesSerializer
    model=Employee
    queryset=Employee.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAdminUser]

        
            

