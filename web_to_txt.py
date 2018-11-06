from http import client as _http_client
import time
from html.parser import HTMLParser


class HomePage(HTMLParser):
    def __init__(self):
        super(HomePage, self).__init__()
        self.__items = []
        self.__item = [None, None]
        self.__step = 0
        pass

    def handle_starttag(self, tag, attributes):
        if self.__step == 0:
            if tag == 'div':
                for _type, _content in attributes:
                    if _type == 'class' and _content == 'booklist clearfix':
                        self.__step = 1
                        pass
                    pass
                pass
            pass
        if self.__step == 1:
            if tag == 'a':
                for _type, _content in attributes:
                    if _type == 'href':
                        # print(_content)
                        _tmp = _content.split('/')
                        self.__item[1] = _tmp[len(_tmp) - 1]
                        self.__step = 2
                        pass
                    pass
                pass
            pass

    def handle_endtag(self, tag):
        if self.__step == 1:
            if tag == 'div':
                self.__step = 0
                pass
            pass
        elif self.__step == 2:
            if tag == 'a':
                if (self.__item[0] is not None) and (self.__item[1] is not None):
                    self.__items.append(tuple(self.__item))
                    self.__item[0] = None
                    self.__item[1] = None
                    pass
                else:
                    pass
                self.__step = 1
                pass
            pass
        pass

    def handle_data(self, data):
        if self.__step == 2:
            # print('>', data)
            self.__item[0] = data
        pass

    def print_items(self):
        print(len(self.__items))
        for _item in self.__items:
            print(_item)
            pass
        pass

    @property
    def items(self):
        return self.__items
    pass


class SubPage(HTMLParser):
    def __init__(self):
        super(SubPage, self).__init__()
        self.__txt = ''
        self.__step = 0
        pass

    @property
    def txt(self):
        return self.__txt
        pass

    def handle_starttag(self, tag, attributes):
        if self.__step == 0:
            if tag == 'div':
                for _type, _content in attributes:
                    if _type == 'class' and _content == 'bookcontent clearfix':
                        self.__step = 1
                        pass
                    # print(_type, _content, self.__step)
                    pass

                pass
            pass
        if self.__step == 1:
            if tag == 'br':
                self.__txt += '\r\n'
                pass
            pass

    def handle_endtag(self, tag):
        if self.__step == 1:
            if tag == 'div':
                self.__step = 0
                pass
            pass
        pass

    def handle_data(self, data):
        if self.__step == 1:
            self.__txt += data.strip()
        pass
    pass


def main():
    _connection = _http_client.HTTPConnection('www.wddsnxn.org')
    _connection.request("GET", "/")
    _response = _connection.getresponse()
    # print(_response.read())
    _home_page = _response.read()
    if isinstance(_home_page, bytes):
        _home_page = _home_page.decode()
    _parser = HomePage()
    _parser.feed(_home_page)
    print('-----------------')
    # _parser.print_items()
    # i = 0
    with open('output.txt', 'ab') as _f:
        _i = 0
        _items = _parser.items[_i:]
        _len = len(_items)
        for _j in range(_i, _len):
            _name, _url = _items[_j]
            _f.write('{}\r\n'.format(_name).encode('utf-8'))
            # time.sleep(0.5)
            _connection.request('GET', '/{}'.format(_url))
            try:
                _response = _connection.getresponse()
                _sub_page = _response.read()

                try:
                    _sub_page = _sub_page.decode()
                    _sub_parser = SubPage()
                    _sub_parser.feed(_sub_page)
                    _f.write(_sub_parser.txt.encode('utf-8'))
                    print('{}/{}: '.format(_i, _len), _name, _url, '[OK]')

                except UnicodeDecodeError as _e:
                    with open('error_{}.txt'.format(_name), 'wb') as _sf:
                        _sf.write(_sub_page)
                        pass
                    print('{}: {}'.format(_name, _e))
                    _j -= 1
                    pass
                pass
            except ConnectionResetError as _e:
                _j -= 1
                print('{}: {}'.format(_name, _e))
                pass
                # raise _e
            _i += 1
            pass
    pass


if __name__ == '__main__':
    main()
    # a = b'12345'
    # c = b'cdf'
    # b = bytearray()
    # b.extend(a)
    # b.extend(c)
    # print(b)
    pass
