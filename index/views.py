from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login, logout
import re
from django.utils.text import slugify
from .models import Cluster, Candidate, Tabulation, User, News,News_category, Activity_Log, Action_flag, Modules, Programs, Keyword, Landing_page, Info, Page, Live_File, Content_Manager, Identification_Number
from .forms import NewsForm, LogForm, ClientForm, SendMail, NewUserForm
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib import messages
import facebook
import json, urllib.request





def video(request):
    keywords = Keyword.objects.all()
    token = {'EAAKiLZBkybEYBAF4DVZBds0kT8La2z4tPZC7NQzUU3SwQCiznEKwPZBSQn2PGn0RIIMb2LOJjWgLVw2guff0mgLRbGwmkYeFclTZBsDMDPAEvzF41Xcyid0l0iSVpvrTRBbT0NjskgvrMlm4Qj72GlYRNDK0nvjRhVFj6hdapIIrpNNGsL1wy'}
    graph = facebook.GraphAPI(token)
    fields = ['videos{id,title,description,picture,created_time,source,live_status,embed_html}']
    json_data = graph.get_object('RadyoKapanalo90.5', fields=fields)
    parsed_json = json.dumps(json_data, indent=4)
    loaded_json = json.loads(parsed_json)
    video_list = []
    videos = {}
    live_video = {}
    latest_video = {}
    featured_video = {}
    data = loaded_json['videos']['data']
    paging = loaded_json['videos']['paging']
    for index,attributes in enumerate(data):
        #create dict here
        try:
            if attributes['live_status'] == 'LIVE':
                try:
                    live_video['id'] = attributes['id']
                    try:
                        live_video['title'] = attributes['title']
                    except:
                        live_video['title'] = attributes['description']
                    try:
                        live_video['description'] = attributes['description']
                    except:
                        live_video['description'] = 'No Description'
                    live_video['picture'] = attributes['picture']

                    live_video['created_time'] = attributes['created_time']
                    live_video['source'] = "https://www.facebook.com/video.php?v="+ attributes['id']

                except Exception as e:
                    pass

            elif attributes['live_status'] == 'VOD':
                try:
                    if index ==0:
                        latest_video['id'] = attributes['id']
                        try:
                            latest_video['title'] = attributes['title']
                        except:
                            latest_video['title'] = attributes['description']
                        try:
                            latest_video['description'] = attributes['description']
                        except:
                            latest_video['description'] = 'No Description'
                        latest_video['picture'] = attributes['picture']

                        latest_video['created_time'] = attributes['created_time']
                        latest_video['source'] = "https://www.facebook.com/video.php?v="+ attributes['id']

                    videos['id'] = attributes['id']
                    try:
                        videos['title'] = attributes['title']
                    except:
                        videos['title'] = attributes['description']
                    try:
                        videos['description'] = attributes['description']
                    except:
                        videos['description'] = 'No Description'
                    videos['picture'] = attributes['picture']
                    videos['created_time'] = attributes['created_time']
                    i = 0
                    for keyword in keywords:
                        if i >= 1: break
                        if keyword.keyword.casefold() in videos.get('title').casefold() or keyword.keyword.casefold() in videos.get('description').casefold() :

                            programs = Programs.objects.filter(title__iexact=keyword.program)
                            for program in programs:
                                videos['program'] = program.title
                                i+=1
                        else:
                            videos['program'] = 'others'

                    video_list.append(videos.copy())
                except Exception as e:
                    pass
        except Exception as e:
            messages.error(request, {e})

    url = paging['next']
    bool = True
    while(bool):
        response = urllib.request.urlopen(url)
        loaded_json = json.loads(response.read())
        data = loaded_json['data']
        for index, attributes in enumerate(data):
            try:
                videos['id'] = attributes['id']
                try:
                    videos['title'] = attributes['title']
                except:
                    videos['title'] = attributes['description']
                try:
                    videos['description'] = attributes['description']
                except:
                    videos['description'] = 'No Description'
                videos['picture'] = attributes['picture']
                videos['created_time'] = attributes['created_time']
                i = 0
                for keyword in keywords:
                    if i >= 1: break
                    if keyword.keyword.casefold() in videos.get('title').casefold() or keyword.keyword.casefold() in videos.get('description').casefold():
                        programs = Programs.objects.filter(title__iexact=keyword.program)
                        for program in programs:
                            videos['program'] = program.title
                            i += 1
                    else:
                        videos['program'] = 'others'
                video_list.append(videos.copy())

            except Exception as e:
                pass
        try:
            paging = loaded_json['paging']
            url = paging['next']
            bool = True
        except:
            bool = False
    return render(request, 'index/videos/videos.html', {'live_video':live_video,
                                                        'latest_video': latest_video,
                                                        'video_list':video_list})

