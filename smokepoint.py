"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome to Smokepoint!"
    speech_output = "Please tell me the name of the oil or cooking substance you'd like the smoke point of."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please request the smoke point of an oil, such as canola oil"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Smokepoint!"
    reprompt_text = "Thank you for using Smokepoint! Feedback is always welcome. You can find me on Twitter at @percontate."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_smoke_points():
    SMOKE_POINT = {
        "almond oil": 420,
        "avocado oil": 520,
        "avocado oil refined": 520,
        "butter": 302,
        "canola oil": 435,
        "canola oil refined": 400,
        "canola oil semi-refined": 350,
        "canola oil unrefined": 225,
        "coconut oil": 350,
        "corn oil": 410,
        "corn oil refined": 450,
        "corn oil unrefined": 320,
        "cottonseed oil": 420,
        "EVOO": 406,
        "evoo": 406,
        "extra-virgin olive oil": 406,
        "extra virgin olive oil": 406,
        "flaxseed oil unrefined": 225,
        "grapeseed oil": 420,
        "hazelnut oil": 430,
        "hemp oil": 330,
        "hemp seed oil": 330,
        "high-oleic sunflower oil unrefined": 320,
        "high-oleic sunflower oil refined": 450,
        "lard": 374,
        "macadamia oil": 413,
        "macadamia nut oil": 413,
        "olive oil": 375,
        "olive oil extra light": 468,
        "olive oil extra virgin": 406,
        "olive oil unrefined": 320,
        "olive oil virgin": 420,
        "olive pomace oil": 460,
        "peanut oil": 440,
        "peanut oil refined": 450,
        "peanut oil unrefined": 320,
        "rapeseed oil": 435,
        "safflower oil": 510,
        "safflower oil refined": 450,
        "safflower oil semi-refined": 320,
        "safflower oil unrefined": 225,
        "sesame oil": 410,
        "sesame oil semi-refined": 450,
        "sesame oil unrefined": 350,
        "shortening emulsified vegetable": 325,
        "soy bean oil": 495,
        "soy oil refined": 450,
        "soy oil semi-refined": 350,
        "soy oil unrefined": 320,
        "sunflower oil": 440,
        "sunflower oil semi-refined": 450,
        "sunflower oil unrefined": 225,
        "tallow": 420,
        "tea seed oil": 485,
        "vegetable shortening": 360,
        "walnut oil semi-refined": 400,
        "walnut oil unrefined": 320
    }

    return SMOKE_POINT


def get_smoke_point(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = "Smokepoint"
    session_attributes = {}
    should_end_session = False

    """
    Should look like:
    "slots": {
        "Oil": {
          "name": "Oil",
          "value": "canola oil"
        }
      }

    But sometimes it doesn't have the "value"
    """

    smoke_points = get_smoke_points()

    if 'Oil' in intent['slots'] and 'value' in intent['slots']['Oil'] and intent['slots']['Oil']['value'] in smoke_points:
        oil = intent['slots']['Oil']['value']
        card_title = "Smoke point of %s" % oil

        smoke_point = smoke_points[oil]
        speech_output = "The smoke point of %s is %s degrees fahrenheit" % (oil, smoke_point)
        reprompt_text = "The smoke point of %s is %s degrees Fahrenheit" % (oil, smoke_point)
        should_end_session = True
    else:
        speech_output = "I did not recognize the name of the oil or cooking substance. " \
                        "Please try again."
        reprompt_text = "I did not recognize the name of the oil or cooking substance. " \
                        "Please try again."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "SmokePointIsIntent":
        return get_smoke_point(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.6daba50f-fc89-4c18-a046-b5245aad9de8"):
        raise ValueError("Invalid Application ID (received %s)" % event['session']['application']['applicationId'])

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
