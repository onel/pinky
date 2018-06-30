
from premailer import Premailer
from bs4 import BeautifulSoup

from logging import info, warn, exception
# log levels
from logging import INFO, CRITICAL


class Pinky(object):

    @staticmethod
    def replace_container(soup):
        container = soup.find('container')

        if not container:
            warn('Every inky template should have a <container> element')
            return

        try:
            table = soup.new_tag("table")
            table['align'] = 'center'
            table['class'] = 'container'

            container.wrap(table)
            container.wrap(soup.new_tag("tbody"))
            container.wrap(soup.new_tag("tr"))
            container.wrap(soup.new_tag("td"))

            container.unwrap()
        except Exception as e:
            warn('Could not convert container to table')

        return container

    @staticmethod
    def replace_spacers(soup):

        spacers = soup.find_all('spacer')
        for spacer in spacers:
            try:
                classes = spacer.get('class', [])
                classes.append('spacer')
                size = spacer.get('size', 16)

                table = soup.new_tag("table")
                table['class'] = classes
                tbody = soup.new_tag("tbody")
                tr = soup.new_tag("tr")

                td = soup.new_tag("td")
                td['height'] = '{0}px'.format(size)
                td['style'] = "font-size:{0}px;line-height:{0}px;".format(size)

                tr.append(td)
                table.append(tr)

                spacer.replace_with(table)
            except Exception as e:
                warn('Could not replace spacer inside email template')
                continue

    @staticmethod
    def replace_columns(row, soup):

        columns = row.find_all('columns')
        no_of_columns = len(columns)
        for i, column in enumerate(columns):
            expander = ''

            try:
                no_expander = hasattr(column, 'no-expander')
                classes = column.get('class', [])

                small = column.get('small', 12)
                large = column.get('large', 12)
                classes.append('columns')

                classes.append('small-{0}'.format(small))
                classes.append('large-{0}'.format(large))

                if i == 0:
                    classes.append('first')
                if i == no_of_columns - 1:
                    classes.append('last')

                if large == no_of_columns and not column.find_all('row') and not column.find_all(class_ = 'row') and not no_expander:
                    expander = soup.new_tag('th')
                    expander['class'] = 'expander'

                th = soup.new_tag("th")
                th['class'] = classes

                column.wrap(th)

                table_wrap = soup.new_tag("table")
                # TODO: fix this
                # hack: premailer doesn't apply a width: 100%; rule to this table. idk why
                # the rule is in email.css, line 140
                table_wrap['style'] = 'width: 100%;'
                column.wrap(table_wrap)

                column.wrap(soup.new_tag("tbody"))

                tr = soup.new_tag("tr")
                column.wrap(tr)
                if expander:
                    tr.append(expander)

                column.wrap(soup.new_tag("th"))
                column.unwrap()
            except Exception as e:
                exception('Could not replace column')

    @staticmethod
    def replace_rows(soup):

        rows = soup.find_all('row')
        for row in rows:
            try:
                classes = row.get('class', [])
                classes.append('row')

                row_table = soup.new_tag("table")
                row_table['class'] = classes

                Pinky.replace_columns(row, soup)

                row.wrap(row_table)
                row.wrap(soup.new_tag("tbody"))
                row.wrap(soup.new_tag("tr"))

                row.unwrap()
            except Exception as e:
                exception('Could not replace row')

    @staticmethod
    def replace_buttons(soup):
        
        buttons = soup.find_all('button')
        for button in buttons:
            expander = False

            try:
                classes = button.get('class', [])
                classes.append('button')

                if button.get('href'):
                    button.name = 'a'

                if 'expander' in classes or 'expanded' in classes:
                    button.wrap(soup.new_tag('center'))
                    expander = True

                button['class'] = ''

                table = soup.new_tag("table")
                table['class'] = classes

                button.wrap(table)
                button.wrap(soup.new_tag('tbody'))
                button.wrap(soup.new_tag('tr'))
                td = soup.new_tag('td')
                button.wrap(td)

                if expander:
                    # https://stackoverflow.com/a/23043358
                    td.append(soup.new_tag('td', **{'class':"expander"}))

                button.wrap(soup.new_tag('table'))
                button.wrap(soup.new_tag('tbody'))
                button.wrap(soup.new_tag('tr'))
                button.wrap(soup.new_tag('td'))
                
            except Exception as e:
                exception('Could not replace button')

    @staticmethod
    def replace_center(soup):

        centers = soup.find_all('center')
        for center in centers:

            childrens = center.find_all(recursive=False)
            for chd in childrens:

                try:
                    chd['align'] = 'center'

                    classes = chd.get('class', [])

                    # when we have the container inside the center element
                    # classes is a string, very strange
                    if isinstance(classes, str):
                        # force it as an array
                        classes = chd.get_attribute_list('class')

                    classes.append('float-center')
                    chd['class'] = classes
                except Exception as e:
                    exception('Could not replace center element')

    @staticmethod
    def replace_wrappers(soup):

        wrappers = soup.find_all('wrapper')
        for wrapper in wrappers:

            try:
                classes = wrapper.get('class', [])
                classes.append('wrapper')

                table = soup.new_tag("table")
                table['class'] = classes
                table['align'] = 'center'

                wrapper.wrap(table)
                wrapper.wrap(soup.new_tag('tbody'))
                wrapper.wrap(soup.new_tag('tr'))
                wrapper.wrap(soup.new_tag('td', **{'class':"wrapper-inner"}))

                wrapper.unwrap()
            except Exception as e:
                exception('Could not replace wrapper')

    @staticmethod
    def parse(content):

        soup = BeautifulSoup(content, 'lxml')

        Pinky.replace_container(soup)

        Pinky.replace_spacers(soup)

        Pinky.replace_rows(soup)

        Pinky.replace_buttons(soup)

        Pinky.replace_center(soup)

        Pinky.replace_wrappers(soup)

        # get the html string from BeautifulSoup
        try:
            final_html = soup.prettify()
        except Exception as e:
            exception(e)
            warn('Could not get soup html string.')
            return content

        # inline the css
        try:

            # in prod we don't need all the logs
            # logging_level = INFO if DEV else CRITICAL
            logging_level = CRITICAL

            # if we use the option keep_style_tags=True
            # lxml 2.3.5 throws an error: 
            # All strings must be XML compatible: Unicode or ASCII, no NULL bytes or control characters
            # TODO: find a fix

            inlined_css = Premailer(final_html, include_star_selectors=True, cssutils_logging_level=logging_level).transform()

            return inlined_css.encode('utf-8')
        except Exception as e:
            exception(e)
            warn('Failed to inline css')
            return final_html
