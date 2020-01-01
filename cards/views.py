from django.shortcuts import render, redirect
from .models import *
from .forms import *
import random
import re

hashtag = re.compile(r'[^\\](\#[^\s]+)')


cur  = object()
old_pk = 0
no_cards = False



def makedict(**kwargs):
    return kwargs

def help(request):

    context = {}
    if request.POST:
        print(request.POST)
        for i in range(1,len(request.POST)):
            if i == 1: i = 0
            a = Card()
            texts = request.POST[str(i)].split('-')
            print(texts)
            if len(texts) < 1: texts = ['','']
            elif len(texts) == 1: texts.append('')
            else: 
                latter = ''
                for text in texts[1:]:
                    latter+=text
                texts = [texts[0],latter]
            a.title = texts[0]
            
            hashtags = hashtag.findall(texts[1])
            if len(hashtags) == 0:
                hashtags.append('#default')
            texts[1] = hashtag.sub('',texts[1])
            a.tags = ' '.join(hashtags)
            a.txt = texts[1]
            a.save()
            
    
    return render(request,"cards/create.html",context=context)
    

def see_card(request):
    global cur
    if request.POST:
        keys = request.POST.keys()
        if 'defer' in keys:
            if cur.title == "No Cards":
                Card.objects.get(pk=cur.pk).delete()
            loadcurrent()
        if 'done' in keys:
            changecurrent()
        return redirect('cards_see')
    context = makedict(card=cur, tags=[])
    tags = cur.tags.split(' ')
    for tag in tags:
        context['tags'].append(tag)

    return render(request,"cards/card_test.html",context=context)

def changecurrent():
    global cur,  old_pk,no_cards
    Card.objects.get(pk=cur.pk).delete()
    cd = Card.objects.all()
    #print(cd)
    print("c-c-1")
    if len(cd) != 0:
        print("c-c-2")
        new_pk = random.randint(0,len(cd)-1)
        if len(cd) >= 2:
            while new_pk == old_pk:
                new_pk = random.randint(0,len(cd)-1)
        old_pk  =  new_pk
        cur = cd[old_pk]
    else:
        print("c-c-3")
        create_default_card()
    #print(cur)

def loadcurrent():
    global cur, old_pk, no_cards
    cd = Card.objects.all()
    print("l-c-1")
    if len(cd) != 0:
        print("l-c-2")
        new_pk = random.randint(0,len(cd)-1)
        if len(cd) >= 2:
            while new_pk == old_pk:
                new_pk = random.randint(0,len(cd)-1)
        old_pk  =  new_pk
        cur = cd[old_pk]
    else:
        print("l-c-3")
        create_default_card()


def create_default_card():
    global cur, no_cards
    a = Card()
    a.txt = "you have no cards yet!"
    a.title = "No Cards"
    a.tags = '#default'
    a.save()
    no_cards = True
    cur = a

loadcurrent()