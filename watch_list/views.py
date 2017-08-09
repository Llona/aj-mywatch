# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from .forms import WatchListForm, WatchAddForm
from collections import OrderedDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from watch_list.models import Anime, WatchState, News
import os
from allauth.account.decorators import verified_email_required

# for test, need remove============
from .forms import CommentForm, AddForm, photoForm
from watch_list.models import photo
from django.contrib.auth.models import User
# ====================================

"""
from django.template.loader import get_template
from django.template import Context


def hello_world(request):
    now = str(datetime.now())
    t = get_template('hello_world.html')
    html = t.render(Context({'current_time': now}))
    return HttpResponse(html)

"""
ERROR_TYPE = 0

ITEM_OF_ONE_PAGE = 10
PAGE_PRE_RANGE = 3
PAGE_NEXT_RANGE = 3


def index_home(request):
    news_h = News.objects.all().order_by('-date')
    anime_h = Anime.objects.all().order_by('-modify_date')[0:9]

    return render_to_response('home.html', locals(), context_instance=RequestContext(request))

def page_segmented(model_obj, current_page, item_num_of_one_page):
    pages = Paginator(model_obj, item_num_of_one_page)  # get all page
    tmp_page_range = []

    try:
        # get current page
        one_page_data = pages.page(current_page)
    except PageNotAnInteger:
        # if page number format incorrect, show page 1
        one_page_data = pages.page(1)
    except EmptyPage:
        # if page number is empty page, show last page
        one_page_data = pages.page(pages.num_pages)

    if pages.num_pages >= PAGE_PRE_RANGE + PAGE_NEXT_RANGE:
        # count page range
        pre_range_start = one_page_data.number - PAGE_PRE_RANGE
        next_range_end = one_page_data.number + PAGE_NEXT_RANGE

        if pre_range_start < 1:
            next_range_end += abs(pre_range_start)
            pre_range_start = 1
        elif next_range_end > pages.num_pages:
            pre_range_start -= next_range_end - pages.num_pages
            next_range_end = pages.num_pages

        # page range store into list
        for i in range(pre_range_start, next_range_end + 1):
            tmp_page_range.append(i)
    else:
        tmp_page_range = pages.page_range

    return one_page_data, tuple(tmp_page_range), pages


def watch_add_save_item(request, f, name):
    # Add new data to anime table
    anime_new_h = Anime.objects.create(name=name,
                                       origin_name=f.cleaned_data['origin_name'],
                                       url=f.cleaned_data['url'],
                                       media_type=f.cleaned_data['media_type'],
                                       total=f.cleaned_data['total'],
                                       type=f.cleaned_data['type'],
                                       publication_date=f.cleaned_data['publication_date'],
                                       # watch_state=,
                                       # creator=User.objects.get(id=request.user.id),
                                       creator=request.user,
                                       summary=f.cleaned_data['summary'],
                                       modify_date=datetime.utcnow() + timedelta(hours=8))

    # Add to request user watch list
    if request.POST['add_to_list'] == 'yes':
        # get templeats and form data
        watch_last_date = request.POST['watch_last_date']

        if watch_last_date == '':
            WatchState.objects.create(user=request.user,
                                      anime=anime_new_h,
                                      num_of_chapter=f.cleaned_data['watch_num_of_chapter'],
                                      watch_state=request.POST['watch_state'])
        else:
            WatchState.objects.create(user=request.user,
                                      anime=anime_new_h,
                                      watch_last_date=watch_last_date,
                                      num_of_chapter=f.cleaned_data['watch_num_of_chapter'],
                                      watch_state=request.POST['watch_state'])
    return anime_new_h


