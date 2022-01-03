from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404, JsonResponse
from django.utils import timezone
import random
from teamapp.models import Article,Comment

def index(request):
	if request.method == 'POST':
		article = Article(title=request.POST['title'],body=request.POST['text'],picture=request.POST['picture'])
		article.save()
		return redirect(detail, article.id)

	if ('sort' in request.GET):
		if request.GET['sort']=='like':
			articles=Article.objects.order_by('-like')
		else:
			articles=Article.objects.order_by('-posted_at')
	else:
		articles=Article.objects.order_by('-posted_at')			
		
	context = {
		"articles":articles
    }
	return render(request, 'teamapp/index.html', context)

def hello(request):
	data={
		'name':'Alice',
		'account': True,
		'menu':['自分の投稿: なし', '保存済み: 0', 'フォロー中: 0', 'フォロワー: 0'],
		'news':'ありません'
	}
	return render(request, 'teamapp/hello.html', data)

def redirect_test(request):
	return redirect(hello)	

def detail(request, article_id):
	try:
		article= Article.objects.get(pk=article_id)
	except Article.DoesNotExist:
		raise Http404("Article does not exist")
	if request.method=='POST':
		comment=Comment(article=article, text=request.POST['text'],picture=request.POST['picture'])
		comment.save()

	context={
		'article': article,
		'comments':article.comments.order_by('-posted_at')
	}	
	return render(request, "teamapp/detail.html",context)

def update(request, article_id):
	try:
		article=Article.objects.get(pk=article_id)
	except Article.DoesNotExist:
		raise Http404("Article does not exist")	
	if request.method =='POST':
		article.title=request.POST['title']
		article.body=request.POST['text']
		article.picture=request.POST['picture']
		article.save()
		return redirect(detail, article_id)		
	context={
		"article":article
	}	
	return render(request, "teamapp/edit.html",context)

def delete(request, article_id):
	try:
		article=Article.objects.get(pk=article_id)
	except Article.DoesNotExist:
		raise Http404("Article does not exist")

	article.delete()		

	return redirect(index)

def like(request, article_id):
	try:
		article=Article.objects.get(pk=article_id)
		article.like += 1
		article.save()
	except Article.DoesNotExist:
		raise Http404("Article does not exist")
	return redirect(detail,article_id)	

def api_like(request, article_id):
	try:
		article=Article.objects.get(pk=article_id)
		article.like+=1
		article.save()
	except Article.DoesNotExist:
		raise Http404("Articles does not exist")
	result={
		'id':article_id,
		'like':article.like
	}
	return JsonResponse(result)