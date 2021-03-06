# Selinon

An advanced task flow management on top of [Celery](https://www.celeryproject.org/).

![codecov](https://codecov.io/gh/selinon/selinon/branch/master/graph/badge.svg)
![PyPI Current Version](https://img.shields.io/pypi/v/selinon.svg)
![PyPI Implementation](https://img.shields.io/pypi/implementation/selinon.svg)
![PyPI Wheel](https://img.shields.io/pypi/wheel/selinon.svg)
![Travis CI](https://travis-ci.org/selinon/selinon.svg?branch=master)
![GitHub stars](https://img.shields.io/github/stars/selinon/selinon.svg)
![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)
![Twitter](https://img.shields.io/twitter/url/http/github.com/selinon/selinon.svg?style=social)

## TLDR;

An advanced flow management above Celery (an asynchronous distributed task queue) written in Python3, that allows you to:

  - Dynamically schedule tasks based on results of previous tasks
  - Group tasks to flows
  - Schedule flows from other flows (even recursively)
  - Store results of tasks in your storages and databases transparently, validate results against defined JSON schemas
  - Track flow progress via the build-in tracing mechanism
  - Complex per-task or per-flow failure handling with fallback tasks or fallback flows
  - Make your flow orchestrated by orchestration tools such as [Kubernetes](https://kubernetes.io)
  - And (of course) much more...

## About

This tool is an implementation above Celery that enables you to define flows and dependencies in flows, schedule tasks based on results of Celery workers, their success or any external events. If you are not familiar with Celery, check out its homepage [www.celeryproject.org](http://www.celeryproject.org) or [this nice tutorial](https://tests4geeks.com/distribute-tasks-python-celery-rabbitmq/).

Selinon was originally designed to take care of advanced flows in one of Red Hat products, where it already served thousands of flows and tasks. Its main aim is to simplify specifying group of tasks, grouping tasks into flows, handle data and execution dependencies between tasks and flows, easily reuse tasks and flows, model advanced execution units in YAML configuration files and make the whole system easy to model, easy to maintain and easy to debug.

By placing declarative configuration of the whole system into YAML files you can keep tasks as simple as needed. Storing results of tasks in databases, modeling dependencies or executing fallback tasks/flows on failures are separated from task logic. This gives you a power to dynamically change task and flow dependencies on demand, optimize data retrieval and data storage from databases per task bases or even track progress based on events traced in the system.

Selinon was designed to serve millions of tasks in clusters or data centers orchestrated by [Kubernetes](https://kubernetes.io), [OpenShift](https://openshift.com) or any other orchestration tool, but can simplify even small systems. Moreover, Selinon can make them easily scalable in the future and make developer's life much easier.

## A Quick First Overview

Selinon is serving recipes in a distributed environment, so let's make a dinner!

If we want to make a dinner, we need to buy ingredients. These ingredients are bought in `buyIngredientsFlow`. This flow consists of multiple tasks, but let's focus on our main flow. Once all ingredients are bought, we can start preparing our dinner in `prepareFlow`. Again, this flow consists of some additional steps that need to be done in order to accomplish our future needs. As you can see, if anything goes wrong in mentioned flows (see red arrows), we make a fallback to pizza with beer which we order. To make beer cool, we place it to our `Fridge` storage. If we successfully finished `prepareFlow` after successful shopping, we can proceed to `serveDinnerFlow`.

Just to point out - grey nodes represent flows (which can be made of other flows or tasks) and white (rounded) nodes are tasks. Conditions are represented in hexagons (see bellow). Black arrows represent time or data dependencies between our nodes, grey arrows pinpoint where results of tasks are stored.

![Main dinner flow](/example/graph/dinnerFlow.png?raw=true "Main dinner flow")

For our dinner we need eggs, flour and some additional ingredients. Moreover, we conditionally buy a flower based on our condition. Our task `BuyFlowerTask` will not be scheduled (or executed) if our condition is `False`. Conditions are made of predicates and these predicates can be grouped as desired with logical operators. You can define your own predicates if you want (default are available in `selinonlib.predicates`). Everything that is bought is stored in `Basket` storage transparently.

Let's visualise our `buyIngredientsFlow`:
![Buy ingredients flow](/example/graph/buyIngredientsFlow.png?raw=true "How to buy ingredients")

As stated in our main flow after buying ingredients, we proceed to dinner preparation but first we need to check our recipe that is hosted at `http://recipes.lan/how-to-bake-pie.html`. Any ingredients we bought are transparently retrieved from defined storage as defined in our YAML configuration file. We warm up our oven to expected temperature and once the temperature is reached and we have finished with dough, we can proceed to baking.

Based on the description above, our `prepareFlow` will look like the following graph:
![Preparation](/example/graph/prepareFlow.png?raw=true "How to prepare dinner")

Once everything is done we serve plates. As we want to serve plates for all guests we need to make sure we schedule N tasks of type `ServePlateTask`. Each time we run our whole dinner flow, number of guests may vary so make sure no guest stays hungry. Our `serveDinnerFlow` would look like the following graph:
![Serving plates](/example/graph/serveDinnerFlow.png?raw=true "How to serve plates")

This example demonstrates very simple flows. The whole configuration can be found [here](/example/dinner.yaml). Just check it out how you can easily define your flows! You can find a script that visualises graphs based on the YAML configuration in [this repo](/example/) as well.

## More info

The example was intentionally simplified. You can also parametrize your flows, schedule N tasks (where N is a run-time evaluated variable), do result caching, placing tasks on separate queues in order to be capable of doing fluent system updates, throttle execution of certain tasks in time, propagate results of tasks to sub-flows etc. Just check [documentation](https://selinon.github.io/selinon) for more info.

## Live Demo

A live demo with few examples can be found [here](https://github.com/selinon/demo). Feel free to check it out.

## Installation

```
$ pip3 install selinon
```

