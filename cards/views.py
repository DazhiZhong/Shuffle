from django.shortcuts import render, redirect
from .models import *
from .forms import *
import random
import re

hashtag = re.compile(r'[^\\](\#[^\s]+)')


cur  = object()
old_pk = 0
no_cards = False

def filtercards(hashtag):
    """
    filters cards using hashtag, card.tag stores tags like "#sth #tag #tag"
    """
    allcards = Card.objects.all()
    ok_cards = []
    for card in allcards:
        if hashtag in card.tags:
            ok_cards.append(card)
    print(ok_cards)
    return ok_cards


def makedict(**kwargs):
    # makedict(name='damn') -> {'name':'damn'}
    return kwargs

def create(request):
    """
    no form, parse the lines of info
    the POST is like {'0':'sth', '1':'sth'}, text linside the line is 
    formatted like 'title - txt #tag #tag'
    parse through the lines, and manually add them to Cards db
    """
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


def tagview(request, tag): 
    """
    name = cards_tag
    same to cards_see, but adds tags, if current is not the same tag it will be deferred
    """
    try:
        cards = filtercards(tag)
    except:
        return redirect('cards_see')
    if len(cards) == 0:
        return redirect('cards_see')
    if tag not in cur.tags:
        loadcurrent(tag=tag)
    if request.POST:
        keys = request.POST.keys()
        if 'defer' in keys:
            if cur.title == "No Cards":
                Card.objects.get(pk=cur.pk).delete()
            loadcurrent(tag=tag)
        if 'done' in keys:
            changecurrent(tag=tag)
        return redirect('cards_tag', tag=tag)
    context = makedict(card=cur, tags=[])
    tags = cur.tags.split(' ')
    for tag in tags:
        context['tags'].append(tag)
    return render(request,"cards/card_test.html",context=context)

  


def see_card(request):
    """
    name = cards_see
    shows card, POST can have 'defer' or 'done' 
    defer shows another card, done deletes it and shows another
    context includes card, and tags, tags are put in a list
    """
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

def changecurrent(tag = None):
    global cur,  old_pk,no_cards
    Card.objects.get(pk=cur.pk).delete()
    cd = Card.objects.all()
    #print(cd)
    print("c-c-1")
    if len(cd) != 0:
        print("c-c-2")
        new_pk = random.randint(0,len(cd)-1)
        if len(cd) >= 2:
            if tag == None:
                while new_pk == old_pk:
                    new_pk = random.randint(0,len(cd)-1)
            else:
                while new_pk == old_pk and not (tag in cur.tags):
                    new_pk = random.randint(0,len(cd)-1)
        old_pk  =  new_pk
        cur = cd[old_pk]
    else:
        print("c-c-3")
        create_default_card()
    #print(cur)

def loadcurrent(tag = None):
    """
    load current same as change current but does not delete current card
    picks cur from Card.objects.all() using random
    """
    global cur, old_pk, no_cards
    cd = Card.objects.all()
    print("l-c-1")
    if len(cd) != 0:
        print("l-c-2")
        new_pk = random.randint(0,len(cd)-1)
        if len(cd) >= 2:
            if tag == None:
                while new_pk == old_pk:
                    new_pk = random.randint(0,len(cd)-1)
            else:
                while new_pk == old_pk and not (tag in cur.tags):
                    new_pk = random.randint(0,len(cd)-1)
        old_pk  =  new_pk
        cur = cd[old_pk]
    else:
        print("l-c-3")
        create_default_card()


def create_default_card():
    """
    self explanatory
    """
    global cur, no_cards
    a = Card()
    a.txt = "you have no cards yet!"
    a.title = "No Cards"
    a.tags = '#default'
    a.save()
    no_cards = True
    cur = a

loadcurrent()