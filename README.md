# StackOverflow Exception Troubleshooting

A simple Django Middleware for Exception Troubleshooting. It is meant to be used in debug mode only.

In a nutshell, the Middleware intercepts a exception thrown by a view and look up for the three most relevant questions
on StackOverflow and print the result to the console.