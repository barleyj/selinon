Selinon - A Dynamic Task Flow Management on top of Celery
=========================================================

What is Selinon and why should I use it?
########################################

Selinon is a tool that gives you a power to define flows, subflows of tasks that should be executed in `Celery <http://www.celeryproject.org>`_ - a distributed task queue. If you want to define very simple flows, Celery offers you workflow primitives that can be used. Unfortunately these workflow primitives are very limited when it comes to extending your workflow, working with multiple dependencies or scheduling tasks based on particular conditions.

If you are looking for a workflow solution, take a look at existing solutions, such as `Azkaban <https://azkaban.github.io/>`_, `Apache Airflow <https://github.com/apache/incubator-airflow>`_, `Apache Nifi <https://nifi.apache.org>`_, `Spotify Luigi <https://luigi.readthedocs.io>`_ and others. The main advantage of using Selinon over these is the fact, that you can use it in fully distributed systems and for example let `Kubernetes <https://kubernetes.io>`_ do the workload (and much more, such as recursive flows, subflows support, ...).

Is there available a demo?
##########################

You can take a look at `selinon-demo <https://github.com/fridex/selinon-demo>`_ so you can see how Selinon works without deep diving into configuration. Just run `docker-compose up`.

What do I need?
###############

In order to use Selinon, you need:

  * a basic knowledge of Python3 (yes, there is no support for Python2!)
  * YAML language
  * a basic knowledge of Celery 4 (older versions are not supported) and its `configuration <http://docs.celeryproject.org/en/latest/configuration.html>`_
  * vegetable appetite :)

How does it work? - a high level overview
#########################################

The key idea lies in Dispatcher - there is created Dispatcher Celery task for each flow. Dispatcher takes care of starting new tasks and subflows, checking their results and scheduling new tasks based on your configuration.

The only thing that needs to be provided by you is a YAML configuration file that specifies dependencies of your tasks and where results of tasks should be stored. This configuration file is parsed by `Selinonlib <https://fridex.github.io/selinonlib>`_ and automatically transformed to a Python3 code which is then used by Selinon.

Documentation
#############

.. toctree::
   :maxdepth: 1

   start
   faq
   yaml.conf
   tasks
   storage
   trace
   migration
   patterns
   development
   api/selinon

See also
********

   * `Selinonlib <https://fridex.github.io/selinonlib>`_
   * `Celery configuration <http://docs.celeryproject.org/en/latest/configuration.html>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

