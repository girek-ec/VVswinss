from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from core.utils import current_language, get_by_localized_slug

from .models import BlogCategory, BlogTag, Post


# ============================================================
# POST LIST
# ============================================================

def post_list(request):
    posts = (
        Post.objects
        .filter(is_published=True)
        .select_related(
            "category",
            "author",
        )
        .prefetch_related(
            "tags",
        )
        .order_by("-published_at")
    )

    categories = (
        BlogCategory.objects
        .filter(is_active=True)
        .order_by("name_fr")
    )

    tags = (
        BlogTag.objects
        .filter(is_active=True)
        .order_by("name_fr")
    )

    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    tag_slug = request.GET.get("tag", "").strip()

    active_category = None
    active_tag = None

    # ========================================================
    # CATEGORY FILTER
    # ========================================================

    if category_slug:
        active_category = (
            BlogCategory.objects
            .filter(is_active=True)
            .filter(
                Q(slug_fr=category_slug)
                | Q(slug_de=category_slug)
                | Q(slug_it=category_slug)
                | Q(slug_en=category_slug)
            )
            .first()
        )

        if active_category:
            posts = posts.filter(category=active_category)
        else:
            posts = posts.none()

    # ========================================================
    # TAG FILTER
    # ========================================================

    if tag_slug:
        active_tag = (
            BlogTag.objects
            .filter(is_active=True)
            .filter(
                Q(slug_fr=tag_slug)
                | Q(slug_de=tag_slug)
                | Q(slug_it=tag_slug)
                | Q(slug_en=tag_slug)
            )
            .first()
        )

        if active_tag:
            posts = posts.filter(tags=active_tag)
        else:
            posts = posts.none()

    # ========================================================
    # KEYWORD SEARCH
    # ========================================================

    if query:
        posts = posts.filter(
            Q(title_fr__icontains=query)
            | Q(title_de__icontains=query)
            | Q(title_it__icontains=query)
            | Q(title_en__icontains=query)
            | Q(excerpt_fr__icontains=query)
            | Q(excerpt_de__icontains=query)
            | Q(excerpt_it__icontains=query)
            | Q(excerpt_en__icontains=query)
            | Q(content_fr__icontains=query)
            | Q(content_de__icontains=query)
            | Q(content_it__icontains=query)
            | Q(content_en__icontains=query)
            | Q(category__name_fr__icontains=query)
            | Q(category__name_de__icontains=query)
            | Q(category__name_it__icontains=query)
            | Q(category__name_en__icontains=query)
            | Q(tags__name_fr__icontains=query)
            | Q(tags__name_de__icontains=query)
            | Q(tags__name_it__icontains=query)
            | Q(tags__name_en__icontains=query)
        ).distinct()

    # ========================================================
    # PAGINATION
    # ========================================================

    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    query_params = request.GET.copy()
    query_params.pop("page", None)
    preserved_query = query_params.urlencode()

    context = {
        "posts": page_obj.object_list,
        "page_obj": page_obj,
        "categories": categories,
        "tags": tags,
        "search_query": query,
        "active_category": active_category,
        "active_category_slug": category_slug,
        "active_tag": active_tag,
        "active_tag_slug": tag_slug,
        "preserved_query": preserved_query,
    }

    return render(request, "blog/post_list.html", context)


# ============================================================
# POST DETAIL
# ============================================================

def post_detail(request, slug):
    language = current_language()

    queryset = (
        Post.objects
        .filter(is_published=True)
        .select_related(
            "category",
            "author",
        )
        .prefetch_related(
            "tags",
            "sections",
        )
    )

    post = get_by_localized_slug(
        Post,
        slug,
        queryset=queryset,
    )

    # ========================================================
    # CANONICAL LOCALIZED SLUG
    # ========================================================

    localized_slug = getattr(post, f"slug_{language}", None) or post.slug_fr

    if slug != localized_slug:
        return redirect("blog:detail", slug=localized_slug)

    # ========================================================
    # RELATED POSTS
    # ========================================================

    related_posts = (
        Post.objects
        .filter(is_published=True, category=post.category)
        .exclude(pk=post.pk)
        .select_related("category", "author")
        .order_by("-published_at")[:3]
    )

    categories = (
        BlogCategory.objects
        .filter(is_active=True)
        .order_by("name_fr")
    )

    all_tags = (
        BlogTag.objects
        .filter(is_active=True)
        .order_by("name_fr")
    )

    context = {
        "post": post,
        "related_posts": related_posts,
        "categories": categories,
        "all_tags": all_tags,
    }

    return render(request, "blog/post_detail.html", context)