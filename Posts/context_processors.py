from Posts.models import Category, Tag
def get_categories_and_tags(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return {
        'categories': categories,
        'tags': tags
    }
