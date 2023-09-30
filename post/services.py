from post.models import Post


def generate_unique_slug(slug):
    num = 1
    new_slug = slug
    while Post.objects.filter(slug=new_slug).exists():
        new_slug = f"{slug}-{num}"
        num += 1
    return new_slug


def increase_views_count(post):
    post.views_count += 1
    post.save()
