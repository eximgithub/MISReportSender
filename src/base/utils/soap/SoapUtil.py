from zeep import Client
from lxml import etree
import requests
import logging

logger = logging.getLogger()


@staticmethod
def __post_bak(wsdl_url: str, operation_name: str, request_as_xml_string):
    try:
        print('Begin execute', operation_name)
        client = Client(wsdl_url)
        headers = {'content-type': 'text/xml'}
        data = client.create_message(
            client.service, operation_name, request_as_xml_string)
        data_xml_str = etree.tostring(data, pretty_print=True).decode()
        print(data_xml_str)
        response = requests.post(
            wsdl_url, data=data_xml_str, headers=headers)
        if response.status_code == 200:
            rawResponse = response.content.decode("utf-8")
            print(f"RawResponse: {rawResponse}")
            return rawResponse
        elif response.status_code == 500:
            print('Exception from web service when executed',
                  operation_name, 'status code = 500')
            return None
        else:
            print('Exception from web service when executed', operation_name,
                  'status code =', response.status_code)
            return None
    except Exception as ex:
        print('Exception:', ex)
        return None
    finally:
        print('Finish execute', operation_name)


@staticmethod
def post(wsdl_url: str, operation_name: str, request_as_xml_string):
    try:
        logger.info(f"Begin execute {operation_name}")
        client = Client(wsdl_url)
        headers = {'content-type': 'text/xml'}
        data = client.create_message(
            client.service, operation_name, request_as_xml_string)
        data_xml_str = etree.tostring(data, pretty_print=True).decode()
        # print(data_xml_str)
        return requests.post(
            wsdl_url, data=data_xml_str, headers=headers)
    except Exception as ex:
        logger.error(ex)
    finally:
        logger.info(f"Finish execute {operation_name}")
