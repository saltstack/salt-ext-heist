# Salt Extension for Heist

This is a collection of Salt-maintained extension modules for use with [Heist](https://heist.readthedocs.io/en/latest/)
and [Heist-Salt](https://heist-salt.readthedocs.io/en/latest/).

## Security

If you think you've found a security vulnerability, see [Salt's security guide][security].


## Contributing

The salt-ext-heist project team welcomes contributions from the community. If you wish to
contribute code and you have not signed our contributor license agreement (CLA), our bot
will update the issue when you open a Pull Request. For any questions about the CLA process,
please refer to our [FAQ](https://cla.vmware.com/faq).

The [Salt Contributing guide][salt-contributing] has a lot of relevant information, but if
you'd like to jump right in here's how to get started:

    # Clone the repo
    git clone --origin salt https://github.com/saltstack/salt-ext-heist.git

    # Change to the repo dir
    cd salt-ext-heist

    # Create a new venv
    python3 -m venv env --prompt heist-ext
    source env/bin/activate

    # On mac, you may need to upgrade pip
    python -m pip install --upgrade pip

    # Install extension + test/doc dependencies into your environment
    python -m pip install -e . -r requirements/tests.in -r requirements/base.txt -r requirements/docs.in

    # Run tests!
    python -m nox -e tests-3

    # skip requirements install for next time
    export SKIP_REQUIREMENTS_INSTALL=1

    # Build the docs, serve, and view in your web browser:
    python -m nox -e docs && (cd docs/_build/html; python -m webbrowser localhost:8000; python -m http.server; cd -)


For code contributions, as part of VMware we require [a signed CLA][cla-faq].
If you've already signed the VMware CLA, you're probably good to go.

Of course, writing code isn't the only way to contribute! We value
contributions in any of these areas:

- Documentation - especially examples of how to use this module to solve
  specific problems.
- Triaging [issues][issues] and participating in [discussions][discussions]
- Reviewing [Pull Requests][PRs] (we really like [Conventional
  Comments][comments]!)

You could also contribute in other ways:

- Writing blog posts
- Posting on social media about how you used Salt+Heist to solve your
  problems, including videos
- Giving talks at conferences
- Publishing videos
- Asking/answering questions in IRC, Slack, or email groups

Any of these things are super valuable to our community, and we sincerely
appreciate every contribution!


For more information, build the docs and head over to http://localhost:8000/ —
that's where you'll find the rest of the documentation.


[security]: https://github.com/saltstack/salt/blob/master/SECURITY.md
[salt-contributing]: https://docs.saltproject.io/en/master/topics/development/contributing.html
[issues]: https://github.com/saltstack/salt-ext-heist/issues
[PRs]: https://github.com/saltstack/salt-ext-heist/pulls
[discussions]: https://github.com/saltstack/salt-ext-heist/discussions
[comments]: https://conventionalcomments.org/
[cla-faq]: https://cla.vmware.com/faq
