from django.shortcuts import render,redirect
from django.shortcuts import render
from googleapiclient.discovery import build
import re,random
import requests
from quizengine.models import Questiondb, Quizsession
from django.db.models import Count

# Create your views here.



#      fetch_comments

def fetch_comments_view(request):
    return render(request, 'service/fetchcomments.html') 
    # return render(request, 'service/Comment.html', {'comments': comments, 'video_url': video_url})

API_KEY = "AIzaSyDAQeAT-Xf7uynBhbVDH-ysXEufofCNJss"
# def index(request):
#     return render(request, 'page/index.html')

def get_video_comments(request):
    if request.method == "POST":
        video_url = request.POST.get('video_url')
        video_id = extract_video_id(video_url)
        comments = fetch_comments(video_id)

        return render(request, 'service/Comment.html', {'comments': comments, 'video_url': video_url})

    return render(request, 'home.html')



def extract_video_id(url):
    # Regex to extract video ID from full or short YouTube URLs
    match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None




def fetch_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    comments = []
    next_page_token = None

    while True:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100,
            pageToken=next_page_token
        ).execute()
        
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return comments







def home(request):
   return render(request,'home.html')

def about(request):
    return render(request,'service/about.html')

def contact(request):
    return render(request,'service/contact.html')

def service(request):


    return render(request,'service/service.html')









def news_view(request):
    api_key = "9475baf9ee25403eb14bdbde1ca8712c"
    api_url = f"https://newsapi.org/v2/everything?q=tesla&from=2025-01-23&sortBy=publishedAt&apiKey={api_key}"

    response = requests.get(api_url)
    

    news_data = response.json().get("articles", [])  # Extract articles
    if len(news_data) ==0:
        return redirect("service")

    return render(request, "service/news.html", {"news_data": news_data})











def creatingQuiz(request):
    return render(request,'service/Quz/quiz.html')

def start_quiz(request):
    # return render(request, 'service/Quz/base.html')

    return render(request, 'service/Quz/quiz.html')



def get_question(request, num_questions=5):
    questions = list(Questiondb.objects.all())  # Convert queryset to list
    random.shuffle(questions)  # Shuffle the questions
    selected_questions = questions[:num_questions]  # Pick first 'num_questions' from shuffled list

    # ✅ Store selected questions' IDs in session
    request.session['quiz_questions'] = [q.id for q in selected_questions]
    request.session.modified = True  # Ensure session updates

    
    return render(request, 'service/Quz/question.html', {'questions': selected_questions})




def submit_answer(request):
    if request.method == 'POST':
        quiz_questions = request.session.get('quiz_questions', [])  # Retrieve stored question IDs
        
        for index, question_id in enumerate(quiz_questions, start=1):  # Loop through session questions
            user_answer = request.POST.get(f'answer_{index}')  # Get user's selected answer
            
            if user_answer:
                try:
                    question = Questiondb.objects.get(id=question_id)
                    is_correct = question.right_answer == user_answer  # Check correctness

                    # ✅ Save response in `Quizsession`
                    Quizsession.objects.create(
                        question_id=question.id,
                        user_answer=user_answer,
                        correct=int(is_correct)  # Convert `True/False` to `1/0`
                    )

                except Questiondb.DoesNotExist:
                    return render(request, 'service/Quz/error.html', {'error': 'Question not found'})

        # ✅ After processing, clear session questions
        # request.session.pop('quiz_questions', None)

        return redirect('quizengine:results')  # Redirect to results page

    return redirect('quizengine:get_question')  # Redirect if request is not POST



def results(request):
    # ✅ Get latest 5 attempts first
    latest_attempts = list(Quizsession.objects.order_by('-id')[:5])  # Convert to list to execute separately

    if not latest_attempts:
        return render(request, 'service/Quz/error.html', {'error': 'No quiz session found'})

    # ✅ Extract question IDs
    question_ids = [attempt.question_id for attempt in latest_attempts]

    # ✅ Fetch quiz attempts using separate query
    quiz_attempts = Quizsession.objects.filter(question_id__in=question_ids)

    correct_count = quiz_attempts.filter(correct=True).count()
    incorrect_count = quiz_attempts.count() - correct_count

    # ✅ Calculate Score (Avoid division by zero)
    score = (correct_count / quiz_attempts.count() * 100) if quiz_attempts.count() > 0 else 0  

    return render(request, 'service/Quz/results.html', {
        'quiz_attempts': quiz_attempts,
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'total_questions': quiz_attempts.count(),
        'score': score
    })




def reset_quiz(request):
    Quizsession.objects.all().delete()
    return redirect('quizengine:start_quiz')




def web_saper(request):
    return render(request,'service/web.html')



def recommender(request):
    return render(request,'service/rction.html')