def video_detail(request, grouper, title, video_id, status):
    try:
        token = {
            'EAAKiLZBkybEYBAF4DVZBds0kT8La2z4tPZC7NQzUU3SwQCiznEKwPZBSQn2PGn0RIIMb2LOJjWgLVw2guff0mgLRbGwmkYeFclTZBsDMDPAEvzF41Xcyid0l0iSVpvrTRBbT0NjskgvrMlm4Qj72GlYRNDK0nvjRhVFj6hdapIIrpNNGsL1wy'}
        graph = facebook.GraphAPI(token)
        fields = ['id,title,description,picture,created_time,source, embed_html']
        json_data = graph.get_object(str(video_id), fields=fields)
        parsed_json = json.dumps(json_data, indent=4)
        loaded_json = json.loads(parsed_json)
        video = {}
        if str(video_id) == loaded_json['id']:
            video['id'] = loaded_json['id']
            try:
                video['title'] = loaded_json['title']
            except:
                video['title'] = loaded_json['description']
            try:
                video['description'] = loaded_json['description']
            except:
                video['description'] = 'No Description'
            video['picture'] = loaded_json['picture']
            video['created_time'] = loaded_json['created_time']
            if status == 'LIVE':
                video['source'] = "https://www.facebook.com/video.php?v="+ loaded_json['id']
            elif status == 'VOD':
                video['source'] = "https://www.facebook.com/video.php?v="+ loaded_json['id']
            video['status'] = status
        return render(request, 'index/videos/video_detail.html', {'video': video})
    except Exception as e:
        return HttpResponse("ERROR 500 "+str(e))