@verified_email_required
@login_required
def watch_list_page(request):
    # user press add item button
    if request.method == 'POST' and 'add_item' in request.POST:
        return HttpResponseRedirect('/search_add/')

    # uses type="reset" in template to replace
    # if request.method == 'POST' and 'cancel' in request.POST:
    #     return HttpResponseRedirect(request.get_full_path())

    watch_state_model_h = WatchState.objects.select_related('user').select_related('anime').filter(user__id=request.user.id).order_by('-watch_last_date')

    # user press modify data button
    if request.method == 'POST' and 'renew_all_item' in request.POST:
        watch_num_of_chapter = ''
        num_input_num_of_chapter = ''
        watch_num_of_anime_id = ''

        # if user has no item in list, do nothing
        if watch_state_model_h.count():
            count = 1
            while count <= int(request.POST['len_of_count']):
                tm_input_num_of_chapter = str('num_%s' % count)
                tm_anime_id = str('anime_id_%s' % count)
                tm_input_num_of_chapter_ori = str('num_of_chapter_ori_%s' % count)
                watch_state_ori = str('watch_state_ori_%s' % count)
                watch_state = str('watch_state_%s' % count)

                # get templeats data
                watch_num_of_chapter = request.POST[tm_input_num_of_chapter]
                watch_anime_id = request.POST[tm_anime_id]
                watch_num_of_chapter_ori = request.POST[tm_input_num_of_chapter_ori]
                watch_watch_state_ori = request.POST[watch_state_ori]
                watch_watch_state = request.POST[watch_state]

                watch_anime_model = watch_state_model_h.filter(anime__id=str(watch_anime_id))
                if watch_num_of_chapter_ori != watch_num_of_chapter:
                    watch_anime_model.update(num_of_chapter=watch_num_of_chapter,
                                             watch_last_date=(datetime.utcnow() + timedelta(hours=8)))

                if watch_watch_state_ori != watch_watch_state:
                    watch_anime_model.update(watch_state=watch_watch_state)

                count += 1

            # re-flush current page
            return HttpResponseRedirect(request.get_full_path())
        #     temp_text = '<br>watch_watch_state_ori:%s, watch_watch_state:%s</br>' % (str(watch_watch_state_ori), str(watch_watch_state))
        #     text = text + temp_text
        #     temp_text = ''
        # return HttpResponse(text)

        # watch_state_model = tuple(watch_state_model_h)
        # return render_to_response('watch_list.html', locals(), context_instance=RequestContext(request))

        # return HttpResponseRedirect('/my_watch/')

    # user press delete selected item button
    if request.method == 'POST' and 'delete_item' in request.POST:
        # if user has no item in list, do nothing
        if watch_state_model_h.count():
            # get templeats data
            check_selected_list = tuple(request.POST.getlist('selected_anime'))
            # get request user own all anime id
            watch_state_model = tuple(watch_state_model_h)
            user_animid_list = []
            for i in watch_state_model:
                user_animid_list.append(i.anime.id)
            user_animid_list = tuple(user_animid_list)

            # if anime id is in user own list, delete it
            for i in check_selected_list:
                if i not in user_animid_list:
                    watch_state_model_h.get(anime__id=i).delete()

            # return HttpResponseRedirect('/my_watch/')

        # re-flush current page
        return HttpResponseRedirect(request.get_full_path())

    # normal view state
    else:
        # pages
        current_page = request.GET.get("page", 1)
        current_page_data, page_range, pages_h = page_segmented(watch_state_model_h, current_page, ITEM_OF_ONE_PAGE)

        # one_page_data = pages.page(current_page)  # get current page

        # return render_to_response('watch_list.html', data, context_instance=RequestContext(request))

        # watch_state_model = tuple(watch_state_model_h)
        # return render_to_response('watch_list.html', locals(), context_instance=RequestContext(request))
        return render_to_response('watch_list.html', locals(), context_instance=RequestContext(request))


@verified_email_required
@login_required
def search_add(request):
    # if request.method == 'GET' and 'goto_add_item' in request.GET:
    #     return HttpResponseRedirect('/watch_add/')
    # else:
    #     return render_to_response('search_add.html', locals(), context_instance=RequestContext(request))
    return render_to_response('search_add.html', locals(), context_instance=RequestContext(request))

