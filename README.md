Some friends dabbling in sabermetrics and things.

# Installation

Make yourself a shiny new conda (or virtualenv) environment like so:

``` shell
conda create --name fantasy-baseball python=3.X
```

then, from the project root, pip install this package ~in editable mode`

``` shell
pip install -e ./
```

## Yahoo Auth

Register an app with Yahoo and get your ID and secret and put it in a json file like so:

The api module will look by default for your api credentials at `~/.yahoo_auth.json`.
If you don't want it there, you can pass in an alternative.

#  Usage

We won't make the scripts globally available for now. Head over to scripts/ to use them.
It looks like they need to be adapted to pull data automatically using yahoo_api, now,
but I haven't looked too closely.
