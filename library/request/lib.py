import requests


class RequestLib:
    def __init__(self, logger):
        self.logger = logger

    def get_method(self, url, parameter):
        try:
            request = requests.get(url, params=parameter)
            self.logger.write_log(self.get_message('success', url, parameter), method='INFO')
            return self.get_response(request)
        except requests.exceptions.RequestException:
            self.logger.write_log(self.get_message('error', url, parameter), method='ERROR')
            return self.get_method(url, parameter)

    @staticmethod
    def get_response(response):
        return {
            'status': response.status_code,
            'data': response.json(),
            'url': response.url
        }

    @staticmethod
    def url_encode(paramater):
        return '&'.join(["{}={}".format(k, v) for k, v in paramater.items()])

    def get_message(self, mode, url, parameter):
        result = {
            'error': lambda x: 'Error fetch data dari {}'.format('{}?{}'.format(
                x.get('url'), self.url_encode(x.get('parameter')))
            ),
            'success': lambda x: 'Sukses fetch data dari {}'.format('{}?{}'.format(
                x.get('url'), self.url_encode(x.get('parameter')))
            ),
        }

        return result.get(mode, lambda x: str('Oops key is not found'))({'url': url, 'parameter': parameter})