def video_list(request, program):
    try:
        keywords = Keyword.objects.all()
        token = {'EAAKiLZBkybEYBAF4DVZBds0kT8La2z4tPZC7NQzUU3SwQCiznEKwPZBSQn2PGn0RIIMb2LOJjWgLVw2guff0mgLRbGwmkYeFclTZBsDMDPAEvzF41Xcyid0l0iSVpvrTRBbT0NjskgvrMlm4Qj72GlYRNDK0nvjRhVFj6hdapIIrpNNGsL1wy'}
        graph = facebook.GraphAPI(token)
        fields = ['videos{id,title,description,picture,created_time,live_status}']
        json_data = graph.get_object('RadyoKapanalo90.5', fields=fields)
        parsed_json = json.dumps(json_data, indent=4)
        loaded_json = json.loads(parsed_json)
        video_list = []
        videos = {}
        data = loaded_json['videos']['data']
        paging = loaded_json['videos']['paging']
        for index, attributes in enumerate(data):
            # create dict here
            try:
                videos['id'] = attributes['id']
                try:
                    videos['title'] = attributes['title']
                except:
                    videos['title'] = attributes['description']
                try:
                    videos['description'] = attributes['description']
                except:
                    videos['description'] = 'No Description'
                videos['picture'] = attributes['picture']
                videos['created_time'] = attributes['created_time']

                x = len(keywords)
                for keyword in keywords:
                    if keyword.keyword.casefold() in videos.get(
                            'title').casefold() or keyword.keyword.casefold() in videos.get('description').casefold():
                        key = Keyword.objects.get(keyword__iexact=str(program).replace('-', ' '))
                        if key.program == keyword.program:
                            programs = Programs.objects.filter(title__iexact=keyword.program)
                            for program in programs:
                                videos['program'] = program.title
                                video_list.append(videos.copy())
                                break
                            break
                    else:
                        videos['program'] = 'others'
                        if x <= 1 and str(program) == 'others':
                            video_list.append(videos.copy())
                        x -= 1

            except Exception as e:
                pass

        url = paging['next']
        bool = True
        while (bool):
            response = urllib.request.urlopen(url)
            loaded_json = json.loads(response.read())
            data = loaded_json['data']
            for attributes in data:
                try:
                    videos['id'] = attributes['id']
                    try:
                        videos['title'] = attributes['title']
                    except:
                        videos['title'] = attributes['description']
                    try:
                        videos['description'] = attributes['description']
                    except:
                        videos['description'] = 'No Description'
                    videos['picture'] = attributes['picture']
                    videos['created_time'] = attributes['created_time']

                    x = len(keywords)
                    for keyword in keywords:

                        if keyword.keyword.casefold() in videos.get(
                                'title').casefold() or keyword.keyword.casefold() in videos.get(
                                'description').casefold():
                            key = Keyword.objects.get(keyword__iexact=str(program).replace('-', ' '))
                            if key.program == keyword.program:
                                programs = Programs.objects.filter(title__iexact=keyword.program)
                                for program in programs:
                                    videos['program'] = program.title
                                    video_list.append(videos.copy())
                                    break
                                break

                        else:
                            videos['program'] = 'others'
                            if x <= 1 and str(program) == 'others':
                                video_list.append(videos.copy())
                            x -= 1

                except Exception as e:
                    pass
            try:
                paging = loaded_json['paging']
                url = paging['next']
                bool = True
            except:
                bool = False
        return render(request, 'index/videos/video_list.html', {'video_list': video_list})
    except Exception as e:
        return HttpResponse("ERROR 500 "+str(e))


def index(request):
    landing_cover = Landing_page.objects.filter(is_show=True).order_by('order')
    live_file = Live_File.objects.get(is_live=True)
    audio_file = live_file.audio_url
    video_file = live_file.video_url
    token = {'EAAKiLZBkybEYBAF4DVZBds0kT8La2z4tPZC7NQzUU3SwQCiznEKwPZBSQn2PGn0RIIMb2LOJjWgLVw2guff0mgLRbGwmkYeFclTZBsDMDPAEvzF41Xcyid0l0iSVpvrTRBbT0NjskgvrMlm4Qj72GlYRNDK0nvjRhVFj6hdapIIrpNNGsL1wy'}
    graph = facebook.GraphAPI(token)
    fields = ['videos{id,live_status}']
    json_data = graph.get_object('RadyoKapanalo90.5', fields=fields)
    parsed_json = json.dumps(json_data, indent=4)
    loaded_json = json.loads(parsed_json)
    data = loaded_json['videos']['data']
    for index, attributes in enumerate(data):
        # create dict here
        try:
            if attributes['live_status'] == 'LIVE':
                try:
                    video_file = "https://www.facebook.com/video.php?v="+ attributes['id']
                except Exception as e:
                    pass
            elif attributes['live_status'] == 'VOD':
                try:
                    if index == 0:
                        video_file = "https://www.facebook.com/video.php?v="+ attributes['id']
                except Exception as e:
                    pass
        except Exception as e:
            pass

    return render(request, 'index/landing_page.html', {'landing_cover': landing_cover,
                                                       'audio_url':audio_file,
                                                       'video_url':video_file})

def validate_password(password1, password2 , first_name, last_name, username, email):

    is_error = False
    error = None
    count = Content_Manager.objects.filter(password = password1)
    if len(count) > 0:
        is_error = True
        error = 'Your password is too common.'
    if password1 != password2:
        is_error = True
        error = "Your must enter the same password."
    if password1.casefold() == (first_name.casefold()+last_name.casefold()) or password1.casefold() == first_name.casefold() or password1.casefold() == last_name.casefold() or password1.casefold() == username.casefold() or password1.casefold() == email.casefold():
        is_error = True
        error = "Your password can't be too similar to your other personal information."
    if len(password1) < 8:
        is_error = True
        error = "Your password must contain at least 8 characters."
    if password1.isdigit():
        is_error = True
        error = "Your password cannot be entirely numeric."
    return [password1, error, is_error]

def validate_email(email):
    count = User.objects.filter(email=email)
    if len(count) > 0:
        is_error = True
        error = 'Email already exists.'
    else:
        is_error = False
        error = None
    return [email, error, is_error]

def validate_username(username):
    count = User.objects.filter(username=username)
    if len(count) > 0:
        is_error = True
        error = 'Username already in use.'
    else:
        is_error = False
        error = None
    return [username, error, is_error]

def validate_id(id):
    try:
        content_manager = Content_Manager.objects.get(employee_id = id)
        user = User.objects.get(username = content_manager.username)
        is_error = True
        error = 'This ID is currently in use. Contact Admin for ID issuance.'
    except:
        if id.isdigit():
            is_error = False
            error = None
        else:
            is_error = True
            error = "Enter correct ID."


    return [id, error,is_error]

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        valid_id = validate_id(request.POST['employee_id'])
        valid_password = validate_password(request.POST['password1'],
                                           request.POST['password2'],
                                           request.POST['first_name'],
                                           request.POST['last_name'],
                                           request.POST['username'],
                                           request.POST['email'])
        valid_email = validate_email(request.POST['email'])
        valid_username = validate_username(request.POST['username'])
        if id == None:
            messages.error(request,  "You should be an employee to access this page!")
        else:
            content_manager = Content_Manager()
            try:
                coded_id = Identification_Number.objects.get(employee_id = valid_id[0])
                if valid_id[2]:
                    messages.error(request, str(valid_id[1]))
                elif valid_username[2]:
                    messages.error(request, str(valid_username[1]))
                elif valid_email[2]:
                    messages.error(request, str(valid_email[1]))
                elif valid_password[2]:
                    messages.error(request, str(valid_password[1]))
                else:
                    try:
                        if form.is_valid():
                            user = form.save(commit=False)
                            user.set_password(valid_password[0])
                            user.save()
                            content_manager.employee_id = coded_id.employee_id
                            content_manager.first_name = user.first_name
                            content_manager.last_name = user.last_name
                            content_manager.username = user.username
                            content_manager.email = user.email
                            content_manager.password = valid_password[0]
                            content_manager.is_confirmed = True
                            content_manager.save()
                            login(request, user)
                            messages.success(request, f"New account created: {user.username}")
                            return redirect(reverse('index:mod', kwargs={'user_id': user.id}))
                        else:
                            return render(request, 'index/register.html', {"form": form})
                    except Exception as e:
                        messages.error(request, str(e))
            except Exception as e:
                if valid_id[2]:
                    messages.error(request, str(valid_id[1]))
                elif valid_username[2]:
                    messages.error(request, str(valid_username[1]))
                elif valid_email[2]:
                    messages.error(request, str(valid_email[1]))
                elif valid_password[2]:
                    messages.error(request, str(valid_password[1]))
                else:
                    try:
                        content_manager.employee_id = valid_id[0]
                        content_manager.first_name = request.POST['first_name']
                        content_manager.last_name = request.POST['last_name']
                        content_manager.username = request.POST['username']
                        content_manager.email = request.POST['email']
                        content_manager.password = valid_password[0]
                        content_manager.is_confirmed = False
                        content_manager.save()
                        messages.info(request, "Thank you. Your request has been sent. Further notice will be sent thru email.")
                        return redirect(reverse('index:login_user'))
                    except Exception as e:
                        messages.error(request, str(e))

        return render(request=request,
                  template_name="index/register.html",
                  context={"form": form})

    form = NewUserForm
    return render(request = request,
                     template_name = "index/register.html",
                      context={"form":form})

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("index:login_user")

