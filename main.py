import json
import datetime
import time
import os
import dateutil.parser
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#-----Main Handler-----


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)


# --- Intents ---


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(
        intent_request['userId'], intent_request['currentIntent']['name']))

    ##Parsing the incoming JSON to gather key information
    intent_name = intent_request['currentIntent']['name']
    slots = intent_request['currentIntent']['slots']    

    # Dispatch to your bot's intent handlers
    if intent_name == 'Minors':
        return minors()
    elif intent_name == 'GPA':
        return GPA()
    elif intent_name == 'Prerequisite':
        return preReqCheck(slots)

    raise Exception('Intent with name ' + intent_name + ' not supported')


def minors():
    session_attributes = {}
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': "Here is a list of university approved minors. (http://registrar.tamu.edu/Registrar/media/REGI_SpecPDFDocs/UniversityApprovedMinors.pdf)"
        }
    )


def GPA():
    session_attributes = {}
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': "Go to the Howdy Portal"
        }
    )

def preReqCheck(slots):
    course = slots['course']
    prereqs = ''
    if course == 'ISEN210' or course == 'isen210':
        prereqs = 'ENGR112'

    session_attributes = {}
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': "The prequisites for the course are: " + prereqs
        }
    )



# --- Helpers that build all of the responses ---


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }
