import base64
import hashlib
import hmac
import json

import requests


def to_json_str(json_object):
    return json.dumps(json_object, sort_keys=True, separators=(',', ':'))

  
def hmac_signature(key, msg):
    hmac_buffer = hmac.new(
        key=bytes(key, 'utf-8'),
        msg=bytes(msg, 'utf-8'),
        digestmod=hashlib.sha256
    )
    return base64.b64encode(hmac_buffer.digest()).decode('utf-8')

  
def embed_request_query_params(api_key, card_uuid, expiration, css_url, target_origin):
    embed_request_dict = {
        # Globally unique identifier for the card to display
        "token" : card_uuid,
    }
    
    if css_url:
        # Stylesheet URL to style the card element
        embed_request_dict["css"] = css_url
    
    if expiration:
        # Expiration to make request invalid
        embed_request_dict["expiration"] = expiration
    
    if target_origin:
        # Only required if you want to post the element clicked to the parent iframe
        embed_request_dict["target_origin"] = target_origin
        
    embed_request_json = to_json_str(embed_request_dict)

    embed_request = base64.b64encode(bytes(embed_request_json, 'utf-8')).decode('utf-8')
    embed_request_hmac = hmac_signature(api_key, embed_request_json)

    return {
        "embed_request": embed_request,
        "hmac": embed_request_hmac,
    }


def get_embed_html(api_key, card_uuid, css_url=None, expiration=None, target_origin=None):
    url = "https://sandbox.lithic.com/v1/embed/card"

    headers = {
        "Accept": "text/html",
    }

    print('api_key', api_key)
    print('card_uuid', card_uuid)
    print('css_url', css_url)

    params = embed_request_query_params(api_key, card_uuid, expiration, css_url, target_origin)

    response = requests.request("GET", url, params=params, headers=headers)
    response.raise_for_status()
    
    return response.text