def login_user(request):

    if request.user.id is not None:
        messages.error(request, str(request.user.id))
        return redirect(reverse('index:mod', kwargs={'user_id': request.user.id}))
    else:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)

            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                #user is valid content manager
                try:
                    content_manager = Content_Manager.objects.get(username = username)
                    if content_manager.is_confirmed:
                        pass
                    else:
                        content_manager.is_confirmed = True
                        content_manager.save()
                        messages.warning(request, "Status updated")
                except Exception as e:
                    if user.is_superuser:
                        pass
                    else:
                        messages.warning(request, str(e))

                login(request, user)
                messages.success(request, f"You are now logged in as {username}")
                return redirect(reverse('index:mod', kwargs={'user_id': request.user.id}))
            else:
                try:
                    content_manager = Content_Manager.objects.get(username=username)
                    try:
                        valid_id = Identification_Number.objects.get(employee_id=content_manager.employee_id)
                        try:
                            content_manager.is_confirmed = True
                            content_manager.save()
                            messages.warning(request, "Status updated")
                            new_user = User()
                            new_user.first_name = content_manager.first_name
                            new_user.last_name = content_manager.last_name
                            new_user.username = content_manager.username
                            new_user.email = content_manager.email
                            new_user.set_password(content_manager.password)
                            new_user.save()
                            login(request, new_user)
                            messages.success(request, f"You are now logged in as {new_user.username}")
                            return redirect(reverse('index:mod', kwargs={'user_id': request.user.id}))
                            # user is now a valid content manager
                        except Exception as e:
                            messages.error(request, str(e))
                    except:
                        if content_manager.is_confirmed:
                            #user is confirmed but not yet registered
                            #id wasnt added after user registration
                            #user not yet registered
                            try:
                                new_id = Identification_Number()
                                new_id.employee_id = content_manager.employee_id
                                new_id.save()
                            except Exception as e:
                                messages.error(request, str(e))
                            try:
                                new_user = User()
                                new_user.first_name = content_manager.first_name
                                new_user.last_name = content_manager.last_name
                                new_user.username = content_manager.username
                                new_user.email = content_manager.email
                                new_user.set_password(content_manager.password)
                                new_user.save()
                                login(request, new_user)
                                messages.success(request, f"You are now logged in as {new_user.username}")
                                return redirect(reverse('index:mod', kwargs={'user_id': request.user.id}))
                                #user is now a valid content manager
                            except Exception as e:
                                messages.error(request, str(e))
                        else:
                            messages.warning(request, "Im sorry, your request is still under validation process.")

                except Exception as e:
                    messages.error(request, "Invalid username or password")
                    messages.error(request, str(e))

    form = AuthenticationForm()
    return render(request, "index/login.html",{"form":form})

def mod(request, user_id):

    news = News.objects.filter(author = user_id).order_by('-date')[:5]
    cluster = Cluster.objects.filter(user=user_id)
    logs = Activity_Log.objects.filter(user=user_id).order_by('-datetime')[:10]
    logCount = Activity_Log.objects.filter(user=user_id).count

    if request.user.id is None or request.user.id != int(user_id):
        return redirect("index:forbidden")
    else:
        return render(request, 'index/admin.html', {'news': news,
                                                    'cluster': cluster,
                                                    'user': request.user,
                                                    'logs': logs,
                                                    'logCount': logCount})

def compose_article(request, user_id):
    try:
        if request.user.id is None:
            return redirect("index:forbidden")
        else:
            form = NewsForm(request.POST or None, request.FILES or None)
            log = LogForm()
            user = User.objects.filter(id=user_id)
            if form.is_valid():
                news = form.save(commit=False)
                news.author = request.user
                news.is_published = request.POST.get('is_published', '') == 'on'
                news.save()
                # Log Entry
                logs = log.save(commit=False)
                logs.action_flag = Action_flag.objects.get(action='ADD')
                logs.user = User.objects.get(id=user_id)
                logs.affected_table = Modules.objects.get(module='NEWS')
                logs.news_obj = News.objects.get(id=news.id)
                logs.save()

                messages.info(request, f"Your article is posted")
                return redirect(reverse('index:news_detail', kwargs={'category': slugify(news.category.title),
                                                                     'headline': slugify(news.headline),
                                                                     'news_id': news.id}))
            return render(request, 'index/news/write_news.html', {"form": form, "user": user})

    except Exception as e:
        return HttpResponse("ERROR 500 "+str(e))

