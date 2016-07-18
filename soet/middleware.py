# coding: utf-8

import re
import requests
import json
from HTMLParser import HTMLParser

from django.conf import settings


GRID_LINE = '+' + (78 * '-') + '+'


def break_string(string, every=76):
    lines = []
    for i in xrange(0, len(string), every):
        lines.append(string[i:i+every])
    return lines


def print_string(string):
    lines = break_string(string)
    for line in lines:
        print u'| {}'.format(line) + ((76 - len(line)) * ' ') + ' |'


class StackOverflowMiddleware(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'github.com/vitorfs/seot'
        }
        self.url = 'https://api.stackexchange.com/2.2/search'
        self.default_params = {
            'order': 'desc',
            'sort': 'votes',
            'site': 'stackoverflow',
            'pagesize': 3,
            'filter': '!*1SgQGDOL9bUjMgbu_yYx4IC-MQSUH*aDX9WRdjjI'
        }

    def get_questions(self, intitle, tagged):
        query_params = { 'tagged': tagged, 'intitle': intitle }
        params = dict(self.default_params.items() + query_params.items())
        r = requests.get(self.url, params=params, headers=self.headers)
        questions = r.json()
        return questions

    def process_exception(self, request, exception):
        if settings.DEBUG:
            intitle = u'{}: {}'.format(exception.__class__.__name__, exception.message)
            questions = self.get_questions(intitle, 'python;django')

            if len(questions['items']) == 0:
                message = exception.message.split("'")[0]
                intitle = u'{}: {}'.format(exception.__class__.__name__, message)
                questions = self.get_questions(intitle, 'python;django')

                if len(questions['items']) == 0:
                    intitle = exception.__class__.__name__
                    questions = self.get_questions(intitle, 'django')

            count = 0

            for question in reversed(questions['items']):
                if 'answers' in question and len(question['answers']) > 0:
                    print '\n' + GRID_LINE
                    body = question['body_markdown']
                    lines = body.splitlines()
                    print_string('Question: ')
                    print_string(' ')
                    for line in lines:
                        text = HTMLParser().unescape(re.sub('\s+', ' ', line))
                        print_string(text)

                    print GRID_LINE

                    best_answer = None
                    for answer in question['answers']:
                        if best_answer == None or answer['score'] > best_answer['score']:
                            best_answer = answer
                    if best_answer != None:
                        answer_body = best_answer['body_markdown']
                        answer_lines = answer_body.splitlines()
                        print_string('Best Answer: ')
                        print_string(' ')
                        for line in answer_lines:
                            text = HTMLParser().unescape(re.sub('\s+', ' ', line))
                            print_string(text)

                    print GRID_LINE
                    print_string('Score: {} / Views: {} / Answers: {}'.format(
                        question['score'],
                        question['view_count'],
                        question['answer_count']
                    ))
                    print_string('Tags: {}'.format(', '.join(question['tags'])))
                    print GRID_LINE
                    print_string(u'Title: {}'.format(HTMLParser().unescape(question['title'])))
                    print GRID_LINE
                    link = 'Link: http://stackoverflow.com/questions/{}'.format(question['question_id'])
                    print_string(link)
                    print GRID_LINE

                    count += 1

            if count == 0:
                print '\n' + GRID_LINE
                print_string('No result found.')
                print GRID_LINE

            print '\n' + GRID_LINE
            print_string(u'Exception: {}'.format(exception.__class__.__name__))
            print_string(u'Message: {}'.format(exception.message))
            print GRID_LINE

            print ''

        return None
