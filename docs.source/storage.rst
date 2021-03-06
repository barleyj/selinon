Storage Implementation
======================

Currently, there are available three database adapters, see 'selinon.storage' module. In order to use these storages, you have to manually install database adapters as they are not explicitly included by Pypi.

  * `SqlStorage` - SQLAlchemy adapter for SQL databases
    Example:

    .. code-block:: yaml

      storages:
        - name: 'MySqlStorage'
          classname: 'SqlStorage'
          import: 'selinon.storage'
          configuration:
            connection_string: 'postgres://postgres:postgres@postgres:5432/postgres'
            encoding: 'utf-8'
            echo: false

  * `RedisStorage` - Redis database adapter
    Example:

    .. code-block:: yaml

      storages:
        - name: 'MyRedisStorage'
          classname: 'RedisStorage'
          import: 'selinon.storage'
          configuration:
            host: 'redishost'
            port: 6379
            db: 0
            password: 'secretpassword'
            charset: 'utf-8'
            host: 'mongohost'
            port: 27017

  * `MongoStorage` - MongoDB database adapter
    Example:

    .. code-block:: yaml

      storages:
        - name: 'MyMongoStorage'
          classname: 'MongoStorage'
          import: 'selinon.storage'
          configuration:
            db_name: 'database_name'
            collection_name: 'collection_name'
            host: 'mongohost'
            port: 27017

You can define your own storage by inheriting from `DataStorage` defined in `selinon.storage`:

::

  from selinon.storage import DataStorage

  class MyStorage(DataStorage):
      def __init__(self, host, port):
          # arguments from YAML file are pasased to constructor as key-value arguments
          pass

      def is_connected():
          # predicate that is used to connect to database
          return False

      def connect():
          # define how to connect based on your configuration
          pass

      def disconnect():
          # define how to disconnect from database
          pass

      def retrieve(self, flow_name, task_name, task_id):
          # define how to retrieve result based on flow, task name and task id
          pass

      def store(self, flow_name, task_name, task_id, result):
          # define how to store result from task with id task_id based on flow and task name
        pass

You can also reuse current implementation of a storage in order to  define your custom `retrieve()` and `store()` methods based on your requirements.

Database Connection Pool
########################

Each Celery worker is trying to be efficient when it comes to number of connections to a database. There is held only one instance of `DataStorage` class per whole worker. This means that your database has to be concurrency-safe if you plan to run your Celery worker with concurrency level bigger than one.

You can simply share connection across multiple `DataStorage` classes in inheritance hierarchy and reuse already defined connections.

If you would like to limit number of connections to database, you have to do it on your own by sharing connection information in parent of type `DataStorage` and implement connection limitation logic in your database adapter. This is not possible on Selinon level, since database adapters are black box for Selinon and they can share connection across multiple instances.
