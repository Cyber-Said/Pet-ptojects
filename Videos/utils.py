from .models import Video
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginatVideos(request, video):
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 2))

    paginator = Paginator(video, size)

    try:
        paginated_video = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        paginated_video = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        paginated_video = paginator.page(page)

    return {
        "video": paginated_video.object_list,
        "current_page": page,
        "total_pages": paginator.num_pages,
        "total_video": paginator.count,
    }



def searchVideos(request):
    if request.GET.get('search'):
        search = request.GET.get('search', '')

        video = Video.objects.distinct().filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

        return video, search
    elif request.GET.get('filter'):
        search = request.GET.get('filter', '')


        video = Video.objects.distinct().filter(
            Q(author__icontains=search)
        )

        return video, search
    else:
        video = Video.objects.all()
        return video, None