@verified_email_required
@login_required
def watch_data(request, offset):
    # user press cancel button, go to my_watch page
    if request.method == 'POST' and 'cancel' in request.POST:
        return HttpResponseRedirect('/my_watch/')

    # user press upload image button
    if request.method == 'POST' and 'upload_img' in request.POST:
        f = WatchListForm(request.POST, request.FILES)
        if f.is_valid():
            # is upload file
            if 'imgfile' in request.FILES:
                image = request.FILES["imgfile"]
                if image.size > 51200:
                    ERROR_TYPE = 1
                    return render_to_response('error.html', locals(), context_instance=RequestContext(request))

                anime_model_h = Anime.objects.get(id=offset)
                # if already has cover file, remove first
                if anime_model_h.cover:
                    if os.path.isfile(anime_model_h.cover.path):
                        os.remove(anime_model_h.cover.path)

                # return HttpResponse('image name=%s\n image size=%s\n image width=%s' % (image.name, image.size, image.width))

                # rename cover image file name
                img_filename, img_ext = os.path.splitext(image.name)
                cover_name = '%s_%s%s' % (img_filename, str(datetime.now()), img_ext)

                # save user upload file into database and MEDIA_ROOT path
                anime_model_h.cover.save(cover_name, image, save=True)

            return HttpResponseRedirect(request.get_full_path())

        else:
            ERROR_TYPE = 2
            image = None
            return render_to_response('error.html', locals(), context_instance=RequestContext(request))

    # ===is creator or not, is owner or not=====
    try:
        offset = int(offset)

    except ValueError:
        return render_to_response('error.html', locals(), context_instance=RequestContext(request))

    try:
        # anime id should only one
        anime_data_model_h = Anime.objects.get(id=offset)
    except:
        # can't find anime id, show error page
        return render_to_response('error.html', locals(), context_instance=RequestContext(request))

    is_owner = 0
    is_creator = 0

    if WatchState.objects.select_related('user').select_related('anime').filter(anime__id=offset, user__id=request.user.id).exists():
        # request user is own this anime
        is_owner = 1
        watch_data_model_h = WatchState.objects.select_related('user').select_related('anime').filter(user__id=request.user.id, anime__id=offset)
        watch_data_model = tuple(watch_data_model_h)[0]
        if anime_data_model_h.creator.id == request.user.id:
            # request user is own this anime and is creator
            is_creator = 1
    else:
        # request user is not own this anime
        if anime_data_model_h.creator.id == request.user.id:
            # request user is not own this anime but is creator
            is_creator = 1
    # =====

    # user press submit button, need to renew database data
    if request.method == 'POST' and 'renew_data' in request.POST:

        if is_owner == 1:  # request user own this anime
            if is_creator == 1:  # request user is owner and is creator
                f = WatchListForm(request.POST)
                if f.is_valid():
                    # get templeats and form data
                    total = str(f.cleaned_data['total'])
                    type = str(f.cleaned_data['type'])
                    publication_date = f.cleaned_data['publication_date']
                    origin_name = str(f.cleaned_data['origin_name'])
                    url = str(f.cleaned_data['url'])
                    summary = str(f.cleaned_data['summary'])

                    watch_num_of_chapter = str(f.cleaned_data['watch_num_of_chapter'])
                    watch_watch_state = str(request.POST['watch_state'])

                    watch_num_of_chapter_ori = str(request.POST['num_of_chapter_ori'])
                    watch_watch_state_ori = str(request.POST['watch_state_ori'])

                    total_ori = str(request.POST['total_ori'])
                    type_ori = str(request.POST['type_ori'])
                    publication_date_ori = str(request.POST['publication_date_ori'])
                    origin_name_ori = str(request.POST['origin_name_ori'])
                    url_ori = str(request.POST['url_ori'])
                    summary_ori = str(request.POST['summary_ori'])

                    try:
                        int(total)
                    except:
                        total = 0

                    # update watch_state table
                    if watch_num_of_chapter_ori != watch_num_of_chapter and watch_watch_state_ori != watch_watch_state:
                        watch_data_model_h.update(num_of_chapter=watch_num_of_chapter,
                                                  watch_state=watch_watch_state,
                                                  watch_last_date=(datetime.utcnow() + timedelta(hours=8)))
                    elif watch_num_of_chapter_ori != watch_num_of_chapter:
                        watch_data_model_h.update(num_of_chapter=watch_num_of_chapter,
                                                  watch_last_date=(datetime.utcnow() + timedelta(hours=8)))
                    elif watch_watch_state_ori != watch_watch_state:
                        watch_data_model_h.update(watch_state=watch_watch_state)

                    # update anime table
                    if total != total_ori or type != type_ori or publication_date != publication_date_ori \
                            or origin_name != origin_name_ori or url != url_ori or summary != summary_ori:
                        # temp_text = '<br>offset:%s total:%s total_ori:%s type:%s type_ori:%s publication_date:%s publication_date_ori:%s</br>' % (offset, total, total_ori, type, type_ori, publication_date, publication_date_ori)
                        # return HttpResponse(temp_text)
                        anime_data_model_h = Anime.objects.filter(id=str(offset)).update(total=total,
                                                                                         type=type,
                                                                                         publication_date=publication_date,
                                                                                         modify_date=datetime.utcnow() + timedelta(hours=8),
                                                                                         origin_name=origin_name,
                                                                                         url=url,
                                                                                         summary=summary)

                    # temp_text = '<br>%s</br>' % (str(request.POST['watch_state']))
                    # return HttpResponse(temp_text)
                    return HttpResponseRedirect('/my_watch/')

            # request user is own this anime but not creator
            else:
                watch_num_of_chapter = request.POST['num_of_chapter']
                watch_watch_state = request.POST['watch_state']
                watch_num_of_chapter_ori = request.POST['num_of_chapter_ori']
                watch_watch_state_ori = request.POST['watch_state_ori']

                #  if user is not creator, only need to update watch_state table
                if watch_num_of_chapter_ori != watch_num_of_chapter and watch_watch_state_ori != watch_watch_state:
                    watch_data_model_h.update(num_of_chapter=watch_num_of_chapter,
                                              watch_state=watch_watch_state,
                                              watch_last_date=(datetime.utcnow() + timedelta(hours=8)))
                elif watch_num_of_chapter_ori != watch_num_of_chapter:
                    watch_data_model_h.update(num_of_chapter=watch_num_of_chapter,
                                              watch_last_date=(datetime.utcnow() + timedelta(hours=8)))
                elif watch_watch_state_ori != watch_watch_state:
                    watch_data_model_h.update(watch_state=watch_watch_state)

                # text = '<br>watch_num_of_chapter:%s, watch_watch_state:%s</br>' % (str(watch_num_of_chapter), str(watch_watch_state))
                # return HttpResponse(text)
                return HttpResponseRedirect('/my_watch/')
        # user not own this anime
        else:
            # user not own this anime and is creator
            if is_creator == 1:
                f = WatchListForm(request.POST)
                if f.is_valid():
                    # get templeats and form data
                    total = str(f.cleaned_data['total'])
                    type = str(f.cleaned_data['type'])
                    publication_date = f.cleaned_data['publication_date']
                    origin_name = str(f.cleaned_data['origin_name'])
                    url = str(f.cleaned_data['url'])
                    summary = str(f.cleaned_data['summary'])

                    total_ori = str(request.POST['total_ori'])
                    type_ori = str(request.POST['type_ori'])
                    publication_date_ori = str(request.POST['publication_date_ori'])
                    origin_name_ori = str(request.POST['origin_name_ori'])
                    url_ori = str(request.POST['url_ori'])
                    summary_ori = str(request.POST['summary_ori'])

                    # update anime table
                    if total != total_ori or type != type_ori or publication_date != publication_date_ori \
                            or origin_name != origin_name_ori or url != url_ori or summary != summary_ori:
                        anime_data_model_h = Anime.objects.filter(id=str(offset)).update(total=total,
                                                                                         type=type,
                                                                                         publication_date=publication_date,
                                                                                         modify_date=datetime.utcnow() + timedelta(hours=8),
                                                                                         origin_name=origin_name,
                                                                                         url=url,
                                                                                         summary=summary)
                    return HttpResponseRedirect('/my_watch/')

            # if user not own this anime and not creator, user can't modify any thing

        # show this page when user input format incorrect
        return render_to_response('data.html', locals(), context_instance=RequestContext(request))
    # normal state, show information only
    else:
        # request user own this anime and is creator
        if is_owner == 1 and is_creator == 1:
            f = WatchListForm(None, initial={'total': watch_data_model.anime.total,
                                             'type': watch_data_model.anime.type,
                                             'publication_date': watch_data_model.anime.publication_date,
                                             'watch_num_of_chapter': watch_data_model.num_of_chapter,
                                             'origin_name': anime_data_model_h.origin_name,
                                             'media_type': anime_data_model_h.media_type,
                                             'url': anime_data_model_h.url,
                                             'summary': anime_data_model_h.summary})
        # request user not own this anime but is creator
        elif is_creator == 1:
            f = WatchListForm(None, initial={'total': anime_data_model_h.total,
                                             'type': anime_data_model_h.type,
                                             'publication_date': anime_data_model_h.publication_date,
                                             'origin_name': anime_data_model_h.origin_name,
                                             'media_type': anime_data_model_h.media_type,
                                             'url': anime_data_model_h.url,
                                             'summary': anime_data_model_h.summary})

        # if not own this anime and not creator, user can't modify any thing

        return render_to_response('data.html', locals(), context_instance=RequestContext(request))


