StackOverflow Exception Troubleshooting
=======================================

A simple Django Middleware for Exception Troubleshooting. It is meant to be used in debug mode only.

In a nutshell, the Middleware intercepts a exception thrown by a view and look up for the three most relevant questions
on StackOverflow and print the result to the console.

Quick Start
-----------

**1. Install using pip:**

.. code-block:: console

    pip install django-soet

**2. Include "soet" to your INSTALLED_APPS:**

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'soet',
    ]

**3. Include "StackOverflowMiddleware" to your MIDDLEWARE_CLASSES:**

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'soet.middleware.StackOverflowMiddleware',
    )

**4. Make sure you are running your project with DEBUG=True.**

**5. Start your development server and wait for the view exceptions (or not).**

Preview
-------

This is how it looks like in your Terminal:

.. image:: https://github.com/vitorfs/soet/raw/master/soet.png
