from django.shortcuts import render

from core.utils import get_by_localized_slug

from .models import BlogCategory, Post


def post_list(request):
    posts = (
        Post.objects
        .filter(publicado=True)
        .select_related(
            "categoria",
            "autor",
        )
    )

    categorias = (
        BlogCategory.objects
        .filter(activo=True)
        .order_by("nombre_fr")
    )

    context = {
        "posts": posts,
        "categorias": categorias,
    }

    return render(
        request,
        "blog/post_list.html",
        context,
    )


def post_detail(request, slug):
    queryset = (
        Post.objects
        .filter(publicado=True)
        .select_related(
            "categoria",
            "autor",
        )
    )

    post = get_by_localized_slug(
        Post,
        slug,
        queryset=queryset,
    )

    relacionados = (
        Post.objects
        .filter(publicado=True)
        .exclude(pk=post.pk)
        .order_by("-fecha_publicacion")[:3]
    )

    context = {
        "post": post,
        "relacionados": relacionados,
    }

    return render(
        request,
        "blog/post_detail.html",
        context,
    )