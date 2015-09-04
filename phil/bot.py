from secrets import *
from twitter import Twitter, TwitterStream, OAuth
from pprint import pprint
import random

def main():
	USERNAME = 'chic_phil_a'
	quotes = 'quotes.txt'
    
	with open(quotes) as quotes_file:
		quotes = [line.strip() for line in quotes_file if line != "\n"]

	pprint(quotes)

	auth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET)
	t = Twitter(auth=auth)
	ts = TwitterStream(domain='userstream.twitter.com', auth=auth)

	stream = ts.user()

	for tweet in stream:

		pprint(tweet)

		if 'event' in tweet:
			print('received event %s' % tweet['event'])

		elif 'hangup' in tweet:
			return

		elif 'text' in tweet and tweet['user']['screen_name'] != USERNAME:

			print('from @%s: %s' % (tweet['user']['screen_name'], tweet['text']))

			line = random.choice(quotes)
			print('responding with line: %s' % line)
			reply = '@' + tweet['user']['screen_name'] + ' ' + line
			t.statuses.update(status=reply, in_reply_to_status_id=tweet['id'])


if __name__ == '__main__':
	while True:
		main()