import json
import decimal


class DecimalEncoder(json.JSONEncoder):

    def default(self, num):
        if isinstance(num, decimal.Decimal):
            return str(num)
        return super(DecimalEncoder, self).default(num)
