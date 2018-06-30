# Pinky

Inky is an HTML-based templating language that converts simple HTML into complex, responsive email-ready HTML. Designed for [Foundation for Emails](http://foundation.zurb.com/emails), a responsive email framework from [ZURB](http://zurb.com).

**Inky is built for node, Pinky is just python port of this great library.**

Give Inky simple HTML like this:

```html
<row>
  <columns large="6"></columns>
  <columns large="6"></columns>
</row>
```

And get complicated, but battle-tested, email-ready HTML like this:

```html
<table class="row">
  <tbody>
    <tr>
      <th class="small-12 large-6 columns first">
        <table>
          <tr>
            <th class="expander"></th>
          </tr>
        </table>
      </th>
      <th class="small-12 large-6 columns first">
        <table>
          <tr>
            <th class="expander"></th>
          </tr>
        </table>
      </th>
    </tr>
  </tbody>
</table>
```

## Installation
Git clone this repo and then install with pip locally
```bash
git clone https://github.com/onel/pinky.git
pip install ./pinky
```
**COMING SOON: pip package**

## Usage

Pinky can be used programatically or from the command line

### Programmatic Use

```py
from pinky import Pinky

html_string = '<html>...</html>'
result = Pinky.parse(html_string)
```

### Command Line
```bash
pinky "[html string]"
```
The command returns the resulted HTML string.

## Under the hood
Pinky uses [BeautifulSoop4](https://pypi.org/project/beautifulsoup4/) (with the lxml option) to parse the received html string and then replace all the custom Inky tags with the proper html elements (table, tr, td, etc.).

In the second step is uses [Premailer](https://github.com/peterbe/premailer) to inline the CSS and minify the HTML.