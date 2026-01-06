class GhostpmError(Exception):
    """Base error for ghostpm"""

class DownloadError(GhostpmError): pass

class InstallError(GhostpmError): pass

class RemoveError(GhostpmError): pass

class ConfigError(GhostpmError): pass

class PermissionDeniedError(GhostpmError): pass

class GithubError(GhostpmError): pass

class AssetsError(GhostpmError): pass

class InvalidCommandError(GhostpmError): pass
