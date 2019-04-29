Some friends dabing in sabermetrics and things.

Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidance on how to contribute.

# Installation

Make yourself a shiny new conda (or virtualenv, I guess) environment like so:

``` shell
conda create --name fantasy-baseball python=3.X
```

then, from the project root, pip install this package ~in editable mode`

``` shell
pip install -e ./
```

``` shell
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
```


Python copies packages to a subfolder of it's installation directory when you install them.
If you want to actively hack away at a project and also have it installed, this is a problem.
We solve this with editable mode, which drops a link in the installation directory back to
package directory where it was when you installed, instead of moving it. Try running `pip list`
now, you'll see the difference.

## Yahoo Auth

Register an app with Yahoo and get your ID and secret and put it in a json file like so:

The api module will look by default for your api credentials at `~/.yahoo_auth.json`.
If you don't want it there, you can pass in an alternative.

#  Usage

We won't make the scripts globally available for now. Head over to scripts/ to use them.
It looks like they need to be adapted to pull data automatically using yahoo_api, now,
but I haven't looked too closely.