def update_article(request, user_id, news_id, show):
    try:
        if request.user.id is None:
            return redirect("index:forbidden")
        else:
            if bool(show):
                user = User.objects.filter(id=user_id)
                news_to_edit = News.objects.get(id=news_id)
                data = {'Category': news_to_edit.category, 'Headline': news_to_edit.headline,
                        'Content': news_to_edit.content, 'Cover Image': news_to_edit.picture}
                log = LogForm()
                form_to_update = NewsForm(request.POST or None, request.FILES or None, instance=news_to_edit,
                                          initial=data)
                if form_to_update.is_valid():
                    form_to_update.save()
                    news_to_edit.is_published = request.POST.get('is_published', '') == 'on'
                    news_to_edit.save()
                    # Log Entry
                    logs = log.save(commit=False)
                    logs.action_flag = Action_flag.objects.get(action='UPDATE')
                    logs.user = User.objects.get(id=user_id)
                    logs.affected_table = Modules.objects.get(module='NEWS')
                    logs.news_obj = News.objects.get(id=news_to_edit.id)
                    logs.save()

                    messages.info(request, f"You have successfully updated your article")
                    return redirect(reverse('index:news_detail',
                                            kwargs={'category': slugify(news_to_edit.category.title),
                                                    'headline': slugify(news_to_edit.headline),
                                                    'news_id': news_to_edit.id}))
                previous_url = request.META.get('HTTP_REFERER')
                if previous_url is not None:
                    split_url = re.split(r"[^A-Za-z']+", previous_url)
                    for word in split_url:
                        if word == "list":
                            return render(request, 'index/news/update_news.html', {"form": form_to_update,
                                                                                   "user": user,
                                                                                   "url": 'news_list',
                                                                                   "news": news_to_edit})
                        else:
                            continue
                else:
                    return redirect("index:forbidden")
                return render(request, 'index/news/update_news.html', {"form": form_to_update,
                                                                       "user": user,
                                                                       "url": 'mod',
                                                                       "news": news_to_edit})
            else:
                return redirect("index:forbidden")
    except Exception as e:
        return HttpResponse("ERROR 500 "+str(e))



def candidates(request, cluster_id):

    Cluster.objects.filter(pk=cluster_id).update(user=request.user)

    lungsod_list = Candidate.objects.filter(position=10)
    vice_mayor_list = Candidate.objects.filter(position=9)
    mayor_list = Candidate.objects.filter(position=8)
    lalawigan_list = Candidate.objects.filter(position=7)
    vice_gov_list = Candidate.objects.filter(position=6)
    governor_list = Candidate.objects.filter(position = 5)
    congressman_list = Candidate.objects.filter(position=4)

    candidate_list = Candidate.objects.all()
    return render (request, 'index/bantay_piniliay/candidate.html', {'candidate_list':candidate_list,
                                                                     'lungsod_list':lungsod_list,
                                                                     'vice_mayor_list':vice_mayor_list,
                                                                     'mayor_list':mayor_list,
                                                                     'lalawigan_list':lalawigan_list,
                                                                     'vice_gov_list':vice_gov_list,
                                                                     'governor_list':governor_list,
                                                                     'congressman_list':congressman_list,
                                                                     'cluster_id':cluster_id,
                                                                     'user':request.user})
def candidate_detail(request,cluster_id,  candidate_id):
    candidate = get_object_or_404(Candidate, pk = candidate_id)
    vote = Tabulation.objects.filter(candidate = candidate_id)
    return render(request, 'index/bantay_piniliay/candidate_detail.html', {'candidate':candidate,
                                                                           'vote': vote,
                                                                           'cluster_id':cluster_id})

def forbidden(request):
    return render(request, 'index/forbidden.html')

def news(request):
    news_category = News_category.objects.all()
    news = News.objects.all().order_by('-date')
    return render(request, 'index/news/news.html', {'news_category':news_category,
                                                    'news': news})