@verified_email_required
@login_required
def watch_add(request):
    if request.method == 'POST' and 'cancel' in request.POST:
        return HttpResponseRedirect('/my_watch/')

    elif request.method == 'POST' and 'add_item' in request.POST:
        f = WatchAddForm(request.POST)
        if f.is_valid():
            # get templeats and form data
            name = f.cleaned_data['name']

            if Anime.objects.filter(name__iexact=name).count() > 0:
                # item name already exist, go to search page for user add this item
                return HttpResponseRedirect('/item_search/?keyword=%s&exist=%s' % (name, 1))

            # create new anime table
            anime_new_h = watch_add_save_item(request, f, name)

            # save new anime id to session for add cover page
            # request.session['id'] = anime_new_h.id

            # user input success, return to data page for add cover
            return HttpResponseRedirect('/watch_data/%s/' % anime_new_h.id)

        # user input has format error, reload this page
        return render_to_response('add_page_data.html', locals(), context_instance=RequestContext(request))

    elif request.method == 'POST' and 'add_next_item' in request.POST:
        f = WatchAddForm(request.POST)
        if f.is_valid():
            # get templeats and form data
            name = f.cleaned_data['name']

            if Anime.objects.filter(name__iexact=name).count() > 0:
                # item name already exist, go to search page for user add this item
                return HttpResponseRedirect('/item_search/?keyword=%s&exist=%s' % (name, 1))

            watch_add_save_item(request, f, name)

            # user input success, return to my_watch page
            return HttpResponseRedirect(request.get_full_path())

        # user input has format error, reload this page
        return render_to_response('add_page_data.html', locals(), context_instance=RequestContext(request))
    else:
        f = WatchAddForm()
        # f = WatchListForm(None, initial={'total': watch_data_model.anime.total,
        #                                  'type': watch_data_model.anime.type,
        #                                  'publication_date': watch_data_model.anime.publication_date,
        #                                  'watch_num_of_chapter': watch_data_model.num_of_chapter})

    return render_to_response('add_page_data.html', locals(), context_instance=RequestContext(request))

