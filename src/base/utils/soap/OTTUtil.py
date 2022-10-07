
import xmltodict
from lxml import etree  # type: ignore
from dataclasses import dataclass, field
from typing import Optional

from base.serialization.XMLSerializer import XMLSerializer
from base.utils.soap.SoapUtil import post as soap_post
from dataclass_wizard import JSONWizard


@dataclass(init=False)
class OTTRequest(JSONWizard):
    type: Optional[str] = field(metadata=dict(type="Element"))
    content: Optional[str] = field(metadata=dict(type="Element", required=True))
    mobile: Optional[str] = field(metadata=dict(type="Element", required=True))
    cif: Optional[str] = field(metadata=dict(type="Element", required=True))
    messageId: Optional[str] = field(metadata=dict(type="Element", required=True))
    priority: Optional[str] = field(metadata=dict(type="Element"))
    mediaUrl: Optional[str] = field(metadata=dict(type="Element"))
    mediaType: Optional[str] = field(metadata=dict(type="Element"))
    expireTime: Optional[str] = field(metadata=dict(type="Element", required=True))
    messageTime: Optional[str] = field(metadata=dict(type="Element", required=True))
    isEncrypt: Optional[str] = field(metadata=dict(type="Element"))


@dataclass()
class OTTResponse(JSONWizard):
    referenceNo: Optional[str] = field(metadata=dict(type="Element"))
    requestTime: Optional[str] = field(metadata=dict(type="Element"))
    errorCode: Optional[str] = field(metadata=dict(type="Element"))
    errorDesc: Optional[str] = field(metadata=dict(type="Element"))
    responseTime: Optional[str] = field(metadata=dict(type="Element"))


@staticmethod
def send(url: str, req: OTTRequest) -> OTTResponse:
    operation_name = 'sendOTT'
    request_as_string = req.to_json()
    print(f"Raw Request: [{request_as_string}]")
    soap_response = soap_post(url, operation_name, request_as_string)
    if soap_response.status_code == 200:
        stack_d = xmltodict.parse(soap_response.content)
        response_as_string = stack_d['soap:Envelope']['soap:Body']['sendOTTResponse']['sendOTTResult']
        print(f"Raw Response: [{response_as_string}]")
        res: OTTResponse = OTTResponse.from_json(response_as_string)
        return res
    elif soap_response.status_code == 500:
        print('Exception from web service when executed',
              operation_name, 'status code = 500')
        return None
    else:
        print('Exception from web service when executed', operation_name,
              'status code =', soap_response.status_code)
        return None
