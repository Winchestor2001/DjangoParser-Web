from __future__ import absolute_import, unicode_literals
from celery import shared_task
from config.celery import app
from .models import Work
from .utils import _24freelance_parser, freelancermap_parser, freelancer_parser, flexjobs_parser, fl_parser, weblancer_parser, theprotocol_parser


@app.task
def paser_web_1():
    _24freelance_parser()


@app.task
def paser_web_2():
    freelancermap_parser()


@app.task
def paser_web_3():
    freelancer_parser()


@app.task
def paser_web_4():
    flexjobs_parser()


@app.task
def paser_web_5():
    fl_parser()


@app.task
def paser_web_6():
    weblancer_parser()


@app.task
def paser_web_7():
    theprotocol_parser()



