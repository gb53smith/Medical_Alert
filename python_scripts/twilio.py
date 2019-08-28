# Python Script to Extend Features of the Twilio Call Component
# https://www.twilio.com/labs/twimlets/message
# Parameters
# contacts: [<int>]  # Number of contacts 
# The following are optional
# voice: [man | woman | alice] # default man
# delay: [1;10] # delay before message is said.  Default is 0. 
#                 This allows time for someone to pickup the phone.
# loop: [1:3] # plays message multiple times.  Default is once.
# language: see https://www.twilio.com/docs/api/twiml/say
# speed: [normal|slow} # default is normal

# Example Service Call
      # - service: python_script.twilio
        # data:
          # contacts: '4'
          # delay: '1'
          # loop: '2'
          # voice: 'alice'
          # language: 'en-CA'
		  # speed: 'slow'

# Get mandatory parameter.  Abort if not found
contacts = int(data.get('contacts', '0'))
#logger.info("contacts {}".format(contacts))

if contacts == 0:
	exit()
	
if hass.states.get('automation.fast_buzzer').state == 'on':
	type = 'alarm'
else:
	type = 'cancel'
	
#logger.info("GBS type {}".format(type))

# Get option parameters for voice

# Voice Parameter
voice = data.get('voice', '0')
#logger.info("voice {}".format(voice))

if voice != '0':
	url_voice = '%20voice%3D%22' + voice + '%22'
else:
	url_voice = ''

# Delay Parameter
delay = data.get('delay', '0')
#logger.info("delay {}".format(delay))
if int(delay) > 0 :
# <Pause length="delay"/>
	url_delay = '%3CPause%20length%3D%22' + delay + '%22%2F%3E%0A'
else:
	url_delay = ''	

# Loop Parameter
loop = data.get('loop', '0')
#logger.info("loop {}".format(loop))
if int(loop) > 0 :
	url_loop = '%20loop%3D%22' + loop + '%22'
else:
	url_loop = ''

# Language Parameter
language = data.get('language', '0')
#logger.info("language {}".format(language))

if language != '0':
	url_language = '%20language%3D%22' + language + '%22'
else:
	url_language = ''

# Speed Parameter
speed = data.get('speed', '0')
#logger.info("speed {}".format(speed))
#I replaced spaces with commas just too slow down the text to speech
#Use %20 to speed up
if speed == 'slow':
	spacer = '%2C'
else:
	spacer = '%20'

for i in range(1, contacts + 1):
	# logger.info("GBS index {}".format(i))	

	# Get message to send from text input
	if type == 'alarm':
		message = hass.states.get('input_text.message' + str(i)).state
	else:
		message = hass.states.get('input_text.cancel_message').state
		
	phone = '+1' + hass.states.get('input_text.phone' + str(i)).state
	
	send  = hass.states.get('input_select.type' + str(i)).state
	
	if send == 'Voice' or send == 'Both':
		#Format message for a url transmission.  ie no spaces

		url_message = '%3E' + message.replace(' ',spacer) + spacer
		url_root = 'https://twimlets.com/echo?Twiml=%3CResponse%3E%0A'
		url_say = '%3CSay'
		url_close = '%3C%2FSay%3E%0A%3C%2FResponse%3E%0A&'
		#Assemble complete url message
		url = url_root + url_delay + url_say + url_voice + url_language \
			+ url_loop + url_message + url_close

		#logger.info("{}".format(url))
		# Paste url output in homeassistant.log into a chrome browser to test.

		# send url to notify.twilio service
		data = { "message" : url, "target" : phone }
		hass.services.call('notify', 'medical_alert_call', data)
		
	if send == 'Text' or send == 'Both':
		data = { "message" : message, "target" : phone }
		hass.services.call('notify', 'medical_alert_sms', data)
	
	# logger.info("GBS type {}".format(type))	
	# logger.info("GBS message {}".format(message))
	# logger.info("GBS phone {}".format(phone))
	
# EOF

            