def auto_update_add_save_item(request, f, name):
    # Add new data to anime table
    total = f.cleaned_data['total']
    try:
        int(total)
    except:
        total = 0

    anime_new_h = Anime.objects.create(name=name,
                                       origin_name=f.cleaned_data['origin_name'],
                                       url=f.cleaned_data['url'],
                                       media_type=f.cleaned_data['media_type'],
                                       total=total,
                                       type=f.cleaned_data['type'],
                                       publication_date=f.cleaned_data['publication_date'],
                                       creator=request.user,
                                       summary=f.cleaned_data['summary'],
                                       modify_date=datetime.utcnow() + timedelta(hours=8))

    # Add to request user watch list
    if request.POST['add_to_list'] == 'yes':
        # get templeats and form data
        watch_last_date = request.POST['watch_last_date']

        if watch_last_date == '':
            WatchState.objects.create(user=request.user,
                                      anime=anime_new_h,
                                      num_of_chapter=f.cleaned_data['watch_num_of_chapter'],
                                      watch_state=request.POST['watch_state'])
        else:
            WatchState.objects.create(user=request.user,
                                      anime=anime_new_h,
                                      watch_last_date=watch_last_date,
                                      num_of_chapter=f.cleaned_data['watch_num_of_chapter'],
                                      watch_state=request.POST['watch_state'])
    return anime_new_h


