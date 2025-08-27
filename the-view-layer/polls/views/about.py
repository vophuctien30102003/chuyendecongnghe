from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "polls/about.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'About Our Django Application',
            'description': 'This application demonstrates Django views, templates, URLs, and forms.',
            'features': [
                'Class-based and function-based views',
                'Django template language with inheritance',
                'URL routing with custom converters',
                'Form handling with validation',
                'CSRF protection',
                'Error handling',
                'Static file management',
                'Responsive design'
            ]
        })
        return context