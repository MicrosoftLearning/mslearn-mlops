---
title: Online Hosted Instructions
permalink: index.html
layout: home
---

# MLOps Challenges

This repository contains hands-on challenges for end-to-end machine learning operations (MLOps) with Azure Machine Learning.

To complete these exercises, you’ll need a Microsoft Azure subscription. If your instructor has not provided you with one, you can sign up for a free trial at [https://azure.microsoft.com](https://azure.microsoft.com/).

## Labs

{% assign labs = site.pages | where_exp:"page", "page.url contains '/docs'" %}
{% for activity in labs  %}
<hr>
### [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})

{{ activity.lab.description }}

{% endfor %}