@login_required
def auto_update_item_only(request):
    if request.method == 'POST' and 'add_item' in request.POST:
        f = WatchAddForm(request.POST)
        if f.is_valid():
            # get templeats and form data
            name = f.cleaned_data['name']

            anime_search_h = Anime.objects.filter(name=name)

            item_total_count = anime_search_h.count()

            if item_total_count > 0:  # item name already exist
                anime_wiki_h = Anime.objects.select_related('creator').filter(name=name).filter(creator__username='william_liu')
                item_wiki_count = anime_wiki_h.count()
                if item_wiki_count == 1:  # this is modify from wiki
                    total = f.cleaned_data['total']
                    try:
                        int(total)
                    except:
                        total = 0

                    anime_wiki_h.update(origin_name=f.cleaned_data['origin_name'],
                                         url=f.cleaned_data['url'],
                                         media_type=f.cleaned_data['media_type'],
                                         total=total,
                                         type=f.cleaned_data['type'],
                                         publication_date=f.cleaned_data['publication_date'],
                                         # creator=request.user,
                                         summary=f.cleaned_data['summary'],
                                         modify_date=datetime.utcnow() + timedelta(hours=8))

                    anime_model_h = anime_wiki_h[0]

                    if 'imgfile' in request.FILES:
                        image = request.FILES["imgfile"]
                        print(' ')
                        print(image.name)
                        print(' ')
                        # if already has cover file, remove first
                        if anime_model_h.cover:
                            if os.path.isfile(anime_model_h.cover.path):
                                os.remove(anime_model_h.cover.path)

                        # rename cover image file name
                        img_filename, img_ext = os.path.splitext(image.name)
                        cover_name = '%s_%s%s' % (img_filename, str(datetime.now()), img_ext)

                        # save user upload file into database and MEDIA_ROOT path
                        anime_model_h.cover.save(cover_name, image, save=True)

                    if item_wiki_count > item_wiki_count:
                        return HttpResponse('duplicate')
                    else:
                        return HttpResponse('renew')
                else:
                    return HttpResponse('dup_wiki')

            # create new anime table
            anime_new_h = auto_update_add_save_item(request, f, name)

            # save image
            if 'imgfile' in request.FILES:
                image = request.FILES["imgfile"]
                if anime_new_h.cover:
                    if os.path.isfile(anime_new_h.cover.path):
                        os.remove(anime_new_h.cover.path)

                # rename cover image file name
                img_filename, img_ext = os.path.splitext(image.name)
                cover_name = '%s_%s%s' % (img_filename, str(datetime.now()), img_ext)

                # save user upload file into database and MEDIA_ROOT path
                anime_new_h.cover.save(cover_name, image, save=True)
            # else:
            #     temp_text = '<br>image:%s</br>' % (str(anime_new_h.cover))
            #     return HttpResponse(temp_text)

            return HttpResponse('success')

        # user input has format error
        return HttpResponse('error')
    else:
        f = WatchAddForm()
        return render_to_response('auto_update_item.html', locals(), context_instance=RequestContext(request))


