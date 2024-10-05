# myapp/context_processors.py
from Ad.models import project

def project_info(request):
    active_project = None
    active_project = request.COOKIES.get('active_project')

    if active_project:
        active_project = project.objects.filter(projectno=active_project).first()
    
    role = None
    if request.user and request.user.is_authenticated:
        role = request.user.role

    return {
        'active_project': active_project,
        'user_role': role
    }
