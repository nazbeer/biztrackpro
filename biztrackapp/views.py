from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.views.generic import TemplateView
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


def index(request):
    print('re',request.user)
    user = request.user
    business = ShopAdmin.objects.get(user = user)
    return HttpResponse(f"{user}  {business}")




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print('usser',user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
    


def logout_view(request):
    logout(request)
    return redirect('login') 

 
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            # Fetch the shop details associated with the logged-in user
            # try:
            try:
                shop_admin = ShopAdmin.objects.get(user=self.request.user)
            except ShopAdmin.DoesNotExist:

                return redirect('login')
            context['shop'] = shop_admin.shop
                
                # Get employees associated with the shop
                # employees = Employee.objects.filter(business_profile=context['shop'])
                
        #         today = timezone.now()
        #         start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        #         next_month = start_of_month.replace(month=start_of_month.month + 1, day=1)
        #         end_of_month = next_month - timezone.timedelta(days=1)
        #         current_month_year = timezone.now().strftime("%B %Y") 
        #         total_services_all = 0
        #         total_sales_all = 0
        #         # Fetch day closings from both models using a Union query
        #         day_closings1 = DayClosing.objects.filter(
        #             Q(date__range=[start_of_month, end_of_month]) & Q(employee__in=employees)
        #         ).annotate(
        #             total_services_annotated=Cast('total_services', output_field=DecimalField()),
        #             total_sales_annotated=Cast('total_sales', output_field=DecimalField()),
        #             total_advance_annotated=Cast('advance', output_field=DecimalField())  # Assuming advance is a DecimalField
        #         ).values('date', 'employee', 'total_services_annotated', 'total_sales_annotated', 'total_advance_annotated')

        #         day_closings_admin = DayClosingAdmin.objects.filter(
        #             Q(date__range=[start_of_month, end_of_month]) & Q(employee__in=employees)
        #         ).annotate(
        #             total_services_annotated=Cast('total_services', output_field=DecimalField()),
        #             total_sales_annotated=Cast('total_sales', output_field=DecimalField()),
        #             total_advance_annotated=Cast('advance', output_field=DecimalField())  # Assuming advance is a DecimalField
        #         ).values('date', 'employee', 'total_services_annotated', 'total_sales_annotated', 'total_advance_annotated')
        #         # print(day_closings_admin)
        #         # Combine the two querysets using Union
        #         combined_day_closings = day_closings1.union(day_closings_admin)

        #         for closing in combined_day_closings:
        #             # Extract relevant information from the closing
        #             date = closing['date']
        #             employee = closing['employee']
        #             total_services = closing['total_services_annotated']
        #             total_sales = closing['total_sales_annotated']
        #             total_advance = closing['total_advance_annotated']

        #             # Perform processing or actions with the extracted data
        #             # For example, you can print the information
        #             # print(f"Date: {date}, Employee: {employee}, Total Services: {total_services}, Total Sales: {total_sales}, Total Advance: {total_advance}")

        #             # Or you can perform other operations, such as calculations or saving to another data structure
        #             # For instance, you might aggregate the total services and total sales for all employees
        #             total_services_all += total_services
        #             total_sales_all += total_sales
                    
        #         # Optionally, you can pass the combined_day_closings queryset to the template context
        #             context = {
        #                 'combined_day_closings': combined_day_closings,
        #                 'total_services_all': total_services_all,
        #                 'total_sales_all': total_sales_all,
        #                 # Other context data as needed
        #             }
        #         # Fetch day closings for the current month
        #         day_closings = DayClosingAdmin.objects.filter(date__range=[start_of_month, end_of_month], employee__in=employees)
                
        #         # Calculate totals for services, sales, and advances for the current month
        #         total_services_this_month = day_closings.aggregate(total_services=Sum('total_services'))['total_services'] or 0
        #         total_sales_this_month = day_closings.aggregate(total_sales=Sum('total_sales'))['total_sales'] or 0
        #         total_advance_given_this_month = day_closings.aggregate(total_advance=Sum('advance'))['total_advance'] or 0
        #         employee_totals = []
        #         for employee in employees:
        #             employee_day_closings = DayClosingAdmin.objects.filter(date__range=[start_of_month, end_of_month], employee=employee)
        #             employee_total_services = employee_day_closings.aggregate(total_services=Sum('total_services'))['total_services'] or Decimal(0)
        #             employee_total_sales = employee_day_closings.aggregate(total_sales=Sum('total_sales'))['total_sales'] or Decimal(0)
        #             employee_total_advance = employee_day_closings.aggregate(total_advance=Sum('advance'))['total_advance'] or Decimal(0)

        #             # Fetching the first closing date of the employee
        #             first_closing_date = employee_day_closings.order_by('date').first().date.strftime('%Y-%m-%d') if employee_day_closings.exists() else None

        #             employee_totals.append({
        #                 'date': first_closing_date,
        #                 'employee': employee.id,
        #                 'employee_total_services': float(employee_total_services),
        #                 'employee_total_sales': float(employee_total_sales),
        #                 'employee_total_advance': float(employee_total_advance)
        #             })

        #         # Prepare chart data
        #         chart_data_json = [{
        #             'date': closing.date.strftime('%Y-%m-%d'),
        #             'total_services': float(closing.total_services),
        #             'total_sales': float(closing.total_sales),
        #             'advance': float(closing.advance),
        #         } for closing in day_closings]

        #         # Add totals to the context
        #         context['total_services_this_month'] = total_services_this_month
        #         context['total_sales_this_month'] = total_sales_this_month
        #         context['total_advance_given_this_month'] = total_advance_given_this_month
        #         context['chart_data_json'] = json.dumps(chart_data_json)
        #         context['employee_json'] = json.dumps(employee_totals)
        #         context['employees'] = employees
        #         context['current_month_year'] = current_month_year
        #         # print(json.dumps(employee_totals))
        #     except ShopAdmin.DoesNotExist:
        #         context['shop'] = None
        #         context['total_services_this_month'] = 0
        #         context['total_sales_this_month'] = 0
        #         context['total_advance_given_this_month'] = 0
        #         context['chart_data_json'] = '[]'
        #         context['employee_json'] = '[]'
        #         context['current_month_year'] = current_month_year
                
        categories = [
            {
                'name': 'Shop Management',
                'links': [
                    # {'label': 'Create Business', 'url_name': 'create_business_profile'},
                    # {'label': 'Business Profiles', 'url_name': 'business_profile_list'},
                ]
            },
            {
                'name': 'Role Management',
                'links': [
                    # {'label': 'Create Role', 'url_name': 'create_role'},
                    # {'label': 'Role List', 'url_name': 'role_list'},
                   
                ]
            },
            {
                'name': 'Employee Management',
                'links': [
                    #     {'label': 'Create Employee', 'url_name': 'create_employee'},
                    # {'label': 'Employee List', 'url_name': 'employee_list'},
                  
                ]
            },
        ]

        # context['categories'] = categories
        # return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to login page if user is not logged in
            return redirect(reverse('login'))  # Adjust 'login' to your login URL name
        return super().dispatch(request, *args, **kwargs)