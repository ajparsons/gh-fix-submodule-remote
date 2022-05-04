# gh-fix-submodule-remote


In codespaces, submodules don't have the right credentials to push back changes, this fixes that by authenticating, then re-writing the remote urls to use that auth details.

Steels bits from [https://github.com/jongio/gh-setup-git-credential-helper](https://github.com/jongio/gh-setup-git-credential-helper)

# Install

```
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
apt update
apt install gh
gh extension install ajparsons/gh-fix-submodule-remote
```

## Run


`gh gh-fix-submodule-remote --auth`

This will extract the username and token from the gh cli storage, and modify the URLs of the github submodules. 