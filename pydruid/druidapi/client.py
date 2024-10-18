from .druid import DruidClient

class Client:
    def __init__(self, druid=None) -> DruidClient:
        # If the client is None, it must be backfilled by the caller.
        # This case occurs only when creating the DruidClient to avoid
        # a circular dependency.
        self._druid = druid


    def client(endpoint, auth=None) :
        '''
        Create a Druid client for use in Python scripts that uses a text-based format for
        displaying results. Does not wait for the cluster to be ready: clients should call
        `status().wait_until_ready()` before making other Druid calls if there is a chance
        that the cluster has not yet fully started.
        '''
        return DruidClient(endpoint, auth=auth)

    def jupyter_client(endpoint, auth=None) -> DruidClient:
        '''
        Create a Druid client configured to display results as HTML within a Jupyter notebook.
        Waits for the cluster to become ready to avoid intermittent problems when using Druid.
        '''
        from .html_display import HtmlDisplayClient
        druid = DruidClient(endpoint, HtmlDisplayClient(), auth=auth)
        druid.status.wait_until_ready()
        return druid