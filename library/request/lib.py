import requests


class RequestLib:
    def __init__(self, logger):
        self.logger = logger

    def get_method(self, url, parameter):
        try:
            request = requests.get(url, params=parameter)
            self.logger.write_log('Sukses fetch data dari {}'.format(request.url))
            return self.get_response(request)
        except requests.exceptions.RequestException:
            self.logger.write_log(self.get_message(url, parameter), method='ERROR')
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

    def get_message(self, url, parameter):
        return 'Error fetch data dari {}'.format('{}?{}'.format(url, self.url_encode(parameter)))

