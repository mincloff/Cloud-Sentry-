from django.shortcuts import render
from .aws_logic import run_aws_scan
from .models import WasteReport

def dashboard_view(request):
    # Trigger the scan whenever the page is refreshed (for now)
    run_aws_scan()
    
    reports = WasteReport.objects.all()
    total_savings = sum(report.monthly_loss for report in reports)
    
    return render(request, 'scanner/dashboard.html', {
        'reports': reports,
        'total_savings': total_savings
    })

# Create your views here.
