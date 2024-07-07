"""
Definition of views.
"""

from django.shortcuts import render


def pastats(request):
    return render(request, "pastats/research.html")
