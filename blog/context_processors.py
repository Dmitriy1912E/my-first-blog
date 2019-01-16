from .models import Category


def blog(request):
        return {"categories": Category.objects.all()}
