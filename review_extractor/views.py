from django.http import JsonResponse
from bs4 import BeautifulSoup
import urllib3
from urllib.parse import unquote

# Create your views here.


def extractReview(request) : 
	http = urllib3.PoolManager()
	reviewUrl = unquote(request.GET.get('url'))
	try : 
		response = http.request('GET', reviewUrl, retries=False)
		htmlRaw = response.data
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

		return JsonResponse({'success': True, 'review': review})
	except Exception as e : 
		return JsonResponse({'success': False})