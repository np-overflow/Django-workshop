from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.db import IntegrityError
from .models import ShortenedURL


def index(request: HttpRequest) -> HttpResponse:
    all_urls = ShortenedURL.objects.all()

    if request.method == "POST":
        original_url = request.POST.get("original_url")
        alias = request.POST.get("alias", "").strip()

        if not original_url:
            messages.error(request, "Please provide a valid URL.")
            return render(request, "index.html", {"all_urls": all_urls})

        if not alias:
            messages.error(request, "Please provide a custom alias.")
            return render(request, "index.html", {"all_urls": all_urls})

        if not alias.replace("_", "").replace("-", "").isalnum():
            messages.error(
                request,
                "Alias can only contain letters, numbers, hyphens, and underscores.",
            )
            return render(request, "index.html", {"all_urls": all_urls})

        if not original_url.startswith(("http://", "https://")):
            original_url = "https://" + original_url

        try:
            shortened_url = ShortenedURL(original_url=original_url, alias=alias)
            shortened_url.save()

            short_url = request.build_absolute_uri(f"/{shortened_url.alias}")
            messages.success(request, f"Short URL created: {short_url}")

        except IntegrityError:
            messages.error(
                request, "This alias is already taken. Please choose a different one."
            )
        except Exception:
            messages.error(request, "An error occurred while creating the short URL.")

        return redirect("url_shortener:index")

    return render(request, "index.html", {"all_urls": all_urls})


def redirect_to_original(request, alias):
    """Redirect to original URL and increment click count"""
    url_obj = get_object_or_404(ShortenedURL, alias=alias)

    ShortenedURL.objects.filter(pk=url_obj.pk).update(
        click_count=url_obj.click_count + 1
    )

    return redirect(url_obj.original_url)
