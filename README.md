# GitHub API Mining Utility

This is a simplified repository miner based on [caiusb/miner-utils](https://github.com/caiusb/miner-utils), and targeting the GitHub REST API (v3).

## Installation

### Requirements
The following must be installed and available for the mining utility:
  * [Python 3](https://www.python.org/downloads/)
  * [`pip`](https://pypi.org/project/pip/)

To verify that these packages are installed and updated, use the following commands in a terminal/console:
```bash
python --version
# example:
# > python3 --version
# Python 3.7.4

pip --version
# example:
# > pip --version
# pip 20.2.3 from /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pip (python 3.7)
```

### Installing the mining utility
To install the mining utility into a Python global environment, run the following command in a terminal/console:
```bash
pip install "git+https://github.com/EPICLab/miner-utils"
```

To install the mining utility into an enhanced shell like IPython or the Jupyter notebook, run the following commands in a code cell:
```python
!pip install 'git+https://github.com/EPICLab/miner-utils'
```

## Usage

The GitHub REST API (v3) has rate limits for the number of resource objects that can be requested in a given timeframe.

For API requests using Basic Authentication or OAuth, you can make up to 5000 requests per hour. Authenticated requests are associated with the authenticated user, regardless of whether Basic Authentication or an OAuth token was used. This means that all OAuth applications authorized by a user share the same quota of 5000 requests per hour when they authenticate with different tokens owned by the same user.

For unauthenticated requests, the rate limit allows for up to 60 requests per hour. Unauthenticated requests are associated with the originating IP address, and not the user making the requests.

For more information on GitHub's rate limiting policy, see the [rate limiting documentation](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting).

### Obtaining a GitHub authentication token
The GitHub REST API (v3) originally supported Basic Authentication using either a username/password or username/token. However, authentication using username/password is currently being deprecated and will be completely removed as of November 13, 2020 at 16:00 UTC ([GitHub Developer release note](https://developer.github.com/changes/2020-02-14-deprecating-password-auth/)). 

Follow the GitHub documentation, ["Creating a personal access token"](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token), obtain a personal access token (PAT) that has `(no scope)` set so that read-only access to public information is allowed (i.e. leave the scope fields unchecked).

> **WARNING**: Treat your tokens like passwords and keep them secret. When using the GitHub API Mining Utility, set the token during instantiation, but do not publish the token in any Python programs or IPython/Jupyter notebooks. 

### Instantiating the GitHub API Mining Utility
To create an instance of the GitHub API Mining Utility in either a Python environment or a IPython/Jupyter notebook, run the following commands:
```python
from minerutils import GitHub

gh = GitHub(username, token)

# example:
# gh = GitHub(username='nelsonni', token='b123c123d123e123')
```

### Interacting with the GitHub API Mining Utility
Once the GitHub API Mining Utility has been instantiated, you can interact with the GitHub REST API through GET requests that take the following format:
```python
gh.get(url, params, headers)

# example (these are equivalent):
# gh.get("/repos/scala/scala/pulls", params={'state': 'all'})
# gh.get("/repos/scala/scala/pulls?state=all")
```

The examples above get all of the pull requests for the specified project (e.g. `scala/scala`). The `params` and `header` arguments are optional, but useful for passing a parameter or query for a particular resource. Both parameters take a map of `(key, value)` pairs for the arguments that you want to pass to the GitHub API endpoint. The alternative is to embed the parameters directly into the `url` (as demonstrated in the second example above).

For all available GitHub REST API (v3) resources, including `url` and `params` values, refer to the [GitHub Docs: REST API](https://docs.github.com/en/rest/reference) site.

### Python 3
This miner is written in Python 3, and should be run in a Python 3.x environment. If you attempt to run in a Python 2 environment, runtime errors will warn that `urllib.parse` module cannot be imported (this is because the `urlparse` module was renamed to `urllib.parse` in Python 3).

## Commands Documentation

| Command | Return Type | Description |
| :------ | ----------- | ----------: |
|`printConfig()` | `None` | Prints the symbols table associated with the GitHub API Mining Utility instance, including authentication values. |
| `get(url, params={}, headers={}, perPage=100)` | `list` | Calls the GitHub REST API (v3) using GET requests that include the authentication parameters (if provided during instantiation), any `params` pairs (if provided), any `headers` pairs (if provided), and paginates the results based on the `perPage` rate. This call respects the GitHub REST API (v3) rate limits (included in 403 status code responses) to determine when the rate limit has been exhausted, and will sleep until the limit has been reset. |
| `getRepoRoot(repo)` | `string` | Accepts a `repo` parameter in the form of a map containing `username` and `repo` key-value pairs, and returns a GitHub URL of the form `https://api.github.com/{username}/{repo}`. |
| `getRemainingRateLimit()` | `int` | Obtains the numerical count of the remaining GitHub REST API (v3) calls allowed before reaching the rate limit. |
| `printRemainingRateLimit()` | `None` | Prints the numerical count of the remaining GitHub API (v3) calls allowed before reaching the rate limit. |
| `repoExists(user, repo)` | `bool` | Calls the GitHub REST API (v3) using a GET request with a URL of the form `https://api.github.com/repos/{user}/{repo}` and indicates whether that response was successful (i.e. whether the repository exists on GitHub). |

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.