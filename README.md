# Iron Legacy Foundation Website

Repository of the Iron Legacy foundation website. 

[Live Website](https://dewewrhino.github.io/iron-legacy/) |
[Zerostatic Themes (Where the theme came from)](https://www.zerostatic.io)

![Jekyll Serif Theme screenshot](https://www.zerostatic.io/theme/jekyll-serif/jekyll-serif-screenshot.png)

## Installation

### Installing Ruby & Jekyll

If this is your first time using Jekyll, please follow the [Jekyll docs](https://jekyllrb.com/docs/installation/) and make sure your local environment (including Ruby) is setup correctly.

### Installing Theme

Download or clone the theme.

To run the theme locally, navigate to the theme directory and run:

```
bundle install
```

To start the Jekyll local development server.

```
bundle exec jekyll serve
```

To build the theme.

```
bundle exec jekyll build
```

## Deployment

### Github Pages

This theme has been tested to work with Github Pages (and Github Project Pages). When using Github Pages you will need to update the `baseurl` in the `_config.yml` otherwise all the css, images and paths will be broken.

For example the site https://zerostaticthemes.github.io/jekyll-serif-theme would have `baseurl: "/jekyll-serif-theme/"`