def watch_all_data(request):
    goto_page_one = False

    # for generate html select option data
    select_sort_odic = OrderedDict()
    select_sort_odic['1'] = '依字母'
    select_sort_odic['2'] = '依出版日期'
    select_sort_odic['3'] = '依修改日期'

    # press button
    if request.method == 'POST' and 'add_to_mywatch' in request.POST:
        # if is guest user, redirect to login page
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        else:
            # get templeats data
            check_selected_list = tuple(request.POST.getlist('selected_anime'))
            sort_type = str(request.POST['sort_type'])

            # get request user own all anime id
            watch_state_model = tuple(
                WatchState.objects.select_related('user').select_related('anime').filter(user__id=request.user.id))
            user_animid_list = []
            for i in watch_state_model:
                user_animid_list.append(i.anime.id)
            user_animid_list = tuple(user_animid_list)

            for i in check_selected_list:
                # print(" %s " % i)
                if i not in user_animid_list:
                    WatchState.objects.create(user=request.user,
                                              anime=Anime.objects.get(id=i))

        # current_page = request.GET.get("page", 1)
        # return HttpResponseRedirect('/item_search/?page=%s&keyword=%s' % (request.GET.get("page", 1), request.GET.get('keyword')))
        return HttpResponseRedirect(request.get_full_path())

    # html select item has changed
    elif request.method == 'POST':
        sort_str = str(request.POST['sort_type'])

        if sort_str == '1':
            anime_all_data_list = tuple(Anime.objects.all())
        elif sort_str == '2':
            anime_all_data_list = tuple(Anime.objects.all().order_by('-publication_date'))
        elif sort_str == '3':
            anime_all_data_list = tuple(Anime.objects.all().order_by('-modify_date'))
        else:
            anime_all_data_list = tuple(Anime.objects.all())

        goto_page_one = True

        # temp_text = ('<br>sort_type:%s</br>' % sort_type)
        # return HttpResponse(temp_text)

    # normal show page function
    else:
        sort_str = str(request.GET.get('sort', 1))

        if sort_str == '1':
            anime_all_data_list = tuple(Anime.objects.all())
        elif sort_str == '2':
            anime_all_data_list = tuple(Anime.objects.all().order_by('-publication_date'))
        elif sort_str == '3':
            anime_all_data_list = tuple(Anime.objects.all().order_by('-modify_date'))
        else:
            anime_all_data_list = tuple(Anime.objects.all())


    # get request user own all anime id
    watch_state_model = tuple(
        WatchState.objects.select_related('user').select_related('anime').filter(user__id=request.user.id))
    user_animid_list = []
    for i in watch_state_model:
        user_animid_list.append(i.anime.id)
    user_animid_list = tuple(user_animid_list)

    # page
    if goto_page_one:
        # if change sort type, go to page 1
        current_page = 1
    else:
        current_page = request.GET.get("page", 1)

    current_page_data, page_range, pages_h = page_segmented(anime_all_data_list, current_page, ITEM_OF_ONE_PAGE)

    return render_to_response('all_data.html', locals(), context_instance=RequestContext(request))


