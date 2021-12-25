from bs4 import BeautifulSoup
import urllib3

example = 'https://www.amazon.in/gp/customer-reviews/RQQFD7PCBMQ4R'
 
http = urllib3.PoolManager()
response = http.request('GET', example)
htmlRaw = response.data
try : 
	html = BeautifulSoup(htmlRaw, features="html.parser")
	review = dict()
	review['customerName'] = html.select('.a-profile-name')[0].text
	review['productName'] = html.find('a', attrs={'data-hook': 'product-link'}).text
	review['rating'] = int(html.find('i', attrs={'data-hook': 'review-star-rating'}).span.text[:1])
	review['title'] = html.find('a', attrs={'data-hook': 'review-title'}).span.text
	review['verifiedPurchase'] = html.find('span', attrs={'data-hook': 'avp-badge'}).text
	review['body'] = str(html.find('span', attrs={'data-hook': 'review-body'}))

	profileAvatar = html.select('.a-profile-avatar')[0];
	profilePicture = profileAvatar.select('img')[1]['src']
	review['profilePicture'] = profilePicture[:-7] + profilePicture[-5:]

	print(review)
except Exception as e : 
	print(e)