
class BaseConfig(object):

    # Can be set to 'MasterUser' or 'ServicePrincipal'
    AUTHENTICATION_MODE = 'ServicePrincipal'

    # Workspace Id in which the report is present
    WORKSPACE_ID = '4026fbe8-7431-4417-9550-4686cbe034ea'
    
    # Report Id for which Embed token needs to be generated
    REPORT_ID = 'd377f144-2a1d-41b4-b566-0aebd99a2fbe'
    
    # Id of the Azure tenant in which AAD app and Power BI report is hosted. Required only for ServicePrincipal authentication mode.
    TENANT_ID = 'e5834a25-aff9-453d-882e-78ff2b3fb62c'
    
    # Client Id (Application Id) of the AAD app
    CLIENT_ID = '5287b66c-9c86-481b-b6af-7da56166a164'
    
    # Client Secret (App Secret) of the AAD app. Required only for ServicePrincipal authentication mode.
    CLIENT_SECRET = 'skq8Q~IG0iSrxc0gmYEWwr-Xdb~_9S16SMDffaKn'
    
    # Scope of AAD app. Use the below configuration to use all the permissions provided in the AAD app through Azure portal.
    SCOPE = ['https://analysis.windows.net/powerbi/api/.default']
    
    # URL used for initiating authorization request
    AUTHORITY = 'https://login.microsoftonline.com/organizations'
    
    # Master user email address. Required only for MasterUser authentication mode.
    POWER_BI_USER = ''
    
    # Master user email password. Required only for MasterUser authentication mode.
    POWER_BI_PASS = ''
