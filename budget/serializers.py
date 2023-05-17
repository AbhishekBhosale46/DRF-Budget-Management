from rest_framework import serializers
from core.models import Budget, Expense
from django.db.models import Sum



class ExpenseSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d-%m-%Y", input_formats=["%d-%m-%Y"])
    class Meta:
        model = Expense
        fields = ['id', 'date', 'name', 'amount']
        read_only_fields = ['id']



class BudgetSerializer(serializers.ModelSerializer):
    expenses = ExpenseSerializer(many=True, read_only=True)
    total_used = serializers.SerializerMethodField()

    """
    The aggregate method of the related expenses queryset calculates the total of the 
    amount field using the Sum function. The result of this calculation is a dictionary 
    with a single key-value pair, where the key is 'total' and the value is the sum of 
    the amount field of all related expenses.The method returns the value of the 'total' 
    key of this dictionary, which is the total amount used for the given budget.
    """
    def get_total_used(self, obj):
        return obj.expenses.aggregate(total=Sum('amount'))['total'] or 0

    class Meta:
        model = Budget
        fields = ['id', 'created_date', 'name', 'amount', 'total_used', 'expenses']
        read_only_fields = ['id', 'total_used']



class BudgetDetailSerializer(serializers.ModelSerializer):
    expenses = ExpenseSerializer(many=True, read_only=True)
    total_used = serializers.SerializerMethodField()

    """
    The get_total_used function simply returns the total_used value that was added 
    to the serializer context in the BudgetDetail view. This allows the total_used 
    value to be included in the serialized response for the budget detail view.
    """
    def get_total_used(self, obj):
        return self.context.get('total_used')

    class Meta:
        model = Budget
        fields = ['id', 'created_date', 'name', 'amount', 'total_used', 'expenses']
        read_only_fields = ['id', 'total_used']