def news_list(request, user_id):
    news_list = News.objects.filter(author = user_id).order_by('-date')
    return render(request, 'index/news/news_list.html', {'news_list': news_list,
                                                         'user_id': int(user_id)})

def news_detail(request, category, headline, news_id):
    try:
        news = News.objects.filter(id = news_id)
        return render(request, 'index/news/news_detail.html', {'news':news})
    except Exception as e:
        return HttpResponse("ERROR 500 "+str(e))

def advertise(request):
    try:
        form = ClientForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            try:
                client = form.save(commit=False)
                client.is_newsletter = request.POST.get('is_newsletter', '') == 'on'
                client.save()
                messages.success(request, f"Your request has been sent!")
                return redirect(reverse('index:advertise'))
            except Exception as e:
                messages.error(request, f"Your request failed to send! Error: " + str(e))
        return render(request, 'index/advertise.html', {"form": form,
                                                        'title': 'Advertise! ',
                                                        'subtext': 'Let your brand be heard.'})
    except Exception as e:
        return HttpResponse("ERROR 500 "+str(e))




def info(request, page):

    try:
        if page == 'about-jack':
            title = 'About JACK'
            subtext = 'Everything about us'
            form = None
            pagee = Page.objects.get(title=title)
            content = Info.objects.filter(page=pagee.pk)
            return render(request, 'index/info.html', {'content': content,
                                                       'form': form,
                                                       'title': title,
                                                       'subtext': subtext})
        elif page == 'contact-jack':
            title = 'Contact JACK'
            subtext = 'Fancy a natter?'
            form = SendMail(request.POST or None, request.FILES or None, initial={'phone_number': '+63'})
            if form.is_valid():
                try:
                    mail = form.save(commit=False)
                    mail.save()
                    messages.success(request, f"Your mail has been sent!")
                    return redirect(reverse('index:info', kwargs={'page': 'contact-jack'}))
                except Exception as e:
                    messages.error(request, f"Your mail failed to send! Error: " + str(e))

            pagee = Page.objects.get(title=title)
            content = Info.objects.filter(page=pagee.pk)
            return render(request, 'index/info.html', {'content': content,
                                                       'form': form,
                                                       'title': title,
                                                       'subtext': subtext})
        elif page == 'xtrm':
            form = None
            title = 'XTRM'
            subtext = 'Daily Xanthone Supplement'
            pagee = Page.objects.get(title=title)
            content = Info.objects.filter(page=pagee.pk)
            return render(request, 'index/info.html', {'content': content,
                                                       'form': form,
                                                       'title': title,
                                                       'subtext': subtext})
        elif page == 'first-cee':
            form = None
            title = 'First-CEE'
            subtext = 'The Ultimate Vit.C'
            pagee = Page.objects.get(title=title)
            content = Info.objects.filter(page=pagee.pk)
            return render(request, 'index/info.html', {'content': content,
                                                       'form': form,
                                                       'title': title,
                                                       'subtext': subtext})
        elif page == 'terms-and-conditions':
            form = None
            title = 'Terms and Conditions'
            subtext = ' '
            pagee = Page.objects.get(title=title)
            content = Info.objects.filter(page=pagee.pk)
            return render(request, 'index/info.html', {'content': content,
                                                       'form': form,
                                                       'title': title,
                                                       'subtext': subtext})
        elif page == 'privacy-policy':
            form = None
            title = 'Privacy Policy'
            subtext = ' '
            pagee = Page.objects.get(title=title)
            content = Info.objects.filter(page=pagee.pk)
            return render(request, 'index/info.html', {'content': content,
                                                       'form': form,
                                                       'title': title,
                                                       'subtext': subtext})

    except Exception as e:

        return HttpResponse("ERROR 500 "+str(e))



def how_to_listen(request):
    try:
        return render(request, 'index/listen_to_jack.html')
    except Exception as e:
        return HttpResponse("ERROR 500 "+str(e))

def radio(request):
    try:
        return render(request, 'index/radio_how.html')
    except Exception as e:
        return HttpResponse("ERROR 500 " + str(e))