from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from budget.serializers import BudgetSerializer, ExpenseSerializer, BudgetDetailSerializer 
from core.models import Budget, Expense
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter



class BudgetList(generics.ListCreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'amount', 'total_used', 'created_date']

    def get_queryset(self):
        queryset = Budget.objects.filter(user=self.request.user).annotate(
            total_used=Sum('expenses__amount')
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class BudgetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    The total_used value is calculated by annotating the queryset with the sum of all expenses 
    related to the budget. This value is then added to the serializer context using the 
    get_serializer_context method.
    """
    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(user=self.request.user).annotate(
            total_used = Sum('expenses__amount')
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['total_used'] = self.get_object().total_used
        return context



class ExpenseList(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'amount', 'date']

    def get_queryset(self):
        budget_id = self.kwargs['budget_id']
        return Expense.objects.filter(budget__user=self.request.user, budget=budget_id)

    def perform_create(self, serializer):
        budget_id = self.kwargs['budget_id']
        budget = Budget.objects.get(user=self.request.user, pk=budget_id)
        serializer.save(user=self.request.user, budget=budget)



class ExpenseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(user=self.request.user)



class BudgetListFilter(generics.ListAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'amount', 'total_used', 'created_date']


    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('name', None)
        created_date = self.request.query_params.get('created_date', None)
        
        if not name and not created_date:
            raise ValidationError({"error" : "Please provide filtering parameters"})
        
        if name:
            queryset = queryset.filter(name__iexact=name)

        if created_date:
            queryset = queryset.filter(created_date__date=created_date)

        return queryset.filter(user=self.request.user)

    

class ExpensesListFilter(generics.ListAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'amount', 'date']  

    def get_queryset(self):
        budget_id = self.kwargs['budget_id']
        date = self.request.query_params.get('date', None)
        name = self.request.query_params.get('name', None)
        queryset = self.queryset.filter(budget__user=self.request.user, budget=budget_id)

        if not name and not date:
            raise ValidationError({"error" : "Please provide filtering parameters"})

        if name:
            queryset = queryset.filter(name__iexact=name)
        
        if date:
            queryset = queryset.filter(date__exact=date)
        
        return queryset