@verified_email_required
@login_required
def watch_search(request):
    # get keyword from search bar
    if request.method == 'GET':
        in_keyword = request.GET.get('keyword')
        is_exist = request.GET.get('exist')

        if not in_keyword:
            temp = '<br>請輸入關鍵字</br>'
            return HttpResponse(temp)

        # get request user own all anime id
        watch_state_model = tuple(WatchState.objects.select_related('user').select_related('anime').filter(user__id=request.user.id))
        user_animid_list = []
        for i in watch_state_model:
            user_animid_list.append(i.anime.id)
        user_animid_list = tuple(user_animid_list)

        anime_search_list = tuple(Anime.objects.filter(name__icontains=in_keyword))

        # page
        current_page = request.GET.get("page", 1)
        current_page_data, page_range, pages_h = page_segmented(anime_search_list, current_page, ITEM_OF_ONE_PAGE)

        return render_to_response('search_list.html', locals(), context_instance=RequestContext(request))

    # user press add button to add selected item to my_watch list
    elif request.method == 'POST' and 'add_to_mywatch' in request.POST:
        # get templeats data
        check_selected_list = tuple(request.POST.getlist('selected_anime'))

        # get request user own all anime id
        watch_state_model = tuple(WatchState.objects.select_related('user').select_related('anime').filter(user__id=request.user.id))
        user_animid_list = []
        for i in watch_state_model:
            user_animid_list.append(i.anime.id)
        user_animid_list = tuple(user_animid_list)

        for i in check_selected_list:
            # print(" %s " % i)
            if i not in user_animid_list:
                WatchState.objects.create(user=request.user,
                                          anime=Anime.objects.get(id=i))

        return HttpResponseRedirect(request.get_full_path())
        # return HttpResponseRedirect('/my_watch/')
    else:
        # error, return to my_watch page
        return HttpResponseRedirect('/my_watch/')


# for test, need remove ===================================================================================
def upload_image(request):
    photos = photo.objects.filter(id=1)
    if request.method == 'POST':
        form = photoForm(request.POST, request.FILES)
        if form.is_valid():
            # 判断是否上传了文件

            if 'docfile' in request.FILES:
                image = request.FILES["docfile"]

                # 修改文件名字
                image.name = str(request.user)+str(datetime.now())+'.jpg'
                s = photo(owner=request.user, image=image)
                s.save()
                return HttpResponse('上传成功')
            else:
                #没有上传文件直接点了上传就重定向到上传页面
                return HttpResponseRedirect('/upload/')
        else:

            image = None
            return HttpResponse('上传失败')
    else:
        return render_to_response('upload_image.html', locals(), context_instance=RequestContext(request))
        # return render(request, 'upload_image.html')


def comment(request):
    if request.method == 'POST':
        f = CommentForm(request.POST)

        if f.is_valid():
            user = f.cleaned_data['user']
            content = f.cleaned_data['content']
            email = f.cleaned_data['email']
            date_time = datetime.now()
            f = CommentForm()
    else:
        f = CommentForm()
    return render_to_response('comments.html', locals(), context_instance=RequestContext(request))


# def index(request):
#     if request.method == 'POST':
#
#         form = AddForm(request.POST)
#
#         if form.is_valid():
#             c = form.cleaned_data['a']
#             d = form.cleaned_data['b']
#             return HttpResponse(str(int(c) + int(d)))
#
#     else:
#         form = AddForm()
#     return render(request, 'index.html', {'form': form})


@login_required
def anime_watch_page(request):
    # return render(request, 'hello_world.html', {'current_time': str(datetime.now())})
    # return HttpResponse("Hello World!")

    username = request.user.username
    current_time = str(datetime.now())
    if request.user.email == "":
        email = "email is empty"
    else:
        email = request.user.email

    # return render_to_response('anime_watch.html', locals())


    # return render_to_response('watch_list_test.html', locals())
    return render_to_response('Untitled-9.html', locals())


@login_required
def test(request):
    USER_LIST = []
    for i in range(1, 999):
        temp = {"name": "root" + str(i), "age": i}
        USER_LIST.append(temp)

    # 模拟测试网页数据
    current_page = request.GET.get('p')
    paginator = Paginator(USER_LIST, 10)
    try:
        paginator = paginator.page(current_page)  # 获取前端传过来显示当前页的数据
    except PageNotAnInteger:
        # 如果有异常则显示第一页
        paginator = paginator.page(1)
    except EmptyPage:
        # 如果没有得到具体的分页内容的话,则显示最后一页
        paginator = paginator.page(paginator.num_pages)

    return render(request, 'test.html', {"users": paginator})
# ===================================================================================
