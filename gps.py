#pip install geocoder
import geocoder

# 현재 위치의 위도와 경도 가져오기
g = geocoder.ip('me')
latitude, longitude = g.latlng

# 현재 위치의 위도와 경도 출력
print(latitude, longitude)